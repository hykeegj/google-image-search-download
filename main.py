from scrollBrowserToEnd import scrollBrowserToEnd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os

# [원하는 검색어를 지정]
googleSearchKeyword = "포도"

# [이미지가 저장될 폴더의 이름을 검색어로 설정]
saveImageDirectory = f"./{googleSearchKeyword}"

# [구글 크롬 웹 드라이버 초기 설정]
driver = webdriver.Chrome()

# [구글 이미지 검색 홈페이지 띄우기] 프로그램 시작 시, 첫 화면으로 띄워지길 원하는 웹사이트의 URL 주소를 get() 함수로 받아옴
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl")

# [구글 검색창 찾기] 구글 크롬 브라우저 접속 후, 개발자 도구(F12)를 눌러 구글 검색창의 요소 중 "name"="q"를 찾아 googleSearchElement 변수에 저장하고 커서를 위치시킨다.
googleSearchElement = driver.find_element_by_name("q")

# [검색어 입력] 구글 검색창에 원하는 검색어를 입력한다. 7번째 줄의 googleSearchKeyword 변수 참조
googleSearchElement.send_keys(googleSearchKeyword)

# [검색 결과 표시] Enter 키를 눌러 검색 결과를 표시한다.
googleSearchElement.send_keys(Keys.RETURN)

# [검색 결과 이미지를 전부 띄움] 구글 검색 결과 창에 스크롤을 내릴수록 검색 결과가 계속 추가되어 표시되기 때문에, 검색 결과를 모두 받아오기 위해 스크롤을 최하단까지 내린다.
scrollBrowserToEnd(driver)

# [이미지 찾기] css 선택자로 검색 결과 나타난 이미지들을 모두 찾는다.
images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")

# [각각의 이미지 처리]
for index, image in enumerate(images):
    try:
        # [각각의 이미지 클릭]
        image.click()

        # [2초 기다림] 이미지 클릭 후 2초간 기다려서 로딩이 전부 완료될 때까지 기다린다.
        time.sleep(2)

        # [이미지 URL 추출] 크롬 개발자 도구(F12)를 눌러 큰 이미지의 태그를 우 클릭 후 Copy -> Copy full XPath를 클릭하여 경로 복사 후, xpath로 찾은 다음 "src" 경로 요소를 얻기
        imgURL = driver.find_element_by_xpath(
            "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img").get_attribute("src")

        # [403 Fobbiden 에러를 해결하기 위해 브라우저 header 추가]
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        # [이미지 저장 경로 존재 확인]
        if not(os.path.isdir(saveImageDirectory)):  # 만약 이미지를 저장할 폴더가 없다면
            os.makedirs(saveImageDirectory)  # 폴더를 생성한다.

        # [이미지를 저장] (ex 포도 1, 포도 2, 포도 3, ...)
        urllib.request.urlretrieve(
            imgURL, f"{saveImageDirectory}/{googleSearchKeyword} {index + 1}.jpg")

    # [오류 검출] 이미지를 처리하는 도중에 어떤 오류가 나면 오류를 출력하고 건너뛴다.
    except Exception as e:
        print(f"이미지 처리 도중 에러 발생: {e}")
        pass

# [프로그램 종료] 모든 이미지를 다운로드했으면 프로그램을 종료한다.
print("프로그램을 종료합니다.")
driver.close()
