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
import os
import emoji


credential_path = ""
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

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


def detect_properties(path):
    """Detects image properties in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation

    max_fraction = 0.0
    color_count = 0
    color_r = 0.0;  color_g = 0.0; color_b = 0.0

    for color in props.dominant_colors.colors:
        color_count += 1
        if color.pixel_fraction >= max_fraction:
            max_fraction = color.pixel_fraction
            color_r = color.color.red
            color_g = color.color.green
            color_b = color.color.blue

        if color_count >= 5:    # 시간상 최대 5개 색 비교
            break

    # 해당 image의 가장 큰 fraction을 차지하는 color의 rgb값을 출력
    print("r: {}\tg: {}\tb: {}".format(color_r, color_g, color_b))

    if response.error.message:
        raise Exception('{}\nFor more info on error messages, check: ''https://cloud.google.com/apis/design/errors'.format(response.error.message))


# login 유지

driver.implicitly_wait(5)
driver.get("https://www.instagram.com/accounts/login/")
login_x_path = '/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button'

# 개인정보 보안을 위한 수정

#insta_id = 'myaho_123' # input("인스타그램 아이디를 입력하세요 : ")
#insta_pw = 'capstonemyaho' # input("인스타그램 비밀번호를 입력하세요 : ")

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
    for i in range(21,len(search_id)):

        # print(mbti, search_id[i].text)
        print(f"search_id 길이 = {len(search_id)}")
        if mbti not in search_id[i].text:
            secret = 0
            print(search_id[i].text)
            # time.sleep(3)
            # search_id[i].click()
            driver.execute_script("arguments[0].click();", search_id[i])
            elements=[]
            time.sleep(3)
            elements = driver.find_element_by_css_selector('article.ySN3v').text
            print(elements)
            print(len(elements))
            #print(elements)
            if( len(elements) != 0):
                # 비공개 계정
                secret = 1
                print(secret)
            else:
                # 공개 계정
                cnt += 1
                time.sleep(3)
                # 필요한 정보 크롤링
                post = driver.find_element_by_css_selector('span.-nal3 span').text
                follower = driver.find_element_by_css_selector('li.Y8-fY:nth-child(2) span').text
                following = driver.find_element_by_css_selector('li.Y8-fY:nth-child(3) span').text
                story = len(driver.find_elements_by_css_selector('div.tUtVM'))
                print('open account')

                print(f'story = {story}')
                # tag post 없는 경우에서 오류나는 듯? 수정 할 것
                # 태그된 게시물 버튼 경로가 위에 스토리가 있을 때와 없을때가 다르다.....ㅅㅂ... ++ 릴스 있으면 또 달라지지만 오류는 안나니까...희희 -> 가능성 희박...
                time.sleep(3)
                #tag_index = 0
                if (story != 0):
                    tag_index = len(driver.find_elements_by_css_selector('div.fx7hk a'))
                    print(f'tag_index={tag_index}')
                    tag = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[2]/a[' + str(tag_index) + ']').click()
                    #tag = driver.find_element_by_xpath("//*[@aria-label='태그됨']").click()
                    #driver.find_elements_by_css_selector('svg._8-yf5 ').click()
                else:
                    tag_index = len(driver.find_elements_by_css_selector('div.fx7hk a'))
                    tag = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/a[' + str(tag_index) + ']').click()

                tag_list = []
                tag_length = 0
                try:
                    while True:
                        for image in add_image():
                            # 이미 확인한 image의 경우, pass
                            tag_length = len(tag_list)
                            #print(image)
                            if image in tag_list:
                                pass
                            else:
                                tag_list.append(image)
                        scroll_down()
                        if len(tag_list) > 20 or tag_length == len(tag_list):
                            break
                except NoSuchElementException:
                    pass
                tag_post = len(tag_list)
                driver.back()

                # tag_post = len(driver.find_elements_by_css_selector('div._9AhH0'))

                # 이미지 크롤링 구현 -> id 폴더 생성 -> id에 해당하는 게시글 사진(여러장인 게시글 일 경우 대표사진만) 폴더에 모음
                # 폴더 약 200개 생성 예정

                print(f'secret = {secret}')
                print(f"post: {post},follower: {follower},following: {following},story: {story}, tag_post: {tag_post}")

                # 게시글의 색감 추출
                # 게시글 속 이모티콘 수 세기 => image_list의 개수로 나눠주어서 평균 내기

                image_list = []
                emoticons = 0  # 게시글 속 이모티콘 수
                try:
                    while True:
                        for n in add_image():
                            # 이미 확인한 image의 경우, pass
                            if n in image_list:
                                pass
                            else:
                                image_list.append(n)
                                print(n)

                                # 게시글 속 이모티콘 수 세기
                                # 게시글 선택
                                idx = image_list.index(n)
                                print(image_list.index(n))
                                row = int(idx/3) + 1
                                col = int(idx % 3) + 1
                                if story != 0:
                                    story_idx = 3
                                else:
                                    story_idx = 2
                                print(f'row = {row}, col = {col}')

                                driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div['+str(story_idx)+']/article/div[1]/div/div['+str(row)+']/div['+str(col)+']').click()

                                # 게시글 텍스트 추출
                                try :
                                    context = driver.find_element_by_css_selector('div.C4VMK').text
                                    emoji_list = re.findall(emoji.get_emoji_regexp(), context)
                                    emoticons += len(emoji_list)
                                    print(emoji_list)
                                except NoSuchElementException:
                                    print('No context in post')
                                time.sleep(2)
                                driver.find_element_by_xpath('/html/body/div[5]/div[3]/button').click() #X : 창 닫기
                                driver.back()
                        scroll_down()
                        if (int(post) == len(image_list)) or (len(image_list) > 20):
                            break
                except NoSuchElementException:
                    pass
                print('-----------------------------------------------------')
                # image 저장하고 색상 값 분석
                for j, n in enumerate(image_list):
                    urllib.request.urlretrieve(n['src'], str(j)+'.jpg')
                    image_name = os.path.join(os.path.dirname(__file__), str(j)+'.jpg')
                    detect_properties(image_name)

                # 게시글 당 평균 이모티콘 수
                if len(image_list) != 0:  # 게시글이 없으면 나눗셈 오류나므로 예외 처리
                    print(f'average of emoticons = {emoticons / len(image_list)}')
                else:
                    print('No emoticons')

            print(cnt, max, i)
            time.sleep(5)
            driver.back()

            if cnt == max or i == len(search_id) - 1:
                print("test", cnt, i)
                break
            else:
                driver.find_element_by_xpath(search_xpath).send_keys(mbti)
                print(mbti)
                time.sleep(2)
                search_id = driver.find_elements_by_css_selector("div._7UhW9.xLCgt.qyrsm.KV-D4.uL8Hv")
                print(len(search_id))
    print(f"mbti {mbti}의 계정을 총 {cnt}개 찾았습니다")
