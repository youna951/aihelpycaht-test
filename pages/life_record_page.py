
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait



class LifeRecordPage(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
        self.wait = WebDriverWait(self.driver, 10)
   
    locators ={
        
        "TOOL_MENU" : (By.XPATH, "//span[contains(text(),'도구')]"),
        "LIFE_MENU" : (By.XPATH, "//*[contains(text(),'행동특성 및 종합의견')]"),
        "TEACHER_COMMENT_TEXTAREA": (By.NAME, "teacher_comment"),
        
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
        
    }
    
    # -------------------------------------
    # 페이지 이동
    # -------------------------------------
    def go_to_life_record(self):
        self.find("TOOL_MENU").click()
        self.find("LIFE_MENU").click()
        
    def is_life_record_page_opened(self): # 페이지 이동확인
        return self.wait_visible("TEACHER_COMMENT_TEXTAREA").is_displayed()
    
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

    
