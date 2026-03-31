import urllib.request
import urllib.parse
import re

def extract_links(url, output_file="links.txt"):
    try:
        # Відправляємо GET-запит за вказаною URL-адресою
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        
        # Читаємо та декодуємо HTML-код сторінки
        html_content = response.read().decode('utf-8', errors='ignore')

        # Регулярний вираз для пошуку атрибутів href всередині тегів <a>
        # Шукає конструкцію: <a ... href="URL" ...>
        regex = r'<a[^>]+href=["\'](.*?)["\']'
        
        # Знаходимо всі збіги
        links = re.findall(regex, html_content)

        # Зберігаємо знайдені посилання у текстовий файл
        with open(output_file, 'w', encoding='utf-8') as file:
            for link in links:
                link=urllib.parse.unquote(link)
                file.write(link + '\n')

        print(f"Успішно знайдено посилань: {len(links)}.")
        print(f"Результати збережено у файл: {output_file}")

    except Exception as e:
        print(f"Сталася помилка під час обробки {url}: {e}")

# Приклад виклику функції
if __name__ == "__main__":
    target_url = "https://uk.wikipedia.org" # Замініть на потрібний URL
    extract_links(target_url)