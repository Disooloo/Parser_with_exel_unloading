import requests
from bs4 import BeautifulSoup
import openpyxl

# Указываем URL страницы раздела магазина, который нам нужен
url = "https://example.com/products"

# Создаем объект Excel-файла
workbook = openpyxl.Workbook()
# Получаем активный лист
worksheet = workbook.active
# Добавляем заголовки столбцов
worksheet.append(["Название", "Описание", "Цена"])

# Функция для получения информации о товаре
def parse_product(product_url):
    # Запрос к странице товара
    response = requests.get(product_url)
    # Создаем объект BeautifulSoup для парсинга страницы
    soup = BeautifulSoup(response.content, "html.parser")
    # Находим заголовок товара
    title = soup.find("h1").text.strip()
    # Находим описание товара
    description = soup.find("div", class_="description").text.strip()
    # Находим цену товара
    price = soup.find("span", class_="price").text.strip()
    # Возвращаем полученную информацию в виде словаря
    return {"title": title, "description": description, "price": price}

# Отправляем запрос к странице раздела магазина
response = requests.get(url)
# Создаем объект BeautifulSoup для парсинга страницы
soup = BeautifulSoup(response.content, "html.parser")
# Находим список карточек товаров на странице
product_cards = soup.find_all("div", class_="product-card")

# Обрабатываем каждую карточку товара
for product_card in product_cards:
    # Находим ссылку на страницу товара в карточке
    product_url = product_card.find("a")["href"]
    # Получаем информацию о товаре с помощью функции parse_product
    product_info = parse_product(product_url)
    # Добавляем информацию о товаре в Excel-файл
    worksheet.append([product_info["title"], product_info["description"], product_info["price"]])

# Сохраняем Excel-файл
workbook.save("products.xlsx")