#!/bin/bash

# ==============================================
# Мой первый инструмент для разведки
# Использование: ./recon.sh http://example.com
# ==============================================

# Проверяем, передан ли аргумент (URL сайта)
if [ -z "$1" ]; then
    echo "[!] Ошибка: укажите URL сайта"
    echo "[!] Пример: ./recon.sh http://127.0.0.1:5000"
    exit 1
fi

URL=$1
DOMAIN=$(echo $URL | cut -d'/' -f3) # Извлекаем домен из URL

echo "========================================="
echo "Начинаем разведку против: $URL"
echo "Домен: $DOMAIN"
echo "Время: $(date)"
echo "========================================="

# Создаём папку для результатов
mkdir -p recon_results/$DOMAIN
cd recon_results/$DOMAIN

echo "[1] Получаем заголовки ответа..."
curl -I "$URL" > headers.txt 2>&1
echo "    [+] Заголовки сохранены в: headers.txt"

echo "[2] Получаем полный ответ сервера..."
curl -s "$URL" > index.html
echo "    [+] HTML сохранён в: index.html"

echo "[3] Ищем интересные подсказки в HTML..."
echo "    [+] Ищем email-адреса:"
grep -E -o "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b" index.html | sort -u > emails.txt
cat emails.txt

echo "    [+] Ищем комментарии в коде:"
grep -n "<!--" index.html > comments.txt
echo "        Найдено комментариев: $(wc -l < comments.txt)"

echo "    [+] Ищем JavaScript файлы:"
grep -o 'src="[^"]*\.js"' index.html | cut -d'"' -f2 > js_files.txt
echo "        Найдено JS файлов: $(wc -l < js_files.txt)"
cat js_files.txt

echo "[4] Проверяем стандартные пути (фаззинг директорий)..."
echo "    Это может занять минуту..."

# Создаём простой список для проверки (ты можешь расширить его)
PATHS="admin login register api dashboard phpmyadmin wp-admin config backup profile search catalog register"

for path in $PATHS; do
    response_code=$(curl -o /dev/null -s -w "%{http_code}" "$URL/$path")
    
    if [ "$response_code" != "404" ] && [ "$response_code" != "000" ]; then
        echo "    [+] Найдено: /$path (код: $response_code)"
        echo "/$path" >> found_paths.txt
    fi
done

echo ""
echo "[5] Итоги разведки:"
echo "    [+] Все файлы сохранены в папке: recon_results/$DOMAIN/"
echo "    [+] Проверь файлы:"
echo "        - headers.txt     (заголовки сервера)"
echo "        - index.html      (код главной страницы)"
echo "        - found_paths.txt (найденные интересные пути)"
echo "        - emails.txt      (найденные email)"
echo "        - js_files.txt    (подключённые JS файлы)"
echo ""
echo "========================================="
echo "Разведка завершена! Изучи файлы выше."
echo "Следующий шаг — анализ найденных точек входа."
echo "========================================="

# Возвращаемся в исходную папку
cd ../..
