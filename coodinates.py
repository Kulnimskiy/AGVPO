import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint

def connect_web(url_adress: str):
    """
    Создаем элемент класса webdriver и переходим на страницу по url-адресу
    :param url_adress: url-адрес сайта
    :return: driver: элемент класса webdriver
    """
    # options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome()
    driver.get(url_adress)
    time.sleep(randint(3, 6))
    return driver


def search_input(driver, delay, adress):
    """
    Функция для внесения данных в поисковую форму
    :param driver: элемент класса webdriver
    :param delay: время ожидания
    :param adress: адрес
    """

    try:
        # Поиск формы ввода на сайте
        elem_search_string = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//input[@class='input__control _bold']")))
        # Вписываем данные в форму
        elem_search_string.send_keys(adress)
        # Запускаем поиск
        elem_search_string.send_keys(Keys.ENTER)
    except Exception as ERROR_search_input:
        print(f'{adress} - не отработал. Ошибка: {ERROR_search_input}')


def clear_input_form(driver, delay):
    """
    Очистка формы ввода на сайте
    :param driver: элемент класса webdriver
    :param delay: время ожидания
    """
    try:
        elem_clear = WebDriverWait(driver, 2) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//a[@class='small-search-form-view__pin']")))

    except Exception as ex:
        elem_clear = WebDriverWait(driver, 2) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='small-search-form-view__icon _type_close']")))

    elem_clear.click()


def get_coordinates(driver, delay, address: str) -> dict:
    """
    Функция для получения координат адреса
    :param driver: элемент класса webdriver
    :param delay: время ожидания
    :param address: адрес
    :return: coord: координаты адреса
    """
    coord = None
    name = None
    try:
        elem_first_list = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='toponym-card-title-view__description']")))
        name = elem_first_list.text
        elem_first_list.click()
        # Запускаем повторно функцию
    except Exception as e:
        print("Full address is not found. I will take what you've typed")
        name = address

    try:
        # Поиск координат на сайте
        elem_search_2 = WebDriverWait(driver, delay) \
            .until(EC.presence_of_element_located(
            (By.XPATH, "//div[@class='toponym-card-title-view__coords-badge']")))

        # Запись в переменную координат адреса
        coord = elem_search_2.text
    except Exception:
        print(f"There are several options of the {address}")
        try:
            # Если поиск выдал несколько результатов. выбираем 1 в списке элемент
            elem_first_list = WebDriverWait(driver, delay) \
                .until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='search-snippet-view__body _type_toponym']")))
            elem_first_list.click()
            # Запускаем повторно функцию
            get_coordinates(driver, delay, name)

        except:
            print('Error getting coordinates')

    clear_input_form(driver, delay)
    return {"address": name, "coordinates": coord}





def work_selenium(adresses: list, url_adress) -> list[tuple] | None:
    """
    Основная функция работы скрипта
    :param np_search_adress: список адресов
    :param url_adress: url-адрес сайта
    """
    driver = connect_web(url_adress)  # Настройка selenium
    delay = 10  # Время ожидания
    coords = []  # Словарь для записи результатов работы

    if len(adresses) < 2:
        return None

    for address in tqdm(adresses):
        time.sleep(1)
        search_input(driver, delay, address)  # Вносим адрес в поисковую форму
        coord = get_coordinates(driver, delay, address)  # Получаем координаты адреса
        coords.append(coord)  # Записываем результат в словарь

    return coords


if __name__ == '__main__':
    adresses = ["Злынка", "Москва"]
    url_adress = 'https://yandex.ru/maps/'  # Сайт "Яндекс карты"
    work_selenium(adresses, url_adress)  # Запуск основной функции
