import requests

url = 'https://api.codelife.cc/api/top/list'
data = {
    'id': 'KqndgxeLl9'
}
response = requests.post(url, data=data).json()
news_list = response['data']
for item in news_list:
    print(item)
