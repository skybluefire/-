#coding:utf-8
#build by LandGrey
#2016-03-10
import re
import socket
import json
# 查询函数, 接收用户输入的ip地址
import requests
import pandas as pd
import streamlit as st
# {"data":
# {"area": "",
#   "country": "中国",
#   "isp_id": "100026",
#   "queryIp": "123.145.210.216",
#   "city": "重庆",
#   "ip": "123.145.210.216",
#   "isp": "联通",
#   "county": "",
#   "region_id": "500000",
#   "area_id": "",
#   "county_id": null,
#   "region": "重庆",
#   "country_id": "CN",
#   "city_id": "500100"},
#  "msg": "query success",
#  "code": 0}

#根据ip获取地理位置
def find_position(ips):
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    # request方式请求taobao的数据 分别有国家 省 区 运营商
    request = s.get("https://ip.taobao.com/outGetIpInfo?ip=+"+ips+"&accessKey=alibaba-inc")
    country.append(json.loads(request.text)['data']['country'])
    region.append(json.loads(request.text)['data']['region'])
    city.append(json.loads(request.text)['data']['city'])
    name.append(str(json.loads(request.text)['data']['isp']))

#根据网址获取ip
def URL2IP():
   for oneurl in urllist.splitlines(True):
       # 只取出//到/中间的字符串 例如：https://www.baidu.com/ 只取出www.baidu.com 上传需要注意格式
       a=re.findall("//([\s\S]*?)/",str(oneurl.strip()))[0]
       # 设置多次尝试
       try:
           # 新的数据 添加列表末尾
           ips =socket.gethostbyname(a)
           ip.append(ips)
           main.append(a)
           # 引用上面定义的方法 用找出的ip 再找出位置
           find_position(ips)

       except:
           # 一次不成功 显示错误
           st.write( "this URL 2 IP ERROR ")
           # 输入默认数据到列表
           ip.append("XX")
           main.append("XX")
           country.append("XX")
           region.append("XX")
           city.append("XX")
           name.append("XX")
# 用户从文本框输入的数据
urllist = st.text_area("Your Indented Markdown goes here: ", "")
# 按钮事件
if st.button("convert!"):
    try:
        # 开始时新建空列表 然后在URL2IP()不断添加
        main = []
        ip = []
        country = []
        region = []
        city = []
        name = []

        URL2IP()
        # 列表输入到表格
        df = pd.DataFrame({'main':main, 'ip':ip, 'country':country, 'region':region, 'city':city, 'name':name})
        # 表格输出到网页
        st.table(df)

        st.write("complete !")
    except:
        st.write("ERROR !")





