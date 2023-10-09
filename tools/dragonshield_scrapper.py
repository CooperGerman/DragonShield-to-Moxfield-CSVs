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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def run(args):

	# Set up the driver
	options = Options()
	options.add_argument('--headless')
	driver = webdriver.Firefox(options=options)
	driver.get("https://auth.dragonshield.com/Account/Login/")

	# Log in
	username = driver.find_element(by="id", value="Email")
	password = driver.find_element(by="id", value="Password")
	username.send_keys(args.username)
	password.send_keys(args.password)
	# xpath /html/body/div[1]/main/div/div/form/fieldset/div/div[4]/button

	login = driver.find_element(by="xpath", value="/html/body/div[1]/main/div/div/form/fieldset/div/div[4]/button")
	login.click()
	time.sleep(5)
	# Go to the collection page
	driver.get("https://mtg.dragonshield.com/folders")
	time.sleep(10)
   #export xpath /html/body/app-root/div/master-layout/div/div/div[2]/div/folders/div[1]/div/div[3]/div/div[2]/div[2]/i
	download = driver.find_element(by="xpath", value="/html/body/app-root/div/master-layout/div/div/div[2]/div/folders/div[1]/div/div[3]/div/div[2]/div[2]/i")
	download.click()
	time.sleep(10)

	# Close the driver
	driver.close()

def main():
   parser = argparse.ArgumentParser(description='Scrapes the Dragonshield website and downloads the csv files containing the entire collection of a user.')
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