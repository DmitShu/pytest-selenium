import pytest
from selenium import webdriver
from logins import *
import time

@pytest.fixture(autouse=True)
def testing():
   # pytest.driver = webdriver.Firefox()
   pytest.driver = webdriver.ChromeOptions.binary_location = 'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'
   pytest.driver = webdriver.Chrome('D:/Work/web_driver/chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get(url+'login')

   yield

   pytest.driver.quit()


def test_show_my_pets():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys(valid_email)
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys(valid_password)
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"


def test_all_pets_info():

   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys(valid_email)
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys(valid_password)
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

   pytest.driver.get(url)
   time.sleep(3)
   images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
   names = pytest.driver.find_elements_by_css_selector('.card-deck .card-title')
   descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')
   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0


# def test_show_my_pets(selenium):
#    selenium.get(url+'login')
#    # Вводим email
#    selenium.find_element_by_id('email').send_keys(valid_email)
#    # Вводим пароль
#    selenium.find_element_by_id('pass').send_keys(valid_password)
#    # Нажимаем на кнопку входа в аккаунт
#    selenium.find_element_by_css_selector('button[type="submit"]').click()
#    # Проверяем, что мы оказались на главной странице пользователя
#    assert selenium.find_element_by_tag_name('h1').text == "PetFriends"