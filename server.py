#!/usr/bin/env python3
print("Сервер запущен: http://localhost:8000")
print("Отправляй запросы: curl 'http://localhost:8000/?test=123'")
print("CTRL+C для остановки\n")

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8000))
sock.listen(1)

while True:
    conn, addr = sock.accept()
    data = conn.recv(1024).decode()
    
    if data:
        print("[ЗАПРОС]:")
        print(data[:200])
        
        # Простейший ответ
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html\r\n"
        response += "\r\n"
        response += "<h1>Работает!</h1>"
        response += "<p>Смотри вывод в консоли сервера</p>"
        
        conn.send(response.encode())
    conn.close()
