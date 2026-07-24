import os
import re
import json

# קןבץ זה משמש ליצירת מאגר שאלות מתיקיית מסוימת 

def parse_markdown_files_to_json(directory_path, output_json_path):
    all_tasks = {}
    
    # חיפוש תבנית השם
    filename_pattern = re.compile(r"^ex([^_]+)_.*\.md$")
    
    # חיפוש תבנית השאלה
    question_pattern = re.compile(r"##\s*(?:שאלה|תרגיל)\s+(\d+)")
    
    # חיפוש סעיפים פנימיים
    bullet_pattern = re.compile(r"(?:^|\n)\s*([א-ת])\.\s+")
    
    # מילון המרה מעברית לאנגלית
    hebrew_to_english = {
        'א': 'a', 'ב': 'b', 'ג': 'c', 'ד': 'd', 'ה': 'e',
        'ו': 'f', 'ז': 'g', 'ח': 'h', 'ט': 'i', 'י': 'j',
        'כ': 'k', 'ל': 'l', 'מ': 'm', 'נ': 'n', 'ס': 'o',
        'ע': 'p', 'פ': 'q', 'צ': 'r', 'ק': 's', 'ר': 't',
        'ש': 'u', 'ת': 'v'
    }

    for filename in os.listdir(directory_path):
        match = filename_pattern.match(filename)
        if match:
            task_key = match.group(1)
            file_path = os.path.join(directory_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            parts = question_pattern.split(content)
            task_dict = {}
            
            for i in range(1, len(parts), 2):
                q_num = parts[i]
                q_text = parts[i+1].replace('<mycode>', '').strip()
                
                sub_parts = bullet_pattern.split(q_text)
                
                if len(sub_parts) > 1:
                    # מדלגים לחלוטין על sub_parts[0] שזה הפתיח של השאלה
                    for j in range(1, len(sub_parts), 2):
                        heb_letter = sub_parts[j]
                        sub_text = sub_parts[j+1].rstrip()
                        
                        eng_letter = hebrew_to_english.get(heb_letter, 'x')
                        key = f"ex{q_num}{eng_letter}"
                        
                        # שמירת הסעיף בלבד (לדוגמה: "א. ממוצע ציונים.")
                        task_dict[key] = f"{heb_letter}. {sub_text}"
                else:
                    task_dict[f"ex{q_num}"] = q_text
            
            if task_dict:
                all_tasks[task_key] = task_dict

    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_tasks, json_file, ensure_ascii=False, indent=4)
        
    print(f"✅ עובדו {len(all_tasks)} קבצים. הקובץ נשמר בהצלחה ב-{output_json_path}")
# --- הפעלת הסקריפט ---
# החלף את נתיב התיקייה שבה נמצאים קבצי ה-md שלך
directory = r'C:\\TEACHING\\חומר לימוד\\עמט\\Python\\MD_assignment\\MD Files' 
output_file = r'C:\\Users\\User\\Google_Drive_1002129899_educ_org_il\\auto_grading_repo\\auto_grading\\tasks_db.json'

parse_markdown_files_to_json(directory, output_file)