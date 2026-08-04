import ipywidgets as widgets
from .constants import SHEET_WEB_APP_URL
from IPython.display import HTML, display, clear_output
import requests

def show_ai_helper_button(ai_enabled_for_user,task_code,filename):
    """
    פונקציה זו מציירת את לחצן ה-AI במחברת ומנהלת את הלוגיקה שלו.
    """
    # הגדרת המצב ההתחלתי של הלחצן לפי המשתנה שהתקבל
    if ai_enabled_for_user:
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
        description=' קבל עזרה חכמה מ-AI 💡',
        button_style='primary',
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
                b.disabled = True
                b.description = 'מנתח שגיאות... ⏳'
                b.button_style = 'warning'
                
                # מפעילים את הפונקציות שהועברו מבחוץ
                # log_usage_func()
                # run_summary_func(ai_requested=True)
                update_ai_status_in_sheet(SHEET_WEB_APP_URL,task_code,filename,True) 

                b.description ='הפסק בינה מלאכותית'
                b.button_style = 'danger'
                b.disabled = False
                b.ai_is_on = True 
                
            else:
                clear_output() 
                b.description = 'הפעל עזרה מבינה מלאכותית'
                b.button_style = 'primary'
                b.ai_is_on = False
                update_ai_status_in_sheet(SHEET_WEB_APP_URL,task_code,filename,False) 

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
        "ai_enabled": ai_enabled
    }
    
    try:
        response = requests.post(web_app_url, json=payload)
        result = response.json()
        
        if result.get("status") == "success":
            print("<div dir=rtl><center>✅ סטטוס ה-AI עודכן בהצלחה בגיליון.</center></div>")
        else:
            print(f"<div dir=rtl><center>❌ שגיאה בעדכון הגיליון: {result.get('message')}</center></div>")
            
        return result
        
    except Exception as e:
        print(f"<div dir=rtl><center>❌ שגיאת תקשורת: {str(e)}</center></div>")
        return {"status": "error", "message": str(e)}