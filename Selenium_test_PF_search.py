import pytest
from selenium import webdriver
from logins import *

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Firefox()
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