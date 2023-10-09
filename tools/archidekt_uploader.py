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

from logger import *

def run(args, driver):

   driver.maximize_window()
   driver.get("https://archidekt.com/login/")

   # Accept cookies
   time.sleep(2)
   logger.info("Accepting cookies")
   driver.find_element(by=By.CSS_SELECTOR , value="div.sc-qRumB:nth-child(2)").click()
   time.sleep(3)
   # Log in
   logger.info("Logging in")
   username = driver.find_element(by=By.NAME, value="username")
   password = driver.find_element(by=By.NAME, value="password")
   username.send_keys(args.username)
   password.send_keys(args.password)

   # submit button
   logger.info("Submitting")
   driver.find_element(by=By.CSS_SELECTOR, value="button.ui").click()
   time.sleep(3)

   # Go to the collection page
   logger.info("Goto collection")
   driver.find_element(by=By.CSS_SELECTOR, value="a.globalToolbar_forumsAndCollection__C__GP").click()
   time.sleep(3)

   # click on Paper
   logger.info("Select Paper collection")
   driver.find_element(by=By.CSS_SELECTOR, value="div.style__GameButton-sc-1etwy9d-0:nth-child(1)").click()
   time.sleep(3)

   # click on Settings
   logger.info("Click on settings")
   driver.find_element(by=By.CSS_SELECTOR, value="div.bannerControls_groups__VZcim:nth-child(2) > span:nth-child(2) > button:nth-child(1)").click()
   time.sleep(3)

   # click on DELETE
   logger.info("Write Delete my collection")
   driver.find_element(by=By.CSS_SELECTOR, value="div.ui:nth-child(4) > input:nth-child(1)").send_keys("Delete my collection")

   # click on Back
   logger.info("Go back")
   driver.find_element(by=By.CSS_SELECTOR, value=".overlay_backButton__6gCuA > i:nth-child(1)").click()
   time.sleep(3)

   # click on import_btn
   logger.info("Click on import")
   driver.find_element(by=By.CSS_SELECTOR, value="div.bannerControls_groups__VZcim:nth-child(1) > span:nth-child(1) > button:nth-child(1)").click()
   time.sleep(2)

   # click on file_upload
   logger.info("Unfold upload file ")
   driver.find_element(by=By.CSS_SELECTOR, value="div.accordion:nth-child(2) > div:nth-child(1)").click()
   time.sleep(1)

   # click on cols
   logger.info("Select columns field")
   driver.find_element(by=By.CSS_SELECTOR, value="div.fields:nth-child(2) > div:nth-child(1) > div:nth-child(2)").click()
   time.sleep(1)

   # set dropdown value to 8
   logger.info("Set it to 8")
   driver.find_element(by=By.CSS_SELECTOR, value="div.visible:nth-child(3) > div:nth-child(8)").click()
   time.sleep(1)

   # set dropdown value of last col
   logger.info("Select the last col")
   driver.find_element(by=By.CSS_SELECTOR, value="div.field:nth-child(9) > div:nth-child(1) > i:nth-child(1)").click()
   time.sleep(1)

   # set dropdown value of last col to collector number
   logger.info("Set it to collector number")
   driver.find_element(by=By.CSS_SELECTOR, value="div.visible:nth-child(3) > div:nth-child(10) > span:nth-child(1)").click()
   time.sleep(1)

   # click file import C:\Users\UBOE-yannicklp\Downloads\all-folders.csv
   logger.info("Click on import file")
   file_path = os.path.abspath(args.file)
   input = driver.find_element(by=By.CSS_SELECTOR, value=".style__StyledDropzone-sc-1ksfv9p-1 > input:nth-child(2)")
   input.send_keys(file_path)

   # set dropdown value of last col
   logger.info("Start upload")
   driver.find_element(by=By.CSS_SELECTOR, value="button.ui:nth-child(8)").click()
   time.sleep(600)

   driver.close()

def main():
   parser = argparse.ArgumentParser(description='Logs into the archidekt website to upload the csv files containing the entire collection of a user previously formatted with DSConvert.py.')
   parser.add_argument('file', type=str, help='Input csv file')
   parser.add_argument('-u', '--username', type=str, help='Username of the Dragonshield account', required=True)
   parser.add_argument('-p', '--password', type=str, help='Password of the Dragonshield account', required=True)
   parser.add_argument('-a', '--attempts', type=int, help='Number of attempts', required=False, default=5)
   args = parser.parse_args()
   attempts = 1

   # Set up the driver
   options = Options()
   # options.add_argument('--headless')
   while attempts <= args.attempts:
      driver = webdriver.Firefox(options=options)
      try :
         run(args, driver)
         return
      except Exception as e:
         print("Attempt {} failed with error: {}".format(attempts, e))
         driver.close()
         attempts += 1
         time.sleep(2)
   raise Exception("Failed to run after {} attempts".format(args.attempts))

if __name__ == '__main__':
   main()