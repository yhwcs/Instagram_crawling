import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import openpyxl
import time
import re

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# 크롬창(웹드라이버) 열기
driver = webdriver.Chrome("./chromedriver")

# parsing을 위한 함수를 생성
def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ',str(data))

def get_crawl(URL):
    response = driver.get(URL)
    html = driver.page_source
    soup7 = BeautifulSoup(html, 'html.parser')
    ex_id_divs = soup7.find('div',{'id':'view_content'})
    crawl_data = remove_html_tags(ex_id_divs)
    return crawl_data

# login 유지

driver.implicitly_wait(3)
driver.get("https://www.instagram.com/accounts/login/")
login_x_path = '/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button'
driver.find_element_by_name('username').send_keys('auspicious_.w.cherry')
driver.find_element_by_name('password').send_keys('xhvkwm_25_')
driver.find_element_by_xpath(login_x_path).click()

driver.implicitly_wait(3)
login_x_path2 = '/html/body/div[1]/section/main/div/div/div/section/div/button'
driver.find_element_by_xpath(login_x_path2).click()

driver.implicitly_wait(3)
login_x_path3 = '/html/body/div[4]/div/div/div/div[3]/button[2]'
driver.find_element_by_xpath(login_x_path3).click()

########################### 0428 완료 ############################

search_xpath = '/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input'

search_name = 'istj'  #input("mbti를 입력하세요: ")
driver.find_element_by_xpath(search_xpath).send_keys(search_name)

# 검색 칸에서 뜨는 사용자 id
search_id = driver.find_elements_by_css_selector("div._7UhW9.xLCgt.qyrsm.KV-D4.uL8Hv")
# 검색 칸에서 뜨는 사용자 bio
search_bio = driver.find_elements_by_css_selector("div._7UhW9.xLCgt.MMzan._0PwGv.fDxYl")

max = 15
cnt = 0



# 들어가야하는 계정 선택
for i in range(len(search_id)):
    print(search_name, search_id[i].text)
    if search_name not in search_id[i].text:
        secret = 0

        print(search_id[i].text)
        #time.sleep(3)
        #search_id[i].click()
        driver.execute_script("arguments[0].click();", search_id[i])
        elements = driver.find_element_by_css_selector('article.ySN3v').text

        if elements:
            # 비공개 계정
            secret = 1
            print(secret)
        else:
            # 공개 계정
            cnt += 1
            # 필요한 정보 크롤링
            print(secret)


        driver.back()
        driver.find_element_by_xpath(search_xpath).send_keys(search_name)
        search_id = driver.find_elements_by_css_selector("div._7UhW9.xLCgt.qyrsm.KV-D4.uL8Hv")
        if max == cnt:
            print(f"mbti {search_name}의 계정을 총 {max}개 찾았습니다")


print(f"mbti {search_name}의 계정을 총 {cnt}개 찾았습니다")

# 컨테이너(포스트) 12개 저장
instagram = driver.find_elements_by_css_selector("div.v1Nh3")
instagram = instagram[:12]

# 컨테이너 반복하기
for insta in instagram:
    # 포스트 클릭하기
    insta.click()

    # 시간 지연
    time.sleep(1)

    # 본문 선택 후 출력
    post = driver.find_element_by_css_selector("div.C4VMK span").text
    print(post)

    # 닫기 버튼 클릭
    but_close = driver.find_element_by_css_selector("button.ckWGn")
    but_close.click()