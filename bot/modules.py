# GENERAL
import os
import sys
import csv
import json
import time
import traceback
from datetime import datetime
from termcolor import colored

# SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# GLOBAL VARIABLES
BASE_FOLDER = os.getcwd()
PATH_TO_ASSETS = os.path.join( BASE_FOLDER, 'assets' )
PATH_TO_SYSTEM_FILES = os.path.join( BASE_FOLDER, 'system' )
PATH_TO_CHROME_DRIVER = os.path.join(PATH_TO_SYSTEM_FILES, 'drivers', 'chromedriver')
PATH_TO_METAMASK = os.path.join(PATH_TO_SYSTEM_FILES, 'extensions', 'metamask.crx')
PATH_TO_CSV_DATA_FILE = os.path.join(PATH_TO_ASSETS, 'data.csv')

# MODULES
def fileExists(path=PATH_TO_CSV_DATA_FILE):
    return os.path.exists(PATH_TO_CSV_DATA_FILE)

def readData(path=PATH_TO_CSV_DATA_FILE):
    if not fileExists(path):
        text = colored(f"File at path {path} not found.", "red")
        print(text)
        print("Please add the CSV file and re-run the program to continue.")
        raise SystemExit
    # if file found
    data = list()
    with open(path) as csvFile:
        csvFile = csv.reader(csvFile, delimiter=',')
        line_count = 0
        for row in csvFile:
            if line_count == 0:
                # Skip the headers
                # print(f"Header/Column names are {', '.join(row)}")
                line_count = line_count + 1
            else:
                try:
                    if row[0] and row[1] and row[2] and row[3]:
                        data.append(
                            {'url': row[0].strip(),
                            'price': row[1].strip(),
                            'ethAddress': row[2].strip(),
                            'royalties': row[3].strip()
                            }
                        )
                except:
                    pass
                line_count = line_count + 1
        # print(f"Processed {line_count} lines.")
    return data

def writeData(finalResult):
    # csv header
    fieldnames = ['url', 'price', 'ethAddress', 'royalties', 'status', 'timestamp', 'error']
    # csv data in finalResult
    if finalResult:
        rows = finalResult
        PATH_TO_OUTPUT = os.path.join( PATH_TO_ASSETS, "output", f"{ datetime.now().strftime('%d_%m_%Y__%H_%M_%S') }.csv")
        with open(PATH_TO_OUTPUT, 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

def initalizeDriver(path=PATH_TO_CHROME_DRIVER):
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_extension(PATH_TO_METAMASK)
    driver = webdriver.Chrome(executable_path=path, options=options)
    return driver

def waitForLogin():
    txt = "Please login to Cargo website."
    color = "green"
    text = colored(txt, color)
    print(text)
    condition = True
    while(condition):
        val = input("Please 'Y/y' key again to continue: ")
        if val == 'Y' or val == 'y':
            condition = False

def getElement(waittime, xpath, driver):
    return WebDriverWait(driver, waittime).until(
        EC.presence_of_element_located((By.XPATH, xpath)))

def getElements(waittime, xpath, driver):
    try:
        elem = WebDriverWait(driver, waittime).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except Exception as e:
        elem = None
    finally:
        return elem

def scarpe(driver, url, price, ethAddress, royalties):
    driver.get(url)
    # Side Bar
    getElement(5, "//div[contains(@class, 'MuiPaper-root') and @style]", driver)
    # Sell / Edit
    getElement(5, "//div[contains(@class, 'MuiBox-root') and p[contains(., 'Sell/Edit')]]", driver).click()
    # Marked for Sale Checkbox
    getElement(5, "//input[contains(@class, 'MuiSwitch-input')]", driver).click()
    # Set Price
    setPriceInput = getElement(5, "//input[@name='price']", driver)
    setPriceInput.clear()
    setPriceInput.send_keys(price)
    # Save Changes Button
    saveChangesBtnXpath = "//div[contains(@class, 'MuiBox-root')]/button[@data-id='cargo-btn' and contains(text(), 'Save changes')]"
    getElement(5, saveChangesBtnXpath, driver).click()
    # Wait for "Success" Alert
    # getElements(5, "//div[@role='alert']", driver)
    time.sleep(1)
    # Set Royalties Checkbox
    setRoyaltiesXpath = "//div[@data-id='cargo-checkbox' and preceding::input[@id='setRoyalty']]/div[@data-id='inner']"
    getElement(5, setRoyaltiesXpath, driver).click()
    # Address
    addressInput = getElement(5, "//input[@name='address']", driver)
    addressInput.clear()
    addressInput.send_keys(ethAddress)
    # Commission
    commisionInput = getElement(5, "//input[@name='commission']", driver)
    commisionInput.clear()
    commisionInput.send_keys(royalties)
    # Save Changes Button - Last
    getElement(5, "//div[@data-id='itemgroup']/button[@data-id='cargo-btn' and contains(text(), 'Save changes')]", driver).click()
    # Wait for "Success" Alert
    # getElements(5, "//div[@role='alert']", driver)
    time.sleep(1)

# GENERAL CODE
if __name__ == '__main__':
    print("Please execute main.py to run the program.")