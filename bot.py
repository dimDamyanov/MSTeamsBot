import json
import schedule
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from discord_webhook import DiscordWebhook
import winsound

# TODO: Add sound notification when joining
weekdays = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

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
web_hook_url = 'https://discord.com/api/webhooks/783083064279433256/2pPEwQOdCJkwYP3DNGLDUn70nrZzYV-J5wDFD6B3dott3_8ttyoo99QnP0GLmAVRytPr'


def start_browser():
    global driver
    driver.get(url)
    WebDriverWait(driver, 10000).until(EC.visibility_of_element_located((By.TAG_NAME, 'body')))
    print(f'[{datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] SUCCESS: Browser started')
    if 'login.microsoftonline.com' in driver.current_url:
        if login():
            print(f'[{datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] SUCCESS: LOG IN')


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
    class_start = datetime.combine(datetime.today().date(), datetime.strptime(start_time, '%H:%M').time())
    with open('team_names.json') as json_file:
        data = json.load(json_file)
    if driver.current_url != 'https://teams.microsoft.com/_#/school//?ctx=teamsGrid':
        driver.get('https://teams.microsoft.com/_#/school//?ctx=teamsGrid')
    team_name = data[class_name]
    while driver.current_url == 'https://teams.microsoft.com/_#/school//?ctx=teamsGrid':
        teams = driver.find_elements_by_class_name('team-card')
        for team in teams:
            if team_name in team.get_attribute('innerHTML'):
                team.click()
                break
        time.sleep(2)
    f = False
    while datetime.now() - class_start < timedelta(minutes=15):
        try:
            join_button = driver.find_element_by_class_name('ts-calling-join-button')
            join_button.click()
            f = True
            break
        except Exception as e:
            # print(f'[{datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] Exception: {e.__class__}')
            time.sleep(5)
    if f:
        time.sleep(2)
        webcam_button = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
        if webcam_button.get_attribute('title') == 'Turn camera off':
            webcam_button.click()
        time.sleep(1)
        mic_button = driver.find_element_by_xpath('//*[@id="preJoinAudioButton"]/div/button/span[1]')
        if mic_button.get_attribute('title') == 'Mute microphone':
            mic_button.click()
        join_now_button = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
        join_now_button.click()
        message = f'Joining class {class_name} on {datetime.now().strftime("%d/%b/%Y at %H:%M:%S")}, leaving at {end_time}'
        print(f'[{datetime.now().strftime("%d/%b/%Y %H:%M:%S")}]', message)
        web_hook = DiscordWebhook(web_hook_url, content=message)
        web_hook.execute()
        schedule.every().day.at(end_time).do(leave_class, class_name)
        winsound.PlaySound('join_meeting.wav', winsound.SND_ASYNC)
    else:
        message = f'No meeting started for {class_name}.'
        print([{datetime.now().strftime("%d/%b/%Y %H:%M:%S")}], message)
        web_hook = DiscordWebhook(web_hook_url, content=message)
        web_hook.execute()
        teams_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/app-bar/nav/ul/li[2]/button')
        teams_button.click()


def leave_class(class_name):
    teams_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/app-bar/nav/ul/li[2]/button')
    teams_button.click()
    hangup_button = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID, 'hangup-button')))
    hangup_button.click()
    message = f'Leaving class {class_name} on {datetime.now().strftime("%d/%b/%Y at %H:%M:%S")}'
    print(f'[{datetime.now().strftime("%d/%b/%Y %H:%M:%S")}]', message)
    web_hook = DiscordWebhook(web_hook_url, content=message)
    web_hook.execute()
    teams_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/app-bar/nav/ul/li[2]/button')
    teams_button.click()
    winsound.PlaySound('leave_meeting.wav', winsound.SND_ASYNC)
    return schedule.CancelJob


def schedule_classes():
    with open('timetable.json') as json_file:
        data = json.load(json_file)

    for lesson in data:
        day = lesson['day']
        name = lesson['class']
        t_s = lesson['t_s']
        t_e = lesson['t_e']
        if day.casefold() in weekdays:
            if day.casefold() == 'monday':
                schedule.every().monday.at(t_s).do(join_class, name, t_s, t_e)
            elif day.casefold() == 'tuesday':
                schedule.every().tuesday.at(t_s).do(join_class, name, t_s, t_e)
            elif day.casefold() == 'wednesday':
                schedule.every().wednesday.at(t_s).do(join_class, name, t_s, t_e)
            elif day.casefold() == 'thursday':
                schedule.every().thursday.at(t_s).do(join_class, name, t_s, t_e)
            elif day.casefold() == 'friday':
                schedule.every().friday.at(t_s).do(join_class, name, t_s, t_e)
            elif day.casefold() == 'saturday':
                schedule.every().saturday.at(t_s).do(join_class, name, t_s, t_e)
            print(f'[{datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] Class {name} scheduled on {day} at {t_s} to {t_e}')
        else:
            pass


schedule_classes()
start_browser()
while True:
    schedule.run_pending()
