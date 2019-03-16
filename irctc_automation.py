"""
Purpose: Performs IRCTC Automation
Author: Shreyan Jadhav
Date: 30-OCT-2018
"""
import time
import datetime
from configparser import SafeConfigParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

CONFIG = SafeConfigParser()
CONFIG.read('config.ini')

USERNAME_TXT = CONFIG.get('CREDENTIALS', 'USERNAME')
PASSWORD_TXT = CONFIG.get('CREDENTIALS', 'PASSWORD')
BOOKING_TIME = CONFIG.get('TRAIN_INFO', 'BOOKING_TIME')
FROMSTATION_TXT = CONFIG.get('TRAIN_INFO', 'FROM_STATION')
TOSTATION_TXT = CONFIG.get('TRAIN_INFO', 'TO_STATION')
JOURNEYDATE_TXT = CONFIG.get('TRAIN_INFO', 'JOURNEY_DATE')
TRAINCLASS = CONFIG.get('TRAIN_INFO', 'TRAIN_CLASS')
BOOKTYPE = CONFIG.get('TRAIN_INFO', 'BOOK_TYPE')
TRAIN_NO = CONFIG.get('TRAIN_INFO', 'TRAIN_NO')
NAME_TXT = CONFIG.get('PASSENGER_INFO', 'NAME')
AGE_TXT = CONFIG.get('PASSENGER_INFO', 'AGE')
GENDER_TXT = CONFIG.get('PASSENGER_INFO', 'GENDER')
BERTHPREF_TXT = CONFIG.get('PASSENGER_INFO', 'BERTH_PREFERENCE')
PAYMENT_METHOD_TXT = CONFIG.get('PAYMENT_INFO', 'PAYMENT_METHOD')
PEYMENTBANK_TXT = CONFIG.get('PAYMENT_INFO', 'PAYMENT_BANK')
URL = CONFIG.get('MAIN', 'URL')
DRIVER_LOCATION = CONFIG.get('MAIN', 'DRIVER_LOCATION')

def login_irctc():
    """
    Performs Login of IRCTC Website. Confirm the variables declared in config
    """
    loginclick = WebDriverWait(DRIVER, 10).until(
        EC.element_to_be_clickable((By.ID, "loginText"))
        )
    loginclick.click()
    username = WebDriverWait(DRIVER, 10).until(
        EC.presence_of_element_located((By.ID, "userId"))
        )
    username.clear()
    username.send_keys(USERNAME_TXT)
    time.sleep(1)
    password = WebDriverWait(DRIVER, 10).until(
        EC.presence_of_element_located((By.ID, "pwd"))
        )
    password.clear()
    password.send_keys(PASSWORD_TXT)
    try:
        DRIVER.execute_script("document.getElementById('chtbticonWrap')."\
                              "style.transform = 'translate(-680px, -420px)';")
    except:
        print('Error while moving the chatbot. Please move manually.')
    captcha_txt = input('Input Captcha Text:')
    captcha = WebDriverWait(DRIVER, 10).until(
        EC.presence_of_element_located((By.ID, "nlpAnswer"))
        )
    captcha.clear()
    captcha.send_keys(captcha_txt)
    try:
        DRIVER.find_element_by_xpath('//button[contains(text(), "SIGN IN")]').click()
    except:
        print('Error in clicking Sign In Button')

def search_train():
    """
    Performs Searching of trains on IRCTC Website. Confirm the variables declared in config
    """
    fromstation = WebDriverWait(DRIVER, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='From*']"))
        )
    fromstation.clear()
    fromstation.send_keys(FROMSTATION_TXT)
    time.sleep(1)
    tostation = WebDriverWait(DRIVER, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='To*']"))
        )
    tostation.clear()
    tostation.send_keys(TOSTATION_TXT)
    time.sleep(1)
    if JOURNEYDATE_TXT is not None:
        journeydate = DRIVER.find_element_by_xpath("//input"\
                                                   "[@placeholder='Journey Date(dd-mm-yyyy)*']")
        journeydate.clear()
        journeydate.send_keys(JOURNEYDATE_TXT)
        calenderminimize = DRIVER.find_element_by_class_name('fa-calendar')
        calenderminimize.click()
    time.sleep(1)
    click_journeytype_dd()
    print('Waiting for booking timing:', BOOKING_TIME)
    while True:
        time.sleep(1)
        if monitor_time(BOOKING_TIME):
            DRIVER.find_element_by_xpath('//button[contains(text(), "Find trains")]').click()
            break
    print('Find Trains Clicked.')

def monitor_time(starttime):
    """
    Monitors the time to perform action on the specified time. (For Tatkal)
    """
    now = datetime.datetime.now()
    starttime = now.replace(hour=int(starttime[0:2]),
                            minute=int(starttime[3:5]),
                            second=0, microsecond=0)
    return bool(starttime <= now)

def click_tatkal_dd():
    """
    Clicks on Tatkal from the dropdown
    """
    try:
        webdriver.common.action_chains.ActionChains(DRIVER)
        action = webdriver.common.action_chains.ActionChains(DRIVER)
        try:
            finddrop_down = WebDriverWait(DRIVER, 30).until(
                EC.presence_of_element_located((By.XPATH, '//label[contains(text(), "GENERAL")]'))
                )
        except:
            finddrop_down = DRIVER.find_element_by_xpath('//label'\
                                                         '[contains(text(), "'+BOOKTYPE+'")]')
        action.move_to_element_with_offset(finddrop_down, 1, 1).click().perform()
        action = webdriver.common.action_chains.ActionChains(DRIVER)
        find_tatkal = DRIVER.find_element_by_xpath('//span[contains(text(), "'+BOOKTYPE+'")]')
        action.move_to_element_with_offset(find_tatkal, 1, 1).click().perform()
    except:
        print('Error in click_tatkal_dd.. Trying again..')
        click_tatkal_dd()

def click_journeytype_dd():
    """
    Clicks on Journey type from the dropdown. (Sleeper/AC/etc)
    """
    try:
        webdriver.common.action_chains.ActionChains(DRIVER)
        action = webdriver.common.action_chains.ActionChains(DRIVER)
        try:
            finddrop_down = DRIVER.find_element_by_xpath('//label[contains(text(), "All Classes")]')
        except:
            finddrop_down = DRIVER.find_element_by_xpath('//label'\
                                                         '[contains(text(), "'+TRAINCLASS+'")]')
        action.move_to_element_with_offset(finddrop_down, 1, 1).click().perform()
        action = webdriver.common.action_chains.ActionChains(DRIVER)
        find_tatkal = DRIVER.find_element_by_xpath('//span[contains(text(), "'+TRAINCLASS+'")]')
        action.move_to_element_with_offset(find_tatkal, 1, 1).click().perform()
    except:
        print('Error in click_journeytype_dd.. Trying again..')
        click_journeytype_dd()

def check_availability():
    """
    Clicks on Check Availability Button of the train specified
    """
    try:
        all_trains = DRIVER.find_elements_by_class_name('train_avl_border_div')
        for train in all_trains:
            if TRAIN_NO in train.text:
                print('TRAIN NO:', TRAIN_NO, ' TRAIN NAME:',
                      train.find_element_by_class_name('trainName').text.strip())
                trainfind = WebDriverWait(train, 30).until(
                    EC.element_to_be_clickable((By.ID, "check-availability"))
                    )
                trainfind.click()
                break
    except:
        print('Error in check_availability.. Trying again..')
        check_availability()

def click_book_now():
    """
    Clicks on Book Now button if Check Availability returns positively
    """
    CONVERTDATE = datetime.datetime(int(JOURNEYDATE_TXT[6:10]),
                                    int(JOURNEYDATE_TXT[3:5]),
                                    int(JOURNEYDATE_TXT[0:2]))
    CLICKNOW_DT_TXT = CONVERTDATE.strftime("%d %b %Y") #'01 Nov 2018'
    WebDriverWait(DRIVER, 30).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "span3"))
        )
    all_dates = DRIVER.find_elements_by_class_name('span3')
    for date in all_dates:
        if CLICKNOW_DT_TXT in date.text:
            date.find_element_by_class_name('b1').click()
            break

def add_passengers():
    """
    Adds paasenger for the train. Check the config file for adding passenger.
    """
    name = DRIVER.find_element_by_xpath("//input[@formcontrolname='passengerName']")
    name.clear()
    name.send_keys(NAME_TXT)
    age = DRIVER.find_element_by_xpath("//input[@formcontrolname='passengerAge']")
    age.clear()
    age.send_keys(AGE_TXT)
    gender = Select(DRIVER.find_element_by_xpath("//select[@formcontrolname='passengerGender']"))
    gender.select_by_visible_text(GENDER_TXT)
    berthpref = Select(DRIVER.find_element_by_xpath("//select"\
                                                    "[@formcontrolname='passengerBerthChoice']"))
    berthpref.select_by_visible_text(BERTHPREF_TXT)
    DRIVER.find_element_by_xpath('//label[contains(text(), "Yes and I accept")]').click()
    captchatxt = input('Input Captcha Text:')
    if len(captchatxt) > 2:
        captcha = DRIVER.find_element_by_id("nlpAnswer")
        captcha.clear()
        captcha.send_keys(captchatxt)
    DRIVER.find_element_by_xpath('//button[contains(text(), "Continue Booking")]').click()

def continue_booking():
    """
    Clicks on Continue Booking
    """
    continuebooking = WebDriverWait(DRIVER, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Continue Booking")]'))
        )
    continuebooking.click()

def payment_process():
    """
    Processes payment for the train
    """
    paymentmethod = WebDriverWait(DRIVER, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span'\
            '[contains(text(), "'+PAYMENT_METHOD_TXT+'")]'))
        )
    paymentmethod.click()
    paymentbank = WebDriverWait(DRIVER, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span'\
           '[contains(text(), "'+PEYMENTBANK_TXT+'")]'))
        )
    paymentbank.click()
    #makepayment = WebDriverWait(DRIVER, 10).until(
    #        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Make Payment")]'))
    #        )

    makepaymentbtns = DRIVER.find_elements_by_class_name('btn_continue')
    for btn in makepaymentbtns:
        if 'Make Payment' in btn.text:
            btn.click()
            break

##########################################

def page1():
    """
    To run Page 1 of IRCTC Seperately
    """
    search_train()
    time.sleep(1)

def page2():
    """
    To run Page 2 of IRCTC Seperately
    """
    click_tatkal_dd()
    time.sleep(1)
    check_availability()
    time.sleep(1)
    click_book_now()
    time.sleep(1)

def page3():
    """
    To run Page 3 of IRCTC Seperately
    """
    add_passengers()
    time.sleep(1)

def page4():
    """
    To run Page 4 of IRCTC Seperately
    """
    continue_booking()
    time.sleep(1)

def page5():
    """
    To run Page 5 of IRCTC Seperately
    """
    payment_process()

##########################################

def process():
    """
    To Process E2E IRCTC Booking
    """
    page1()
    page2()
    page3()
    page4()
    page5()

##########################################
##########################################


if __name__ == "__main__":
    print('IRCTC URL:', URL)
    DRIVER = webdriver.Chrome(DRIVER_LOCATION)
    DRIVER.maximize_window()
    DRIVER.get(URL)
    login_irctc()
    process()
