#!/bin/python3
'''
██████╗ ██████╗  █████╗  ██████╗  ██████╗ ███╗   ██╗███████╗██╗  ██╗██╗███████╗██╗     ██████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝ ██╔═══██╗████╗  ██║██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗
██║  ██║██████╔╝███████║██║  ███╗██║   ██║██╔██╗ ██║███████╗███████║██║█████╗  ██║     ██║  ██║
██║  ██║██╔══██╗██╔══██║██║   ██║██║   ██║██║╚██╗██║╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║
██████╔╝██║  ██║██║  ██║╚██████╔╝╚██████╔╝██║ ╚████║███████║██║  ██║██║███████╗███████╗██████╔╝
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝

██╗   ██╗████████╗██╗██╗     ██╗████████╗██╗███████╗███████╗
██║   ██║╚══██╔══╝██║██║     ██║╚══██╔══╝██║██╔════╝██╔════╝
██║   ██║   ██║   ██║██║     ██║   ██║   ██║█████╗  ███████╗
██║   ██║   ██║   ██║██║     ██║   ██║   ██║██╔══╝  ╚════██║
╚██████╔╝   ██║   ██║███████╗██║   ██║   ██║███████╗███████║
 ╚═════╝    ╚═╝   ╚═╝╚══════╝╚═╝   ╚═╝   ╚═╝╚══════╝╚══════╝
'''
# This script aims at connecting to the Dragonshield website and downloading the csv files
# containing the entire collection of a user.
#

import argparse
import os
import sys
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def run(args):

   # Set up the driver
   options = Options()
   options.add_argument('--headless')
   driver = webdriver.Firefox(options=options)
   driver.maximize_window()
   driver.get("https://archidekt.com/login/")

   # Accept cookies
   driver.find_element(by=By.CSS_SELECTOR , value="div.sc-qRumB:nth-child(2)").click()
   time.sleep(3)
   # Log in
   username = driver.find_element(by=By.NAME, value="username")
   password = driver.find_element(by=By.NAME, value="password")
   username.send_keys(args.username)
   password.send_keys(args.password)

   # submit button
   driver.find_element(by=By.CSS_SELECTOR, value="button.ui").click()
   time.sleep(3)

   # Go to the collection page
   driver.find_element(by=By.CSS_SELECTOR, value="a.globalToolbar_forumsAndCollection__C__GP").click()
   time.sleep(3)

   # click on Paper
   driver.find_element(by=By.CSS_SELECTOR, value="div.style__GameButton-sc-1etwy9d-0:nth-child(1)").click()
   time.sleep(3)

   # click on Settings
   driver.find_element(by=By.CSS_SELECTOR, value="div.bannerControls_groups__VZcim:nth-child(2) > span:nth-child(2) > button:nth-child(1)").click()
   time.sleep(3)

   # click on DELETE
   driver.find_element(by=By.CSS_SELECTOR, value="div.ui:nth-child(4) > input:nth-child(1)").send_keys("Delete my collection")

   # click on Back
   driver.find_element(by=By.CSS_SELECTOR, value=".red").click()
   time.sleep(3)

   # click on import_btn
   driver.find_element(by=By.CSS_SELECTOR, value=".overlay_backButton__6gCuA > i:nth-child(1)").click()
   time.sleep(1)

   # click on file_upload
   driver.find_element(by=By.CSS_SELECTOR, value="div.bannerControls_groups__VZcim:nth-child(1) > span:nth-child(1) > button:nth-child(1)").click()
   time.sleep(1)

   # click on cols
   driver.find_element(by=By.CSS_SELECTOR, value="div.accordion:nth-child(2) > div:nth-child(1)").click()
   time.sleep(1)

   # set dropdown value to 8
   driver.find_element(by=By.NAME, value="columnCount").click()
   time.sleep(1)

   # set dropdown value to 8
   driver.find_element(by=By.CSS_SELECTOR, value="div.visible:nth-child(3) > div:nth-child(8)").click()
   time.sleep(1)

   # set dropdown value of last col
   driver.find_element(by=By.CSS_SELECTOR, value="div.field:nth-child(9) > div:nth-child(1) > i:nth-child(1)").click()
   time.sleep(1)

   # set dropdown value of last col to collector number
   driver.find_element(by=By.CSS_SELECTOR, value="div.visible:nth-child(3) > div:nth-child(10) > span:nth-child(1)").click()
   time.sleep(1)

   # click file import C:\Users\UBOE-yannicklp\Downloads\all-folders.csv
   time.sleep(1)
   file_path = os.path.join(args.input)
   input = driver.find_element(by=By.CSS_SELECTOR, value=".style__StyledDropzone-sc-1ksfv9p-1 > input:nth-child(2)")
   input.send_keys(file_path)

   # set dropdown value of last col
   driver.find_element(by=By.CSS_SELECTOR, value="button.ui:nth-child(8)").click()
   time.sleep(600)

   driver.close()

def main():
   parser = argparse.ArgumentParser(description='Logs into the archidekt website to upload the csv files containing the entire collection of a user previously formatted with DSConvert.py.')
   parser.add_argument('file', type=str, help='Input csv file', required=True)
   parser.add_argument('-u', '--username', type=str, help='Username of the Dragonshield account', required=True)
   parser.add_argument('-p', '--password', type=str, help='Password of the Dragonshield account', required=True)
   parser.add_argument('-a', '--attempts', type=int, help='Number of attempts', required=False, default=3)
   args = parser.parse_args()
   attempts = 1
   while attempts <= args.attempts:
      try :
         run(args)
         return
      except Exception as e:
         print("Attempt {} failed with error: {}".format(attempts, e))
         attempts += 1
         time.sleep(2)
   raise Exception("Failed to run after {} attempts".format(args.attempts))

if __name__ == '__main__':
   main()