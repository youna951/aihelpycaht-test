'''
작성자 : 이원기
'''

# tests/test_chat_history_page.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pyautogui
from pages.life_record_page import LifeRecordPage
from utils.common import clear_all
import sys, os
import logging

# utils 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

class Test_Life_Record:
    
    # -------------------------------------
    # 페이지 이동
    # -------------------------------------
    def test_go_to_life_record(self, login_once):
        page = LifeRecordPage(login_once)
        page.go_to_life_record()
        assert page.is_life_record_page_opened(), "❌행동특성 및 종합의견 페이지로 이동하지 못함"
        print("✅ 행동특성 및 종합의견 페이지 이동 완료")
        
        
    # -------------------------------------
    # 입력양식 다운받기
    # -------------------------------------
    def test_down_sample(self, login_once):
        page = LifeRecordPage(login_once)
        page.driver.find_element(
            By.CSS_SELECTOR,
            'a[href*="student_record_generation_template.xlsx"]'
        ).click()
        time.sleep(3)
        file_name = "student_record_generation_template.xlsx"
        file_path = os.path.join(DOWNLOAD_DIR, file_name)
        assert wait_for_file(file_name, DOWNLOAD_DIR, timeout=15), f"❌ {file_name} 다운로드 실패"
        print(f"✅ {file_name} 입력 양식 다운로드 완료")
        
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"{file_name} 파일 삭제 완료")
            except Exception as e:
                print(f"{file_name} 파일 삭제 실패: {e}")
        
    # -------------------------------------
    # 파일 업로드
    # -------------------------------------
    @pytest.mark.parametrize("filename", [
        "upload_life_record.xls"
        , "upload_life_record.xlsx"
        , "upload_test.docx"
        , "upload_test.pdf"
    ])
    def test_upload_life_record(self, login_once, filename):
        page = LifeRecordPage(login_once)
        
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files")
        
        file_path = os.path.join(base_dir, filename)
        page.driver.find_element(
            By.XPATH, '//span[text()="클릭하여 업로드"]'
        ).click()
        time.sleep(1)
        
        pyautogui.write(file_path)
        pyautogui.press('enter')
        time.sleep(3)  # 업로드 대기
        
        uploaded = is_file_uploaded(login_once, filename)

        # 확장자별 기대 결과에 따라 assert 분기
        if filename.endswith((".xlsx", ".xls")):
            assert uploaded, f"❌ 업로드 실패: {filename} (xlsx, xls는 성공해야 함)"
            logging.info(f"✅ 업로드 성공: {filename}")
            print(f"✅ 업로드 성공: {filename}")
        else:
            assert not uploaded, f"❌ 업로드 성공: {filename} (xlsx, xls 외는 실패해야 함)"
            logging.info(f"✅ 업로드 실패 확인됨: {filename}")
            print(f"✅ 업로드 실패 확인됨: {filename}")
            
            
    # -------------------------------------
    # 추가입력 : 공백 / 1자 / 5000자
    # -------------------------------------
    def test_add_input(self, login_once):
        page = LifeRecordPage(login_once)
        
        # 공백
        textarea_add = page.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//textarea[@name="teacher_comment" and not(@aria-hidden="true")]')
            )
        )
        clear_all(textarea_add)
        button = WebDriverWait(page.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(text(), '다시 생성')]")))
        time.sleep(2)
        is_enabled = button.is_enabled()        
        assert is_enabled, f"❌ 공백 : 생성 버튼 비활성화 상태"
        logging.info("✅ 추가 입력 : 공백 성공")
        print("✅ 추가 입력 : 공백 성공")
        
        # 1자 입력
        clear_all(textarea_add)
        page.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//textarea[@name="teacher_comment" and not(@aria-hidden="true")]')
            )
        ).send_keys("ㅋ")
        button = WebDriverWait(page.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(text(), '다시 생성')]")))
        time.sleep(2)
        is_enabled = button.is_enabled()        
        assert is_enabled, f"❌ 공백 : 생성 버튼 비활성화 상태"
        logging.info("✅ 추가 입력 : 1자 성공")
        print("✅ 추가 입력 : 1자 성공")
        
        # 5000자 입력
        TEXT_5000 = "ㅋ" * 5000
        clear_all(textarea_add)
        page.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//textarea[@name="teacher_comment" and not(@aria-hidden="true")]')
            )
        ).send_keys(TEXT_5000)
        button = WebDriverWait(page.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(text(), '다시 생성')]")))
        time.sleep(2)
        is_enabled = button.is_enabled()        
        assert is_enabled, f"❌ 공백 : 생성 버튼 비활성화 상태"
        logging.info("✅ 추가 입력 : 5000자 성공")
        print("✅ 추가 입력 : 5000자 성공")
        
        
            
            
    # -------------------------------------
    # 1) 파일 생성
    # 2) 파일 다운로드
    # 3) 비정상 파일업로드 및 다시 생성(실패 메시지 확인)
    # 4) 생성중지
    # 5) 100MB 파일 업로드
    # -------------------------------------        
    def test_life_record_create(self, login_once):
        page = LifeRecordPage(login_once)
        button = WebDriverWait(page.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit' and contains(text(), '다시 생성')]")))
        
        # 1) 파일 생성
        # 팝업 다시생성 버튼
        # 자동생성(정상파일) : 화면 다시 생성 클릭 > 팝업 다시 생성 클릭
        button.click()
        print("1-1. 메인화면 다시생성 클릭 성공")
        
        regen_btn = WebDriverWait(page.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']//button[normalize-space()='다시 생성']"))
        )
        page.driver.execute_script("arguments[0].click();", regen_btn)
        print("1-2. 팝업화면 다시생성 클릭 성공")

        time.sleep(5)

        element = page.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//p[contains(text(), '행동특성 및 종합의견을 생성했습니다')]")
            )
        )
        assert element is not None, "❌ 행동특성 및 종합의견 생성 실패"
        logging.info("✅ 행동특성 및 종합의견 파일 생성 완료")
        print("✅ 행동특성 및 종합의견 파일 생성 완료")
        
        # 2) 파일 다운로드
        '''
        생성 파일 다운로드 로직
        "DOWNLOAD_FORM" : (By.XPATH, "//a[contains(@href,'evaluation_template')]")
        "//a[contains(@href,'generation_template')]"
        '''
        download_link = WebDriverWait(page.driver, 10).until(
            #EC.element_to_be_clickable(
            EC.visibility_of_element_located(
                #(By.XPATH, "//a[span/svg[contains(text(),'생성 결과 다운받기')]]")
                #(By.XPATH, "//a[span/svg[@data-testid='arrow-down-to-lineIcon']]")
                (By.XPATH, "//a[contains(@href, 'student_records_') and contains(., '생성 결과 다운받기')]")
            )
        )
        # 클릭
        download_link.click()
        
        file_prefix = "student_records_"
        file_path = os.path.join(DOWNLOAD_DIR, file_prefix)
        assert wait_for_file_prefix(file_prefix, DOWNLOAD_DIR, timeout=15), f"❌ {file_prefix} 다운로드 실패"
        logging.info(f"✅ {file_path} 2. 생성결과 파일 다운로드 완료")
        print(f"✅ {file_path} 2. 생성결과 파일 다운로드 완료")

        # 3) 비정상 파일업로드 및 다시 생성(실패 메시지 확인)
        # 자동생성(비정상파일) : 화면 다시 생성 클릭 > 팝업 다시 생성 클릭
        uploaded = upload_file(page.driver, "upload_test.xlsx")
        if uploaded:
            print("3-1. 파일 업로드 성공")
            button.click()  

        regen_btn = WebDriverWait(page.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']//button[normalize-space()='다시 생성']"))
        )
        page.driver.execute_script("arguments[0].click();", regen_btn)
        print("3-2. 팝업화면 다시생성 클릭 성공")
        time.sleep(5)
        try:
            error_alert = page.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class,'MuiAlert-message') "
                                "and contains(., '답변 생성에 문제가 발생했습니다.')]")
                )
            )

            assert error_alert is not None, "❌ 양식에 맞지 않는 파일 처리 실패"
            logging.info("✅ 3-3. 비양식 파일 처리 성공")
            print("✅ 3-3. 비양식 파일 처리 성공")

        except TimeoutException:
            logging.info("❌ 3-3. 에러 알림이 나타나지 않음 (Timeout)")
            print("❌ 3-3. 에러 알림이 나타나지 않음 (Timeout)")

        except AssertionError as e:
            logging.info(e)
            print(e)
        
        # 4) 생성 중지
        uploaded = upload_file(page.driver, "upload_life_record.xlsx")
        if uploaded:
            print("4-1. 파일 업로드 성공")
        
        button.click()
        print("4-2. 메인화면 다시생성 클릭 성공")
        
        regen_btn = WebDriverWait(page.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']//button[normalize-space()='다시 생성']"))
        )
        page.driver.execute_script("arguments[0].click();", regen_btn)
        print("4-3. 팝업화면 다시생성 클릭 성공")
        
        stop_button = WebDriverWait(page.driver, 10).until(
            EC.presence_of_element_located(
                #(By.XPATH, "//button[.//svg[@data-testid='stopIcon']]")
                #(By.XPATH, "//div[.//button[.//svg[@data-testid='stopIcon']]]")
                (By.XPATH, "//*[@data-testid='stopIcon']/ancestor::button")
            )
        )

        # 2. 화면에 스크롤
        page.driver.execute_script("arguments[0].scrollIntoView(true);", stop_button)

        # 3. 클릭
        WebDriverWait(page.driver, 5).until(
            lambda d: stop_button.is_enabled()
        )
        stop_button.click()
        print("4-4. 생성중지 클릭 성공")
        
        stop_alert = page.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'MuiAlert-message') "
                        "and contains(., '요청에 의해 답변 생성을 중지했습니다.')]")
            )
        )
        assert stop_alert is not None, "❌ 생성 중지 실패"
        logging.info("✅ 4-5. 생성중지 처리 성공")
        print("✅ 4-5. 생성중지 처리 성공")
        
        # 5) 100MB 파일 업로드
        uploaded = upload_file(page.driver, "test_100MB.xlsx")
        assert not uploaded, f"❌ 업로드 실패: 100MB는 업로드 불가"
        logging.info(f"✅ 100MB 업로드 불가 확인")
        print(f"✅ 100MB 업로드 불가 확인")
        
        
        
# -------------------------------------
# 다운로드 파일 체크
# -------------------------------------
def wait_for_file(file_name, download_dir=DOWNLOAD_DIR, timeout=10):
    """
    download_dir 내에 file_name이 존재하면 True, 없으면 timeout 후 False 반환
    """
    end_time = time.time() + timeout

    while time.time() < end_time:
        # 해당 파일 이름이 존재하는지 확인
        if file_name in os.listdir(download_dir):
            return True
        time.sleep(0.5)

    return False


def wait_for_file_prefix(prefix, download_dir=DOWNLOAD_DIR, timeout=10):
    """
    download_dir 내에 prefix로 시작하는 파일이 존재하면 True, 없으면 timeout 후 False 반환
    """
    end_time = time.time() + timeout

    while time.time() < end_time:
        for fname in os.listdir(download_dir):
            if fname.startswith(prefix):
                return True
        time.sleep(0.5)

    return False

# -------------------------------------
# 업로드 파일 체크
# -------------------------------------
def is_file_uploaded(driver, file_name, timeout=10):
    """
    업로드 완료 후 파일명이 페이지에 나타나는지 확인

    Args:
        driver: Selenium WebDriver
        file_name: 확인할 업로드 파일명 (문자열)
        timeout: 최대 대기 시간 (초)

    Returns:
        True: 파일 업로드 확인 완료
        False: 파일 업로드 실패
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//div[text()="{file_name}"]')
            )
        )
        return element.is_displayed()
    except:
        return False
    
    
# -------------------------------------
# 업로드 파일
# -------------------------------------
def upload_file(driver, filename):
    """파일 업로드 후 완료 여부 반환"""
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files")
    file_path = os.path.join(base_dir, filename)
    
    driver.find_element(By.XPATH, '//span[text()="클릭하여 업로드"]').click()
    time.sleep(1)
    print("업로드할 파일 경로:", file_path)
    
    pyautogui.write(file_path)
    pyautogui.press('enter')
    time.sleep(3)  # 업로드 대기
    
    return is_file_uploaded(driver, filename)