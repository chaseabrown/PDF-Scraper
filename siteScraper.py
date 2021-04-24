#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 15:45:21 2020

@author: chasebrown
"""


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import urllib.request

def download_file(name, download_url):
    response = urllib.request.urlopen(download_url)
    file = open(name + ".pdf", 'wb')
    file.write(response.read())
    file.close()
    print("Completed")




WINDOW_SIZE = "1720,1080"
    
chrome_options = Options()  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('"plugins.always_open_pdf_externally": True')

download_dir = "Path you want this downloaded to"
options = webdriver.ChromeOptions()

profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
               "download.default_directory": download_dir , "download.extensions_to_open": "applications/pdf"}
options.add_experimental_option("prefs", profile)
driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)  # Optional argument, if not specified will search path.


    
browser = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_options)
browser.get("https://web-as.tamu.edu/gradereport/")
yearElement = browser.find_element_by_id("ctl00_plcMain_lstGradYear")
semesterElement = browser.find_element_by_id("ctl00_plcMain_lstGradTerm")
collegeElement = browser.find_element_by_id("ctl00_plcMain_lstGradCollege")
listOfYears = []
counter = 1
for i in browser.find_elements_by_xpath('//*[@id="ctl00_plcMain_lstGradYear"]/option'):
    listOfYears.append({'text':i.text, 'xpath':'//*[@id="ctl00_plcMain_lstGradYear"]/option[' + str(counter) + ']'})
    counter+=1

listOfPDFs = []
for i in listOfYears:
    itext = i['text']
    browser.find_element_by_xpath(i['xpath']).click()
    time.sleep(.5)
    listOfTerms = []
    counter_s = 1
    for s in browser.find_elements_by_xpath('//*[@id="ctl00_plcMain_lstGradTerm"]/option'):
        listOfTerms.append({'text':s.text, 'xpath':'//*[@id="ctl00_plcMain_lstGradTerm"]/option[' + str(counter_s) + ']'})
        counter_s += 1
    for s in listOfTerms:
        stext = s['text']
        browser.find_element_by_xpath(s['xpath']).click()
        time.sleep(.5)
        listOfColleges = []
        counter_h = 1
        for h in browser.find_elements_by_xpath('//*[@id="ctl00_plcMain_lstGradCollege"]/option'):
            listOfColleges.append({'text':h.text, 'xpath':'//*[@id="ctl00_plcMain_lstGradCollege"]/option[' + str(counter_h) + ']'})
            counter_h += 1
        for h in listOfColleges:
            htext = h['text']
            browser.find_element_by_xpath(h['xpath']).click()
            browser.find_element_by_xpath('//*[@id="ctl00_plcMain_btnGrade"]').click()
            time.sleep(.5)
            driver.get(browser.current_url)
            time.sleep(.5)
            browser.back()            

browser.close()
driver.close()
