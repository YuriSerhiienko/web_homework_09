import requests
from bs4 import BeautifulSoup
import json

# Отримання HTML-коду сторінки
base_url = 'http://quotes.toscrape.com'
response = requests.get(base_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Функція для отримання даних автора зі сторінки автора
def get_author_data(author_url):
    author_response = requests.get(author_url)
    author_soup = BeautifulSoup(author_response.text, 'html.parser')
    
    fullname = author_soup.find('h3', class_='author-title').text
    born_date = author_soup.find('span', class_='author-born-date').text
    born_location = author_soup.find('span', class_='author-born-location').text
    description = author_soup.find('div', class_='author-description').text.strip()
    
    author_data = {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }
    return author_data

# Отримання даних про цитати та авторів
quotes_data = []
authors_data = []

while True:
    # Отримання даних про цитати
    for quote in soup.find_all('div', class_='quote'):
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        author = quote.find('small', class_='author').text
        quote_text = quote.find('span', class_='text').text
        
        quote_data = {
            "tags": tags,
            "author": author,
            "quote": quote_text
        }
        quotes_data.append(quote_data)
        
        # Перевірка чи автор вже був доданий до списку авторів
        if author not in [author_data["fullname"] for author_data in authors_data]:
            author_url = base_url + quote.find_next('a')['href']
            author_data = get_author_data(author_url)
            authors_data.append(author_data)
    
    # Перехід на наступну сторінку
    next_page = soup.find('li', class_='next')
    if next_page:
        next_page_url = base_url + next_page.find('a')['href']
        response = requests.get(next_page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        break

# Збереження даних у JSON-файлах
with open('qoutes.json', 'w', encoding='utf-8') as quotes_file:
    json.dump(quotes_data, quotes_file, ensure_ascii=False, indent=4)

with open('authors.json', 'w', encoding='utf-8') as authors_file:
    json.dump(authors_data, authors_file, ensure_ascii=False, indent=4)

print("Дані були успішно зібрані та збережені у JSON-файлах.")
