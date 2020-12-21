import time


# 구글 검색 결과 창에 스크롤을 내릴수록 검색 결과가 계속 추가되어 표시되기 때문에, 검색 결과를 모두 받아오기 위해 스크롤을 최하단까지 내린다.
def scrollBrowserToEnd(driver):
    # 스크롤을 내린 후 새로운 페이지가 로드될 때까지 기다리는 시간
    SCROLL_PAUSE_TIME = 1

    # 브라우저 스크롤 높이 값을 얻는다.
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 최하단으로 스크롤 할 때까지 무한 반복한다.
    while True:
        # 하단까지 스크롤 한다.
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # 페이지 로드될 때까지 기다린다.
        time.sleep(SCROLL_PAUSE_TIME)

        # 추가된 스크롤 높이를 구하고 추가되기 이전 스크롤 높이와 비교한다.
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 추가된 스크롤 높이 값과 추가되기 이전 스크롤 높이 값을 비교하여 같으면 '결과 더보기' 버튼을 클릭한다.
        if new_height == last_height:
            try:
                # '결과 더보기' 버튼을 클릭한다.
                driver.find_element_by_css_selector(".mye4qd").click()
            # '결과 더보기' 버튼이 없어 오류가 나면 오류를 출력하고 무한반복문을 빠져나온다.
            except Exception as e:
                print(f"scrollBrowerToEnd.py에서 오류 발생: {e}")
                break
        # 이전 스크롤 높이 값을 추가된 스크롤 높이 값으로 초기화한다.
        last_height = new_height
