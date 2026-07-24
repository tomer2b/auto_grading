# Copyright (C) 2024 Tomer Tubi - All Rights Reserved

import pandas as pd
import importlib.resources as pkg_resource
import time
import queue
import builtins as __builtin__
import inspect
from . import api
from . import tasks_db

from IPython.display import display, HTML
import traceback


# in order to use AI ollama
# add these rows to the start cell to run in user colab notebook
# 1. התקנת zstd (הנחוץ לפריסת Ollama)
# !apt-get update -qq && apt-get install -y -qq zstd

# # 2. התקנת Ollama (רק אם לא קיים)
# ![ -f /usr/local/bin/ollama ] && echo "✅ Ollama already installed" || (curl -fsSL https://ollama.com/install.sh | sh)


test_weight=0.2
question_weight=0.8
ai_manager=''

RED_TEXT='\033[91m'
REGULAR_TEXT='\033[0m'
GREEN_TEXT='\033[92m'

# the key is the MD file source
questions_dic={
    '1':['ex1','ex2','ex3','ex4','ex5','ex6'],
    '2':['ex2','ex3','ex4'],
    '3':['ex9','ex10','ex11','ex12','ex13','ex14','ex15'],
    '4':['ex4','ex5','ex6','ex7','ex8','ex9'],
    '5':['ex1','ex2','ex3','ex4','ex5','ex6','ex7','ex8'],
    '6':['ex2','ex3','ex4a','ex4b','ex5a','ex5b','ex6'],
    '7a':['ex2','ex3','ex4','ex5','ex6','ex7','ex8','ex9','ex10','ex11'],
    '7b':['ex100','ex101','ex102','ex103','ex104'],
    '7c':['ex100','ex101','ex102','ex103','ex104','ex105','ex106','ex107'],
    '8a':['ex2','ex3','ex4','ex5'],
    '8b':['ex11','ex12','ex13','ex14','ex15','ex16','ex17','ex18'],
    '9':[],
    '10':['ex1','ex2','ex3','ex4','ex6','ex7','ex8','ex9'],
    '11':['ex4','ex6','ex7','ex8','ex9','ex10','ex11','ex12','ex13','ex14'], # strings
    '11z':['ex4','ex6','ex7','ex8','ex9','ex10','ex11','ex12','ex13','ex14','ex15','ex16','ex17','ex18','ex19'], # strings
    # '12':['3a','3b','4a','4b','5a','5b','6a',6,'7a','7b','8a','8b','9a','9b'], # functions
    '12a':['ex3a','ex3','ex4a','ex4','how_many_legs','ex5','ex6a'], # functions
    '12b':['ex7a','ex7b','ex8a','ex8b','ex9a','ex9b'], # functions
    '13a':['ex5','ex6','ex7','ex8'], # lists
    '13b':['ex101','ex102','ex103','ex104','ex106','ex107'], 
    '13c':['ex201','ex202','ex203','ex204'], # lists of list
    '14':['ex1','ex2','ex3','ex4','ex5','ex6','ex7','ex8','ex9','ex10'],
    '14a':['ex1','ex2','ex3','ex4','ex5','ex6','ex7','ex8','ex9','ex10','ex101','ex102','ex103','ex104','ex105','ex106','ex107','ex108','ex109','ex110'],
    '101':['sum_arithmetic','my_power','is_prime','count_div4','sum7_numbers','fibonachi'],
    '102':['donuts','both_ends','fix_start','mix_up','verbing','not_bad','front_back'],
    '103':['factorial','beep','is_palindrom','show_digits','sum_digits'],
    '104':['sort_asc','multiply_items','sum_list','largest_number','copy_list','convert2string','valid_email','remove_item','create_email_address','valid_ip_address','summer'],
    '105':['match_ends','front_x','sort_last','remove_adjacent','linear_merge'],
    '108':['is_capital_letter','is_credit_card','is_phone_number','is_email','is_valid_ip_address','find_all_emails']
   }

curr_exercise_key = 0

# qu1 = queue.Queue()
# for num in [2, 69, 12, 7, 33, 61]:
#     qu1.put(num)
# qu2 = queue.Queue()
# for num in [7, 42, 13, 6]:
#     qu2.put(num)

def create_queue(items):
    q = queue.Queue()
    for item in items:
        q.put(item)
    return q


def print_my_queue(q):
    items = list(q.queue)  
    if not items:
        print("Queue is empty")
        return
    
    print(" => ".join(map(str, items)) + " => head")


def get_questions(exercise_key):
  global curr_exercise_key
  curr_exercise_key = exercise_key
  if questions_dic.get(exercise_key)!=None:
    return questions_dic[exercise_key]
  else:
    return []
  

def import_tasks(grade,question_set,questions ):
  t=[]
  with pkg_resource.open_text('auto_grading','tasks.csv') as file:
    df = pd.read_csv(file,sep=',',on_bad_lines='skip',encoding='utf-8')

  # df = df[df['class']==grade]
  df.question_set = df.question_set.astype(str)
  # ignore last letter of exercise_set in case last letter is subset of questions
  exerciser_set=str(question_set)[:-1] if not str(question_set).isnumeric() else str(question_set)
  df = df[df['question_set']==exerciser_set]     
  df = df[df['function'].isin([f'{str(q)}' for q in questions]) ]
  # df = df[df['question_set'].str.contains(1)]
  #   print(df[['function','func_arg_list','in_list','exp_out_list','return_values']])

  for key, value in df.iterrows():
    sublist=[]
    sublist.append(value["function"])
    sublist.append([]) if value["func_arg_list"]==None else  sublist.append(value["func_arg_list"])
    sublist.append([]) if value["in_list"]==None else  sublist.append(eval(value["in_list"] ))
    sublist.append([]) if value["exp_out_list"]==None else  sublist.append(eval(value["exp_out_list"]) )
    sublist.append([]) if value["return_values"]==None else  sublist.append(eval(value["return_values"]) )
    t.append(sublist)
  return t


run = None

def print(*args,  **kwargs):

    if run != None and run.test_mode==True:
        with open('output.txt', "w",encoding='ISO-8859-8') as out:
            __builtin__.print(*args, **kwargs, file=out)
        with open('output.txt', "r",encoding='ISO-8859-8') as out:
            txt_batch = out.read() #.strip()
        run.output_lst.append(txt_batch)
        return txt_batch
    else:
        txt = __builtin__.print(*args, **kwargs)
        return txt

def input(prompt=None):
    if run != None and run.test_mode==True:
        batch_input = run.input_lst[run.input_counter]
        run.input_counter += 1
    else:
        batch_input = __builtin__.input(prompt)
    return batch_input

# def set_run(new_val):
#     global run
#     run=new_val

import html
import linecache
from IPython import get_ipython
from IPython.display import display, HTML

def custom_syntax_error_handler(shell, etype, evalue, tb, tb_offset=None):
    """
    תופס שגיאות תחביר ומציג אותן בתיבת HTML מעוצבת מימין לשמאל, 
    כולל הצגת השורה הקודמת להקשר נוסף.
    """
    line_num = evalue.lineno
    line_text = evalue.text
    offset = evalue.offset
    file_name = evalue.filename # השם הווירטואלי של התא ב-Colab
    
    line_code_html = ""
    
    if line_num and line_text:
        # 1. שליפת השורה הקודמת מהזיכרון של Colab
        prev_line_html = ""
        if line_num > 1:
            prev_line_text = linecache.getline(file_name, line_num - 1)
            if prev_line_text:
                safe_prev = html.escape(prev_line_text.rstrip("\n\r"))
                # הצגת השורה הקודמת בצבע אפור מעומעם
                prev_line_html = f"<div style='color: #9e9e9e; margin-bottom: 3px;'><code>{line_num - 1:2d} | {safe_prev}</code></div>"
        
        # 2. הכנת השורה שקרסה
        safe_curr = html.escape(line_text.rstrip("\n\r"))
        curr_line_html = f"<div style='color: #eeffff; background-color: #333; padding: 2px 0;'><code>{line_num:2d} | {safe_curr}</code></div>"
        
        # 3. חישוב מיקום החץ (כולל קיזוז של מספר השורה והקו המפריד שהוספנו)
        arrow_html = ""
        if offset:
            # מספר התווים שנוספו בתחילת השורה (מספר השורה + רווח + קו מפריד + רווח)
            prefix_len = len(str(line_num)) + 3 
            spaces = "&nbsp;" * (offset - 1 + prefix_len)
            arrow_html = f"<div style='margin-top: 2px;'><code style='color: #ef5350; font-size: 16px;'>{spaces}⬆️</code></div>"
            
        # 4. הרכבת הבלוק השחור של הקוד
        line_code_html = f"""
        <div style="direction: ltr; text-align: left; background-color: #212121; padding: 10px; border-radius: 5px; margin: 10px 0; font-family: 'Consolas', monospace; font-size: 14px;">
            {prev_line_html}
            {curr_line_html}
            {arrow_html}
        </div>
        """
        
    # 5. הרכבת ה-HTML הסופי
    html_content = f"""
    <div style="font-family: Arial, sans-serif; direction: rtl; text-align: right; border: 2px solid #ef5350; border-radius: 8px; padding: 15px; background-color: #ffebee; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h3 style="color: #c62828; margin-top: 0; display: flex; align-items: center;">
            <span style="font-size: 24px; margin-left: 10px;">🚨</span> שגיאת תחביר (SyntaxError)
        </h3>
        <p style="font-size: 15px; color: #333; margin-bottom: 10px;">נראה שיש בעיה בצורת הכתיבה של הקוד (חסר תו כלשהו, או שיש רווחים לא נכונים).</p>
        
        {line_code_html}
        
        <h4 style="color: #c62828; margin-bottom: 8px; margin-top: 15px;">💡 טיפים לתיקון:</h4>
        <ul style="margin-top: 0; color: #444; line-height: 1.6;">
            <li>אם החץ מצביע על תחילת שורה, בדוק אם <b>בשורה שמעליה</b> שכחת לסגור סוגריים או שצריך טאב במקום של החץ.</li>
            <li>בדוק אם חסרים נקודתיים (<b>:</b>) בסוף משפט <code>def</code>, <code>if</code>, <code>for</code>, או <code>while</code>.</li>
            <li>ודא שלא חסרים גרשיים (<b>"</b> או <b>'</b>) סביב מחרוזות.</li>
        </ul>
    </div>
    """
    
    display(HTML(html_content))
    return None

class CheckAssignment:

    def __init__(self):
        self.test_mode = False
        self.input_counter = 0
        self.input_lst = []
        self.output_lst = []
        self.run_result = {}
        # self.runs = tests

    # is saved for backup to go to text format of the output
    # def run_task_text_output_format(self,func, parms, in_list, expected_result, return_values,student_functions):

    #     try:

    #         self.input_lst=in_list
    #         self.input_counter = 0
    #         self.output_lst = []
    #         if 'create_queue' in parms and func in student_functions:
    #             result = eval(func + '(' + str(parms)[1:-1] + ')',{'create_queue':create_queue,func:student_functions[func]})
    #         else:
    #             result = eval(func + '(' + str(parms)[1:-1] + ')')
                
    #         if type(result) == tuple:
    #             result = list(result)
    #         elif isinstance(result, queue.Queue) :
    #             result = list(result.queue)
    #         else:
    #             result = [result]

    #         func_call = func + '(' + str(parms)[1:-1] + ')'
    #         expected_result = [str(x) for x in expected_result]
    #         result_run =list(result)
    #         # check if the output is the same           
    #         if self.output_lst == expected_result:
    #           if (return_values == result_run):
    #             return True,func_call,f'{GREEN_TEXT}Excellent{REGULAR_TEXT}',self.output_lst,result_run
    #           else:
    #             return False,func_call,f'Returned: {RED_TEXT}{str(result)}{REGULAR_TEXT} != Expected return: {GREEN_TEXT}{str(return_values)}{REGULAR_TEXT}',self.output_lst,result_run
    #         else:
    #           if (return_values == list(result)):
                
    #             return False,func_call,f'Printed: {RED_TEXT}{str(self.output_lst)}{REGULAR_TEXT} != Expected print: {GREEN_TEXT}{str(expected_result)}{REGULAR_TEXT}',self.output_lst,result_run
    #           else:
    #             return False,func_call,f'Returned: {RED_TEXT}{result}{REGULAR_TEXT} != Expected return: {GREEN_TEXT}{str(return_values)}{REGULAR_TEXT} and Printed: {RED_TEXT}{str(self.output_lst)}{REGULAR_TEXT} != Expected print: {GREEN_TEXT}{str(expected_result)}{REGULAR_TEXT}',self.output_lst,result_run
          

    #     except Exception as e:
    #         func_call = func + '(' + str(parms)[1:-1] + ')'
    #         return False, func_call, e,[],[]

    def run_task(self,func, parms, in_list, expected_result, return_values,student_functions,question_set):

        try:

            self.input_lst=in_list
            self.input_counter = 0
            self.output_lst = []
            if 'create_queue' in parms and func in student_functions:
                result = eval(func + '(' + str(parms)[1:-1] + ')',{'create_queue':create_queue,func:student_functions[func]})
            else:
                result = eval(func + '(' + str(parms)[1:-1] + ')')
                
            if type(result) == tuple:
                result = list(result)
            elif isinstance(result, queue.Queue) :
                result = list(result.queue)
            else:
                result = [result]

            func_call = func + '(' + str(parms)[1:-1] + ')'
            expected_result = [str(x) for x in expected_result]
            # result_run =list(result)
            # check if the output is the same           
            if self.output_lst == expected_result:
              if (return_values == list(result)):
                return True,func_call,f'',self.output_lst, list(result),''
              else:
                ai_help_text=get_student_ai_hint(student_functions[func],tasks_db[str(question_set)][func],expected_result,self.output_lst,return_values,list(result))
                return False,func_call,f'',self.output_lst, list(result),ai_help_text
            else:
              if (return_values == list(result)):
                ai_help_text=get_student_ai_hint(student_functions[func],tasks_db[str(question_set)][func],expected_result,self.output_lst,return_values,list(result))
                return False,func_call,f'',self.output_lst, list(result),ai_help_text
              else:
                ai_help_text=get_student_ai_hint(student_functions[func],tasks_db[str(question_set)][func],expected_result,self.output_lst,return_values,list(result))
                return False,func_call,f'',self.output_lst, list(result),ai_help_text
          

        except Exception as e:
            tb_info = traceback.extract_tb(e.__traceback__)[-1]
            error_type = type(e).__name__
            func_call = func + '(' + str(parms)[1:-1] + ')'
            return False, func_call, f"שגיאת {error_type} בשורה {tb_info.lineno}:\n{tb_info.line}",[],[],''

def grade_student_functions(req_functions,student_functions):
    count = 0
    for q in req_functions:
      if q in student_functions.keys() :
         count+=1
    if count==0 or req_functions==[]:
       grade=0
    else:
       grade = 100* count/len(req_functions)
    return grade


def run_test(tasks,student_functions,question_set):
    output = ''
    correct_answer = 0
    run_results = {}
    for k,v in student_functions.items():
        globals()[k]=v
    ex_count = 0
    global run
    run=CheckAssignment()
    run_ai_manager()
    # tasks = function :0 , func_arg_list :1 ,   in_list :2  ,  exp_out_list :3  ,  return_values :4
    for i in range(len(tasks)):
        run.test_mode = True
        start = time.time()
        run_results[ex_count] = run.run_task(tasks[i][0], tasks[i][1], tasks[i][2], tasks[i][3], tasks[i][4],student_functions,question_set)
        end = time.time()
        
        run.test_mode = False
        run_time=end-start
        if run_results[ex_count][0]==True:
            correct_answer+=1
            output += f'{GREEN_TEXT}Ok{REGULAR_TEXT} {tasks[i][0]}({"" if tasks[i][1]==[] else tasks[i][1]})  \tinput: {tasks[i][2]}  '
            # print(output)
            output += '\n'
        else:
            if student_functions.get(tasks[i][0]) :
                answer= '' #  '\n' + ai_manager.ask(f' {inspect.getsource(student_functions[tasks[i][0]])}') 
            else:
                answer=''
            #error_msg=run_results[ex_count][2] if run_time<2 else 'run time too long... '
            run_results[ex_count] =(run_results[ex_count][0],run_results[ex_count][1], run_results[ex_count][2] if run_time<2 else 'run time too long... ',run_results[ex_count][3],run_results[ex_count][4],run_results[ex_count][5])
            output += f'{RED_TEXT}X{REGULAR_TEXT}  {tasks[i][0]}({"" if tasks[i][1]==[] else tasks[i][1]})  \tinput: {tasks[i][2]} \tMessage: {run_results[ex_count][2]}{answer}'
            # print(output)
            output += '\n'

        ex_count += 1
    # print('----------')
    # print('grade:',round(100 * correct_answer / len(run_results)))
    if  len(run_results)!=0:
      if questions_dic.get(curr_exercise_key)!=None :
          question_grade = grade_student_functions(questions_dic[curr_exercise_key],student_functions)
      else:
          question_grade=0
      tests_score =round(100 * correct_answer / len(run_results))
    else:
      tests_score = 0
      question_grade=0
    final_grade=test_weight*tests_score + question_weight*question_grade
    
    output=display_all_results(tasks,run_results,final_grade)
    return round(tests_score),output,round(question_grade),round(final_grade)


from groq import Groq

def get_student_ai_hint(
    question_text: str, 
    student_code: str, 
    expected_output: list, 
    actual_output: list, 
    expected_return: list, 
    actual_return: list, 
) -> str:
    """
    מקבלת את השאלה, הקוד של התלמיד, תוצאות וערכי החזרה צפויים מול בפועל,
    ומחזירה הכוונה קצרה וקולעת בעברית ללא פתרון מלא.
    """
    client = Groq(api_key=api)
    
    # הנחיות מערכת מעודכנות הכוללות התייחסות לפלט וערכי החזרה
    system_prompt = (
        "אתה מורה פרטני ומנוסה למדעי המחשב. "
        "התלמיד יציג בפניך שאלה בפייתון, את הקוד שכתב, וכן השוואה בין מה שהקוד אמור להפיק/להחזיר לבין מה שהוא בפועל הפיק/החזיר. "
        "תפקידך לתת לו הכוונה או רמז קצרצר בלבד (מקסימום 3-4 שורות) המבוסס ישירות על הפערים שנוצרו בפלט או בערך ההחזרה. "
        "חוקי ברזל: "
        "1. אסור לכתוב את הקוד המלא או לתת את הפתרון בשום אופן! "
        "2. מותר לתת שורת קוד אחת כדוגמה כללית (לא של השאלה עצמה) רק כדי להסביר תחביר. "
        "3. השב תמיד בעברית ברורה, ידידותית וקצרה מאוד."
    )
    
    user_content = (
        f"תוכן השאלה:\n{question_text}\n\n"
        f"הקוד שהתלמיד כתב:\n```python\n{student_code}\n```\n\n"
        f"נתוני ההרצה:\n"
        f"- פלט צפוי (Expected Output): {expected_output}\n"
        f"- פלט בפועל (Actual Output): {actual_output}\n"
        f"- ערך החזרה צפוי (Expected Return): {expected_return}\n"
        f"- ערך החזרה בפועל (Actual Return): {actual_return}"
    )

    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.3, 
            max_tokens=300   
        )
        
        return chat_completion.choices[0].message.content.strip()
        
    except Exception as e:
        return f"שגיאה בפנייה למערכת העזר: {str(e)}"


def create_terminal_window(text):
    """פונקציית עזר ליצירת חלון טרמינל"""
    if not text:
        return "<i style='color: #777;'>אין פלט</i>"
    return f"""
    <div style="
        background-color: #1e1e1e;
        color: #4af626;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 14px;
        padding: 10px;
        border-radius: 6px;
        margin-top: 5px;
        margin-bottom: 5px;
        white-space: pre-wrap;
        direction: ltr;
        text-align: left;
        border: 1px solid #444;
        box-shadow: inset 0 0 5px rgba(0,0,0,0.5);
    ">{text}</div>
    """

def display_all_results(tasks, results,final_grade):
    """
    מקבלת את רשימת המשימות ואת תוצאות ההרצה (כרשימה או כמילון התואם באינדקסים),
    ומציגה את כל הפלטים בפורמט קריא, ידידותי וברור ב-Colab.
    """
    html_elements = []
    grade_row =  f"""
    <div style="font-family: Arial, sans-serif; direction: rtl; text-align: center; background-color: #e3f2fd; color: #0d47a1; padding: 15px; border: 1px solid #90caf9; border-radius: 8px; margin-bottom: 25px; font-size: 24px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 1000;">
    ציון סופי במשימה: {final_grade}
    </div>
    """
    html_elements.append(grade_row)
    # מעבר על כל משימות הבדיקה
    for i in range(len(tasks)):
        task = tasks[i]
        
        # תמיכה גם אם results הועבר כמילון (שמפתחותיו הם מספרי האינדקס) וגם כרשימה
        res = results[i] if isinstance(results, (list, tuple, dict)) else None
        
        if not task or not res:
            continue
            
        # 1. חילוץ נתוני המשימה (tasks)
        # task[0] הוא הרפרנס לפונקציה, לא חובה להציג אותו כי יש לנו את func_call
        func_arg_list = task[1]
        in_list = task[2]
        exp_out_list = task[3]
        expected_return = task[4]
        
        # 2. חילוץ נתוני תוצאות ההרצה (results)
        run_status = res[0]
        func_call = res[1]
        error_message = res[2]
        out_list = res[3]
        actual_return = res[4]
        ai_tip = res[5]
        
        # 3. המרת רשימות ההדפסה למחרוזות (כדי שיוצגו נכון בטרמינל)
        expected_prints_str = "".join(exp_out_list) if exp_out_list else ""
        actual_prints_str = "".join(out_list) if out_list else ""
        
        # בדיקה אם ההדפסה תקינה
        print_match = (actual_prints_str == expected_prints_str)
        
        # טיפול השוואתי ב-return values (למקרה שהמצופה נשמר כרשימה בעלת איבר בודד)
        # exp_ret_val = expected_return[0] if (isinstance(expected_return, list) and len(expected_return) == 1) else expected_return
        return_match = (actual_return == expected_return)
        
        # זיהוי הצלחה: לפי run_status (תמיכה ב-'Ok', 'OK', True)
        is_success = str(run_status).strip().lower() in ['ok', 'true', 'v', '1']
        
        # 4. עיצוב המרכיבים הויזואליים

        status_html = "<span style='color: green; font-weight: bold;'>✅ עבר</span>" if is_success else "<span style='color: red; font-weight: bold;'>❌ נכשל</span>"
        bg_color = "#e8f5e9" if is_success else "#ffebee"
        
        details_html = ""
        if not is_success:
            # אם יש שגיאת קומפילציה/קריסה (error_message קיים)
            if error_message:
                details_html += f"<div style='color: #d32f2f; margin-bottom: 10px; font-size: 15px;'><b>שגיאת מערכת / קריסה (Error):</b> <br><code style='color: #d32f2f;'>{error_message}</code></div>"
            
            else:
                # אם הפער הוא בהדפסה
                if not print_match:
                    details_html += f"""
                    <div style='margin-bottom: 15px;'>
                        <b style='color: #d32f2f;'>שגיאה בהדפסה (Print):</b><br>
                        <span style='font-size: 13px;'>פלט התלמיד:</span>
                        {create_terminal_window(actual_prints_str)}
                        <span style='font-size: 13px;'>פלט מצופה:</span>
                        {create_terminal_window(expected_prints_str)}
                    </div>
                    """
                
                # אם הפער הוא בערך המוחזר
                if not return_match:
                    details_html += f"""
                    <div>
                        <b style='color: #d32f2f;'>שגיאה בערך המוחזר (Return):</b><br>
                        <ul style='margin-top: 5px; direction: ltr; text-align: left; background-color: #f8f9fa; padding: 10px 30px; border-radius: 5px; border: 1px solid #ddd;'>
                            <li><b>Actual (הוחזר בפועל):</b> <code>{repr(actual_return)}</code></li>
                            <li><b>Expected (מצופה):</b> <code>{repr(expected_return)}</code></li>
                        </ul>
                    </div>
                    """
                if ai_tip!='':
                                        details_html += f"""
                    <div>
                        <b style='color: #d32f2f;'>הנחיות הבינה מלאכותית:</b><br>
                        <ul dir="rtl" style='margin-top: 5px; direction: ltr; text-align: left; background-color: #f8f9fa; padding: 10px 30px; border-radius: 5px; border: 1px solid #ddd;'>
                            <li><b>Actual (הוחזר בפועל):</b> <code>{ai_tip}</code></li>
                            
                        </ul>
                    </div>
                    """

        else:
            details_html = "<div style='color: #2e7d32; font-weight: bold; padding: 5px 0;'>כל הכבוד! ההדפסות והערך המוחזר תואמים למצופה.</div>"

        # 5. יצירת בלוק ה-HTML עבור הבדיקה הספציפית הזו
        if is_success:
            # תצוגה קומפקטית לבדיקות שעברו בהצלחה (ללא אקורדיון)
            html_block = f"""
            <div style="font-family: Arial, sans-serif; direction: rtl; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); background-color: #e8f5e9; padding: 10px 15px;">
                <h3 style="margin: 0; font-size: 16px; display: flex; justify-content: space-between; align-items: center;">
                    <span><span style='color: green; font-weight: bold;'>✅ עבר</span> | בדיקת פעולה: <code style="background: rgba(255,255,255,0.7); padding: 2px 6px; border-radius: 4px; direction: ltr; display: inline-block;">{func_call}</code></span>
                </h3>
            </div>
            """
        else:
            # תצוגת אקורדיון נפתחת לבדיקות שנכשלו
            html_block = f"""
            <details style="font-family: Arial, sans-serif; direction: rtl; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); background-color: #fff;">
                <summary style="background-color: #ffebee; padding: 10px 15px; border-bottom: 1px solid #ccc; cursor: pointer; outline: none;">
                    <div style="display: inline-flex; justify-content: space-between; align-items: center; width: 95%;">
                        <h3 style="margin: 0; font-size: 16px;">
                            <span style='color: red; font-weight: bold;'>❌ נכשל</span> | בדיקת פעולה: <code style="background: rgba(255,255,255,0.7); padding: 2px 6px; border-radius: 4px; direction: ltr; display: inline-block;">{func_call}</code>
                        </h3>
                        <span style="font-size: 13px; color: #d32f2f; font-weight: bold;">(לחץ לפירוט ▼)</span>
                    </div>
                </summary>
                
                <div style="padding: 15px; background-color: #fafafa;">
                    <table style="width: 100%; border-collapse: collapse; text-align: right; margin-bottom: 15px; font-size: 14px;">
                        <tr style="background-color: #f5f5f5;">
                            <th style="padding: 8px; border: 1px solid #ddd; width: 50%;">פרמטרים שהועברו (Arguments)</th>
                            <th style="padding: 8px; border: 1px solid #ddd; width: 50%;">קלטים מהמשתמש (Inputs)</th>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #ddd; direction: ltr; text-align: left;"><code>{repr(func_arg_list)}</code></td>
                            <td style="padding: 8px; border: 1px solid #ddd; direction: ltr; text-align: left;"><code>{repr(in_list)}</code></td>
                        </tr>
                    </table>
                    
                    <div style="background-color: #fff; padding: 15px; border: 1px solid #eee; border-radius: 6px;">
                        {details_html}
                    </div>
                </div>
            </details>
            """
        html_elements.append(html_block)
    final_html = f"<div style='max-width: 900px; margin: 0 auto;'>{''.join(html_elements)}</div>"
    return final_html




import subprocess
import time
import socket
import os
import requests

import subprocess
import os
import time
import socket
import shutil

class AIManager:
    def __init__(self, model="llama3.2:1b"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def _is_server_running(self):
        """בדיקה אם הפורט של Ollama כבר פתוח"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', 11434)) == 0

    def setup(self):
       return True
        # """הפונקציה המרכזית שמופעלת מה-Package שלך"""
        
        # # 1. בדיקה אם השרת כבר רץ (מונע כפילויות בהרצה חוזרת)
        # if self._is_server_running():
        #     # מוודא שהמודל קיים גם אם השרת כבר רץ
        #     self._pull_model_if_needed()
        #     return True

        # # 2. איתור הנתיב של Ollama שהותקן בתא ה-Colab
        # ollama_path = shutil.which("ollama") or "/usr/local/bin/ollama"
        # print(ollama_path)
        # if not os.path.exists(ollama_path):
        #     print("❌ שגיאה: פקודת ollama לא נמצאה במערכת.")
        #     print("וודא שהרצת את פקודת ההתקנה בתא הראשון: !curl -fsSL https://ollama.com/install.sh | sh")
        #     return False

        # # 3. הרצת השרת ברקע (רק אם הוא לא רץ)
        # print(f"🚀 מפעיל את שרת ה-AI ברקע...")
        # # שימוש ב-nohup וב-setsid מבטיח יציבות ב-Colab
        # cmd = f"nohup {ollama_path} serve > ollama_log.txt 2>&1 &"
        # subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)

        # # 4. המתנה לעלייה ובדיקת תקינות
        # for i in range(10):
        #     if self._is_server_running():
        #         print("✅ שרת ה-AI עלה בהצלחה!")
        #         self._pull_model_if_needed()
        #         return True
        #     time.sleep(2)
        
        # print("🛑 שגיאה: השרת לא הגיב בזמן. בדוק את ה-GPU ב-Colab.")
        # return False

    def _pull_model_if_needed(self):
        """מוודא שהמודל הספציפי משוך ומוכן לעבודה"""
        print(f"📥 מוודא שהמודל {self.model} מוכן...")
        # פקודת pull ב-Ollama לא מורידה מחדש אם המודל כבר קיים
        os.system(f"ollama pull {self.model} > /dev/null 2>&1")

    def ask(self, prompt):
        system_instructions = (
        "אתה מורה למדעי המחשב בחטיבת ביניים. הסבר בשפה פשוטה ובעברית "
        "מה הבעיה בקוד הבא, בלי לתת את הפתרון המלא מיד. תן רק רמזים."
        )
        
        # שילוב ההנחיות עם הקוד של התלמיד
        full_prompt = f"{system_instructions}\n\nקוד התלמיד:\n{prompt}"
        import requests
        # full_prompt = f'explain in hebrew in simple words what is the problem in this function  {full_prompt}'
        payload = {"model": self.model, "prompt": full_prompt, "stream": False}
        try:
            res = requests.post(self.url, json=payload, timeout=60)
            return res.json().get('response', 'לא התקבלה תשובה')
        except Exception as e:
            return f"שגיאה בפנייה ל-AI: {e}"


    


def run_ai_manager():
    global ai_manager
    ai_manager= AIManager()
    ai_manager.setup()
    