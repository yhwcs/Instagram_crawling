import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException
from urllib.request import urlretrieve

# import openpyxl
import time
import re
import urllib.parse
import urllib.request

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
# 크롬창(웹드라이버) 열기
driver = webdriver.Chrome("./chromedriver")


# parsing을 위한 함수를 생성
def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ', str(data))


def get_crawl(URL):
    response = driver.get(URL)
    html = driver.page_source
    soup7 = BeautifulSoup(html, 'html.parser')
    ex_id_divs = soup7.find('div', {'id': 'view_content'})
    crawl_data = remove_html_tags(ex_id_divs)
    return crawl_data


def scroll_down():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)


def add_image():
    temp_image_list = []
    image = driver.find_elements_by_class_name("FFVAD")
    for n in image:
        temp_image = {}
        temp_image['alt'] = n.get_attribute('alt')
        temp_image['src'] = n.get_attribute('src')
        temp_image_list.append(temp_image)
    return temp_image_list


# login 유지

driver.implicitly_wait(3)
driver.get("https://www.instagram.com/accounts/login/")
login_x_path = '/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button'

# 개인정보 보안을 위한 수정 -> 계정을 하나 파자
insta_id = 'myaho_123' # input("인스타그램 아이디를 입력하세요 : ")
insta_pw = 'capstonemyaho' # input("인스타그램 비밀번호를 입력하세요 : ")
driver.find_element_by_name('username').send_keys(insta_id)
driver.find_element_by_name('password').send_keys(insta_pw)
driver.find_element_by_xpath(login_x_path).click()

driver.implicitly_wait(3)
login_x_path2 = '/html/body/div[1]/section/main/div/div/div/section/div/button'
driver.find_element_by_xpath(login_x_path2).click()

driver.implicitly_wait(3)
login_x_path3 = '/html/body/div[4]/div/div/div/div[3]/button[2]'
driver.find_element_by_xpath(login_x_path3).click()

search_xpath = '/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input'

# 미통과 미미 수준 'enfp','istp','infp','esfp','intj' ** 10개 정도로 수정
# 미통과 심각 수준 'estj','estp' 'infj'**굉장히 문제가 많음  est들은 인스타를 안하는 건가 -> 오픈채팅방으로 구하기
# 통과 'istj','isfj','isfp','intp','esfj','entj','entp','enfj'
search_name = ['istj','isfj','isfp','intj','intp','esfj','entj','entp','enfj','enfp','istp','infp','esfp']
for mbti in search_name:
    # print("mbti", mbti)
    driver.find_element_by_xpath(search_xpath).send_keys(mbti)

    # 검색 칸에서 뜨는 사용자 id
    search_id = driver.find_elements_by_css_selector("div._7UhW9.xLCgt.qyrsm.KV-D4.uL8Hv")
    # 검색 칸에서 뜨는 사용자 bio
    search_bio = driver.find_elements_by_css_selector("div._7UhW9.xLCgt.MMzan._0PwGv.fDxYl")

    if mbti == 'istp' or mbti == 'infp' or mbti == 'esfp' or mbti == 'intj' or mbti == 'enfp':
        max = 10
    else:
        max = 15

    cnt = 0

    # 들어가야하는 계정 선택
    for i in range(len(search_id)):
        # print(mbti, search_id[i].text)
        if mbti not in search_id[i].text:
            secret = 0

            print(search_id[i].text)
            # time.sleep(3)
            # search_id[i].click()
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
                post = driver.find_element_by_css_selector('span.-nal3 span').text
                following = driver.find_element_by_css_selector('li.Y8-fY:nth-child(2) span').text
                follower = driver.find_element_by_css_selector('li.Y8-fY:nth-child(3) span').text
                story = len(driver.find_elements_by_css_selector('div.tUtVM'))

                # tag post 없는 경우에서 오류나는 듯? 수정 할 것 - 0430 해결(?) tag_post 개수가 구해지긴 하나, 첫 화면에 보이는 최대 개수 (12개) 이상이 나오지 않음 => 의논 필요

                driver.find_element_by_css_selector('span.qzihg span').click()
                tag_post_lines = len(driver.find_elements_by_css_selector('div.Nnq7C.weEfm')) # tag_post의 라인수
                tag_post = len(driver.find_elements_by_css_selector('div._9AhH0')) # tag_post의 개수
                print(f'tag_post = {tag_post}')
                driver.back() # tag_post click 한 거 되돌리기( 한번 뒤로가기 )

                # 이미지 크롤링 구현 -> id 폴더 생성 -> id에 해당하는 게시글 사진(여러장인 게시글 일 경우 대표사진만) 폴더에 모음
                # 폴더 약 200개 생성 예정

                print(secret)
                print(post,follower,following,story)

                image_list = []
                try:
                    while True:
                        for n in add_image():
                            if n in image_list:
                                pass
                            else:
                                image_list.append(n)
                        scroll_down()
                        if (int(post) == len(image_list)) or (len(image_list) > 20):
                            break
                except NoSuchElementException:
                    pass
                for j, n in enumerate(image_list):
                    urllib.request.urlretrieve(n['src'], str(j)+'.jpg')

            print(cnt, max, i)
            driver.back()

            if cnt == max or i == len(search_id) - 1:
                print("test", cnt, i)
                break
            else:
                driver.find_element_by_xpath(search_xpath).send_keys(mbti)
                search_id = driver.find_elements_by_css_selector("div._7UhW9.xLCgt.qyrsm.KV-D4.uL8Hv")

    print(f"mbti {mbti}의 계정을 총 {cnt}개 찾았습니다")
