import requests
import re
from bs4 import BeautifulSoup

head = 'http://www.weather.com.cn/weather/'
suffix = '.shtml'
txt = 'city_code_in_weather_report.txt'


def __load_code():  # .txt->dict
    result = dict()
    with open(txt, 'r', encoding='utf-8') as f:
        line = f.readline()  # 每行格式为  101010100=北京
        while line != '':
            line.strip()
            if line is not None:
                line = line.strip()
                index = line.find('=')
                code = line[:index]
                city = line[index + 1:]
                result[city] = code
            line = f.readline()
    return result


def get_list(s_html):  # html->字符串list
    result = []
    for i in s_html:
        arr = i.get_text().split('\n')
        while True:  # 删除空白字符
            try:
                arr.remove('')
            except ValueError:
                break
        result.append(arr)
        # 结果的array应该如：['14日（今天）', '多云转晴', '14/4℃', '<3级']
    return result


def wind_dir(s_html):  # 风向比较特殊，有效内容在class内，特殊处理
    result = []
    pattern = r'title=".*"'
    for i in s_html:
        tags = i.find_all('span')

        for j in tags:
            res = re.search(pattern, str(j))
            if res is not None:
                result.append(res.group()[7:-2])
    return result


def get_html(soup, tag):  # 筛选tag为‘li’的内容，因为有效数据在这里
    res = []
    html = soup.find_all(tag)
    for i in html:
        try:
            # sky skyid lv2 被分成了['sky', 'skyid', 'lv2']
            if i['class'][0] == 'sky' and i['class'][1] == 'skyid' and re.fullmatch('lv\d', str(i['class'][2])):
                res.append(i)
        except KeyError:
            pass
    return res


def get_weather(city):
    dic = __load_code()
    if city not in dic:
        return None
    r = requests.get(head + dic[city] + suffix)
    r.encoding = r.apparent_encoding
    html_doc = r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    ori_html = get_html(soup, 'li')

    w_list = get_list(ori_html)
    wind_list = wind_dir(ori_html)
    index = 0
    for i in w_list:  # 合并风向和其他参数
        i.append(wind_list[index])
        index += 1
    # 得到了1-7天完整的数据
    return w_list


if __name__ == "__main__":
    print(get_weather('西安'))
