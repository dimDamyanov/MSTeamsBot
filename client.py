import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")

opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
})

driver = webdriver.Chrome(options=opt, service_log_path='NUL')
url = 'https://teams.microsoft.com/'


def start_browser():
    global driver
    driver.get(url)
    WebDriverWait(driver, 10000).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
    if 'login.microsoftonline.com' in driver.current_url:
        login()
        print('Success')


def login():
    global driver
    with open('credentials.json') as json_file:
        cred = json.load(json_file)
    email_field = driver.find_element_by_id('i0116')
    email_field.click()
    email_field.send_keys(cred['user'])
    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
    next_button.click()
    password_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'i0118')))
    password_field.click()
    password_field.send_keys(cred['passwd'])
    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
    next_button.click()
    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
    next_button.click()
    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Use the web app instead')))
    next_button.click()
    time.sleep(5)


def join_class(class_name, end_time=0):
    global driver
    with open('team_names.json') as json_file:
        data = json.load(json_file)
    team_name = data[class_name]
    teams = driver.find_elements_by_class_name('team-card')
    for team in teams:
        if team_name in team.get_attribute('innerHTML'):
            team.click()
            break


start_browser()
join_class('History')