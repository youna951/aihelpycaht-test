from selenium.webdriver.support.ui import WebDriverWait
import pytest
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys, os
# utils 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.common import clear_all
from utils.constants import LOGIN_ID, LOGIN_PW
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

##########################################################################################
# [채팅 히스토리]
##########################################################################################
def test_chat_history(logged_in_driver):
    # 로그인
    #login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    driver = logged_in_driver
    time.sleep(1)

    wait = WebDriverWait(driver, 10)
    
    # "검색" 아이콘 클릭
    search_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[text()="검색"]')
        )
    )
    search_button.click()
    
    # # "검색" > "입력창" 클릭
    # input = wait.until(
    #     EC.element_to_be_clickable(
    #         (By.XPATH, '//input[@placeholder="Search"]')
    #     )
    # )
    # input.click()
    
    # "검색" > "입력창" > "닫기" 버튼 data-testid="xmarkIcon"
    # xmarkBtn = wait.until(EC.visibility_of_element_located(
    #     (By.XPATH, '//button[.//svg[@data-testid="xmarkIcon"]]')
    # ))
    # xmarkBtn.click()
    try:
        # 특정 요소가 나타날 때까지 기다림
        search_modal = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.MuiStack-root.css-j7qwjs"))
        )
        
        # ESC 키 전송
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    except TimeoutException:
        # 요소가 나타나지 않으면 무시
        # 좌측 메뉴 히스토리 내역 data-testid="virtuoso-item-list"
        history_scroll =  wait.until(
            EC.invisibility_of_element_located(
                (By.XPATH, '//ul[@data-testid="virtuoso-item-list"]')
            )
        )        
    result4 = chat_history_update_no(driver, wait)
    result5 = chat_history_update_no(driver, wait)
    result1 = chat_history_check(driver, wait)    
    result2 = chat_history_update(driver, wait)  
    result3 = chat_history_delete(driver, wait)  
    
    assert result4 and result1 and result5 and result2 and result3, "[채팅 히스토리] 체크 또는 업데이트 실패" 
    

#==================================================================================================
###############################################################
# [채팅 히스토리] 채팅 히스토리 스크롤 확인 (AHCT-T150)
###############################################################
def chat_history_check(driver, wait):
    # data-testid="virtuoso-item-list"
    try:
        # 요소가 나타날 때까지 대기
        chat_title_list = wait.until(
            EC.presence_of_element_located((By.XPATH, '//ul[@data-testid="virtuoso-item-list"]'))
        )
                
        print("[채팅 히스토리] 채팅 히스토리 스크롤 확인 (AHCT-T150) 성공!")
        return True

    except TimeoutException:
        # 요소가 나타나지 않으면 assert 실패
        #assert False, "[채팅 히스토리] 채팅 히스토리 스크롤 확인 (AHCT-T150) 실패"
        print("[채팅 히스토리] 채팅 히스토리 스크롤 확인 (AHCT-T150) 실패 / chat_history_check")
        return False
#==================================================================================================
###############################################################
# [채팅 히스토리] 히스토리 타이틀 수정 - 정상 (AHCT-T151)
###############################################################
def chat_history_update(driver, wait):
   # 1. ul[data-testid="virtuoso-item-list"] 찾기
    chat_list = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[data-testid="virtuoso-item-list"]'))
    )

    # 2. 첫 번째 a 태그 선택
    first_chat = chat_list.find_element(By.CSS_SELECTOR, 'a')    

    # 3. 첫 번째 채팅 항목에 마우스 오버
    ActionChains(driver).move_to_element(first_chat).perform()
    time.sleep(0.2)

    # 4. hover 후 나타나는 SVG 메뉴 버튼 클릭
    ellipsis_icon = first_chat.find_element(By.CSS_SELECTOR, 'svg[data-icon="ellipsis-vertical"]')
    ellipsis_icon.click()    

    # 5. "이름 변경" 텍스트 포함 span 요소 찾기
    rename_span = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "이름 변경")]'))
    )

    # 6. 클릭
    rename_span.click()
    
    # 7. 페이지 내 첫 번째 form 안의 input[type="text"] 찾기
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'form input[type="text"]')
        )
    )

    # 8. 기존 값 지우기    
    clear_all(input_box)

    # 9. 새 값 입력
    input_box.send_keys("이름변경 자동화 테스트")
    
    # 10. 저장 버튼 클릭
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "저장")]'))
    ).click()
    
    try:
        alert_div = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="alert"]'))
        )
        print("[채팅 히스토리] 히스토리 타이틀 수정 - 정상 (AHCT-T151) 성공!")
        return True
    except TimeoutException:
        print("[채팅 히스토리] 히스토리 타이틀 수정 - 정상 (AHCT-T151) 실패 / chat_history_update")
        return False        
#==================================================================================================    
###############################################################
# [채팅 히스토리] 히스토리 타이틀 삭제 - 정상 (AHCT-T152)
###############################################################
def chat_history_delete(driver, wait):
    # 1. ul[data-testid="virtuoso-item-list"] 찾기
    chat_list = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[data-testid="virtuoso-item-list"]'))
    )

    # 2. 첫 번째 a 태그 선택
    first_chat = chat_list.find_element(By.CSS_SELECTOR, 'a')

    # 3. 첫 번째 채팅 항목에 마우스 오버
    ActionChains(driver).move_to_element(first_chat).perform()
    time.sleep(0.2)

    # 4. hover 후 나타나는 SVG 메뉴 버튼 클릭
    ellipsis_icon = first_chat.find_element(By.CSS_SELECTOR, 'svg[data-icon="ellipsis-vertical"]')
    ellipsis_icon.click()    

    # 5. "삭제" 텍스트 포함 span 요소 찾기
    delete_span = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//p[contains(text(), "삭제")]'))
    )

    # 6. 클릭
    delete_span.click()
    
    # 7. "삭제" 텍스트 포함 span 요소 찾기
    delete_span = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "삭제")]'))
    )

    # 8. 클릭
    delete_span.click()
  
    try:
        alert_div = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "대화가 삭제되었습니다!")]'))
        )
        print("[채팅 히스토리] 히스토리 타이틀 삭제 - 정상 (AHCT-T152) 성공!")
        return True
    except TimeoutException:
        print("[채팅 히스토리] 히스토리 타이틀 삭제 - 정상 (AHCT-T152) 실패 / chat_history_delete")
        return False        
#================================================================================================== 
###############################################################
# [채팅 히스토리] 히스토리 타이틀 수정 - 취소 (AHCT-T153)
###############################################################
def chat_history_update_no(driver, wait):
   # 1. ul[data-testid="virtuoso-item-list"] 찾기
    chat_list = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[data-testid="virtuoso-item-list"]'))
    )

    # 2. 첫 번째 a 태그 선택
    first_chat = chat_list.find_element(By.CSS_SELECTOR, 'a')

    # 3. 첫 번째 채팅 항목에 마우스 오버
    ActionChains(driver).move_to_element(first_chat).perform()
    time.sleep(0.2)

    # 4. hover 후 나타나는 SVG 메뉴 버튼 클릭
    ellipsis_icon = first_chat.find_element(By.CSS_SELECTOR, 'svg[data-icon="ellipsis-vertical"]')
    ellipsis_icon.click()    

    # 5. "이름 변경" 텍스트 포함 span 요소 찾기
    rename_span = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "이름 변경")]'))
    )

    # 6. 클릭
    rename_span.click()
    
    # 10. 취소 버튼 클릭
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "취소")]'))
    ).click()
    
    try:
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.XPATH, '//h2[contains(text(), "이름 변경")]'))
        )
        print("[채팅 히스토리] 히스토리 타이틀 수정 - 취소 (AHCT-T153) 성공!")
        return True
    except TimeoutException:
        print("[채팅 히스토리] 히스토리 타이틀 수정 - 취소 (AHCT-T153) 실패 / chat_history_update_no")
        return False    
#==================================================================================================     
###############################################################
# [채팅 히스토리] 히스토리 타이틀 삭제 - 취소 (AHCT-T154)
###############################################################
def chat_history_delete_no(driver, wait):
    # 1. ul[data-testid="virtuoso-item-list"] 찾기
    chat_list = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[data-testid="virtuoso-item-list"]'))
    )

    # 2. 첫 번째 a 태그 선택
    first_chat = chat_list.find_element(By.CSS_SELECTOR, 'a')

    # 3. 첫 번째 채팅 항목에 마우스 오버
    ActionChains(driver).move_to_element(first_chat).perform()
    time.sleep(0.2)

    # 4. hover 후 나타나는 SVG 메뉴 버튼 클릭
    ellipsis_icon = first_chat.find_element(By.CSS_SELECTOR, 'svg[data-icon="ellipsis-vertical"]')
    ellipsis_icon.click()    

    # 5. "삭제" 텍스트 포함 span 요소 찾기
    delete_span = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//p[contains(text(), "삭제")]'))
    )

    # 6. 클릭
    delete_span.click()
    
    # 7. "삭제" 텍스트 포함 span 요소 찾기
    delete_span = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "취소")]'))
    )

    # 8. 클릭
    delete_span.click()
  
    try:
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located((By.XPATH, '//h2[contains(text(), "삭제 확인")]'))
        )
        print("[채팅 히스토리] 히스토리 타이틀 삭제 - 취소 (AHCT-T154) 성공!")
        return True
    except TimeoutException:
        print("[채팅 히스토리] 히스토리 타이틀 삭제 - 취소 (AHCT-T154) 실패 / chat_history_delete_no")
        return False 