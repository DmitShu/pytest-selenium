# Тест проверяет, что на странице со списком питомцев пользователя:
#
# Присутствуют все питомцы.
# Хотя бы у половины питомцев есть фото.
# У всех питомцев есть имя, возраст и порода.
# У всех питомцев разные имена.
# В списке нет повторяющихся питомцев.

import pytest
from selenium import webdriver
from logins import *
import time

@pytest.fixture(autouse=True)
def testing():
   # pytest.driver = webdriver.Firefox()
   pytest.driver = webdriver.ChromeOptions.binary_location = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
   pytest.driver = webdriver.Chrome('driver/chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get(url+'login')
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys(valid_email)
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys(valid_password)
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   pytest.driver.get(url+'my_pets')
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element_by_class_name('btn-outline-success').text == 'Добавить питомца'

   yield

   pytest.driver.quit()


def test_chk_my_pets():

   # time.sleep(3)
   petcount = pytest.driver.find_element_by_css_selector('.\\.col-sm-4.left').text.split('\n')[1]
   petcount = int(petcount.split('Питомцев: ')[1])

   images = pytest.driver.find_elements_by_css_selector('.table-hover tbody th img')
   data = pytest.driver.find_elements_by_css_selector('.table-hover tbody tr td')


   # Присутствуют все питомцы.
   assert petcount > 0, "Питомцев нет"
   assert len(data)/4 == petcount, "В таблице не все питомцы"

   # Хотя бы у половины питомцев есть фото.
   withphoto = 0
   for i in range(petcount):
      if (images[i].get_attribute('src')):
         withphoto += 1

   # Хотя бы у половины питомцев есть фото.
   assert petcount/withphoto <= 2, "Фото есть меньше чем у половины питомцев"

   # Обработка данных
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
   assert '' not in names, "Есть не все имена"
   assert '' not in breeds, "Есть не все породы"
   assert '' not in ages, "Есть не все возрасты"

   # У всех питомцев разные имена.
   assert len(names) == len(list(set(names))), "Есть повторяшки имена"

   # В списке нет повторяющихся питомцев.
   data = pytest.driver.find_elements_by_css_selector('.table-hover tbody tr')
   datal = []
   for i in range(len(data)):
      datal.append(data[i].text)
   # В списке нет повторяющихся питомцев.
   assert len(datal) == len(list(set(datal))), "Есть повторяшки"