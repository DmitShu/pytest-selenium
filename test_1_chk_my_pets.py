# Тест проверяет, что на странице со списком питомцев пользователя:

# Присутствуют все питомцы.
# Хотя бы у половины питомцев есть фото.
# У всех питомцев есть имя, возраст и порода.
# У всех питомцев разные имена.
# В списке нет повторяющихся питомцев.

import pytest
from selenium import webdriver
from logins import *

@pytest.fixture(autouse=True, scope="module")
def testing_preconditions():

   log = ''

   try:

      # pytest.driver = webdriver.Firefox()
      pytest.driver = webdriver.ChromeOptions.binary_location = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
      pytest.driver = webdriver.Chrome('driver/chromedriver.exe')
      log += 'driver+'
      # Переходим на страницу авторизации
      pytest.driver.get(url + 'login')
      log += ' main page+'
      # Вводим email
      pytest.driver.find_element_by_id('email').send_keys(valid_email)
      log += ' email+'
      # Вводим пароль
      pytest.driver.find_element_by_id('pass').send_keys(valid_password)
      log += ' pass+'
      # Нажимаем на кнопку входа в аккаунт
      pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
      log += ' click+'
      # Переходим к таблице
      pytest.driver.get(url + 'my_pets')
      log += ' my_pets+'
      # Проверяем, что мы оказались на главной странице пользователя и есть питомцы
      if len(pytest.driver.find_elements_by_css_selector('.table-hover tbody th img')) > 0:

         #Получаем данные и отправляем в тесты.

         yield

      else:
         log += ' Не найдены питомцы'
         raise AssertionError()

   except:
      raise AssertionError(f'Не удалось подготовить тест / {log}.')

   finally:
      pytest.driver.quit()


def test_1_check_pets_availability():
   # Проверяем, что присутствуют все питомцы.

   # Получаем число питомцев с формы
   petcount = pytest.driver.find_element_by_css_selector('.\\.col-sm-4.left').text.split('\n')[1]
   petcount = int(petcount.split('Питомцев: ')[1])

   # Получаем данные из таблицы
   data = pytest.driver.find_elements_by_css_selector('.table-hover tbody tr td')

   # Присутствуют все питомцы.
   assert len(data)/4 == petcount, "В таблице не все питомцы"


def test_2_check_half_pets_with_photo():
   # Проверяем, что хотя бы у половины питомцев есть фото.

   # Получаем изображения с формы
   images = pytest.driver.find_elements_by_css_selector('.table-hover tbody th img')
   img = 0
   for i in range(len(images)):
      if (images[i].get_attribute('src')):
         img += 1

   # Хотя бы у половины питомцев есть фото.
   assert (i+1)/img <= 2, "Фото есть меньше чем у половины питомцев"


def test_3_check_pets_data():
   # Проверяем, что у всех питомцев есть имя, возраст и порода.

   # Получаем данные из таблицы
   data = pytest.driver.find_elements_by_css_selector('.table-hover tbody tr td')
   # Обработка данных для тестов
   names = []
   breeds = []
   ages = []
   cnt = 0
   for i in range(len(data)):
      cnt += 1
      if cnt == 1:
         names.append(data[i].text)
      if cnt == 2:
         breeds.append(data[i].text)
      if cnt == 3:
         ages.append(data[i].text)
      if cnt == 4:
         cnt = 0

   # У всех питомцев есть имя, возраст и порода.
   assert '' not in names, "Не у всех питомцев есть имена"
   assert '' not in breeds, "Не у всех питомцев есть порода"
   assert '' not in ages, "Не у всех питомцев есть возраст"


def test_4_check_no_clones_names():
   # Проверяем, что у всех питомцев имена уникальные.

   # Получаем данные из таблицы
   data = pytest.driver.find_elements_by_css_selector('.table-hover tbody tr td')
   # Обработка данных для тестов
   names = []
   cnt = 0
   for i in range(len(data)):
      cnt += 1
      if cnt == 1:
         names.append(data[i].text)
      if cnt == 4:
         cnt = 0

   # У всех питомцев разные имена.
   assert len(names) == len(list(set(names))), f"Есть имена повторяшки: {names}"


def test_5_check_no_clones_pets():
   # Проверяем, что в списке нет повторяющихся питомцев.

   # Получаем данные из таблицы
   data = pytest.driver.find_elements_by_css_selector('.table-hover tbody tr')
   datal = []
   for i in range(len(data)):
      datal.append(data[i].text)

   # В списке нет повторяющихся питомцев.
   assert len(datal) == len(list(set(datal))), f"Есть повторяшки среди питомцев: {datal}"