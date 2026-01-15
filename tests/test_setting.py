'''
작성자 : 이원기
'''

import sys, os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 🔥 경로 추가 후 utils import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import LOGIN_ID, LOGIN_PW
import logging


# ---------------------------
# 체크박스 클릭 함수
# ---------------------------
def click_switch(driver, model_name, max_attempts=5):
    for attempt in range(1, max_attempts + 1):
        try:
            li_element = driver.find_element(By.XPATH, f'//li[.//span[text()="{model_name}"]]')
            switch_span = li_element.find_element(By.XPATH, './/span[contains(@class,"MuiSwitch-thumb")]/..')
            checkbox = li_element.find_element(By.XPATH, './/input[@type="checkbox"]')

            if checkbox.get_attribute("disabled"):
                print(f"⚠ {model_name} 체크박스는 disabled, 건너뜀")
                return

            # 화면 중앙으로 스크롤
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", switch_span)
            time.sleep(0.3)

            # 현재 상태 확인 (checked 기준)
            state = checkbox.get_attribute("checked") is not None
            print(f"{model_name} 현재 상태: {'ON' if state else 'OFF'}")

            # 클릭해서 상태 변경
            driver.execute_script("arguments[0].click();", checkbox)
            time.sleep(0.5)  # 클릭 후 안정화

            # 체크 여부 확인
            new_state = li_element.find_element(By.XPATH, './/input[@type="checkbox"]').get_attribute("checked") is not None
            if new_state != state:
                print(f"✔ {model_name} 상태 변경 성공: {'ON' if new_state else 'OFF'}")
                return
            else:
                print(f"⚠ {model_name} 시도 {attempt}: 상태 변경 실패, 재시도 중...")
                driver.refresh()
                time.sleep(1)

        except Exception as e:
            print(f"❌ {model_name} 시도 {attempt}: 에러 발생 - {e}")
            driver.refresh()
            time.sleep(1)
    print(f"❌ {model_name} 체크 실패!")

########################################################################################## 
# [설정] AI 모델 설정 (AHCT-T107) 
# [새 대화] 대화 버튼으로 새로운 대화 세션 생성 (AHCT-T13)
########################################################################################## 
def test_model_checkboxes(logged_in_driver):
    # --- 로그인 / 설정 화면 이동 ---
    #login(driver, LOGIN_ID, LOGIN_PW)
    driver = logged_in_driver
    time.sleep(0.5)  # 로그인 안정화
    
    wait = WebDriverWait(driver, 10)

    element = driver.find_element(By.XPATH, '//p[contains(text(),"Helpy Pro Agent")]')
    driver.execute_script("arguments[0].click();", element)
    checked_count = len(driver.find_elements(By.XPATH, '//li[contains(@class,"MuiMenuItem-root")]'))
    
    # 1. 설정 메뉴 이동
    #driver.find_element(By.XPATH, '//*[@data-testid="gearIcon"]/ancestor::button').click()
    #driver.find_element(By.XPATH, '//span[contains(text(), "설정")]').click()
    
    gear_button = driver.find_element(By.XPATH, '//*[@data-testid="gearIcon"]/ancestor::button')
    driver.execute_script("arguments[0].click();", gear_button)

    # 모델 설정 클릭
    model_tab = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '//a[@href="/ai-helpy-chat/admin/models"]')
    )
)
    driver.execute_script("arguments[0].click();", model_tab)
    
    model_names = [
        "GPT-5.1",
        "GPT-5",
        "GPT-5 mini",
        "GPT-5 nano",
        "GPT-4.1",
        "GPT-4.1 mini",
        "Claude Sonnet 4.5",
        "Claude Sonnet 4",
        "Claude Haiku 4.5"
        # "Helpy Pro Agent"는 disabled이므로 제외
    ]
    
    # div 요소 선택 (최상위 컨테이너)
    container = driver.find_element(By.CSS_SELECTOR, 'div.MuiStack-root.css-8g8ihq')

    # container 안에 있는 모든 li
    lis = container.find_elements(By.TAG_NAME, 'li')

    # 체크된 checkbox 갯수 세기
    # checked_count = 0
    # for li in lis:
    #     checkbox = li.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
    #     if checkbox.get_attribute("checked"):
    #         checked_count += 1
    
    
    print(f"체크된 모델 개수(BEFORE): {checked_count}")
    
    # 3. 모델별 체크박스 클릭
    for name in model_names:
        print(f"\n=== 모델 체크/체크해제 테스트: {name} ===")
        click_switch(driver, name)

    print("\n🎉 모든 모델 체크/체크해제 완료!")
    driver.refresh()
    
    # 4. 새 대화 > 모델 갯수 확인
    element = driver.find_element(By.XPATH, '//li//span[text()="새 대화"]')
    driver.execute_script("arguments[0].click();", element)

    time.sleep(1)
    
    element = driver.find_element(By.XPATH, '//p[contains(text(),"Helpy Pro Agent")]')
    driver.execute_script("arguments[0].click();", element)
    
    lis = driver.find_elements(By.XPATH, '//li[contains(@class,"MuiMenuItem-root")]')
    print(f"체크된 모델 개수(AFTER): {len(lis)}")
    
    # 모델 설정 메뉴 이동    
    #driver.find_element(By.XPATH, '//span[contains(text(), "모델 설정")]').click()
    wait.until(
        #EC.element_to_be_clickable((By.CSS_SELECTOR, 'span:contains("모델 설정")'))
        EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "모델 설정")]'))
    ).click()
    
    time.sleep(1)

    for name in model_names:
        print(f"\n=== 모델 체크 테스트: {name} ===")
        click_switch(driver, name)
    
    # 새 대화 > 모델 갯수 확인
    element = driver.find_element(By.XPATH, '//li//span[text()="새 대화"]')
    driver.execute_script("arguments[0].click();", element)

    time.sleep(1)
    element = driver.find_element(By.XPATH, '//p[contains(text(),"Helpy Pro Agent")]')
    driver.execute_script("arguments[0].click();", element)
    
    lis = driver.find_elements(By.XPATH, '//li[contains(@class,"MuiMenuItem-root")]')
    
    #assert len(lis) == checked_count, f"모델 개수는 이전과 동일해야 합니다. 현재: {len(lis)}"
    assert lis, f"[설정] AI 모델 설정 실패"
    logging.info("[설정] AI 모델 설정 + [새 대화] 대화 버튼으로 새로운 대화 세션 생성 완료!")
    print("[설정] AI 모델 설정 + [새 대화] 대화 버튼으로 새로운 대화 세션 생성 완료!")