'''
작성자 : 신윤아
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ResearchPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    # -------------------------------------
    # Locators
    # -------------------------------------
    TOOL_MENU = (By.XPATH, "//span[contains(text(),'도구')]")
    RESEARCH_MENU = (By.XPATH, "//*[contains(text(),'심층 조사')]")

    TOPIC_INPUT = (By.NAME, "topic")
    INSTRUCTION_INPUT = (By.NAME, "instructions")

    CREATE_BTN = (By.XPATH, "//button[contains(text(),'생성')]")
    STOP_ICON_BTN = (By.XPATH, "//*[@data-testid='stopIcon']/ancestor::button")
    RECREATE_BTN = (By.XPATH,"//button[contains(@class,'MuiLoadingButton-root') and @type='submit']")
    
    OVERLAY = (By.CSS_SELECTOR, ".MuiBackdrop-root")
    STOP_MSG = (By.XPATH, "//div[contains(text(),'요청에 의해 답변 생성을 중지했습니다.')]")


    
    # -------------------------------------
    # 페이지 이동
    # -------------------------------------
    def go_to_research(self):
        self.find(self.TOOL_MENU).click()
        self.find(self.RESEARCH_MENU).click()

    # -------------------------------------
    # 입력 기능
    # -------------------------------------
    def input_title(self, text: str):
        el = self.find(self.TOPIC_INPUT)
        self.clear_all(el)
        el.send_keys(text)

    def input_instruction(self, text: str):
        el = self.find(self.INSTRUCTION_INPUT)
        self.clear_all(el)
        el.send_keys(text)

    # -------------------------------------
    # 버튼 상태
    # -------------------------------------
    def is_create_enabled(self):
        return self.find(self.CREATE_BTN).is_enabled()

    def wait_button_state(self, expected: bool):
        """버튼 활성/비활성 변화를 기다림"""
        self.wait.until(
            lambda d: d.find_element(*self.CREATE_BTN).is_enabled() == expected
        )

    # -------------------------------------
    # 생성 & 정지 기능
    # -------------------------------------
    def click_create(self):
        btn = self.wait_clickable(self.CREATE_BTN)
        btn.click()

    def wait_overlay_gone(self):
        """생성 후 로딩 오버레이가 없어질 때까지 대기"""
        try:
            self.wait_invisible(self.OVERLAY)
        except:
            pass  # overlay가 없으면 그냥 넘어감

    def click_stop(self):
        stop_btn = self.wait.until(
            EC.presence_of_element_located(self.STOP_ICON_BTN)
    )

        self.driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});", stop_btn
    )
        self.driver.execute_script("arguments[0].click();", stop_btn)

    def get_stop_message(self):
        return self.wait_visible(self.STOP_MSG).text
    
    def recreate_btn_click(self):
        btn = self.wait.until(
            EC.presence_of_element_located(self.RECREATE_BTN)
        )

        self.driver.execute_script(
            "arguments[0].form.requestSubmit();", btn
        )


