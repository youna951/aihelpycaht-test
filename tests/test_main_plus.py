'''
작성자 : 이원기
'''

import pytest
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os

# utils 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.common import login, logout
from utils.constants import LOGIN_ID, LOGIN_PW
import logging

# ---------------------------------------------------------------------------------
# 메시지 입력 창 좌측 "+" 버튼 클릭 기능 테스트
# 
# ---------------------------------------------------------------------------------

##########################################################################################
# [채팅 고급기능] 파일업로드 (???) - 취소
##########################################################################################
def test_plus_fileUpload_cancel(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 30)

    # 새로고침
    driver.refresh()
    time.sleep(1)

    # ---------------------------
    # 플러스 버튼 클릭 (업로드 메뉴 열기)
    # ---------------------------
    plus_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button:has(svg[data-testid="plusIcon"])'))
    )
    plus_button.click()
    time.sleep(1)

    # ---------------------------
    # 파일 업로드 메뉴 클릭
    # ---------------------------
    upload_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//span[text()="파일 업로드"]'))
    )
    upload_button.click()
    time.sleep(1)

    # ---------------------------
    # 업로드할 파일 경로 준비
    # ---------------------------
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files")
    file_name = "upload_test.txt"
    file_path = os.path.join(base_dir, file_name)

    # ---------------------------
    # <input type="file">를 통해 파일 업로드
    # ---------------------------
    file_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
    )
    file_input.send_keys(file_path)

    # ---------------------------
    # 업로드 완료 확인
    # ---------------------------
    uploaded_file_span = wait.until(
        EC.visibility_of_element_located((By.XPATH, f'//span[text()="{file_name}"]'))
    )
    time.sleep(3)
    # ---------------------------
    # xmark 버튼 클릭 (업로드 취소)
    # ---------------------------
    uploaded_file_row = uploaded_file_span.find_element(By.XPATH, './ancestor::div[contains(@class,"css-huylf3")]')
    xmark_button = WebDriverWait(uploaded_file_row, 10).until(
        EC.element_to_be_clickable(
            #(By.XPATH, './/button[.//svg[@data-testid="xmarkIcon"]]')
            #(By.XPATH, '//*[@data-testid="xmarkIcon/ancestor::button"]')
            (By.XPATH, "//*[@data-testid='xmarkIcon']/ancestor::button")
        )
    )
    xmark_button.click()
    time.sleep(3)

    # 삭제 완료 확인
    wait.until(EC.staleness_of(uploaded_file_span))
    assert wait.until(EC.staleness_of(uploaded_file_span)), "❌ 파일 업로드 취소 후 요소가 제거되지 않음"
    logging.info("파일 업로드 + 취소 정상 완료 ✅")
    print("파일 업로드 + 취소 정상 완료 ✅")
    
    
    
##########################################################################################
# [채팅 고급기능] 파일업로드 (AHCT-T7)
##########################################################################################
def test_plus_fileUpload(logged_in_driver):
    # 로그인
    #login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    driver = logged_in_driver    
    wait = WebDriverWait(driver, 100)
    driver.refresh()

    # ---------------------------
    # 플러스 버튼 클릭 (업로드 메뉴 열기)
    # ---------------------------
    plus_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button:has(svg[data-testid="plusIcon"])')
        )
    )
    plus_button.click()
    time.sleep(1)

    # ---------------------------
    # 파일 업로드 버튼 클릭
    # ---------------------------
    upload_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[text()="파일 업로드"]')
        )
    )
    upload_button.click()
    time.sleep(2)  # 파일 선택창 대기

    # ---------------------------
    # 업로드할 파일 경로 생성
    # ---------------------------
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files")
    filenames = [
        "upload_test.txt",
        "upload_test.docx",
        "upload_test.pdf",
        "upload_test.png",
        "upload_test.jpg"
    ]

    # 파일 경로 → OS 파일선택창에서 여러 파일 선택 형식:  "경로1" "경로2" ...
    file_paths_string = ' '.join(
        f'"{os.path.join(base_dir, name)}"' for name in filenames
    )

    # ---------------------------
    # 파일 선택창에 여러 파일 경로 입력
    # ---------------------------
    pyautogui.write(file_paths_string)
    pyautogui.press('enter')
    time.sleep(3)  # 업로드 대기

    # ---------------------------
    # 각 파일 업로드 완료 확인
    # ---------------------------
    text_files = ["upload_test.txt", "upload_test.docx", "upload_test.pdf"]
    image_files = ["upload_test.png", "upload_test.jpg"]

    # 텍스트 계열 파일 확인 (span)
    for name in text_files:
        uploaded_file = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//span[text()="{name}"]')
            )
        )
        #assert uploaded_file.is_displayed(), f"{name} 텍스트 파일 업로드 실패!"

    # 이미지 계열 파일 확인 (img alt)
    for name in image_files:
        uploaded_img = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//img[@alt="{name}"]')
            )
        )
        #assert uploaded_img.is_displayed(), f"{name} 이미지 파일 업로드 실패!"
    
    driver.find_element(By.XPATH,"//textarea[@name='input']").send_keys("파일 업로드 테스트")
    
    #data-testid arrow-upIcon
    arrow = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button:has(svg[data-testid="arrow-upIcon"])')
        )
    )
    arrow.click()
    
    complete_element = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//div[@data-status="complete"]')
        )
    )

    assert complete_element.is_displayed(), "업로드 완료 상태(data-status=complete)가 확인되지 않음"
        
    logging.info("[채팅 고급기능] 파일업로드 완료!")
    print("[채팅 고급기능] 파일업로드 완료!")

    

##########################################################################################
# [채팅 고급기능] 이미지생성(중복건)
##########################################################################################
def __test_plus_image(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 100)
    driver.refresh()
    # ---------------------------
    # 플러스 버튼 클릭 (업로드 메뉴 열기)
    # ---------------------------
    plus_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button:has(svg[data-testid="plusIcon"])')
        )
    )
    plus_button.click()
    time.sleep(1)

    # ---------------------------
    # 이미지 생성 버튼 클릭
    # ---------------------------
    upload_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[text()="이미지 생성"]')
        )
    )
    upload_button.click()
    time.sleep(2)    

    image_generate_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[text()="이미지 생성"]')
        )
    )
    #assert image_generate_button.is_displayed(), "이미지 생성 클릭 실패!"
    
    driver.find_element(By.XPATH,"//textarea[@name='input']").send_keys("건방진 치와와 생성해줘")
    
    #data-testid arrow-upIcon
    arrow = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button:has(svg[data-testid="arrow-upIcon"])')
        )
    )
    arrow.click()
    
    complete_element = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//div[@data-status="complete"]')
        )
    )
    # complete_element 안에 img 태그가 존재하는지 확인
    try:
        img_inside = wait.until(
            EC.visibility_of(complete_element.find_element(By.XPATH, ".//img"))
        )
        assert img_inside.is_displayed(), "<img> 태그가 표시되지 않음"
        print("<img> 태그 존재 확인 ✔️")
    except Exception as e:
        raise AssertionError(e)

    logging.info("[채팅 고급기능] 이미지생성 완료!")
    print("[채팅 고급기능] 이미지생성 완료!")

    
##########################################################################################
# [채팅 고급기능] 웹검색
##########################################################################################
def test_plus_web(logged_in_driver):    
    driver = logged_in_driver
    wait = WebDriverWait(driver, 100)
    driver.refresh()

    # ---------------------------
    # 플러스 버튼 클릭 (업로드 메뉴 열기)
    # ---------------------------
    plus_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button:has(svg[data-testid="plusIcon"])')
        )
    )
    plus_button.click()
    time.sleep(1)

    # ---------------------------
    # 웹검색 버튼 클릭
    # ---------------------------
    upload_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[text()="웹 검색"]')
        )
    )
    upload_button.click()
    time.sleep(2)

    image_generate_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//span[text()="웹 검색"]')
        )
    )
    #assert image_generate_button.is_displayed(), "웹 검색 클릭 실패!"
    
    driver.find_element(By.XPATH,"//textarea[@name='input']").send_keys("치와와 종류 검색해줘")
    
    #data-testid arrow-upIcon
    arrow = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'button:has(svg[data-testid="arrow-upIcon"])')
        )
    )
    arrow.click()
    
    complete_element = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//div[@data-status="complete"]')
        )
    )

    assert complete_element.is_displayed(), "웹검색 정상 동작이 확인되지 않음"
    
    logging.info("[채팅 고급기능] 웹검색 완료!")
    print("[채팅 고급기능] 웹검색 완료!")
        
    
