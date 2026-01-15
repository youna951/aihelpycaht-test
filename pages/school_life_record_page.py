'''
작성자 : 신윤아
'''
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage



class SchoolLifeRecordPage(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
    locators ={
        
        "TOOL_MENU" : (By.XPATH, "//span[contains(text(),'도구')]"),
        "RECORD_MENU" : (By.XPATH, "//p[contains(text(),'특기사항')]"),
          
        "DROPBOXES" :(By.CSS_SELECTOR, "div[role='combobox']"),
        "LIST_OPTIONS": (By.XPATH,"//li[@role='option']"),
        "SCHOOL_DROPBOX" : (By.XPATH, "//input[@name='level']/preceding-sibling::div[@role='combobox']"),
        "SUBJECT_DROPBOX" : (By.XPATH, "//input[@name='subject']/preceding-sibling::div[@role='combobox']"),
        "DOWNLOAD_FORM" : (By.XPATH, "//a[contains(@href,'evaluation_template')]"),
        "FILE_UPLOAD" : (By.XPATH, "//span[contains(text(),'클릭하여 업로드')]"),
        "FILE_INPUT": (By.XPATH, "//input[@type='file']"),
        "UPLOADED_FILE_NAME": (By.XPATH, "//div[@data-scope='file-upload' and @data-part='item-name']"),
        "FILE_DROP_ZONE": (By.XPATH,  "//div[@data-scope='file-upload' and @data-part='dropzone']"),
        "FIND_ACHIVEMENTCODE_BTN" : (By.CSS_SELECTOR,"a[href='https://stas.moe.go.kr/']") ,
        "COMMENT_INPUT": (By.NAME,"teacher_comment"),
        
        "CREATE_BUTTON" : (By.XPATH, "//button[contains(text(),'생성')]"),
        "STOP_BTN"  : (By.XPATH, "//*[@data-testid='stopIcon']/ancestor::button"),
        "STOP_MSG" : (By.XPATH, "//div[contains(text(),'요청에 의해 답변 생성을 중지했습니다.')]"),
        "RECREATE_BTNS" : (By.XPATH, "//div[@role='dialog']//button[normalize-space()='다시 생성']"),
        "RECREATE_DIALOG": (By.XPATH,"//div[@role='dialog' and .//h2[normalize-space()='결과 다시 생성하기']]"),
        "RESULT_OK_TEXT" : (By.XPATH,"//p[contains(text(),'입력하신 내용 기반으로 세부 특기사항을 생성했습니다.')]"),
        "RESULT_NO_TEXT" : (By.XPATH,"//p[contains(text(),'수업 지도안을 생성하는데 실패했습니다.')]"),
        "DOWNLOAD_RESULT_BTN": (By.XPATH, "//a[normalize-space()='생성 결과 다운받기']"),

     
     }
    
    # -------------------------------------
    # 페이지 이동
    # -------------------------------------
    def go_to_record(self):
        self.find("TOOL_MENU").click()
        self.wait_clickable("RECORD_MENU")
        self.find("RECORD_MENU").click()
        
    def is_record_page_opened(self): # 페이지 이동확인
        return self.wait_visible("DROPBOXES").is_displayed()    
        
    def go_to_KICE(self):
        self.find("FIND_ACHIVEMENTCODE_BTN").click()
        main_window = self.switch_new_window()
        assert "stas.moe.go.kr" in self.driver.current_url
        self.close_and_back(main_window)
    
    def wait_record_page_loaded(self):
        self.wait_clickable("DROPBOXES")

    # -------------------------------------
    # 입력
    # -------------------------------------
    def input_textarea(self, text:str):
        el = self.find("COMMENT_INPUT")
        self.clear_all(el)
        el.send_keys(text)
     
    def result_download(self):
        self.find("DOWNLOAD_RESULT_BTN").click()
        
    # -------------------------------------
    # 파일 다운로드, 첨부
    # -------------------------------------        
    def click_upload(self):
        self.find("FILE_UPLOAD").click()
        
    def click_result_download(self):
        self.find("DOWNLOAD_RESULT_BTN").click()
    
    def download_form_and_wait(self, file_name: str, timeout: int = 10) -> str:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        download_dir = os.path.join(
            project_root,
            "files",
            "school_record"
        )
        os.makedirs(download_dir, exist_ok=True)
        file_path = os.path.join(download_dir, file_name)
        # 기존 파일 삭제
        if os.path.exists(file_path):
            os.remove(file_path)
        self.find("DOWNLOAD_FORM").click()
        for _ in range(timeout):
            if os.path.exists(file_path):
                return file_path
            time.sleep(1)

        raise TimeoutError(f"다운로드 시간 초과: {file_name}")
    
    
    #클릭기준
    def upload_file(self, relative_path: str):
        project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
        abs_path = os.path.join(project_root, relative_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"테스트 파일 없음: {abs_path}")
        file_input = self.find("FILE_INPUT")
        file_input.send_keys(os.path.abspath(abs_path))
    
    def is_file_uploaded(self, file_name: str) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located((
                    By.XPATH,f"//div[@data-part='item-name' and contains(text(),'{file_name}')]"
                ))
            )
            return True
        except:
            return False    

    #파일 첨부
    def upload_file_data(self):
        file_relative_path = "files/school_record/test_data.xlsx"
        self.upload_file(file_relative_path)
        assert self.is_file_uploaded("test_data.xlsx"), "❌ 파일 업로드 실패"
    
    # -------------------------------------
    # 드롭박스 선택
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
      #국어 선택
    def select_subject(self):
        self.select_option_get_value(
            input_key = "SUBJECT_DROPBOX",
            option_text= "국어"
        )
    # -------------------------------------
    # 버튼 상태
    # ------------------------------------- 
    def is_create_enabled(self):
        btn = self.find("CREATE_BUTTON")
        disabled = btn.get_attribute("disabled")
        return disabled is None
    
    def is_result_download_enabled(self):
        btn = self.find("DOWNLOAD_RESULT_BTN")
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
    
    def is_file_uploaded(self, file_name: str, timeout=5) -> bool:
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{file_name}')]")
                if len(elements) > 0:
                    return True
            except:
                pass
            time.sleep(0.5)
        return False