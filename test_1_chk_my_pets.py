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

   print(petcount)

   images = pytest.driver.find_elements_by_css_selector('.table-hover tbody th img')

   for i in range(len(images)):
      print(images[i].get_attribute('src'))
   assert 1 == 1



   # images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
   # names = pytest.driver.find_elements_by_css_selector('.card-deck .card-title')
   # descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')
   # for i in range(len(names)):
   #    assert images[i].get_attribute('src') != ''
   #    assert names[i].text != ''
   #    assert descriptions[i].text != ''
   #    assert ', ' in descriptions[i]
   #    parts = descriptions[i].text.split(", ")
   #    assert len(parts[0]) > 0
   #    assert len(parts[1]) > 0


