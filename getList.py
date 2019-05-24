# This requires python to run. refer https://www.python.org/downloads/
# After installing python, you will need selenium
# To install selenium, open terminal and type 'pip install selenium'
# You will also need a webdriver.
# You can download one from https://sites.google.com/a/chromium.org/chromedriver/downloads
# Now you will have to add the downloaded driver to the Path variable.
# To do that, copy the location that you have stored the downloaded driver.
# Open Control Panel>System and Security> System> Advanced System Settings
# Click on Environment variables.
# Click on path
# Add new path(The one that you've copied.)

import winsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils import long_beep


# 5645683S0248

def check_report(driver=None, row_num=0):
    # Finding the correct row in the table.
    table = driver.find_element_by_tag_name('tbody')
    row_1 = table.find_elements_by_tag_name('tr')[row_num]
    cols = row_1.find_elements_by_tag_name('td')

    # Extracting Name, House number, status from the selected row.
    name = cols[4].text
    h_no = cols[3].text
    status = cols[5].text

    # Checking if status is Draft
    if status != 'Draft':
        print('Status: ' + status)
        print('Skipping to next row.')
        return row_num + 1

    print('Viewing report of ' + name)
    cols[7].click()
    print('Checking for Livestock/Poultry')
    # Clicking the eye to view the report of selected household.

    # Checking if there are tabs for Livestock/Poultry in the report.
    tab_div = driver.find_element_by_class_name('tabareadata')
    tabs = tab_div.find_elements_by_tag_name('a')

    # if there is more than one tab, it means that a Livestock or Poultry tab must be present.
    if len(tabs) > 1:
        print(name + ' has Livestock/Poultry, going back.')
        action = 'Needs verification'
        cancel_button = driver.find_element_by_id('submitCancel')
        cancel_button.click()
        row_num += 1
        winsound.Beep(2500, 1000)

    # If not, we can send the report to the server.
    else:
        print(name + ' has no Livestock/Poultry, Sending to server')
        # Checking the 'send to server' checkbox.
        print('Clicking checkbox.')
        server_checkbox = driver.find_element_by_id('_changeStatus6')
        server_checkbox.click()
        # Submitting the report.
        print('Clicking submit button.')
        submit_button = driver.find_element_by_id('submit')
        submit_button.click()
        action = 'Sent to server'
        try:
            print('waiting to see if alert pops up.')
            WebDriverWait(driver, 5).until(EC.alert_is_present(), 'Waited for an alert that didn\'t appear')
            # Clicking 'Ok' in the confirmation alert.
            print('Closing alert.')
            alert = driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            print('no alert appeared')

    # Keeping logs like a good boy.
    print('Keeping logs.')
    line = name + '\t' + h_no + '\t' + action + '\n'

    file = open('log.txt', 'a')
    file.write(line)
    file.close()
    return row_num


chrome_driver = webdriver.Chrome()

url = 'http://www.livestockcensus.gov.in/'
chrome_driver.get(url)

long_beep()
a = input('Enter any key after loading the page with the list of households.')

row = 0
timeout_count = 0
page_offset = 0
while row < 10:
    try:
        print('Waiting for the table to load.')
        WebDriverWait(chrome_driver, 10).until(EC.presence_of_element_located((By.ID, 'example_next')))
        print('row number = ' + str(row + 1))
        for x in range(page_offset):
            print('Clicking to next 10 households.')
            next_button = chrome_driver.find_element_by_id('example_next')
            next_button.click()
        row = check_report(chrome_driver, row)
    except TimeoutException:
        print('Timed Out')
        timeout_count += 1
        if timeout_count > 2:
            chrome_driver.refresh()
    if row == 10:
        page_offset += 1
        row = 0
        long_beep()
