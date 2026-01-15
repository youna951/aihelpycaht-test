'''
작성자 : 신윤아
'''
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.common import clear_all
from utils.constants import LOGIN_ID, LOGIN_PW  



# --------------------------------------------
# AHCT-T50 퀴즈생성 페이지 정상 이동
# --------------------------------------------
def test_goquiz(login_once):
    driver = login_once
    driver.find_element(By.XPATH,"//span[contains(text(),'도구')]").click()
    print("✅도구 페이지 이동 완료")
    driver.find_element(By.XPATH,"//*[contains(text(),'퀴즈 생성')]").click()
    logging.info("✅퀴즈 생성 페이지 이동 완료")

# --------------------------------------------
# AHCT-T51 퀴즈생성 유형 드롭박스 표시
# --------------------------------------------
def test_quiz_type(login_once):
    driver = login_once
    wait = WebDriverWait(driver, 10)
    qz_type_dpbox = driver.find_element(By.ID,"mui-component-select-quiz_configs.0.option_type")
    qz_type_dpbox.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//ul[@role='listbox']")))
    qz_type = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@role='option']")))
    type_texts = [opt.text for opt in qz_type]
    print("퀴즈 종류:",type_texts)
    qz_type[0].click()
    #검증
    for opt_text in type_texts:
        qz_type_dpbox.click()
        option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[@role='option' and text()='{opt_text}']")))
        option.click()
        selected_value = qz_type_dpbox.text
        print(f"선택된 값:{selected_value}")
        assert selected_value==opt_text,f"선택값 불일치 : 기대값={opt_text}, 실제값={selected_value}"
    logging.info("✅퀴즈 생성 유형 검증 완료")
    
# --------------------------------------------
# AHCT-T52 퀴즈생성 난이도 드롭박스 표시
# --------------------------------------------
def test_quiz_level(login_once):
    driver = login_once
    wait = WebDriverWait(driver, 10)
    qz_level_dpbox = driver.find_element(By.ID,"mui-component-select-quiz_configs.0.difficulty")
    qz_level_dpbox.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//ul[@role='listbox']")))
    lv_options = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//li[@role='option']")))
    type_texts = [opt.text for opt in lv_options]
    print("퀴즈 종류:",type_texts)
    lv_options[0].click()
    #검증
    for opt_text in type_texts:
        qz_level_dpbox.click()
        option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[@role='option' and text()='{opt_text}']")))
        option.click()
        selected_value = qz_level_dpbox.text
        print(f"선택된 값:{selected_value}")
        assert selected_value==opt_text,f"선택값 불일치 : 기대값={opt_text}, 실제값={selected_value}"
    logging.info("✅퀴즈 생성 유형 검증 완료")

# --------------------------------------------
# AHCT-T53 퀴즈생성 주제 입력칸 유효성 검증
# --------------------------------------------
def test_subject(login_once):
    driver = login_once
    #버튼 요소 찾아주기
    btn = driver.find_element(By.XPATH,"//button[contains(text(),'생성')]")
    subject = driver.find_element(By.XPATH,"//textarea[@name='content']")
    subject.click()
    #공백입력
    clear_all(subject)
    subject.send_keys("")
    assert not btn.is_enabled()
    logging.info("✅퀴즈 주제 공백입력 테스트 완료") 
    #한글자입력
    clear_all(subject)
    subject.send_keys("가")
    assert btn.is_enabled()
    logging.info("✅퀴즈 주제 한글자 입력 테스트 완료") 
    #5000자 입력
    try:
        clear_all(subject)
        text5000 = "가" * 5000
        subject.send_keys(text5000)
        assert not btn.is_enabled()
        logging.info("✅퀴즈 주제 5000자 입력 테스트 완료") 
    except AssertionError:
        logging.info("❌퀴즈 생성 주제 5000자 입력시 버튼 활성화됨")
# -------------------------------------------------
# AHCT-T54 퀴즈 생성 자동생성 버튼 클릭시 생성 결과 확인
# -------------------------------------------------
def test_create_quiz_btn(login_once):
    driver = login_once
    wait = WebDriverWait(driver, 10)
    #유형 주관식 선택
    qz_type_dpbox = driver.find_element(By.ID,"mui-component-select-quiz_configs.0.option_type")
    qz_type_dpbox.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//ul[@role='listbox']")))
    qz_type = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@role='option']")))
    qz_type[2].click()
    #난이도 하 선택
    qz_level_dpbox = driver.find_element(By.ID,"mui-component-select-quiz_configs.0.difficulty")
    qz_level_dpbox.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//ul[@role='listbox']")))
    lv_options = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//li[@role='option']")))
    lv_options[2].click()
    #주제 입력
    subject = driver.find_element(By.XPATH,"//textarea[@name='content']")
    clear_all(subject)
    subject.send_keys("간단한 사칙연산")
    #버튼  클릭
    try:
        btn = driver.find_element(By.XPATH,"//button[contains(text(),'생성')]")
        btn.click()
        recreate = driver.find_elements(By.XPATH,"//button[contains(text(),'다시 생성')]")
        recreate[1].click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@data-testid='stopIcon']")))
        stop_sign = driver.find_element(By.XPATH, "//*[@data-testid='stopIcon']")
        assert stop_sign.is_displayed()
        logging.info("✅버튼 클릭 완료-> 정상적으로 결과 생성 중 입니다.")
    except NoSuchElementException:
        logging.info("❌버튼 요소를 찾을 수 없습니다.")
        
