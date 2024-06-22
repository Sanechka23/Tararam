import requests
from bs4 import BeautifulSoup
import re

def get_loft_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    loft_data = []
    # Находим все блоки с результатами клубов
    result_blocks = soup.find_all('div', class_='card-body')
    for block in result_blocks:
        # Находим название клуба
        club_name = block.find('a', class_='card-title').text.strip()

        # Находим ссылки
        url2 = block.find('a', class_='card-title')['href'] 
        url3 = 'https://www.loft2rent.ru' + url2

        def extract_metro_station(metro_text):
          """Извлекает название станции метро из текста, удаляя все цифры."""
          return re.sub(r'\d+', '', metro_text).strip()

        # Находим станцию метро (уточненный поиск)
        metro_list = []
        metro_elements = block.find_all('p', class_='text-blue')  # Используем find_all для поиска всех элементов
        for metro_element in metro_elements:
          metro_text = metro_element.get_text(strip=True)
          metro_station = metro_text.split(' ')[0]
          metro_station = extract_metro_station(metro_station) 
          metro_list.append('м. '+ metro_station)
         
        # Находим цену
        price_list= []
        pr = block.find('div', class_='card-data d-column')
        
        bold_elements = pr.find_all('b')
        price_value = bold_elements[2].text
        price_list.append('от ' + price_value +' р')


        loft_data.append({
            'name': club_name,
            'url': url3,
            'metro': metro_list,
            'price': price_list 
        })

    return loft_data


def pars_2():
    # Начальная страница
    url = 'https://www.loft2rent.ru/loft/?city=65322&text=&price_start=&price_end=&people_start=&people_end=&area_start=&area_end=&party_date=&&'
    all_loft_data = []

    # Парсим все страницы
    for page_number in range(1, 5):  #Мы сократили количество страниц для быстроты ответа (max 23)
        current_url = url + f'?page={page_number}'
        # Получаем названия лофтов с текущей страницы
        all_loft_data.extend(get_loft_data(current_url))

    return(all_loft_data)

