import requests




def download_code(url,target_name):
  response = requests.get(url, headers={'Cache-Control': 'no-cache'}) # open(url.split('/')[-1], 'w')
  with open(target_name,'w')  as file:
    file.write(response.content.decode())



def download_files():
  url=r'https://raw.githubusercontent.com/tomer2b/auto_grading/main/auto_gradeing.py'
  download_code(url,'auto_gradeing.py')
  url=r'https://raw.githubusercontent.com/tomer2b/auto_grading/main/tasks.csv'
  download_code(url,'tasks.csv')





download_files()
