# Do NOT run this program before running guildcheck.py!

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import getpass

# Reads the file created by the other program and builds a list of character names to be kicked out
with open('../guildchecker/flagged_characters.txt') as f:
    all_list = f.readlines()

flagged_list = []

if all_list:
    for entry in all_list:
        flagged_char = entry.split(',')[0]
        flagged_list.append(flagged_char)        

guild_name = input('Enter the guild name (case sensitive): ')
guild_name = guild_name.replace(' ', '+')



driver = webdriver.Chrome('./chromedriver.exe')
driver.get("https://www.tibia.com/account/?subtopic=accountmanagement")

# Authentication phase. Should work with or without two-factor authentication.
acc_and_password = False

while not acc_and_password:
    acc_name = getpass.getpass("Enter your account e-mail: ")
    password = getpass.getpass("Enter your password: ")
    user = driver.find_element_by_name("loginemail")
    paswd = driver.find_element_by_name("loginpassword")

    user.send_keys(acc_name)
    paswd.send_keys(password)
    paswd.send_keys(Keys.RETURN)
    time.sleep(1) # might not be necessary
    try:
        if driver.find_element_by_name("Manage Account"):
            acc_and_password = True
            logged_in = True
    except NoSuchElementException:
        if driver.current_url == 'https://www.tibia.com/account/?subtopic=accountmanagement&page=twofactor&step=login':
            acc_and_password = True
            logged_in = False

while not logged_in:
    token = driver.find_element_by_name("totp")
    code = input("Enter the two factor authentication token: ")
    token.send_keys(code)
    token.send_keys(Keys.RETURN)
    time.sleep(1) # might not be necessary
    if driver.current_url != 'https://www.tibia.com/account/?subtopic=accountmanagement&page=twofactor':
        logged_in = True


# Goes to the guild page and kicks every character in the list built using flagged_characters.txt
driver.get("https://www.tibia.com/community/?subtopic=guilds&page=promote&GuildName=" + guild_name)
for entry in flagged_list:
    select = Select(driver.find_element_by_name("character"))
    select.select_by_value(entry)

    kick_button = driver.find_element_by_xpath('//input[@value="exclude"]')
    kick_button.click()

    hammer = driver.find_element_by_name("Submit")
    hammer.click()
    print(entry + " has been kicked from the guild.")

    time.sleep(1) # might not be necessary

# Closes the web browser and terminates the program
driver.close()