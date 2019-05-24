import winsound


def check_report(driver=None, row_num=0):
    # Finding the correct row in the table.
    table = driver.find_element_by_tag_name('tbody')
    row_1 = table.find_elements_by_tag_name('tr')[row_num]
    cols = row_1.find_elements_by_tag_name('td')

    # Extracting Name, House number from the selected row.
    name = cols[4].text
    h_no = cols[3].text
    action = ''

    # Clicking the eye to view the report of selected household.
    cols[7].click()
    print('Viewing report of ' + name)
    print('Checking for Livestock/Poultry')

    # Checking if there are tabs for Livestock/Poultry in the report.
    tab_div = driver.find_element_by_class_name('tabareadata')
    tabs = tab_div.find_elements_by_tag_name('a')

    # if there is more than one tab, it means that a Livestock or Poultry tab must be present.
    if len(tabs) > 1:
        print(name + 'has Livestock/Poultry, going back.')
        action = 'Needs verification'
        row_num += 1

    # If not, we can send the report to the server.
    else:
        print(name + 'has no Livestock/Poultry, Sending to server')
        # Checking the 'send to server' checkbox.
        server_checkbox = driver.find_element_by_id('_changeStatus6')
        server_checkbox.click()
        # Submitting the report.
        submit_button = driver.find_element_by_id('submit')
        submit_button.click()
        action = 'Sent to server'
        # Clicking 'Ok' in the confirmation alert.
        alert = driver.switch_to.alert
        alert.accept()

    # Keeping logs like a good boy.
    line = name + '\t' + h_no + '\t' + action + '\n'

    file = open('log.txt', 'a')
    file.write(line)
    file.close()



def long_beep():
    winsound.Beep(2500, 300)
    winsound.Beep(4500, 300)
    winsound.Beep(1500, 300)
    winsound.Beep(2500, 300)
    winsound.Beep(4500, 300)
    winsound.Beep(1500, 300)
    winsound.Beep(2500, 300)
    winsound.Beep(4500, 300)
    winsound.Beep(1500, 300)