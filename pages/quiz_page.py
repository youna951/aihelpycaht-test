'''
작성자 : 신윤아
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class QuizPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
    
    # -------------------------------------
    # Locators
    # -------------------------------------
    TOOL_MENU = (By.XPATH, "//span[contains(text(),'도구')]")
    QUIZ_MENU = (By.XPATH, "//*[contains(text(),'퀴즈 생성')]")
    