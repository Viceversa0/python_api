# 天气预报API
## 功能

从[中国天气网](http://www.weather.com.cn/)抓取数据返回1-7天的天气数据，包括：
+ 日期
+ 天气
+ 温度
+ 风力
+ 风向
```
 def get_weather(city):
 ```
### 入参：
城市名，type为字符串，如西安、北京，因为数据引用中国气象网，因此只支持中国城市
### 返回：
1、列表，包括1-7的天气数据，每一天的分别为一个列表成员，列表内为字符串，代表内容如上所示
2、None，城市不在*city_code_in_weather_report.txt*内

---

## 文件说明
+ city_code_in_weather_report.txt：存放中国天气网内各个城市代码
+ requirements.txt：用到的库及其版本
+ weather_api.py：主角
+ run.png：运行截图

