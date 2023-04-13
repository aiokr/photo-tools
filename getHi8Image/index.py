# %%
from http.server import BaseHTTPRequestHandler
import requests

# 定义卫星图的 URL 地址
url_base = 'https://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/'

# 获取当前时间并将其格式化为字符串
date = datetime.datetime.utcnow().strftime('%Y/%m/%d/')

# 获取当前小时数并减去 1，将其格式化为字符串并补零
hour = str(int(datetime.datetime.utcnow().strftime('%H')) - 1).zfill(2)

# 获取当前分钟数的十位数并补零，将其格式化为字符串
minute = str(datetime.datetime.utcnow().strftime('%M'))[0] + '0'

# 设置秒数为 00，将其格式化为字符串
second = '00'

# 定义卫星图文件的扩展名
ext = '_0_0.png'

# 拼接出完整的卫星图 URL 地址
picture_url = url_base + date + hour + minute + second + ext
print(picture_url)

# 定义一个处理 HTTP 请求的类
class handler(BaseHTTPRequestHandler):
    # 当接收到 GET 请求时执行的方法
    def do_GET(self):
        # 发送 HTTP 响应头
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.end_headers()

        # 向卫星图 URL 发送 HTTP 请求并获取响应结果
        res = requests.get(picture_url)
        
        # 将获取到的卫星图作为响应内容返回给客户端
        self.wfile.write(res.content)

# 如果直接运行该文件，则启动 HTTP 服务器并监听 8080 端口
if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('0.0.0.0', 8080), handler)
    server.serve_forever()



