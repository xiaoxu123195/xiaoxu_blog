import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}


def get_addr_info(ip):
    url = f'https://www.ip138.com/iplookup.php?ip={ip}&action=2'
    res = requests.get(url, headers=headers).text
    result = re.findall(r'<td><span>(.*?)</span></td>', res, re.S)[0]
    print(result)


if __name__ == '__main__':
    get_addr_info('223.88.55.16')
    get_addr_info('106.13.185.190')
    get_addr_info('120.228.2.238')
