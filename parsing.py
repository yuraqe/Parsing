from bs4 import BeautifulSoup
import requests
import csv


def request(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Проверка на HTTP ошибки
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, 'lxml')
    except requests.RequestException as e:
        print(f"Ошибка запроса к {url}: {e}")
        return None

def get_product_links():
    product_links = []
    for chapter in range(1, 6):
        for page in range(1, 5):
            url = f'https://parsinger.ru/html/index{chapter}_page_{page}.html'
            soup = request(url)
            if soup:
                links = soup.find_all('a', class_='name_item')
                product_links.extend(f'https://parsinger.ru/html/{link["href"]}' for link in links)
    return product_links

def extract_product_data(url):
    soup = request(url)
    if not soup:
        return None

    try:
        name = soup.find('p', id='p_header').text.strip()
        article = soup.find('p', class_='article').text.split(':')[-1].strip()
        brand = soup.find('li', id='brand').text.split(':')[-1].strip()
        model = soup.find('li', id='model').text.split(':')[-1].strip()
        in_stock = soup.find('span', id='in_stock').text.split(':')[-1].strip()
        price = soup.find('span', id='price').text.strip()
        old_price = soup.find('span', id='old_price').text.strip()

        return [name, article, brand, model, in_stock, price, old_price, url]
    except AttributeError as e:
        print(f"Ошибка при парсинге {url}: {e}")
        return None

def main():
    output_file = 'file.csv'
    headers = ['Наименование', 'Артикул', 'Бренд', 'Модель', 'Наличие', 'Цена', 'Старая цена', 'Ссылка']

    try:
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(headers)

            product_links = get_product_links()
            for link in product_links:
                product_data = extract_product_data(link)
                if product_data:
                    writer.writerow(product_data)

        print(f"Данные успешно записаны в {output_file}")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")


if __name__ == '__main__':
    main()