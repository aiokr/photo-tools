import requests
from io import BytesIO
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 解析URL中的查询字符串
        query = parse_qs(urlparse(self.path).query)
        url = query.get('url', [''])[0]
        width = query.get('w', [''])[0]
        height = query.get('h', [''])[0]
        quality = query.get('q', [''])[0]

        rawImage = BytesIO(requests.get(url).content)
        image = cv.imread(rawImage)

        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.send_header('Cache-Control', 's-maxage=2419200')
        self.end_headers()