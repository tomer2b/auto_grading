import json
import pkgutil

# טעינת הנתונים מהקובץ שנמצא באותה תיקייה
data = pkgutil.get_data(__name__, 'tasks_db.json')
tasks_db = json.loads(data.decode('utf-8'))
api='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'

error_explanations = {
    "NameError": """
<div dir="rtl">
<p><strong>NameError (שגיאת שם):</strong> מתרחשת כשפייתון אינה מכירה את השם שניסית להשתמש בו. לרוב מדובר בשגיאת כתיב בשם המשתנה, ניסיון להשתמש במשתנה שטרם הוגדר, או ששכחת לשים מירכאות סביב מחרוזת טקסט.</p>
<pre dir="ltr" style="text-align: left; background-color: #272822; color: #f8f8f2; padding: 10px; border-radius: 5px; font-family: monospace;"><code>#  קוד שגוי (חסרות מירכאות ולכן פייתון מחפשת משתנה בשם hello):
print(hello)

#  קוד מתוקן:
print("hello")</code></pre>
</div>
""",

    "TypeError": """
    <div dir="rtl">
        <p><strong>TypeError (שגיאת סוג):</strong> מתרחשת כשמנסים לבצע פעולה בין סוגי נתונים שאינם תואמים, כגון חיבור של מספר וטקסט (מחרוזת) יחד ללא המרה מוקדמת.</p>
        <pre dir="ltr" style="text-align: left; background-color: #272822; color: #f8f8f2; padding: 10px; border-radius: 5px; font-family: monospace;"><code>#  קוד שגוי (חיבור מחרוזת למספר שלם):
age = 16
print("You are " + age)

#  קוד מתוקן (המרה למחרוזת):
print("You are " + str(age))</code></pre>
    </div>
    """,

    "SyntaxError": """
    <div dir="rtl">
        <p><strong>SyntaxError (שגיאת תחביר):</strong> פייתון לא מצליחה לקרוא את הקוד כי חסר סימן פיסוק הכרחי (כמו נקודתיים, פסיק או סוגריים שלא נסגרו כראוי).</p>
        <pre dir="ltr" style="text-align: left; background-color: #272822; color: #f8f8f2; padding: 10px; border-radius: 5px; font-family: monospace;"><code>#  קוד שגוי (חסרות נקודתיים בסוף תנאי if):
if x > 5
    print(x)

#  קוד מתוקן:
if x > 5:
    print(x)</code></pre>
    </div>
    """,

    "IndexError": """
    <div dir="rtl">
        <p><strong>IndexError (חריגה מגבולות):</strong> מתרחשת כשמנסים לגשת למיקום (אינדקס) ברשימה או במחרוזת שאינו קיים. זכור שהספירה בפייתון תמיד מתחילה מ-0.</p>
        <pre dir="ltr" style="text-align: left; background-color: #272822; color: #f8f8f2; padding: 10px; border-radius: 5px; font-family: monospace;"><code>#  קוד שגוי (הרשימה באורך 3, האינדקסים הם 0,1,2):
lst = [10, 20, 30]
print(lst[3])

#  קוד מתוקן (הגישה לאיבר האחרון היא באינדקס 2):
print(lst[2])</code></pre>
    </div>
    """,

    "ValueError": """
    <div dir="rtl">
        <p><strong>ValueError (שגיאת ערך):</strong> מתרחשת כשהפעולה מקבלת את סוג הנתון הנכון, אך התוכן עצמו אינו חוקי עבורה (למשל, ניסיון להמיר מילה שאינה מכילה ספרות למספר).</p>
        <pre dir="ltr" style="text-align: left; background-color: #272822; color: #f8f8f2; padding: 10px; border-radius: 5px; font-family: monospace;"><code>#  קוד שגוי (אי אפשר להמיר מילה כזו למספר מתמטי):
num = int("apple")

#  קוד מתוקן:
num = int("42")</code></pre>
    </div>
    """,

    "AttributeError": """
    <div dir="rtl">
        <p><strong>AttributeError (שגיאת תכונה/פעולה):</strong> מתרחשת כשמנסים להפעיל פעולה שאינה קיימת עבור סוג הנתון המסוים. לרוב מדובר בבלבול בין פעולות של רשימות, מחרוזות ומילונים.</p>
        <pre dir="ltr" style="text-align: left; background-color: #272822; color: #f8f8f2; padding: 10px; border-radius: 5px; font-family: monospace;"><code>#  קוד שגוי (למחרוזת אין פעולת append, היא מיועדת לרשימות):
text = "hello"
text.append("!")

#  קוד מתוקן (שרשור מחרוזות פשוט):
text = text + "!"</code></pre>
    </div>
    """,

    "KeyError": """
    <div dir="rtl">
        <p><strong>KeyError (שגיאת מפתח במילון):</strong> מתרחשת כשמנסים לשלוף נתון ממילון באמצעות מפתח (Key) שאינו קיים בו.</p>
        <pre dir="ltr" style="text-align: left; background-color: #272822; color: #f8f8f2; padding: 10px; border-radius: 5px; font-family: monospace;"><code>#  קוד שגוי (המפתח 'age' טרם הוגדר במילון):
student = {"name": "Ron"}
print(student["age"])

#  קוד מתוקן (שימוש בפעולת get המונעת שגיאה אם המפתח חסר):
print(student.get("age", "הנתון חסר"))</code></pre>
    </div>
    """,
    
    "IndentationError": """
    <div dir="rtl">
        <p><strong>IndentationError (שגיאת הזחה):</strong> פייתון מזהה חוסר התאמה ברווחים או בטאבים בתחילת השורה. זה קורה לרוב בתוך לולאות, תנאים או פונקציות.</p>
        <pre dir="ltr" style="text-align: left; background-color: #272822; color: #f8f8f2; padding: 10px; border-radius: 5px; font-family: monospace;"><code>#  קוד שגוי (חסרה הזחה פנימה לאחר הגדרת הפונקציה):
def say_hi():
print("Hi!")

#  קוד מתוקן (הוספת טאב/רווחים):
def say_hi():
    print("Hi!")</code></pre>
    </div>
    """
}