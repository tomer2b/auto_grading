import requests
  
def download_code(url):
  response = requests.get(url, headers={'Cache-Control': 'no-cache'})
  with open(url.split('/')[-1], 'w') as file:
    file.write(response.content.decode())

  # urllib.request.urlretrieve(url_with_timestamp,url.split('/')[-1])

def download_files():
  url=r'https://raw.githubusercontent.com/RabinSchool/auto_grading/main/auto_gradeing.py'
  download_code(url)
  url=r'https://raw.githubusercontent.com/RabinSchool/auto_grading/main/tasks.csv'
  download_code(url)

download_files()
