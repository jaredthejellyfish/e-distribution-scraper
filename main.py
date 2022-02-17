from shutil import ReadError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException  

import time
import configparser

#Import username and password
config = configparser.ConfigParser()
config.read('config.ini')

username = config['USERDATA']['username']
password = config['USERDATA']['password']

path = config['CHROMEDRIVER']['path']

# Helper functions
def check_exists_by_xpath(xpath):
    '''Takes in the XPath of an element, returns if it exists or not'''
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

def safe_send_keys(driver, input_selector: str, input_text: str, selector_type = By.XPATH ):
    '''Takes in the driver, XPath of an element, and the text to input, sends alt keys without raising errors.'''
    driver.find_element(selector_type, input_selector).click()
    action = ActionChains(driver)
    action.send_keys(input_text)
    action.perform()

# Options to pass to the Chrome driver for it to run headless.
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')

# Create a web driver object so we can run the "tests"
driver = webdriver.Chrome(executable_path= path, options= chrome_options )

# Open the site to test.
driver.get("https://zonaprivada.edistribucion.com/areaprivada/s/wp-reconnect-detail?cupsId=a0r2400000GyH9bAAF&vis=a5U2o0000018156EAA")  

# Wait for element "input-5" to be loaded then enter user credentials...
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div/div[1]/div/span/lightning-input/div/input[@id="input-5"]'))).send_keys(username)

safe_send_keys(driver, '/html/body/div[3]/div[2]/div/div[2]/div/div/div[2]/div/span/lightning-input/div/input[@id="input-6"]', password)

# Click credentials confirm button
driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/div[2]/div/div/div[3]/div/div[2]/button[@class="slds-button slds-button_brand"]').send_keys(Keys.ENTER)

# Wait for element "Consultar Contador" to load then click it
element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div[3]/div/div[2]/div/div/div/div/article/div[1]/div/div[1]/button[@title="Consultar Contador"]')))
time.sleep(1)
element.click()

# Wait for loading wheel to appear then wait until it disappears
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div/div[2]/div/div/div/div/article/lightning-spinner')))

while check_exists_by_xpath('/html/body/div[3]/div[3]/div/div[2]/div/div/div/div/article/lightning-spinner') is True:
    time.sleep(0.2)
    pass

time.sleep(1)

# If the check for power returns an error raise ReadError
if check_exists_by_xpath('/html/body/div[3]/div[3]/div/div[2]/div/div/div/div/article/div[4]/section/div/footer/button[@title="ENTENDIDO"]'):
    raise ReadError

# Check if text data exists 100 times, if not exit the program
for i in range(100):
    if check_exists_by_xpath('/html/body/div[3]/div[3]/div/div[2]/div/div/div/div/article/div[1]/div/div[2]/span[@class="description"]') is False:
        pass
    else:
        break

if check_exists_by_xpath('/html/body/div[3]/div[3]/div/div[2]/div/div/div/div/article/div[1]/div/div[2]/span[@class="description"]') is False:
    exit()

# Read data and print it
reading = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div[2]/div/div/div/div/article/div[1]/div/div[2]/span[@class="description"]').text.split('\n')[1]
print(reading)

# Close the driver and terminate the program
driver.close()