"""
created by 심다영
기능 요약(25-12-17 확인 완료)
- 에이전트 탐색 이동: 상단 메뉴에서 에이전트 탐색 페이지로 이동
- 에이전트 검색: 이름 기준으로 에이전트 검색
- ellipsis 메뉴 조작: 에이전트 카드의 ellipsis 버튼 클릭
- 에이전트 편집: ellipsis 메뉴에서 편집 선택 및 편집 페이지 진입 검증
- 에이전트 삭제: ellipsis 메뉴에서 삭제 선택
- 삭제 확인/취소: 삭제 확인 모달에서 삭제 또는 취소 버튼 클릭
- 결과 검증: 에이전트 검색 결과 존재 여부 / 없음 여부 검증
- 상태 검증: 편집 페이지 진입 여부, 삭제 확인 메시지 표시 여부 검증
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from pages.agent_locators import LOCATORS


class AgentSearchPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # =================================================
    # 공통 유틸
    # =================================================
    def safe_click(self, el):
        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)

    # =================================================
    # 페이지 이동 및 조작
    # =================================================
    # 메뉴 - 에이전트 탐색 이동
    def open(self):
        menu = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[normalize-space(text())="에이전트 탐색"]/ancestor::li'))
        )
        menu.click()
        return self

    # 검색창 입력
    def type_query(self, text: str):
        search_input = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="AI 에이전트 검색"]'))
        )
        search_input.clear()
        search_input.send_keys(text)
        return self

    # =================================================
    # ellipsis 메뉴 (카드 스코프)
    # =================================================
    # 에이전트 탐색 페이지에서 ellipsis 버튼 누르기 (메뉴 열기만)
    def click_ellipsis_for_agent(self, agent_title: str, timeout=30):
        wait = WebDriverWait(self.driver, timeout)

        card_xpath = (f'//a[starts-with(@href,"/ai-helpy-chat/agents/") 'f'and .//p[normalize-space(.)="{agent_title}"]]')
        card = wait.until(EC.presence_of_element_located((By.XPATH, card_xpath)))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", card)
        ActionChains(self.driver).move_to_element(card).pause(0.2).perform()

        ellipsis_xpath = (card_xpath +'//*[name()="svg" and @data-testid="ellipsis-verticalIcon"]/ancestor::button[1]')
        ellipsis_btn = wait.until(EC.element_to_be_clickable((By.XPATH, ellipsis_xpath)))
        ellipsis_btn.click()

        wait.until(EC.presence_of_element_located((By.XPATH, '//ul//li//*[self::span or self::p][normalize-space(.)="편집"]')))
        return self

    # =================================================
    # 메뉴 항목 클릭 (메뉴 스코프) - ellipsis 클릭 후 사용
    # =================================================
    # 편집 클릭
    def click_edit_menu(self, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        edit_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//ul//li//*[self::span or self::p][normalize-space(.)="편집"]'
        )))
        edit_btn.click()
        return self

    # 삭제 클릭
    def click_delete_menu(self, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        delete_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//ul//li//*[self::span or self::p][normalize-space(.)="삭제"]'
        )))
        delete_btn.click()
        return self
    # =================================================
    # 내 에이전트 항목 클릭 (편집/삭제)
    # =================================================
    # 내 에이전트 클릭
    def click_first_myagent(self, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        myagent_btn = wait.until(EC.element_to_be_clickable(LOCATORS["btn_myagent"]))
        myagent_btn.click()
        return self

    # 내 에이전트 첫 번째 항목 편집 버튼 클릭
    def click_first_myagent_edit(self, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        edit_btn = wait.until(EC.element_to_be_clickable(LOCATORS["btn_first_myagent_edit"]))
        edit_btn.click()
        return self
    
    # 내 에이전트 첫 번째 항목 삭제 버튼 클릭
    def click_first_myagent_delete(self, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        delete_btn = wait.until(EC.element_to_be_clickable(LOCATORS["btn_first_myagent_delete"]))
        delete_btn.click()
        return self

    # =================================================
    # 삭제 최종 확인 메세지 표시 후 삭제/취소
    # =================================================
    # 삭제 클릭 후 표시되는 삭제 확인 메세지에서 "삭제 버튼" 클릭
    def confirm_delete_agent(self, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        confirm_delete_btn = wait.until(EC.element_to_be_clickable(LOCATORS["btn_confirm_delete"]))
        confirm_delete_btn.click()
        return self
    
    # 삭제 클릭 후 표시되는 삭제 확인 메세지에서 "취소 버튼" 클릭
    def cancel_delete_agent(self, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        cancel_delete_btn = wait.until(EC.element_to_be_clickable(LOCATORS["btn_cancel_delete"]))
        cancel_delete_btn.click()
        return self

    # =================================================
    # 검증 
    # =================================================
    # 결과 검증: 결과 영역에서 text 포함되는 요소가 하나라도 있으면 PASS
    def assert_result_contains(self, text: str):
        self.wait.until(lambda d: text in d.page_source)
        assert text in self.driver.page_source, f'검색 결과에서 "{text}"를 찾지 못함'
        return self

    def assert_no_result_contains(self, text: str):
        el = self.wait.until(
            EC.visibility_of_element_located(LOCATORS["no_result_title"])
        )
        assert "검색 결과가 없습니다." in el.text
        return self

    # 에이전트 편집을 눌러서 편집 페이지로 왔는지 검증
    def assert_edit_page_opened(self, timeout=10):
        btn = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(LOCATORS["btn_update_on_edit_page"])
        )
        assert btn.is_displayed(), "업데이트 버튼이 보이지 않음 - 편집 페이지 진입 실패"
        return self
    
    # 에이전트 삭제 버튼 누른 후, 정말 삭제할 것인지 여부를 묻는 메세지 표시됐는지 검증
    def assert_delete_message(self, timeout=10):
        del_message = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(LOCATORS["del_message"])
        )
        assert del_message.is_displayed(), "에이전트 삭제 메세지가 표시되지 않음"
        return self
    
    # 삭제 되었다는 메세지가 잘 표시되는지
    def message_after_delete(self, timeout=3):
        wait = WebDriverWait(self.driver, timeout)

        toast = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="alert"] #notistack-snackbar'))
)
        assert "에이전트가 삭제되었습니다." in toast.text, "삭제 실패"

        return True
    
    # 내 에이전트에서 삭제 취소 후에도 여전히 존재하는지 검증
    # 첫 번째 에이전트 항목이 여전히 존재하는지 확인
    def assert_agent_exists_by_name(self, name: str):
        """에이전트 카드가 이름으로 존재하는지 확인"""
        elements = self.driver.find_elements(By.XPATH,f'//p[normalize-space(.)="{name}"]'
        )
        assert len(elements) > 0, f'"{name}" 에이전트가 존재하지 않음'
        return self