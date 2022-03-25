# импортируем библиотеки для работы
import requests
from bs4 import BeautifulSoup as BS

# функция для получения кода страницы
def get_html(url):
    # дожидаемся ответа страницы
    response = requests.get(url)
    # возвращаем структуру страницы
    return response.text

# функция для фильтрации данных
def get_data(html):
    # делаем более строгую разметку текста, который возвращает предыдущая функция
    soup = BS(html, 'lxml')
    # нашли блок, в котором лежат все телефоны
    catalog = soup.find('div', 'list-view')
    # нашли все телефоны и вернули в виде списка элементов
    phones = catalog.find_all('div', 'product_listbox')
    # тестируем нахождение названия и цены на примере одного телефона
    # print(phones[0].find('div', 'listbox_title').find('a').text.strip())
    # print(phones[0].find('div', 'listbox_price').find('strong').text.strip())
    # перебираем все телефоны и из каждого берем название и цену
    for phone in phones:
        # обрабатываем возможное отсутствие цены или названия, во избежание ошибки просто оставляем пустую строку
        try:
            title = phone.find('div', 'listbox_title').find('a').text.strip()
        except: 
            title = ''
        try:
            price = phone.find('div', 'listbox_price').find('strong').text.strip()
        except:
            price = ''

        # вызываем функцию для записи данных в текстовый документ
        write_data(title, price)

# функция, которая будет записывать данные в документ
def write_data(title, price):
    # открыли файл в режиме добавления данных, чтобы они не перезаписывались
    with open('phones.txt', 'a+') as f:
        # записали одну строку, в конце \n перенесет курсор на следующую строку, 
        # таким образом каждая строчка будет начинаться с начала, 
        # а не продолжать предыдущую
        f.write(f'{title}/{price}\n')

# функция, которая запускает всю логику
def main():
    # для одной страницы
    # url = 'https://www.kivano.kg/mobilnye-telefony'
    # html = get_html(url)
    # data = get_data(html)

    # для всех
    pages = 29
    for i in range(1, pages + 1):
        print(f'Парсинг {i} страницы...')
        url = f'https://www.kivano.kg/mobilnye-telefony?page={i}'
        html = get_html(url)
        data = get_data(html)

# запускаем парсинг
main()