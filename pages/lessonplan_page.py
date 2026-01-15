'''
작성자 : 신윤아
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait



class LessonPlanPage(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
   
    locators ={
        
        "TOOL_MENU" : (By.XPATH, "//span[contains(text(),'도구')]"),
        "RESEARCH_MENU" : (By.XPATH, "//*[contains(text(),'수업지도안')]"),
        
        "DROPBOXES" :(By.CSS_SELECTOR, "div[role='combobox']"),
        "SCHOOL_DROPBOX" : (By.XPATH, "//input[@name='school_level']/parent::div//div[@role='combobox']"),
        "GRADE_DROPBOX" : (By.XPATH, "//input[@name='school_year']/parent::div//div[@role='combobox']"),
        "SUBJECT_DROPBOX" : (By.XPATH, "//input[@name='subject']/parent::div//div[@role='combobox']"),
        "CLASSTIME_DROPBOX" : (By.XPATH, "//input[@name='total_time']/parent::div//div[@role='combobox']"),
        "ACHIVEMENT_INPUT" : (By.NAME,"achievement_criteria"),
        "FIND_ACHIVEMENTCODE_BTN" : (By.CSS_SELECTOR,"a[href='https://stas.moe.go.kr/']") ,  
        "COMMENT_INPUT" : (By.NAME,"teacher_comment"),
        "LIST_BOX" : (By.XPATH, "//ul[@role='listbox']"),
        "LIST_OPTIONS": (By.XPATH, "//li[@role='option']"),
        "ALERT_MSG" : (By.CSS_SELECTOR, "div.MuiFormHelperText-root.Mui-error"),
        
        "CREATE_BUTTON" : (By.XPATH, "//button[contains(text(),'생성')]"),
        "STOP_BTN"  : (By.XPATH, "//*[@data-testid='stopIcon']/ancestor::button"),
        "STOP_MSG" : (By.XPATH, "//div[contains(text(),'요청에 의해 답변 생성을 중지했습니다.')]"),
        "RECREATE_BTNS" : (By.XPATH, "//div[@role='dialog']//button[normalize-space()='다시 생성']"),
        "RECREATE_DIALOG": (By.XPATH,"//div[@role='dialog' and .//h2[normalize-space()='결과 다시 생성하기']]"),
        "RESULT_OK_TEXT" : (By.XPATH,"//p[contains(text(),'입력하신 내용 기반으로 수업 지도안을 생성했습니다.')]"),
        "RESULT_NO_TEXT" : (By.XPATH,"//p[contains(text(),'수업 지도안을 생성하는데 실패했습니다.')]")
    }
    
    # -------------------------------------
    # 페이지 이동
    # -------------------------------------
    def go_to_lessonplan(self):
        self.find("TOOL_MENU").click()
        self.find("RESEARCH_MENU").click()
        
    def is_plan_page_opened(self): # 페이지 이동확인
        return self.wait_visible("DROPBOXES").is_displayed()
    
    def go_to_KICE(self):
        self.find("FIND_ACHIVEMENTCODE_BTN").click()
        main_window = self.switch_new_window()
        assert "stas.moe.go.kr" in self.driver.current_url
        self.close_and_back(main_window)
    
    #드롭박스가 열려있으면 클릭 x
    def open_dropdown_if_closed(self):
        combobox = self.find("DROPBOXES")
        expanded = combobox.get_attribute("aria-expanded")

        if expanded == "false":
            combobox.click()
            self.wait_visible("LIST_BOX")

    # -------------------------------------
    # 드롭박스 선택기능 
    # -------------------------------------      
    #초등선택
    def select_el(self):
        self.select_option_get_value(
            input_key="SCHOOL_DROPBOX",
            option_text="초등"
        )
    #중등선택
    def select_mid(self):
        self.select_option_get_value(
            input_key="SCHOOL_DROPBOX",
            option_text="중등"
        )
    #고등선택
    def select_high(self):
        self.select_option_get_value(
            input_key="SCHOOL_DROPBOX",
            option_text="고등"
        )
    #1학년 선택
    def select_grade1(self):
        self.select_option_get_value(
            input_key="GRADE_DROPBOX",
            option_text="1학년"
        )
    #국어 선택
    def select_subject(self):
        self.select_option_get_value(
            input_key = "SUBJECT_DROPBOX",
            option_text= "국어"
        )
    #수업시간 선택
    def select_time(self):
        self.select_option_get_value(
            input_key="CLASSTIME_DROPBOX",
            option_text="45분"
        )
    
    # -------------------------------------
    # 입력
    # -------------------------------------      
    def input_achivement(self, text:str): #지시사항 입력
        el = self.find("ACHIVEMENT_INPUT")
        self.clear_all(el)
        el.send_keys(text)
        
    def input_textarea(self, text:str):
        el = self.find("COMMENT_INPUT")
        self.clear_all(el)
        el.send_keys(text)
        self.clear_all(el)
    
    # -------------------------------------
    # 버튼 상태
    # ------------------------------------- 
    def is_create_enabled(self):
        btn = self.find("CREATE_BUTTON")
        disabled = btn.get_attribute("disabled")
        return disabled is None
    
    def click_create_button(self):
        self.wait_until_not_loading("CREATE_BUTTON")
        self.find("CREATE_BUTTON").click()
        
    def click_recreate_button(self):
        self.wait_visible("RECREATE_DIALOG")   
        self.wait_clickable("RECREATE_BTNS")
        self.find("RECREATE_BTNS").click()
        
    def click_stop(self):
        self.wait_until_not_loading("STOP_BTN")
        self.find("STOP_BTN").click()
        
    def get_stop_message(self):
        return self.wait_visible("STOP_MSG").text
    
    def is_stop_enable(self):
        return self.find("STOP_BTN").is_enabled()
    
    #결과확인
    def wait_get_result(self):
        self.wait_until_result("RESULT_OK_TEXT")
        return self.wait_visible("RESULT_OK_TEXT").text
    
