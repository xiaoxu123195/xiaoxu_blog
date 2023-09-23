import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}


# 获取ip
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
        return ip
    ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip


def get_addr_info(ip):
    if ip.startswith('10.') or ip.startswith('192.') or ip.startswith('127.'):
        return '中国'
    url = f'https://www.ip138.com/iplookup.php?ip={ip}&action=2'
    res = requests.get(url, headers=headers).text
    result = re.findall(r'<td><span>(.*?)</span></td>', res, re.S)[0]
    return result

#
# if __name__ == '__main__':
#     get_addr_info('223.88.55.16')
#     get_addr_info('106.13.185.190')
#     get_addr_info('120.228.2.238')
