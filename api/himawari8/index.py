
import requests
import time
from PIL import Image
from io import BytesIO
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

# 向卫星图 URL 发送 HTTP 请求并获取响应结果
# res = requests.get(picture_url)

# 四分片高清图
hdPic1_url = 'https://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/' + \
    date + hour + minute + second + '_0_0.png'
hdPic2_url = 'https://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/' + \
    date + hour + minute + second + '_0_1.png'
hdPic3_url = 'https://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/' + \
    date + hour + minute + second + '_1_0.png'
hdPic4_url = 'https://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/' + \
    date + hour + minute + second + '_1_1.png'

hdPic1 = BytesIO(requests.get(hdPic1_url).content)
hdPic2 = BytesIO(requests.get(hdPic2_url).content)
hdPic3 = BytesIO(requests.get(hdPic3_url).content)
hdPic4 = BytesIO(requests.get(hdPic4_url).content)

img1 = Image.open(hdPic1)
img2 = Image.open(hdPic2)
img3 = Image.open(hdPic3)
img4 = Image.open(hdPic4)

IMAGE_COLUMN = 2
IMAGE_ROW = 2
IMAGE_SIZE_y = 550
IMAGE_SIZE_x = 550


def image_compose():
    # 创建一个新的空白图像，宽度为两张图片宽度之和，高度为两张图片高度之和
    new_image = Image.new('RGB', (IMAGE_SIZE_x*2, IMAGE_SIZE_y*2))

    # 将四张图片依次粘贴到新图像上
    new_image.paste(img1, (0, 0))
    new_image.paste(img3, (IMAGE_SIZE_x, 0))
    new_image.paste(img2, (0, IMAGE_SIZE_y))
    new_image.paste(img4, (IMAGE_SIZE_x, IMAGE_SIZE_y))

    output = BytesIO()
    new_image.save(output, format='JPEG')
    result_image = output.getvalue()

    return result_image


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 发送 HTTP 响应头
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.send_header('Cache-Control', 's-maxage=600')
        self.end_headers()

        # 将获取到的卫星图作为响应内容返回给客户端
        self.wfile.write(image_compose())
        return
