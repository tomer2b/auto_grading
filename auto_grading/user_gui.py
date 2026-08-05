import ipywidgets as widgets

from auto_grading.auto_gradeing_code import get_notebook_filename, get_questions, import_tasks, run_test
from .constants import SHEET_WEB_APP_URL
from .constants import get_academic_year
from IPython.display import HTML, Javascript,display, clear_output

import requests



def run_dashboard(notebook_globals,  question_set,grade):

    questions=get_questions(question_set)
    tasks = import_tasks(grade,question_set,questions)
    student_functions = {k: v for (k, v) in notebook_globals.items() if callable(v)}
    
    score, output, question_grade, final_grade, ai_enabled_for_user = run_test(tasks, student_functions, question_set)
    
    test_results_out = widgets.Output()
    with test_results_out:
        display(Javascript('google.colab.output.setIframeHeight(0, true, {maxHeight: 10000})'))
        display(HTML(output))
    
    # 3. מציגים את לחצן ה-AI למעלה
    # (בהנחה ש-get_notebook_filename זמינה בחבילה שלך)
    show_ai_helper_button(ai_enabled_for_user, SHEET_WEB_APP_URL, question_set, get_notebook_filename(), test_results_out)
    
    # 4. מציגים את התוצאות למטה
    display(test_results_out)
    
    # 5. כוונון גובה נוסף
    display(Javascript('google.colab.output.setIframeHeight(0, true, {maxHeight: 10000})'))


def show_ai_helper_button(ai_enabled_for_user,task_code,filename, results_widget=None):
    """
    פונקציה זו מציירת את לחצן ה-AI במחברת ומנהלת את הלוגיקה שלו.
    """
    is_ai_active = str(ai_enabled_for_user).strip().lower() in ['true', '1', 'yes']
    # הגדרת המצב ההתחלתי של הלחצן לפי המשתנה שהתקבל
    if is_ai_active:
        initial_desc = 'הפסק בינה מלאכותית'
        initial_style = 'danger'
        initial_state = True
    else:
        initial_desc = 'הפעל עזרה מבינה מלאכותית'
        initial_style = 'primary'
        initial_state = False

    custom_css = """
    <style>
        /* זה ישפיע על כל הלחצנים של ipywidgets במחברת */
        .jupyter-widgets.jupyter-button {
            border-radius: 25px !important; /* !important מבטיח שהעיצוב הזה יעקוף את ברירת המחדל */
        }
    </style>
    """
    display(HTML(custom_css))

    # כעת ניצור לחצן רגיל, וה-CSS שהזרקנו יעניק לו פינות מעוגלות
    ai_button = widgets.Button(
        description=initial_desc,
        button_style=initial_style,
        layout=widgets.Layout(
            width='280px', height='45px', 
            font_weight='bold', margin='15px 0px'
        )
    )
    
    # עדכון משתנה המצב הפנימי של הלחצן
    ai_button.ai_is_on = initial_state 
    out = widgets.Output()
    
    def on_ai_button_clicked(b):
        with out:
            if not b.ai_is_on:
                clear_output()
                if results_widget:
                    results_widget.layout.display = 'none'
                b.disabled = True
                b.description = 'מעדכן הגדרות... ⏳'
                b.button_style = 'warning'
                
                # מפעילים את הפונקציות שהועברו מבחוץ
                # log_usage_func()
                # run_summary_func(ai_requested=True)
                update_ai_status_in_sheet(SHEET_WEB_APP_URL,task_code,filename,True) 

                b.description ='הפסק בינה מלאכותית'
                b.button_style = 'danger'
                b.disabled = False
                b.ai_is_on = True 

                alert_msg = """
                <div dir="rtl" style="text-align: center; margin-top: 15px; font-size: 16px; color: #31708f; background-color: #d9edf7; padding: 12px; border-radius: 10px; border: 1px solid #bce8f1; font-family: sans-serif;">
                    <strong>שים לב:</strong> סטטוס העזרה התעדכן בהצלחה.<br>
                    יש <b>להריץ את התא מחדש</b> כדי לקבל את הניתוח של הבינה המלאכותית 🚀
                </div>
                """
                display(HTML(alert_msg))
            else:
                clear_output() 
                if results_widget:
                    results_widget.layout.display = 'block'
                update_ai_status_in_sheet(SHEET_WEB_APP_URL,task_code,filename,False) 
                b.description = 'הפעל עזרה מבינה מלאכותית'
                b.button_style = 'primary'
                b.ai_is_on = False

    ai_button.on_click(on_ai_button_clicked)
    
    centered_layout = widgets.HBox(
        [ai_button], 
        layout=widgets.Layout(justify_content='center')
    )
    
    # מציגים את הקופסה הממורכזת (שמכילה את הלחצן), ואת אזור הפלט מתחתיה
    display(centered_layout, out)


def update_ai_status_in_sheet(web_app_url, task_code, filename, ai_enabled):
    """
    מעדכנת את סטטוס הפעלת ה-AI עבור משתמש ומשימה ספציפיים בגוגל שיטס.
    """
    payload = {
        "action": "update_ai_status",
        "task_code": task_code,
        "filename": filename,
        "ai_enabled": ai_enabled,
        "academic_year": get_academic_year()
    }
    
    try:
        response = requests.post(web_app_url, json=payload)
        result = response.json()
        
        # if result.get("status") == "success":
        #     print("✅ סטטוס ה-AI עודכן בהצלחה בגיליון.")
        # else:
        #     print(f"❌ שגיאה בעדכון הגיליון: {result.get('message')}")
            
        return result
        
    except Exception as e:
        print(f"❌ שגיאת תקשורת: {str(e)}")
        return {"status": "error", "message": str(e)}