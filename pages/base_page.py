'''
작성자 : 신윤아
'''

import time, platform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _resolve(self, locator_or_key):
        # key(string) → locator dict
        if isinstance(locator_or_key, str):
            return self.locators[locator_or_key]
        # 기존 방식 그대로
        return locator_or_key

    def find(self, locator_or_key):
        locator = self._resolve(locator_or_key)
        return self.driver.find_element(*locator)

    def finds(self, locator_or_key):
        locator = self._resolve(locator_or_key)
        return self.driver.find_elements(*locator)

    def wait_visible(self, locator_or_key):
        locator = self._resolve(locator_or_key)
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator_or_key):
        locator = self._resolve(locator_or_key)
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_invisible(self, locator_or_key):
        locator = self._resolve(locator_or_key)
        return self.wait.until(EC.invisibility_of_element_located(locator))
    
    def wait_until_enabled(self, key):
        self.wait.until(
            lambda d: self.find(key).get_attribute("aria-disabled") != "true"
        )

    def wait_until_not_loading(self, key):
        self.wait.until(
            lambda d: "MuiLoadingButton-loading" not in self.find(key).get_attribute("class")
        )

    def wait_until_result(self, locator_or_key, timeout=90):
        locator = self._resolve(locator_or_key)
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    
    # 입력된 텍스트 지우기
    def clear_all(self, element):
        # element.send_keys(Keys.CONTROL, 'a')
        # element.send_keys(Keys.DELETE)

        system = platform.system()
        if system == "Darwin":  # macOS
            element.send_keys(Keys.COMMAND, 'a')
        else:  # Windows 
            element.send_keys(Keys.CONTROL, 'a')

        element.send_keys(Keys.DELETE)


    #드롭박스 옵션 선택
    def verify_mui_select_options(driver, select_id):
        wait = WebDriverWait(driver, 10)

        select_box = driver.find_element(By.ID, select_id)
        select_box.click()

        wait.until(EC.visibility_of_element_located((By.XPATH, "//ul[@role='listbox']")))
        options = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//li[@role='option']")))

        option_texts = [opt.text for opt in options]
        print("옵션 목록:", option_texts)

        # 하나 선택해서 초기화
        options[0].click()

        for text in option_texts:
            select_box = driver.find_element(By.ID, select_id)  # 🔥 다시 찾기
            select_box.click()

            option = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//li[@role='option' and normalize-space(text())='{text}']")
                )
            )
            option.click()

            selected_value = select_box.text
            print(f"선택된 값: {selected_value}")

            assert selected_value == text, (
                f"선택값 불일치 : 기대값={text}, 실제값={selected_value}"
            )
    #드롭다운 박스 고르기
    def select_dropdown_by_name(self,input_name, option_text):
        combobox = self.driver.find_element(By.CSS_SELECTOR,"div[role='combobox]")
        combobox.click()
        option = WebDriverWait(self.driver,10).until(
            EC.element_to_be_clickable(
                By.XPATH,f"//li[@role='option' and normalize-space(text())='{option_text}']"))
        option.click()
        value = self.driver.find_element(By.NAME, input_name).get_attribute("value")
        assert value != "", f"{input_name} 값이 설정되지 않음"
    
    #드롭박스 옵션 가져오기    
    def select_option_get_value(self, input_key,option_text):
        self.open_dropdown_safely(input_key)
        option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,f"//li[@role='option' and normalize-space(text())='{option_text}']")
            )
        )
        option.click()
        return self.find(input_key).get_attribute("valie")
    
        # -------------------------------------
    # 드롭박스 옵션 선택 + 반환 
    # -------------------------------------
    def select_option_get_value(self, input_key,option_text):
        self.open_dropdown_safely(input_key)
        option = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,f"//li[@role='option' and normalize-space(text())='{option_text}']")
            )
        )
        option.click()
        return self.find(input_key).get_attribute("valie")
    
    def open_dropdown_safely(self, dropbox_key):
        combobox = self.find(dropbox_key)

        expanded = combobox.get_attribute("aria-expanded")

        if expanded != "true":
            combobox.click()
            time.sleep(0.3)  
    
    # -------------------------------------
    # 드롭박스 옵션 목록 가져오기 
    # -------------------------------------
    def get_dropdown_option(self,combobox_key):
        self.open_dropdown_safely(combobox_key)
        
        options = self.finds("LIST_OPTIONS")
        return [opt.text.strip() for opt in options if opt.text.strip()]

    
    def get_selected_text(self):
        combobox = self.find("DROPBOXES")
        return combobox.text.strip()
    
    # -------------------------------------
    # 새창 열기 + 닫기
    # -------------------------------------
    def switch_new_window(self):
        main = self.driver.current_window_handle
        WebDriverWait(self.driver,10).until(
            lambda d : len(d.window_handles) > 1
        )
        for w in self.driver.window_handles:
            if w != main:
                self.driver.switch_to.window(w)
                return main
    
    def close_and_back(self,main_window):
        self.driver.close()
        self.driver.switch_to.window(main_window)