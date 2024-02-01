# Copyright (C) 2024 Tomer Tubi - All Rights Reserved

import pandas as pd
import urllib.request
import time
import builtins as __builtin__

test_weight=0.2
question_weight=0.8

# the key is the MD file source
questions_dic={
    '2':['ex2','ex3','ex4'],
    '3':['ex9','ex10','ex11','ex12','ex13','ex14','ex15'],
    '4':['ex4','ex5','ex6','ex7','ex8','ex9'],
    '5':['ex1','ex2','ex3','ex4','ex5','ex6','ex7'],
    '6':['ex2','ex3','ex4','ex5','ex6'],
    '7a':['ex2','ex3','ex4','ex5','ex6','ex7','ex8','ex9','ex10','ex11','ex12'],
    '7b':['ex100','ex101','ex102','ex103','ex104','ex107'],
    '8a':['ex2','ex3','ex4','ex5'],
    '8b':['ex11','ex12','ex13','ex14','ex15','ex16','ex17','ex18'],
    '9':[],
    '10':[],
    '11':['ex4','ex6','ex7','ex8','ex9','ex10','ex11','ex12','ex13','ex14'], # strings
    '11z':['ex4','ex6','ex7','ex8','ex9','ex10','ex11','ex12','ex13','ex14','ex15','ex16','ex17','ex18','ex19'], # strings
    # '12':['3a','3b','4a','4b','5a','5b','6a',6,'7a','7b','8a','8b','9a','9b'], # functions
    '12a':['ex3a','ex3b','ex4a','ex4b','how_many_legs','ex5','ex6a'], # functions
    '12b':['ex7a','ex7b','ex8a','ex8b','ex9a','ex9b'], # functions
    '13a':['ex5','ex6','ex7','ex8'],
    '13b':['ex101','ex102','ex103','ex104','ex105','ex106','ex107'],
    '14':['ex201','ex202','ex203','ex204']
   }

curr_exercise_key = 0

def get_questions(exercise_key):
  global curr_exercise_key
  curr_exercise_key = exercise_key
  if questions_dic.get(exercise_key)!=None:
    return questions_dic[exercise_key]
  else:
    return []
  

def import_tasks(grade,question_set,questions ):
  t=[]
  df = pd.read_csv('./tasks.csv',sep=',',on_bad_lines='skip',encoding='utf-8')

  df = df[df['class']==grade]
  df.question_set = df.question_set.astype(str)
  # ignore last letter of exercise_set
  exerciser_set=str(question_set)[:-1] if not str(question_set).isnumeric() else str(question_set)
  df = df[df['question_set'].isin([exerciser_set])]     
  df = df[df['function'].isin([f'{str(q)}' for q in questions]) ]
  # df = df[df['question_set'].str.contains(1)]
  #   print(df[['function','func_arg_list','in_list','exp_out_list','return_values']])

  for key, value in df.iterrows():
    sublist=[]
    sublist.append(value["function"])
    sublist.append([]) if value["func_arg_list"]==None else  sublist.append(eval(value["func_arg_list"]))
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
            txt_batch = out.read().strip()
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



class CheckAssignment:

    def __init__(self):
        self.test_mode = False
        self.input_counter = 0
        self.input_lst = []
        self.output_lst = []
        self.run_result = {}
        # self.runs = tests




    def run_task(self,func, parms, in_list, expected_result, return_values):
        try:

            self.input_lst=in_list
            self.input_counter = 0
            self.output_lst = []
            result = eval(func + '(' + str(parms)[1:-1] + ')')
            if type(result) == tuple:
                result = list(result)
            else:
                result = [result]

            func_call = func + '(' + str(parms)[1:-1] + ')'
            expected_result = [str(x) for x in expected_result]
            if self.output_lst == expected_result:
              if (return_values == list(result)):
                return True,func_call,'Excellent'
              else:
                return False,func_call,f'Returned: {str(result)} != Expected return: {str(return_values)}'
            else:
              if (return_values == list(result)):
                return False,func_call,f'Printed: {str(self.output_lst)} != Expected print: {str(expected_result)}'
              else:
                return False,func_call,f'Returned: {result} != Expected return: {str(return_values)} and Printed: {str(self.output_lst)} != Expected print: {str(expected_result)}'
          

        except Exception as e:
            func_call = func + '(' + str(parms)[1:-1] + ')'
            return False, func_call, e

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

def run_test(tasks,student_functions):
    output = ''
    correct_answer = 0
    run_results = {}
    for k,v in student_functions.items():
        globals()[k]=v
    ex_count = 0
    global run
    run=CheckAssignment()
    # tasks = function :0 , func_arg_list :1 ,   in_list :2  ,  exp_out_list :3  ,  return_values :4
    for i in range(len(tasks)):
        run.test_mode = True
        start = time.time()
        run_results[ex_count] = run.run_task(tasks[i][0], tasks[i][1], tasks[i][2], tasks[i][3], tasks[i][4])
        end = time.time()
        
        run.test_mode = False
        run_time=end-start
        if run_results[ex_count][0]==True:
            correct_answer+=1
            output += f'Ok {tasks[i][0]}({"" if tasks[i][1]==[] else tasks[i][1]})  \tinput: {tasks[i][2]}  '
            # print(output)
            output += '\n'
        else:

            error_msg=run_results[ex_count][2] if run_time<2 else 'run time too long... '
            output += f'X  {tasks[i][0]}({"" if tasks[i][1]==[] else tasks[i][1]})  \tinput: {tasks[i][2]} \tMessage: {error_msg}'
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
    return round(tests_score),output,round(question_grade),round(final_grade)
