__version__ = '0.1'
__author__ = 'Tomer Tubi'

from .auto_gradeing_code import test_weight,question_weight
from .auto_gradeing_code import questions_dic
from .auto_gradeing_code import get_questions
from .auto_gradeing_code import import_tasks
from .auto_gradeing_code import custom_syntax_error_handler
from .auto_gradeing_code import ai_manager
from .auto_gradeing_code import print,input,grade_student_functions,run_test,CheckAssignment,create_queue,run_ai_manager

import json
import pkgutil

# טעינת הנתונים מהקובץ שנמצא באותה תיקייה
data = pkgutil.get_data(__name__, 'tasks_db.json')
tasks_db = json.loads(data.decode('utf-8'))

api1='gsk'
api2='_TLltgHckDD34'
api3='0O1mYIyxWGdyb3FYjjrbYpZj'
api4='tDJDXD8EaUT6DoeG'
api=api1+api2+api3+api4