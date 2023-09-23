from urllib.parse import *


dic = {
    'word': [12, 22],
    'key': 'python'
}  # => word=12&word=22&key=python

print(parse_qs('word=12&word=22'))  # {'word': ['12', '22']},
print(urlencode(dic, doseq=True))  # word=12&word=22
print(urlencode(dic))  # word=%5B12%2C+22%5D
