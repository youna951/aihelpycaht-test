"""
created by 심다영
기능 요약(25-12-17 확인 완료)
- 에이전트 생성: 에이전트 만들기 페이지 진입, 이름/소개/규칙/시작대화 입력
- 에이전트 수정: 기존 에이전트 편집 화면에서 정보 수정 및 업데이트
- 공개 범위 설정: 나만 보기 / 기관 내 공유 선택 및 저장
- 미리보기: 설정한 내용 기준 미리보기 확인 및 채팅 입력/전송
- 검증: 입력값 기준 검증, 미리보기 반영 여부 검증
- 알림 확인: 업데이트 완료 토스트 메시지 표시 여부 확인
"""

import os
import time
import sys, os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from pages.agent_locators import LOCATORS


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AgentBuilderPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    
    # 공통 유틸 추가
    def input_with_clear(self, element, text):
        """기존 내용 전체 선택 후 덮어쓰기"""
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(text)

    # =================================================
    # 이동
    # =================================================
        #에이전트 탐색 클릭
    def go_to_agent_search(self):
        agent_search = self.wait.until(
            EC.element_to_be_clickable(LOCATORS["menu_agent_search"])
        )
        agent_search.click()
        # + 만들기 클릭 (만들기 페이지로 이동)
    def click_agent_create_btn(self):
        create_btn = self.wait.until(
            EC.element_to_be_clickable(LOCATORS["agent_builder_create"])
        )
        create_btn.click()
        return self
    
    def click_agent_setting_btn(self):
        # 설정 클릭
        setting_tab = self.wait.until(
            EC.element_to_be_clickable(LOCATORS["agent_builder_settings"])
        )
        setting_tab.click()
        return self

    # =================================================
    # 입력
    # =================================================
        #챗봇 이름
    def input_name(self, text):
        el = self.wait.until(
            EC.visibility_of_element_located(LOCATORS["input_agent_name"])
        )
        self.input_with_clear(el, text)
        return self
        #한줄 소개
    def input_description(self, text):
        el = self.wait.until(
            EC.visibility_of_element_located(LOCATORS["input_agent_description"])
        )
        self.input_with_clear(el, text)
        return self
        #규칙
    def input_rules(self, text):
        el = self.wait.until(
            EC.visibility_of_element_located(LOCATORS["input_agent_rules"])
        )
        self.input_with_clear(el, text)
        return self
        #시작 대화 1~4
    def input_starter(self, index: int, text: str):
        css = f'input[name="conversationStarters.{index}.value"]'
        el = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css))
        )
        self.input_with_clear(el, text)
        return self
    
    #  ===============================================
    # 만들기 > 기능
    # ==============================================
    # 웹 검색 기능 활성화
    def enable_websearch_function(self, timeout=10):
        websearch_checkbox = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(LOCATORS["checkbox_websearch_function"])
        )
        # 체크되어 있지 않으면 클릭하여 활성화
        if not websearch_checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", websearch_checkbox)
        return self
    
    # 웹 검색 기능 비활성화
    def disenable_websearch_function(self, timeout=10):
        websearch_checkbox = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(LOCATORS["checkbox_websearch_function"])
        )
        # 체크되어 있으면 클릭하여 비활성화
        if websearch_checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", websearch_checkbox)
        return self
    
    # 웹 브라우징 기능 활성화
    def enable_webbrowsing_function(self, timeout=10):
        webbrowsing_checkbox = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(LOCATORS["checkbox_webbrowsing_function"])
        )
        # 체크되어 있지 않으면 클릭하여 활성화
        if not webbrowsing_checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", webbrowsing_checkbox)
        return self
    
    # 웹 브라우징 기능 비활성화
    def disable_webbrowsing_function(self, timeout=10):
        webbrowsing_checkbox = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(LOCATORS["checkbox_webbrowsing_function"])
        )
        # 체크되어 있으면 클릭하여 비활성화
        if webbrowsing_checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", webbrowsing_checkbox)
        return self
    
    # 이미지 생성 기능 활성화
    def enable_imagegeneration_function(self, timeout=10):
        imagegeneration_checkbox = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(LOCATORS["checkbox_imagegeneration_function"])
        )
        # 체크되어 있지 않으면 클릭하여 활성화
        if not imagegeneration_checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", imagegeneration_checkbox)
        return self
    
    # 이미지 생성 기능 비활성화
    def disable_imagegeneration_function(self, timeout=10):
        imagegeneration_checkbox = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(LOCATORS["checkbox_imagegeneration_function"])
        )
        # 체크되어 있으면 클릭하여 비활성화
        if imagegeneration_checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", imagegeneration_checkbox)
        return self

    # 코드 실행 및 데이터 분석 기능 활성화
    def enable_codeexecution_function(self, timeout=10):
        codeexecution_checkbox = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(LOCATORS["checkbox_codeexecution_function"])
        )
        # 체크되어 있지 않으면 클릭하여 활성화
        if not codeexecution_checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", codeexecution_checkbox)
        return self
    
    # 코드 실행 및 데이터 분석 기능 비활성화
    def disable_codeexecution_function(self, timeout=10):
        codeexecution_checkbox = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(LOCATORS["checkbox_codeexecution_function"])
        )
        # 체크되어 있으면 클릭하여 비활성화
        if codeexecution_checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", codeexecution_checkbox)
        return self
    
    #  =================================================
    # 파일 업로드
    # =================================================
    def upload_knowledge_files(self, timeout=10):
        
        file_input = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(LOCATORS["input_agent_fileupload"])
        )
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files")
        filenames = [
            "upload_test.txt",
            "upload_test.docx",
            "upload_test.pdf",
            "upload_test.png",
            "upload_test.jpg"
        ]
        
        # 여러 파일은 \n으로 구분해서 전달
        file_paths = '\n'.join(
            os.path.join(base_dir, name) for name in filenames
        )
        file_input.send_keys(file_paths)
        
        return self
    
    # =================================================
    # 만들기 버튼을 눌러서 에이전트 생성하기 -> 범위 설정하기
    # =================================================
    # 만들기 버튼 클릭
    def click_create_btn(self, timeout=10):
        click_create = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(LOCATORS["btn_create"] )
        )
        try:
            click_create.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", click_create)
        return self

    # 업데이트 버튼 클릭
    def click_agent_updated_btn(self, timeout=10):
        updated_btn = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(LOCATORS["btn_update"])
        )
        try:
            updated_btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", updated_btn)
        return self
    # =================================================
    # 공개 범위 설정
    # =================================================
    # 나만 보기
    def scope_private_setting(self):
        private_radio = self.wait.until(
            EC.element_to_be_clickable(LOCATORS["scope_private"]
            )
        )
        private_radio.click()
        return self
        
    # 기관 내 공유
    def scope_organization_setting(self):
        org_radio = self.wait.until(
            EC.element_to_be_clickable((LOCATORS["scope_organization"]) )
        )
        try:
            org_radio.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", org_radio)
        return self
    
    # 공유 범위 설정 후 저장 버튼 클릭
    def click_agent_scope_setting_save_btn(self):
        saved_btn = self.wait.until(
            EC.element_to_be_clickable(
                (LOCATORS["btn_scope_save"])
            )
        )
        saved_btn.click()
        return self
    
    # 범위 설정 확인
    # 나만 보기
    def assert_scope_private_icon(self):
        icon = self.wait.until(
            EC.visibility_of_element_located(LOCATORS["icon_scope_private"])
        )
        assert icon.is_displayed(), "공개 범위 아이콘이 나만 보기로 설정되지 않음"
        return self
    # 기관 내 공유
    def assert_scope_organization_icon(self):
        icon = self.wait.until(
            EC.visibility_of_element_located(LOCATORS["icon_scope_organization"])
        )
        assert icon.is_displayed(), "공개 범위 아이콘이 기관 내 공유로 설정되지 않음"
        return self
    
    # =================================================
    # 미리보기
    # =================================================
    # 미리보기 새로고침 버튼 클릭
    def refresh_preview(self):
        btn = self.wait.until(
            EC.element_to_be_clickable(LOCATORS["btn_preview_refresh"])
        )
        btn.click()
        return self
    
    # =================================================
    # 미리보기에 채팅 입력하기
    # =================================================
    # 미리보기에 채팅 입력
    def input_preview_talk(self, text: str):
        by, xp = LOCATORS["input_preview_textarea"]

        def _get_preview_textarea(d):
            els = d.find_elements(by, xp)
            visible = []
            for e in els:
                try:
                    if e.is_displayed() and e.is_enabled():
                        visible.append(e)
                except Exception:
                    continue
            return visible[-1] if visible else False

        el = self.wait.until(_get_preview_textarea)
        el.clear()
        el.send_keys(text)
        return self
    

    # 미리보기 채팅 입력 보내기
    def preview_talk_send(self):
        def _get_preview_send_btn(d):
            btns = d.find_elements(*LOCATORS["btn_preview_send"])
            clickable = [b for b in btns if b.is_displayed() and b.is_enabled()]
            return clickable[-1] if clickable else False

        btn = self.wait.until(_get_preview_send_btn)
        btn.click()
        return self


    # =================================================
    # 검증 - input 값 기준(안정적)
    # =================================================
    #이름 검증
    def assert_name_input_value(self, expected):
        el = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="name"]'))
        )
        value = el.get_attribute("value") or ""
        assert expected in value, f"이름 input에 '{expected}' 없음: 실제값={value}"
    #한줄 소개 검증
    def assert_description_input_value(self, expected):
        el = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="description"]'))
        )
        value = el.get_attribute("value") or ""
        assert expected in value, f"한줄 소개 input에 '{expected}' 없음: 실제값={value}"
    #규칙 검증
    def assert_rules_input_value(self, expected):
        el = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'textarea[name="systemPrompt"]'))
        )
        value = el.get_attribute("value") or ""
        assert expected in value, f"규칙 textarea에 '{expected}' 없음: 실제값={value}"
    # 시작 대화 검증
    def assert_starter_input_value(self, index: int, expected: str):
        """시작 대화 검증 (index: 0~3)"""
        css = f'input[name="conversationStarters.{index}.value"]'
        el = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, css))
        )
        value = el.get_attribute("value") or ""
        assert expected in value, f"시작 대화 {index+1}에 '{expected}' 없음: 실제값={value}"    
    # 웹 검색 기능이 활성화 되었는지 검증
    def assert_websearch_function_enabled(self, timeout=10):
        checkbox = WebDriverWait(self.driver, timeout).until(
        EC.presence_of_element_located(LOCATORS["checkbox_websearch_function"])
    )
        assert checkbox.is_selected(), "웹 검색이 비활성화 상태임"
        return self
    
    # 웹 검색 기능이 비활성화 되었는지 검증
    def assert_websearch_function_disabled(self, timeout=10):
        checkbox = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(LOCATORS["checkbox_websearch_function"])
        )
        assert not checkbox.is_selected(), "웹 검색이 활성화 상태임"
        return self
    
    # 웹 브라우징 기능이 활성화 되었는지 검증
    def assert_webbrowsing_function_enabled(self, timeout=10):
        checkbox = WebDriverWait(self.driver, timeout).until(
        EC.presence_of_element_located(LOCATORS["checkbox_webbrowsing_function"])
    )
        assert checkbox.is_selected(), "웹 브라우징이 비활성화 상태임"
        return self
    
    # 웹 브라우징 기능이 비활성화 되었는지 검증
    def assert_webbrowsing_function_disabled(self, timeout=10):
        checkbox = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(LOCATORS["checkbox_webbrowsing_function"])
        )
        assert not checkbox.is_selected(), "웹 브라우징이 활성화 상태임"
        return self
    
    # 이미지 생성 기능이 활성화 되었는지 검증
    def assert_imagegeneration_function_enabled(self, timeout=10):
        checkbox = WebDriverWait(self.driver, timeout).until(
        EC.presence_of_element_located(LOCATORS["checkbox_imagegeneration_function"])
    )
        assert checkbox.is_selected(), "이미지 생성이 비활성화 상태임"
        return self
    
    # 이미지 생성 기능이 비활성화 되었는지 검증
    def assert_imagegeneration_function_disabled(self, timeout=10):
        checkbox = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(LOCATORS["checkbox_imagegeneration_function"])
        )
        assert not checkbox.is_selected(), "이미지 생성이 활성화 상태임"
        return self
    
    # 코드 실행 및 데이터 분석 기능이 활성화 되었는지 검증
    def assert_codeexecution_function_enabled(self, timeout=10):
        checkbox = WebDriverWait(self.driver, timeout).until(
        EC.presence_of_element_located(LOCATORS["checkbox_codeexecution_function"])
    )
        assert checkbox.is_selected(), "코드 실행 및 데이터 분석이 비활성화 상태임"
        return self
    
    # 코드 실행 및 데이터 분석 기능이 비활성화 되었는지 검증
    def assert_codeexecution_function_disabled(self, timeout=10):
        checkbox = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(LOCATORS["checkbox_codeexecution_function"])
        )
        assert not checkbox.is_selected(), "코드 실행 및 데이터 분석이 활성화 상태임"
        return self

    # =================================================
    # 검증 - 미리보기 기준(불안정할 수 있어 DEBUG 포함)
    # =================================================
    def assert_preview_name(self, expected):
        # 기존 네 코드에서 사용하던 h6 기반(다만 class는 자주 바뀔 수 있음)
        title = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "h6.MuiTypography-h6"))
        )
        assert expected in title.text, f'이름 미리보기 불일치: 실제="{title.text.strip()}"'

    def assert_preview_description(self, expected, debug=True):
        ps = self.driver.find_elements(By.CSS_SELECTOR, "p.MuiTypography-body1")
        texts = [p.text.strip() for p in ps if p.text and p.text.strip()]
        if debug:
            print("\n[DEBUG] p.MuiTypography-body1 count =", len(texts))
            for i, t in enumerate(texts[:40], start=1):
                print(f"[DEBUG body1 {i}] {t}")
        assert any(expected in t for t in texts), (
            f'미리보기(추정)에서 "{expected}"를 찾지 못함. '
            f"(현재는 p.MuiTypography-body1 전체에서 검색 중)"
        )

    def assert_preview_starter(self, text, debug=False):
        # 시작 대화는 보통 미리보기 버튼 span에 들어감(기존 접근 유지)
        spans = self.driver.find_elements(By.CSS_SELECTOR, "button span")
        span_texts = [s.text.strip() for s in spans if s.text and s.text.strip()]
        if debug:
            print("\n[DEBUG] button span count =", len(span_texts))
            for i, t in enumerate(span_texts[:60], start=1):
                print(f"[DEBUG span {i}] {t}")
        assert any(text in t for t in span_texts), f'미리보기 시작 대화 "{text}" 없음'
    
    # 답변이 test로 끝나는지
    def assert_preview_answer(self, timeout=20):
        def _answer_endswith_test(d):
            answers = d.find_elements(By.CSS_SELECTOR, "p.css-dmwv96.e1d5acfy0")
            texts = [a.text.strip() for a in answers if a.text and a.text.strip()]
            return any(t.endswith("test") for t in texts)
        try:
            WebDriverWait(self.driver, timeout).until(_answer_endswith_test)
            return self  # ← 추가
        except TimeoutException:
            answers = self.driver.find_elements(By.CSS_SELECTOR, "p.css-dmwv96.e1d5acfy0")
            texts = [a.text.strip() for a in answers if a.text and a.text.strip()]
            assert False, f"test로 끝나는 답변이 나오지 않음. 현재 답변={texts}"

    # 답변이 "예"인지 검증
    def assert_preview_answer_is_yes(self, timeout=20):
        def _answer_is_yes(d):
            answers = d.find_elements(By.CSS_SELECTOR, "p.css-dmwv96.e1d5acfy0")
            texts = [a.text.strip() for a in answers if a.text and a.text.strip()]
            return any("예" in t for t in texts)
        try:
            WebDriverWait(self.driver, timeout).until(_answer_is_yes)
            return self  # ← 추가
        except TimeoutException:
            answers = self.driver.find_elements(By.CSS_SELECTOR, "p.css-dmwv96.e1d5acfy0")
            texts = [a.text.strip() for a in answers if a.text and a.text.strip()]
            assert False, f"'예'로 답변이 나오지 않음. 현재 답변={texts}"

    # 답변이 "아니오"인지 검증
    def assert_preview_answer_is_no(self, timeout=20):
        def _answer_is_no(d):
            answers = d.find_elements(By.CSS_SELECTOR, "p.css-dmwv96.e1d5acfy0")
            texts = [a.text.strip() for a in answers if a.text and a.text.strip()]
            return any(("아니오" in t or "아니요" in t) for t in texts)
        try:
            WebDriverWait(self.driver, timeout).until(_answer_is_no)
            return self  # ← 추가
        except TimeoutException:
            answers = self.driver.find_elements(By.CSS_SELECTOR, "p.css-dmwv96.e1d5acfy0")
            texts = [a.text.strip() for a in answers if a.text and a.text.strip()]
            assert False, f"'아니오'로 답변이 나오지 않음. 현재 답변={texts}"

    # 답변이 시작 대화와 일치하는지
    def assert_preview_answer_is_starter(self, n: int, prompt: str, timeout=10):
        expected = f"{prompt}_{n}"
        
        user_msg = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH, f'//span[@data-status="complete" and contains(text(), "{expected}")]'
            ))
        )
        assert expected in user_msg.text, f"사용자 메시지에 '{expected}' 없음"
        return self

    # 에이전트가 생성되었다는 메세지가 잘 표시되는지
    def message_after_created(self, timeout=3):
        wait = WebDriverWait(self.driver, timeout)

        toast = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="alert"] #notistack-snackbar'))
)
        assert "에이전트가 생성 되었습니다." in toast.text, "생성 실패되었습니다."

        return True
    

    # 에이전트가 업데이트 되었다는 메세지가 잘 표시되는지
    def message_after_updated(self, timeout=3):
        wait = WebDriverWait(self.driver, timeout)

        toast = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="alert"] #notistack-snackbar'))
)
        assert "에이전트가 업데이트 되었습니다." in toast.text, "업데이트가 실패되었습니다."

        return True
    
    # =================================================
    # 에이전트 지식 업로드가 잘 되었는지 검증
    # =================================================
    def assert_files_uploaded(self, timeout=30):
        time.sleep(2)
        filenames = [
            "upload_test.txt",
            "upload_test.docx",
            "upload_test.pdf",
            "upload_test.png",
            "upload_test.jpg",
    ]       
        for name in filenames:
            # 파일명이 포함된 p 태그 찾기
            file_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((
                    By.XPATH, f'//p[contains(text(), "{name}")]'
                ))
            )
            print(f"  {name} 발견")
        
        # 성공 아이콘 개수로 전체 확인 (5개 이상이면 OK)
        success_icons = self.driver.find_elements(
            By.CSS_SELECTOR, 'svg[data-testid="circle-checkIcon"]'
        )
        assert len(success_icons) >= len(filenames), f"성공 아이콘 부족: {len(success_icons)}개"
        print(f"  성공 아이콘 {len(success_icons)}개 확인")
        
        return self
    
    # =================================================
    # 미리보기 시작 대화 1~4에 'test_userSetting_1~4'가 들어가있는지 확인
    # =================================================
    
    def assert_preview_startscr(self, n: int, prompt: str):
        """시작 대화 미리보기 검증 (n: 1~4)"""
        expected = f"{prompt}_{n}"
        item = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//button//span[contains(text(), "{expected}")]')
            )
        )
        text_value = item.text.strip()
        assert expected in text_value, (
            f"시작 대화 {n}번에서 '{expected}' 없음: 실제값={text_value}"
        )
        return self

    def assert_click_starter(self, n: int, prompt: str):
        """시작 대화 클릭"""
        expected = f"{prompt}_{n}"
        item = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//button//span[contains(text(), "{expected}")]'))
        ).click()
        return self