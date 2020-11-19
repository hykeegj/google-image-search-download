from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os

searchKeyword = "포도"  # Enter the search keyword you want.
path = f"./{searchKeyword}"

driver = webdriver.Chrome()
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl")

elem = driver.find_element_by_name("q")
elem.send_keys(searchKeyword)
elem.send_keys(Keys.RETURN)

SCROLL_PAUSE_TIME = 1
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        try:
            driver.find_element_by_css_selector(".mye4qd").click()
        except Exception as e:
            print(e)
            break
    last_height = new_height

images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")

for index, image in enumerate(images):
    try:
        image.click()

        time.sleep(2)

        imgURL = driver.find_element_by_xpath(
            "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img").get_attribute("src")

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        if not(os.path.isdir(path)):
            os.makedirs(path)

        urllib.request.urlretrieve(
            imgURL, f"{path}/{searchKeyword}{index + 1}.jpg")  # Make the directory the name of the 'searchKeyword' value.

    except Exception as e:
        print(e)
        pass

print("프로그램을 종료합니다.")
driver.close()
