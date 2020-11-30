import json
import schedule
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions

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
    print('SUCCESS: Browser started')
    if 'login.microsoftonline.com' in driver.current_url:
        if login():
            print('SUCCESS: LOG IN')


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
    return driver.current_url == 'https://teams.microsoft.com/_#/school//?ctx=teamsGrid'


def join_class(class_name, start_time, end_time):
    global driver
    with open('team_names.json') as json_file:
        data = json.load(json_file)
    team_name = data[class_name]
    teams = driver.find_elements_by_class_name('team-card')
    for team in teams:
        if team_name in team.get_attribute('innerHTML'):
            team.click()
            break
    time.sleep(5)
    class_start = datetime.combine(datetime.today().date(), datetime.strptime(start_time, '%H:%M').time())
    f = False
    while datetime.now() - class_start < timedelta(minutes=15):
        try:
            # TODO: Testing with no class
            time.sleep(5)
            join_button = driver.find_element_by_class_name('ts-calling-join-button')
            join_button.click()
            f = True
            break
        except exceptions.NoSuchElementException:
            driver.refresh()
    if f:
        time.sleep(4)
        webcam_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
        if webcam_button.get_attribute('title') == 'Turn camera off':
            webcam_button.click()
        time.sleep(1)
        mic_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[2]/div/button/span[1]')
        if mic_button.get_attribute('title') == 'Mute microphone':
            mic_button.click()
        join_now_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
        join_now_button.click()
        print(f'Joining class {class_name} at {datetime.now()}, leaving at {end_time}')
        schedule.every().day.at(end_time).do(leave_class)
    else:
        print('No class found!')


def leave_class():
    print('Leaving...')
    teams_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/app-bar/nav/ul/li[2]/button')
    teams_button.click()
    hangup_button = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID, 'hangup-button')))
    hangup_button.click()
    teams_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/app-bar/nav/ul/li[2]/button')
    teams_button.click()
    return schedule.CancelJob


def schedule_classes():
    with open('timetable.json') as json_file:
        data = json.load(json_file)

    for lesson in data:
        day = lesson['day']
        name = lesson['class']
        t_s = lesson['t_s']
        t_e = lesson['t_e']
        if day.lower() == 'monday':
            schedule.every().monday.at(t_s).do(join_class, name, t_s, t_e)
            print(f'Class {name} scheduled on {day} at {t_s} to {t_e}')
        elif day.lower() == 'tuesday':
            schedule.every().tuesday.at(t_s).do(join_class, name, t_s, t_e)
            print(f'Class {name} scheduled on {day} at {t_s} to {t_e}')
        elif day.lower() == 'wednesday':
            schedule.every().wednesday.at(t_s).do(join_class, name, t_s, t_e)
            print(f'Class {name} scheduled on {day} at {t_s} to {t_e}')
        elif day.lower() == 'thursday':
            schedule.every().thursday.at(t_s).do(join_class, name, t_s, t_e)
            print(f'Class {name} scheduled on {day} at {t_s} to {t_e}')
        elif day.lower() == 'friday':
            schedule.every().friday.at(t_s).do(join_class, name, t_s, t_e)
            print(f'Class {name} scheduled on {day} at {t_s} to {t_e}')
        elif day.lower() == 'saturday':
            schedule.every().saturday.at(t_s).do(join_class, name, t_s, t_e)
            print(f'Class {name} scheduled on {day} at {t_s} to {t_e}')
        else:
            pass


schedule_classes()
start_browser()
while True:
    schedule.run_pending()

# TODO: Discord 