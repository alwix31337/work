import requests
import difflib

url = "http://localhost:8000/"

# Эталонный нормальный запрос
normal = requests.get(url, params={'id': '1'}).text

tests = [
    ("SQLi проверка", "1'"),
    ("SQLi всегда true", "1' OR '1'='1"),
    ("SQLi всегда false", "1' AND '1'='2"),
    ("XSS basic", "<script>alert(1)</script>"),
    ("Path Traversal", "../../etc/passwd"),
]

print("Анализ ответов сервера:\n")

for name, payload in tests:
    r = requests.get(url, params={'id': payload})
    
    print(f"\n{'='*60}")
    print(f"ТЕСТ: {name}")
    print(f"Payload: {payload}")
    print(f"Длина ответа: {len(r.text)} (норма: {len(normal)})")
    
    # Сравниваем с нормальным ответом
    diff = difflib.SequenceMatcher(None, normal, r.text).ratio()
    print(f"Схожесть с нормальным ответом: {diff:.1%}")
    
    # Ищем ключевые слова
    keywords = ['error', 'sql', 'syntax', 'warning', 'exception', 'undefined']
    found = []
    for kw in keywords:
        if kw in r.text.lower():
            found.append(kw)
    
    if found:
        print(f"⚠️  Найдены ключевые слова: {found}")
    
    # Если длина сильно отличается
    if abs(len(r.text) - len(normal)) > 100:
        print("🚨 БОЛЬШАЯ разница в длине ответа!")
        print("Вероятные причины:")
        print("  - Сервер вернул ошибку")
        print("  - Вернул больше/меньше данных")
        print("  - Изменилась структура страницы")

print("\n" + "="*60)
print("ВЫВОД: Если есть различия в ответах - сайт может быть уязвим.")
print("Следующий шаг: доказать уязвимость, поняв КАК сервер обрабатывает ввод.")
