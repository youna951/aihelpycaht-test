import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# utils import
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.common import login
from utils.constants import LOGIN_ID, LOGIN_PW
from datetime import datetime
import logging

# 로그 포맷과 레벨 설정
logging.basicConfig(
    level=logging.INFO,  # INFO 이상 로그 출력
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

#########################################
# 기본 WebDriver Fixture
# 독립 브라우저, 로그인 필요 없음 → driver
#########################################
@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    #chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1440,1280")
    chrome_options.add_argument("--window-position=0,0")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)

    yield driver
    driver.quit()

########################################################################
# 브라우저 공유, 로그인 필요 없음 → driver_session
########################################################################
@pytest.fixture(scope="module")
def driver_session():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--window-size=1440,1280")
    chrome_options.add_argument("--window-position=0,0")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)

    yield driver
    driver.quit()


########################################################################
# 로그인 (pytest 전체 세션에서 1회만 실행)
# 브라우저 공유 + 로그인 필요 → login_once
########################################################################
@pytest.fixture(scope="module")
def login_once(driver_session):
    login(driver_session, LOGIN_ID, LOGIN_PW, check_success=True)    
    return driver_session

# #########################################
# # 로그인된 상태가 필요한 테스트를 위한 Fixture
# #########################################
@pytest.fixture
def logged_in_driver(driver):
    """로그인이 필요한 테스트용 Fixture"""
    login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    time.sleep(1)
    return driver

# #########################################
# # 다운로드를 위한 Fixture
# #########################################
@pytest.fixture(scope="module")
def login_once_with_download():
    # 🔹 프로젝트 루트 계산
    project_root = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(project_root)

    download_dir = os.path.join(
        project_root,
        "files",
        "school_record"
    )
    os.makedirs(download_dir, exist_ok=True)
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--window-size=1440,1280")
    chrome_options.add_argument("--window-position=0,0")
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5)
    login(driver, LOGIN_ID, LOGIN_PW, check_success=True)
    time.sleep(1)

    yield driver
    driver.quit()
    
    
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # 테스트 실행(call) 단계에서 실패했을 때만
    if report.when == "call" and report.failed:

        driver = None

        # 🔹 현재 테스트에서 사용 중인 fixture들 중 WebDriver 찾기
        for fixture_name in [
            "login_once",
            "logged_in_driver",
            "driver",
            "driver_session",
            "login_once_with_download",
        ]:
            driver = item.funcargs.get(fixture_name)
            if driver:
                break

        if driver is None:
            return  # WebDriver 못 찾으면 캡처 안 함

        # 🔹 스크린샷 저장 폴더
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = item.name

        file_path = os.path.join(
            screenshots_dir,
            f"{test_name}_{timestamp}.png"
        )

        driver.save_screenshot(file_path)

        print(f"\n📸 Screenshot saved: {file_path}")