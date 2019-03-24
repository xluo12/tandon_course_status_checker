from selenium import webdriver
from datetime import datetime
import time
import smtplib


def send_alert(message):
    gmail_user = 'xxx@xxx'    # your email address
    gmail_password = 'xxxxxx'   # your email password

    sent_from = gmail_user
    to = ['xxx@xxx']     # your send-to email address
    subject = 'Course open alert'
    body = message

    email_text = """\  
    From: %s  
    To: %s  
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)   # you email server, ex: gmail server
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()
    print('Email alert sent!')

    
browser = webdriver.Chrome()
browser.implicitly_wait(5)

browser.get('http://albert.nyu.edu/albert_index.html?FolderPath=PORTAL_ROOT_OBJECT.NYU_STUDENT_CTR&IsFolder=false&IgnoreParamTempl=FolderPath,IsFolder')
browser.find_element_by_class_name('buttonLink').click()
browser.find_element_by_id('netid').send_keys('xxxxx')   # your NetID
browser.find_element_by_id('password').send_keys('xxxxxxx')    # your password
browser.find_element_by_xpath('//button[@type="submit"]').click()
# WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, 'passcode')))
browser.switch_to.frame(browser.find_element_by_id('duo_iframe'))
browser.find_element_by_id('passcode').click()
browser.find_element_by_xpath('//input[@name="passcode"]').send_keys('xxxxxx')  # your passcode received on your cellphone
browser.find_element_by_id('passcode').click()
browser.find_element_by_xpath('//a[@class="nyuCourseSearch"]').click()

while len(browser.find_elements_by_xpath('//table[@class="PSLEVEL1GRID accordion-table"]')) == 0:
    browser.find_element_by_xpath('//a[@class="nyuCourseSearch"]').click()
to_quit = False
message = ''

while True:
    # modify below format according to your courses layout in your shopping cart
    if browser.find_element_by_xpath('//table[@class="PSLEVEL1GRID accordion-table"]/tbody[1]/tr[2]/td[7]/div[1]/div[1]/img[1]').get_attribute('src') == 'https://sis.nyu.edu/cs/csprod/cache/855/PS_CS_STATUS_OPEN_ICN_1.gif':
        message = message + 'xxxxx is open '   # log what course is found open
        to_quit = True
    if browser.find_element_by_xpath('//table[@class="PSLEVEL1GRID accordion-table"]/tbody[1]/tr[4]/td[7]/div[1]/div[1]/img[1]').get_attribute('src') == 'https://sis.nyu.edu/cs/csprod/cache/855/PS_CS_STATUS_OPEN_ICN_1.gif':
        message = message + 'xxxxx is open '
        to_quit = True
    if not to_quit:
        time.sleep(30)
        browser.refresh()
        print('Retry: {}'.format(str(datetime.now())))
        browser.find_element_by_xpath('//a[@class="nyuCourseSearch"]').click()
        while len(browser.find_elements_by_xpath('//table[@class="PSLEVEL1GRID accordion-table"]')) == 0:
            browser.find_element_by_xpath('//a[@class="nyuCourseSearch"]').click()
    else:
        send_alert(message)
        break






