from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.keys import Keys
import os

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service

def get_instagarm(plusUrl):
   baseUrl = 'https://www.instagram.com/explore/tags/'
   url = baseUrl + quote_plus(plusUrl)

   # DRIVER_SETTING
   options = webdriver.ChromeOptions()
   options.add_argument('headless')
   options.add_argument('window-size=1920x1080')
   options.add_argument("disable-gpu")
   cap = DesiredCapabilities().CHROME
   cap["marionette"] = True
   options.add_experimental_option("excludeSwitches", ["enable-logging"])

   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
   driver.get(url)
   time.sleep(2) 

   html = driver.page_source
   soup = BeautifulSoup(html, "html.parser")
   insta = soup.select('div._aabd._aa8k._aanf > .x1i10hfl')
   n = 1
   확인폴더 = "./img/" + plusUrl
   for i in insta:
      if not os.path.exists(확인폴더):
         os.mkdir(확인폴더)
      imgUrl = i.select_one('._aagv').img['src']
      with urlopen(imgUrl) as f:
         with open(f"{확인폴더}/{str(n)}.jpg", 'wb') as h:
            img = f.read()
            h.write(img)
      n += 1
   print("[알림] {0} 태그 관련 이미지 다운로드가 완료 되었습니다".format(plusUrl))
   driver.close()

if __name__ == '__main__':
   plusUrl = input('검색할 태그를 입력하세요 : ')
   get_instagarm(plusUrl)