from selenium import webdriver #подключение библиотеки
driver = webdriver.Firefox() #получение объекта веб-драйвера для нужного браузера
driver.get('https://google.com')
driver.quit()