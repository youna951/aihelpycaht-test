import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


def login(driver, login_id, login_pw, check_success=True):
    """로그인 처리 공통 함수"""

    driver.get("https://qaproject.elice.io/ai-helpy-chat")
    time.sleep(1)

    # ID 입력
    el_login_id = driver.find_element(By.NAME, "loginId")
    el_login_id.send_keys(login_id)

    # PW 입력
    el_login_pw = driver.find_element(By.NAME, "password")
    el_login_pw.send_keys(login_pw)

    # 로그인 버튼 클릭
    driver.find_element(By.ID, ":r3:").click()

    # 로그인 성공 검증
    if check_success:
        try:
            textarea = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//textarea[@name="input"]')
                )
            )
            assert textarea.is_displayed(), "로그인 후 textarea가 표시되지 않음"
            print("로그인 성공!")
        except NoSuchElementException:
            assert False, "로그인 실패: textarea 요소 없음"


def logout(driver):
    """로그아웃 처리 공통 함수"""

    # 메뉴 버튼 클릭
    driver.find_element(
        By.XPATH, '//*[@data-testid="PersonIcon"]/ancestor::button'
    ).click()
    time.sleep(1)

    # 로그아웃 버튼 클릭
    driver.find_element(
        By.XPATH, '//p[contains(text(), "로그아웃")]'
    ).click()
    time.sleep(1)

    # 로그아웃 성공 검증
    try:
        pw_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
        assert pw_input.is_displayed(), "로그아웃 후 password 입력창 미표시"
        print("로그아웃 성공!")
    except NoSuchElementException:
        assert False, "로그아웃 실패: password 요소가 없음"
        
        
#util_clearall 값 모두 삭제
def clear_all(element):
    element.click()
    element.send_keys(Keys.CONTROL, "a")
    element.send_keys(Keys.DELETE)
    
#
def wait_visible(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )

def wait_clickable(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )

def wait_invisible(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.invisibility_of_element_located(locator)
    )
    
