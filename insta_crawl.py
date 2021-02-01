import selenium
import time
import datetime
import urllib.request
import os

from selenium import webdriver

def get_url():
    url = 'https://www.instagram.com/'
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options = options,executable_path='chromedriver.exe')
    driver.get(url)
    time.sleep(3)

    return driver

def tag_():
    input_num = int(input("검색하고자 하는 내용이 무엇입니까?(1번 : 태그, 2번 : 사용자)"))
    if input_num == 1:
        print("=== 태그를 선택하셨습니다. ===")
        print("태그를 기준으로 이미지 추출하겠습니다.")
        tag = input("추출할 사진의 주제를 입력하시오 : ")
        return '#'+tag
    elif input_num == 2:
        print("=== 사용자를 선택하셨습니다. ===")
        print("사용자를 기준으로 이미지 추출하겠습니다.")
        tag = input("사용자의 아이디를 입력하시오 : ")
        return tag
    else:
        print("잘못입력하셨습니다. 프로그램이 강제 종료됩니다.")
        return False

def login(id, password, driver):
    # 인스타그램 로그인
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(id)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
    time.sleep(5)

    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
    time.sleep(5)

    driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
    time.sleep(5)

def search(driver, tag):
    # 검색
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input').send_keys(tag)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[4]/div/a[1]').click()
    time.sleep(5)

    # 스크롤 내리기
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=2)
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        if datetime.datetime.now() > end:
            break

def download(driver):
    print(driver.current_url)

    imgs = driver.find_elements_by_css_selector('img.FFVAD')

    for img in imgs:
        print(img.get_attribute('src'))

    DATA_DIR = './insta_img'
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)

    count = 1
    for img in imgs:
        urllib.request.urlretrieve(img.get_attribute('src'), './insta_img/img_{}.jpg'.format(count))
        count+=1

if __name__ == '__main__':
    print("=== 해당 프로그램은 인스타그램의 사진을 추출하는 프로그램입니다. ===")
    id = input("아이디를 입력하시오 : ")
    password = input("비밀번호를 입력하시오 : ")
    tag = tag_()
    if tag is False:
        print("프로그램이 종료되었습니다.")
    else:
        drvier = get_url()
        login(id=id, password=password, driver=drvier)
        search(driver=drvier, tag=tag)
        download(driver=drvier)