"""
This Python script emulates a headless browser to interact with the ChatGPT language model 
through OpenAI's website. After logging in, the script sends a message to ChatGPT that includes 
instructions on how to communicate. The model responds with a command that satisfies the task, 
in the format of "GPTCMD-XXXX: <command>". The script waits for up to 30 seconds for a response 
before moving on to the next task. If no response is found within 9999 tasks, the script will 
terminate. The script uses the Chrome driver and various Selenium modules to automate the browser 
and interact with ChatGPT.

This software is the property of Brian Peters(aka 0xdreadnaught) and is protected by intellectual 
property laws. No part of the software may be reproduced, distributed, or transmitted in any form 
or by any means, including photocopying, recording, or other electronic or mechanical methods, without 
the prior written permission of the owner.

Note that this software is not open source, and the license does not grant any permissions to users. 
Only those with written consent from the owner may use this software. Any unauthorized use, 
reproduction, or distribution of this software is strictly prohibited and may result in legal action.
"""

import random
import re
import time
import undetected_chromedriver as uc
import subprocess

#enable try/catch with info, key input, searching, dynamic waits, etc.
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

target_url = 'https://chat.openai.com/chat'

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

# Example usage:
html = '<p>GPTCMD-0003: curl <a href="https://www.google.com/" target="_new">https://www.google.com/</a> --head</p>'
text = normalize_html(html)
print(text)  # Output: "GPTCMD-0003: curl https://www.google.com/ --head"

def random_decimal(start, end, precision=2):
    return round(random.uniform(start, end), precision)

# Set up the Chrome driver and navigate to the OpenAI chat page
options = uc.ChromeOptions()
#options.add_argument("--headless=new")
driver = uc.Chrome(use_subprocess=True, options=options)
driver.maximize_window()
driver.delete_all_cookies()
driver.get(target_url)

input("Press {ENTER} when logged in.")
input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//textarea")))
input_field.send_keys("you will respond like a systems admin typing into a powershell terminal. I will present you with tasks and you will return the raw commands. for example: if I say 'find the current directory' you respond with something like 'GPTCMD-0001: pwd'. and if I asked you after that for the current ip address, you would respond with 'GPTCMD-0002: ip a'. if I supply you with error output from the terminal, continue the command sequence in order to resolve the problem. any terminal responses from your commands will be returned by me with GPTIN-xxxx: <text>, where xxxx corresponds to the matching GPTCMD ID. If the command you supplied generated no visual results, I will send you a message like 'GPTIN: NO RESULTS SHOWN.'. the first task is find the hostname, the os type is windows. remember only one command at a time, wait until your first command has reported back before continuing on." + Keys.RETURN)



#running loop
ticker = 1
while ticker <= 9999:
    #add some human type lag
    time.sleep(3)
    WebDriverWait(driver, 3)
    driver.implicitly_wait(3)

    #check for rate limit
    try:
        GPT_response = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Too many requests in 1 hour. Try again later.')]")))
        text = normalize_html(GPT_response.text)
        print("LIMIT: " + text)
        print("INFO: Try again after manual confirmation the rate limit is released.")
        input("Press Enter to close")
        exit()
    except:
        pass

    #check for response limit limit
    try:
        GPT_response = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'The message you submitted was too long, please reload the conversation and submit something shorter.')]")))
        print("LIMIT: " + text)
        print("INFO: Identify why the results weren't truncated into multiple chunks.")
        input("Press Enter to close")
        exit()
    except:
        pass

    #check for GPT command
    tick = f"{ticker:04d}"
    try:
        GPT_response = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(),'GPTCMD-" + str(tick) + "')]")))
        text = normalize_html(GPT_response.text)
        command = re.sub(r'GPTCMD\-\d{4}:\s*', '', text)

        """
        OK, YOU MUST READ THE COMMAND THAT IS ABOUT TO BE EXECUTED. 
        THIS IS YOUR ONLY CHANCE TO STOP IT.
        """
        # prompt the user for confirmation
        if input(f"Are you sure you want to run the following command against your system? (Y/N)\n{command}\n").strip().lower() != "y":
            print(f"Skipping command for task {tick}.")
            continue
        else:
        
            # Run the command and capture output
            process = subprocess.Popen(["powershell", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            # Check if output has a value
            if output is not None:
                #handle multi-line responses for returning the output to GPT
                print("GPTIN: " + output.decode('utf-8'))
                input_field.send_keys("GPTIN: ")
                actions = ActionChains(driver)
                actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                
                for line in output.decode('utf-8').splitlines():
                    # Simulate pressing shift + enter
                    input_field.send_keys(str(line))
                    actions = ActionChains(driver)
                    actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
                    
                input_field.send_keys(Keys.RETURN)
            else:
                print("GPTIN: NO RESULTS SHOWN.")
                input_field("GPTIN: NO RESULTS SHOWN." + Keys.RETURN)

            ticker += 1

    except Exception as e:
        print(f"Task issue: {e}")

    
