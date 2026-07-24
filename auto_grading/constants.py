import json
import pkgutil

# טעינת הנתונים מהקובץ שנמצא באותה תיקייה
data = pkgutil.get_data(__name__, 'tasks_db.json')
tasks_db = json.loads(data.decode('utf-8'))
api='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'