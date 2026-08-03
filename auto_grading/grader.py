# grader.py (בתוך חבילת הפייתון שלך)
import ipywidgets as widgets
from IPython.display import display, clear_output

def show_ai_helper_button():
    """
    פונקציה זו מציירת את לחצן ה-AI במחברת ומנהלת את הלוגיקה שלו.
    
    פרמטרים:
    run_summary_func: הפונקציה שמריצה את ה-AI ומדפיסה תוצאות.
    log_usage_func: הפונקציה ששולחת את ה-V לגוגל שיטס.
    """
    ai_button = widgets.Button(
        description=' קבל עזרה חכמה מ-AI 💡',
        button_style='primary',
        layout=widgets.Layout(
            width='280px', height='45px', 
            border_radius='25px', font_weight='bold', margin='15px 0px'
        )
    )
    
    ai_button.ai_is_on = False 
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
                
                b.description = 'הסתר עזרת AI ❌'
                b.button_style = 'danger'
                b.disabled = False
                b.ai_is_on = True 
                
            else:
                clear_output() 
                b.description = ' קבל עזרה חכמה מ-AI 💡'
                b.button_style = 'primary'
                b.ai_is_on = False

    ai_button.on_click(on_ai_button_clicked)
    
    # מציירים את הכפתור בתא שבו הפונקציה זומנה
    display(ai_button, out)


