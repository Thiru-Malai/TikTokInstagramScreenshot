from playwright.sync_api import sync_playwright
import re
from time import sleep
import os
from functools import partial 

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

output_path = "./output"

if not os.path.exists(output_path):
    os.makedirs(output_path)

list = ('instagram/video', 'instagram/profile', 'tiktok/video', 'tiktok/profile') 

concat_root_path = partial(os.path.join, output_path) 
make_directory = partial(os.makedirs, exist_ok=True) 
  
for path_items in map(concat_root_path, list): 
    make_directory(path_items) 

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox') #for linux avoid chrome not started
chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"')
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

url = "https://www.instagram.com/"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)
driver.get(url)

username_input = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
username_input.send_keys("obviouskings@gmail.com")
sleep(2)
password_input.send_keys("Obviouskings")
login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()
sleep(5)


def extract_audio_ids(url):
    audio_id = ""
    match = re.search(r'/audio/(\d+)', url)
    if match:
        audio_id = match.group(1)
    return audio_id

with open("links.txt", "r") as f:
    for link in f.readlines():
        try:
            driver.implicitly_wait(10)
            driver.get(link)
            sleep(4)
            # Close Tiktok Dialog
            if('video' in link):
                wait = WebDriverWait(driver,8)
                guestBtnSele = '#loginContainer > div > div > div.css-txolmk-DivGuestModeContainer.exd0a435 > div > div'
                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='loginContainer']/div/div/div[3]/div/div"))).click()
                except:
                    pass
                
            filename = link.split('/')[-1]
            filename = link.split('/')[-1].rstrip('\n')
            if('reel' in link):
                driver.save_screenshot(f'./output/instagram/video/{filename}.png')
            elif('instagram' in link):
                sleep(12)
                driver.save_screenshot(f'./output/instagram/profile/{filename}.png')
            elif('video' in link):
                filename = filename.split('?')[0]
                driver.save_screenshot(f'./output/tiktok/video/{filename}.png')
            elif('tiktok' in link):
                driver.save_screenshot(f'./output/tiktok/profile/{filename}.png')
            sleep(2)
            driver.execute_script("window.scrollTo(0, 164)")
        except Exception as e:
            print(e)
            pass
    driver.close()
            
