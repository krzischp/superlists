from selenium import webdriver

path_to_driver = "C:/Users/Utilisateur/chromedriver_win32/bin/chromedriver.exe"
browser = webdriver.Chrome(path_to_driver)
browser.get("http://localhost:8000")

assert 'worked successfully' in browser.title