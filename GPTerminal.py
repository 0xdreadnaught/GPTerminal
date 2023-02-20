import random
import re
import time
import psutil
import os
import undetected_chromedriver as uc
import subprocess
from html.parser import HTMLParser
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from colorama import init
init()
# Pure Python 3.x demo, 256 colors
# Works with bash under Linux and MacOS

# Define the color functions
fg = lambda text, color: "\33[38;5;" + str(color) + "m" + str(text) + "\33[0m"
bg = lambda text, color: "\33[48;5;" + str(color) + "\33[0m"

# Define the message types and their associated colors
bg_black = 0
bg_gray = 245
bg_light_gray = 246
bg_dark_gray = 235
bg_red = 124
bg_green = 34
bg_yellow = 221
bg_blue = 32
bg_purple = 93
bg_pink = 198

fg_gray = 250
fg_white = 15
fg_red = 203
fg_green = 46
fg_yellow = 220
fg_blue = 75
fg_purple = 176
fg_pink = 211

message_types = {
    "GPTCMD": (bg_light_gray, fg_pink),
    "GPTIN": (bg_light_gray, fg_purple),
    "GPTTASK": (bg_light_gray, fg_blue),
    "STATUS": (bg_light_gray, fg_green),
    "ERROR": (bg_light_gray, fg_red),
    "WARNING": (bg_light_gray, fg_yellow)
}

def fancy_print(message_type, message):
    if message_type in message_types:
        bg_color, fg_color = message_types[message_type]
        message_type = re.sub("\033\[[0-9]+m", "", f"[{message_type}]")
        print(bg(bg_color, fg(message_type, fg_color)) + " " + message)
    else:
        print(message)


#color test
def print_six(row, format):
    for col in range(6):
        color = row*6 + col + 4
        if color>=0:
            text = "{:3d}".format(color)
            print (format(text,color), end=" ")
        else:
            print("   ", end=" ")

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []

    def handle_data(self, data):
        self.data.append(data)

def normalize_html(html):
    parser = MyHTMLParser()
    parser.feed(html)
    return ''.join(parser.data)

def random_decimal(start, end, precision=2):
    return round(random.uniform(start, end), precision)

def get_command(driver, input_field):

    ticker = 1
    while ticker <= 9999:
        tick = f"{ticker:04d}"
        print("Entering 6 second sleep...")
        time.sleep(3)
        driver.implicitly_wait(3)

        # Check for "Too many requests in 1 hour. Try again later." message
        try:
            element = driver.find_element(By.XPATH, "//div[contains(text(),'Too many requests in 1 hour. Try again later.')]")
            if element:
                # Handle message size limit error
                fancy_print("ERROR", "GPT rate limit hit!")
                fancy_print("Status", "Press Enter to close GPTerminal.")
                input()
                exit()
        except:
            pass
        

        # Check for "The message you submitted was too long, please reload the conversation and submit something shorter." message
        try:
            element = driver.find_element(By.XPATH, "//div[contains(text(),'The message you submitted was too long, please reload the conversation and submit something shorter.')]")
            if element:
                # Handle message size limit error
                fancy_print("ERROR", "Message size limit hit!")
                fancy_print("Status", "Press Enter to close GPTerminal.")
                input()
                exit()
        except:
            pass

        # Check for GPTCMD-xxxx: <command> message
        try:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'GPTCMD-')]")))
            if element:
                text = element.text
                command = re.sub(r'GPTCMD\-\d{4}:\s*', '', str(text))
                print("CMD:"+command)
                fancy_print("GPTCMD", "GPTCMD-" + str(tick) + ": " + str(command))
                fancy_print("WARNING", "Are you sure you want to run the following command against your system?")
                response = input("(Y/N)")
                if response.strip().lower() == "y":
                    # run the command here
                    display_message="GPTTASK-" + str(tick) +": " + "Running GPTCMD-" + str(tick)
                    execute_command(driver, input_field, command, display_message)
                else:
                    fancy_print("STATUS", "Skipping execution of GPTCMD-" + str(tick) + ".")
                    
                #increment ticker and loop
                ticker += 1
        except:
            pass

        # Check for world update (bleep borp) message
        try:
            element = driver.find_element(By.XPATH, "//p[contains(text(),'bleep borp.')]")
            if element:
                # Handle world update
                pass       
        except:
            pass
        
        

    print("Reached maximum number of tasks. Terminating script.")
    exit()

def execute_command(driver, input_field, command, display_message):
    fancy_print("GPTTASK", display_message)
    process = subprocess.Popen(["powershell", str(command)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if output is not None:        
        print("GPTIN: " + output.decode('utf-8'))
        input_field.send_keys("GPTIN: ")
        actions = ActionChains(driver)
        actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
        for line in output.decode('utf-8').splitlines():
            input_field.send_keys(str(line))
            actions = ActionChains(driver)
            actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
        input_field.send_keys(Keys.RETURN)
    elif error is not None:
        print(f"ERROR: {error}")
    else:
        print("GPTIN: NO RESULTS SHOWN.")
        input_field.send_keys("GPTIN: NO RESULTS SHOWN." + Keys.RETURN)

def initialize_driver(target_url):
    options = uc.ChromeOptions()
    driver = uc.Chrome(use_subprocess=True, options=options)
    driver.maximize_window()
    driver.delete_all_cookies()
    driver.get(target_url)
    return driver

def login(driver):
    input("Press {ENTER} when logged in.")
    input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//textarea")))
    input_field.send_keys("you will respond like a systems admin typing into a powershell terminal. I will present you with tasks and you will return the raw commands. for example: if I say 'find the current directory' you respond with something like 'GPTCMD-0001: pwd'. and if I asked you after that for the current ip address, you would respond with 'GPTCMD-0002: ip a'. if I supply you with error output from the terminal, continue the command sequence in order to resolve the problem. any terminal responses from your commands will be returned by me with GPTIN-xxxx: <text>, where xxxx corresponds to the matching GPTCMD ID. If the command you supplied generated no visual results, I will send you a message like 'GPTIN: NO RESULTS SHOWN.'. the first task is find the hostname, the os type is windows. remember only one command at a time, wait until your first command has reported back before continuing on." + Keys.RETURN)
    return input_field

def main():
    #perform color test.
    for row in range(-1,42):
        print_six(row, fg)
        print("",end=" ")
        print_six(row, bg)
        print()
        # Simple usage: print(fg("text", 160))
    print(fg("Press Enter if the color test was successful.", 200))

    #fancy demo
    fancy_print("GPTTASK", "TASK-0001: Started.")
    fancy_print("STATUS", "Entering 6 second sleep...")
    fancy_print("STATUS", "Searching for commands...")
    fancy_print("GPTCMD", "hostname")
    print(fg("Press Enter if the type test was successful.", 200))

    #identify what kind of terminal started this script
    #get the parent process id
    print(fg("", 200))
    ppid = os.getppid() # Get parent process id
    fancy_print("STATUS", psutil.Process(ppid).name())
    input()
    driver = initialize_driver("https://chat.openai.com/chat")
    input_field = login(driver)
    while True:
        get_command(driver, input_field)
        time.sleep(2)
        

if __name__ == "__main__":
    main()
