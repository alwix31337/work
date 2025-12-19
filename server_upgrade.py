from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Парсим URL
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        
        # Логируем в консоль
        print(f"\n[+] Запрос: {self.path}")
        print(f"[+] Параметры: {params}")
        
        # Отправляем ответ
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = f"""
        <html><body>
        <h1>Сервер работает</h1>
        <p>Путь: {self.path}</p>
        <p>Параметры: {params}</p>
        </body></html>
        """
        self.wfile.write(html.encode())

print("Сервер запущен: http://localhost:8000")
print("Тестируй: curl 'http://localhost:8000/?test=123'")
HTTPServer(('localhost', 8000), MyHandler).serve_forever()
EOF
