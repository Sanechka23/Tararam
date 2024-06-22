import requests
from bs4 import BeautifulSoup


def get_club_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    club_data = []
    # Находим все блоки с результатами клубов
    result_blocks = soup.find_all('div', class_='s4bouling-result')
    for block in result_blocks:
        # Находим название клуба
        club_name = block.find('a', class_='s4bouling-result__title').text.strip()

        # Находим ссылки
        url2 = block.find('a', class_='s4bouling-result__title')['href'] 
        

        # Находим все URL
        club_url = block.find('a', class_='s4bouling-result__title').text.strip()

        # Находим станцию метро (уточненный поиск)
        metro_list = []
        metro_elements = block.find_all('div', {'class': 'subway'})
        for metro_element in metro_elements:
          metro_list.append(metro_element.get_text(strip=True))

        price_rows = block.find_all('div', class_='s4bouling-result__price__row')
        text_list = []
        for row in price_rows:
          left_text = row.find('div', class_='s4bouling-result__price__left').text.strip()
          right_text = row.find('div', class_='s4bouling-result__price__right').text.strip()
          text = left_text + " - " + right_text
          text_list.append(text)

        club_data.append({
            'name': club_name,
            'url': url2,
            'metro': metro_list,
            'price': text_list 
        })

    return club_data


def pars_1():
    # Начальная страница
    url = 'https://bouling.moscow/vse-kluby'
    all_club_data = []

    # Парсим все страницы
    for page_number in range(1, 17):  
        current_url = url + f'?page={page_number}'
        # Получаем названия клубов с текущей страницы
        all_club_data.extend(get_club_data(current_url))

    return all_club_data