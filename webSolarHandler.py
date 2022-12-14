from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service





class WebSolarHandler:

    def __init__(self, username: str, passwort: str):
        
        global driver
        global fha
        global settings

        ##setup and open website
        url='https://www.solarweb.com/Account/ExternalLogin'
    
        options = Options()
        # browser is Chromium instead of Chrome
        options.BinaryLocation = "/usr/bin/chromium-browser"
        # we use custom chromedriver for raspberry
        driver_path = "/usr/bin/chromedriver"
        driver = webdriver.Chrome(options=options, service=Service(driver_path))

        time.sleep(2)
        driver.get(url)
        
            
       

        try:

            time.sleep(5)

            

            #login

            pageLoading = True

            while(pageLoading):
                try:
                    username_elem = driver.find_element(By.XPATH,"//input[@name='username']")
                    username_elem.send_keys(username)

                    time.sleep(0.2)   

        
                    password_elem = driver.find_element(By.XPATH,"//input[@name='password']")
                    password_elem.send_keys(passwort)

                    time.sleep(0.3)

                    submit_button = driver.find_element(By.XPATH,'//button[@id="submitButton"]')
                    submit_button.click()

                     
                    pageLoading = False

                except:
                    continue


            pageLoading = True

            while(pageLoading):
                try:
                    cookie_button = driver.find_element(By.XPATH,'//button[@id="CybotCookiebotDialogBodyButtonDecline"]')
                    cookie_button.click()
                    pageLoading = False
                except:
                    continue

            pageLoading = True
            while(pageLoading):
                try:
                    driver.find_element(By.ID,"pvText")
                    pageLoading = False
                except:
                    continue

            

        except:
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("Connecting to SolarWeb failed")
            print("Make sure the website hasn't changed")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            driver.close()

    def getCurrentPowerOutput(self):
        global driver
        ## return [0] output as float ---- [1] unit as string
        pvPower = driver.find_element(By.ID,"pvText").text
        if(pvPower != ""):
        #pvPower = "2,3 kW"
            pvPower = pvPower.split()
            pvPower[0] = float(pvPower[0].replace(",","."))

            if(pvPower[1][0] == 'k'):
                return round(pvPower[0]*1000)

            return pvPower[0]

        else:
            return 0

    def getCurrentPowerUsage(self):
        global driver
        powerUsage = driver.find_element(By.ID,"consumerText").text
        #powerUsage = "2,3 kW"
        if(powerUsage != ""):
            powerUsage = powerUsage.split()
            powerUsage[0] = float(powerUsage[0].replace(",","."))
            
            if(powerUsage[1][0] == 'k'):
                return round(powerUsage[0]*1000)


            return powerUsage[0]
        else:
            return 0

    def getCurrentGridInput(self):
        global driver
        gridInput = driver.find_element(By.ID,"gridText").text
        #gridInput = "2,3 kW"

        if(gridInput != ""):
            gridInput = gridInput.split()
            gridInput[0] = float(gridInput[0].replace(",","."))

            if(gridInput[1][0] == 'k'):
                return round(gridInput[0]*1000)

            return gridInput[0]
        else:
            return 0
    
    def close(self):
        global driver
        driver.close()







