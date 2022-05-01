from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location= 'D:\Program Files\Google\Chrome\Application/chrome.exe'
options.add_argument("--ignore-certificate-error")
options.add_argument("--ignore-ssl-errors")

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def crawling_img(name):
    driver = webdriver.Chrome('./chromedriver', chrome_options = options)
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
    elem = driver.find_element_by_name("q")
    elem.send_keys(name)
    elem.send_keys(Keys.RETURN)

    #
    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")  # 브라우저의 높이를 자바스크립트로 찾음
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 브라우저 끝까지 스크롤을 내림
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            except:
                break
        last_height = new_height

    imgs = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
    dir = ".\icecreams" + "\\" + name

    createDirectory(dir) #폴더 생성
    count = 0
    for img in imgs:
        count += 1
        try:
            img.click()
            time.sleep(2)
            imgUrl = driver.find_element_by_css_selector(".n3VNCb").get_attribute("src")
            print(imgUrl)
            urllib.request.urlretrieve(imgUrl, f'./icecreams/{name}/{count}.jpg')
        except Exception as e:
            print(e)
        if count >= 10:
            break
    driver.close()
    
icecreams = ["월드콘", "누가바"]

for icecream in icecreams:
    crawling_img(icecream)
