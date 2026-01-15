'''
작성자 : 이원기
'''

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.common import login, logout
from utils.constants import LOGIN_ID, LOGIN_PW   # 🔥 상수 import
from selenium.webdriver.support.ui import Select
import logging

# ---------------------------------------------------------------------------------
# 로그인/로그아웃 기능 테스트
# ---------------------------------------------------------------------------------

# @pytest.fixture
# def driver():
#     chrome_options = Options()
#     chrome_options.add_experimental_option("detach", True)
#     chrome_options.add_argument("--start-maximized")

#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=service, options=chrome_options)
#     driver.implicitly_wait(5)

#     yield driver
#     driver.quit()

########################################################################################## 
# [로그인] 정상적인 로그인 (AHCT-T1)
# [로그아웃] (AHCT-T6)
##########################################################################################
def test_login_logout(driver):
    # 🔥 상수 사용
    login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    logout(driver)
    print(f"✅ [SUCCESS] [로그인] 정상적인 로그인 & [로그아웃]")

##########################################################################################
# [로그인] 비정상적인 로그인(ID EMAIL 형식 아닌 경우) (AHCT-T2)
##########################################################################################
def test_login_invalid_email(driver):
    # 잘못된 이메일과 정상 비밀번호
    invalid_email = "invalid_id"  # 이메일 형식 아님
    password = ""

    # 로그인 시도
    login(driver, invalid_email, password, check_success=False)

    try:
        error_msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//p[contains(text(), "Invalid email format.")]')
                #(By.ID, ":r3:-helper-text")
            )
        )
        #assert error_msg.is_displayed(), "잘못된 이메일 입력 시 오류 메시지가 표시되지 않음"
        if "Invalid email format" in error_msg.text:
            logging.info(f"✅ [SUCCESS] [로그인] 비정상적인 로그인(ID EMAIL 형식 아닌 경우)")
            print(f"✅ [SUCCESS] [로그인] 비정상적인 로그인(ID EMAIL 형식 아닌 경우)")
        assert "Invalid email format" in error_msg.text, f"예상 오류 메시지와 다름. 실제 메시지: '{error_msg.text}'"
    except:
        assert False, f"❌ [FAIL] [로그인] 비정상적인 로그인(ID EMAIL 형식 아닌 경우)"

    

##########################################################################################
# [로그인] 비정상적인 로그인(비밀번호 8자리 이하)
# [로그인] view password 버튼 기능 확인
# [로그인] 로그인 화면 언어 변경 버튼 기능 동작 확인
##########################################################################################
def test_login_short_password(driver):
    
    # 정상 이메일, 8자 이하 비밀번호
    valid_email = LOGIN_ID
    short_password = "1234567"  # 7자 (8자 이하)

    # 로그인 시도, 성공 검증은 하지 않음
    login(driver, valid_email, short_password, check_success=False)
    
     # --- View Password 기능 테스트 ---
    try:
        pw_input = driver.find_element(By.NAME, "password")
        view_btn = driver.find_element(By.XPATH, '//button[@aria-label="View password"]')

        # 초기 상태 확인
        assert pw_input.get_attribute("type") == "password", "초기 비밀번호 타입이 password가 아님"
        assert view_btn.get_attribute("aria-expanded") == "false", "초기 aria-expanded가 false가 아님"

        # 클릭 → 타입 변경 + aria-expanded
        view_btn.click()
        time.sleep(0.5)
        assert pw_input.get_attribute("type") == "text", "Eye 클릭 후 타입이 text가 아님"
        assert view_btn.get_attribute("aria-expanded") == "true", "Eye 클릭 후 aria-expanded가 true가 아님"

        # 다시 클릭 → 타입 원복 + aria-expanded
        view_btn.click()
        time.sleep(0.5)
        assert pw_input.get_attribute("type") == "password", "Eye 다시 클릭 후 타입이 password로 돌아오지 않음"
        assert view_btn.get_attribute("aria-expanded") == "false", "Eye 다시 클릭 후 aria-expanded가 false로 돌아오지 않음"

        logging.info("View Password 기능 테스트 완료!")
        print("View Password 기능 테스트 완료!")
    except Exception as e:
        assert False, f"[로그인] 비정상적인 로그인(비밀번호 8자리 이하) & view password 버튼 기능 확인 실패: {e}"

    # 비밀번호 짧음으로 인한 로그인 실패 메시지 확인
    try:
        error_msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//p[contains(text(), "Please enter a password of at least 8 digits.")]')                
            )
        )
        if "Please enter a password of at least 8 digits." in error_msg.text:
            logging.info(f"✅ [SUCCESS] [로그인] 비정상적인 로그인(비밀번호 8자리 이하) + [로그인] view password 버튼 기능 확인")        
            print(f"✅ [SUCCESS] [로그인] 비정상적인 로그인(비밀번호 8자리 이하) + [로그인] view password 버튼 기능 확인")        
        assert "Please enter a password of at least 8 digits." in error_msg.text, f"예상 오류 메시지와 다름. 실제 메시지: '{error_msg.text}'"
    except:
        assert False, f"❌ [FAIL] 로그인 실패 시 예상된 오류 메시지를 찾지 못함"

    
    
##########################################################################################   
# [로그인] 비정상적인 로그인(잘못된 비밀번호) (AHCT-T5)
##########################################################################################
def test_login_wrong_password(driver):
    
    # 정상 이메일, 8자 이하 비밀번호
    valid_email = LOGIN_ID
    short_password = "wrongpassword"  #잘못된 비밀번호

    # 로그인 시도, 성공 검증은 하지 않음
    login(driver, valid_email, short_password, check_success=False)

    # 비밀번호 틀림으로 인한 로그인 실패 메시지 확인
    try:
        error_msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//p[contains(text(), "Email or password does not match")]')                
            )
        )
        if "Email or password does not match" in error_msg.text:
            logging.info(f"✅ [SUCCESS] [로그인] 비정상적인 로그인(잘못된 비밀번호)")        
            print(f"✅ [SUCCESS] [로그인] 비정상적인 로그인(잘못된 비밀번호)")        
        assert "Email or password does not match" in error_msg.text, f"예상 오류 메시지와 다름. 실제 메시지: '{error_msg.text}'"
    except:
        assert False, f"❌ [FAIL] 로그인 실패 시 예상된 오류 메시지를 찾지 못함"

    


##########################################################################################   
# [로그인] 로그인 화면 언어 변경 버튼 기능 동작 확인 (AHCT-T167)
##########################################################################################
def test_login_change_languages(driver):
    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    
    expected_texts = {
        "en-US": "Login",
        "ko-KR": "로그인",
        "th-TH": "เข้าสู่ระบบ",
        "ja-JP": "ログイン"
    }
    
    select_elem = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'select[aria-label="Change Languages"]'))
    )
    select = Select(select_elem)
    failed_languages = []
    
    for option in select.options:
        value = option.get_attribute("value")
        print(f"언어 선택 중: {option.text} ({value})")
        
        # 옵션 선택
        select.select_by_value(value)
        time.sleep(0.5)  # 필요 시 JS 렌더링 대기
        
        try:
            # h2 요소가 나타날 때까지 최대 10초 대기
            h2_elem = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'h2.MuiTypography-h5'))
            )
            actual_text = h2_elem.text

            # 텍스트 비교 후 출력
            if actual_text == expected_texts[value]:
                print(f"{value}: h2 텍스트 일치 ({actual_text})", flush=True)
            else:
                print(f"[로그인] 로그인 화면 언어 변경 버튼 기능 동작 확인", flush=True)
                failed_languages.append(value)
          
        except Exception as e:
            logging.info(f"{value}: h2 요소 확인 실패 ({e})")
            print(f"{value}: h2 요소 확인 실패 ({e})", flush=True)
            failed_languages.append(value)
    if not failed_languages:
        logging.info(f"✅ [SUCCESS] 로그인] 로그인 화면 언어 변경 버튼 기능 동작 확인")  
        print(f"✅ [SUCCESS] 로그인] 로그인 화면 언어 변경 버튼 기능 동작 확인")  
    assert not failed_languages, f"❌ [FAIL] [로그인] 로그인 화면 언어 변경 버튼 기능 동작 확인"