
import requests
import time
from http.server import BaseHTTPRequestHandler

# 获取当前时间
ticks = int(time.time())
print(ticks)
nowTimeArray = time.gmtime(ticks)
print(nowTimeArray)

# 将时间变为20分钟前
bef20 = ticks - 20 * 60
timeB20Array = time.gmtime(bef20)
print(timeB20Array)

# 日期格式化成字符串
date = time.strftime("%Y/%m/%d/", timeB20Array)
print(date)

# 小时格式化成字符串并补零
hour = str(time.strftime("%H", timeB20Array)).zfill(2)

# 分钟格式化并补零
minute = str(time.strftime("%M", timeB20Array))[0] + '0'
# 设置秒数为 00，将其格式化为字符串
second = '00'

# 定义卫星图文件的扩展名
ext = '_0_0.png'

# 拼接出完整的卫星图 URL 地址
picture_url = 'https://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/' + \
    date + hour + minute + second + ext
print(picture_url)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 发送 HTTP 响应头
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()

        # 向卫星图 URL 发送 HTTP 请求并获取响应结果
        res = requests.get(picture_url)

        # 将获取到的卫星图作为响应内容返回给客户端
        self.wfile.write(res.content)
        return
