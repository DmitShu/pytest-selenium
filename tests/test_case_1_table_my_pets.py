"""
Тест проверяет, что на странице со списком питомцев пользователя:

1 Присутствуют все питомцы.
2 Хотя бы у половины питомцев есть фото.
3 У всех питомцев есть имя, возраст и порода.
4 У всех питомцев разные имена.
5 В списке нет повторяющихся питомцев.
"""

import pytest
from selenium import webdriver
from datetime import datetime
from logins import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Подготавливаем тесты.
@pytest.fixture(autouse=True, scope="module")
def testing_preconditions():

   try:
      # Настройки драйвера
      # pytest.driver = webdriver.Firefox()
      err = ''
      options = webdriver.ChromeOptions()
      options.add_experimental_option('excludeSwitches', ['enable-logging'])
      pytest.driver = webdriver.ChromeOptions.binary_location = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
      pytest.driver = webdriver.Chrome('D:/Work/web_driver/chromedriver.exe', options=options)

      # неявноe ожидания для всех тестов
      pytest.driver.implicitly_wait(5)

      # Переходим на страницу авторизации
      pytest.driver.get(url + 'login')

      # Вводим email
      err = 'Не найдено поле "email".'
      WebDriverWait(pytest.driver, 3).until(EC.visibility_of_element_located((By.ID, "email"))).send_keys(valid_email)

      # Вводим пароль
      err = 'Не найдено поле "pass".'
      WebDriverWait(pytest.driver, 3).until(EC.visibility_of_element_located((By.ID, "pass"))).send_keys(valid_password)

      # Нажимаем на кнопку входа в аккаунт
      err = 'Не найдена кнопка "submit".'
      WebDriverWait(pytest.driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))).click()
      # pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

      # Переходим к таблице
      pytest.driver.get(url + 'my_pets')

      # Проверяем, что у пользователя есть таблица, и она не пустая
      err = 'Таблица питомцев пуста или отсутствует.'
      WebDriverWait(pytest.driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.table-hover tbody th img')))

      #Предусловия выполнены, можно запускать тесты.
      yield

   except:
      if err != '':
         pytest.driver.save_screenshot('screenshots/'+ str(datetime.now()).replace(':', '_')+ '_error.png')
      raise AssertionError(f'Не удалось подготовить тест / {err}')

   finally:
      pytest.driver.quit()


# Проверяем, что присутствуют все питомцы.
def test_1_check_pets_availability():

   # Получаем число питомцев с формы, проверяем, что оно отображается.
   petcount = WebDriverWait(pytest.driver, 3).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.\\.col-sm-4.left'))).text.split('\n')[1]
   petcount = int(petcount.split('Питомцев: ')[1])

   # Получаем данные из таблицы
   data = pytest.driver.find_elements_by_css_selector('.table-hover tbody tr td')

   # Присутствуют все питомцы.
   assert len(data)/4 == petcount, "В таблице находятся не все питомцы."


# Проверяем, что хотя бы у половины питомцев есть фото.
def test_2_check_half_pets_with_photo():

   # Получаем изображения с формы, убеждаемся, что они есть в табличке
   images = WebDriverWait(pytest.driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.table-hover tbody th img')))
   img = 0
   for i in range(len(images)):
      if (images[i].get_attribute('src')):
         img += 1

   # Хотя бы у половины питомцев есть фото.
   assert img/(i+1) >= 0.5, "Фото есть меньше чем у половины питомцев."


# Проверяем, что у всех питомцев есть имя, возраст и порода.
def test_3_check_pets_data():

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

   # У всех питомцев есть имя.
   assert '' not in names, f"Не у всех питомцев есть имя: {names}."
   # У всех питомцев есть порода.
   assert '' not in breeds, f"Не у всех питомцев есть порода: {breeds}."
   # У всех питомцев возраст.
   assert '' not in ages, f"Не у всех питомцев есть возраст: {ages}."


# Проверяем, что у всех питомцев имена уникальные.
def test_4_check_no_clones_names():

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
   assert len(names) == len(list(set(names))), f"Есть имена повторяшки: {names}."


# Проверяем, что в списке нет повторяющихся питомцев.
def test_5_check_no_clones_pets():

   # Получаем данные из таблицы
   data = pytest.driver.find_elements_by_css_selector('.table-hover tbody tr')
   datal = []
   for i in range(len(data)):
      datal.append(data[i].text)

   # В списке нет повторяющихся питомцев.
   assert len(datal) == len(list(set(datal))), f"Есть повторяшки среди питомцев: {datal}."