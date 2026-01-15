"""
파일명: chat_main_page.py
작성자: 박예진
작성일: 모름 (최종 수정일 : 12/21)
목적: 헬피챗 채팅 페이지의 UI 요소와 동작을 캡슐화한 Page Object

설명:
- ChatMainPage : 텍스트 입력, 보내기, 답변여부/접근, 답변 복사, 답변 다시생성
- ChatReplyScroll : 긴 답변 스크롤, '맨 아래로 스크롤' 버튼
- AIMakeImage : 이미지 생성, 이미지 '확대'버튼, 이미지 '다운로드' 버튼

"""


import time, sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException





class ChatMainPage:
    def __init__(self, logged_in_driver):
        driver = logged_in_driver
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)


#   ---------------------------
#     텍스트 보내기
#   ---------------------------       
    
    # 텍스트 입력창 요소 찾기
    def get_input_textarea_element(self):
        return self.wait.until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR, 'textarea[placeholder="메시지를 입력해 주세요."]')
    )
)

    # 텍스트 입력
    def input_textarea(self, text: str = ""):
        textarea = self.get_input_textarea_element() 
        textarea.clear()  # 이전 내용 삭제
        textarea.send_keys(text) # 새 입력
        return textarea
    
    

    # 보내기 버튼 클릭
    def send_button_click(self):
        send_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='button' and @aria-label='보내기']")
            )
        )
        send_button.click()
        return send_button

    # 전송된 메시지가 UI에 나타나는지 확인
    def check_UI_visible(self, text: str = ""):
        response = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    (
                        f"//span[@data-status='complete' and text()='{text}']"
                        if text
                        else "//span[@data-status='complete']"
                    ),
                )
            )
        )
        return response

    # "마지막 답변" 기준, 생성 완료 될 때까지 기다림
    # 답변 생성 중 ) data-status=“running”
    # 답변 생성 완료 ) data-status="complete"
    def wait_until_reply_complete(self, timeout=100):
        wait = WebDriverWait(self.driver, timeout)

    # 답변 영역이 나타날 때까지 (running 또는 complete)
        wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.elice-aichat__markdown")
        )
    )

    # data-status가 complete가 될 때까지 (답변 생성 완료)
        wait.until(
        lambda d: d.find_elements(
            By.CSS_SELECTOR, "div.elice-aichat__markdown"
        )[-1].get_attribute("data-status") == "complete"
    )

    # 첫번 째 보이는 답변 "요소" 접근
    def get_ai_reply_element(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.elice-aichat__markdown")
            )
        )

        
    # 마지막 답변 "텍스트" 접근
    def get_ai_reply_elements(self):
        replies = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.elice-aichat__markdown")
            )
        )
        if replies:
            return replies[-1].text.strip()  # 문자열 반환
        return ""

    # 마지막 입력 기준 마지막 답변 (한 개) 가져오기 - "요소"
    def get_last_ai_reply_element(self):
        replies = self.get_ai_reply_elements()
        return replies[-1] if replies else None
    
  
        


    
#   ---------------------------
#     답변 복사 기능 
#   ---------------------------       
        

      # 답변 하단 '복사'버튼 찾기
    def get_copy_button(self):
        return self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="복사"]')
            )
        )
    # 답변 하단 '복사'버튼 클릭

    def click_copy_button(self):
        self.get_copy_button().click()

    # 붙여넣기 (os별로 단축키 다름)

    def paste_clipboard(self, textarea):
        textarea.click()
        if sys.platform == "darwin":
            textarea.send_keys(Keys.COMMAND, 'v')
        else:
            textarea.send_keys(Keys.CONTROL, 'v')

#   ---------------------------
#     답변 다시생성
#   ---------------------------

       # 답변 하단 '다시 생성' 버튼 찾기

    def get_regenerate_button(self):
          return self.wait.until(
        EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button[aria-label="다시 생성"]')

    )
)
    # 답변 하단 '다시 생성'버튼 클릭

    def click_regenerate_button(self):
        self.get_regenerate_button().click()


    # 기존답변 & 새로 생성된 답변 비교
    # 새 답변이 아직 안 바뀌었는데 바로 text를 읽을 수 있어서, 텍스트가 바뀔 때까지 wait

    def compare_reply_regenerate(self, old_text: str, timeout: int = 20) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
            lambda d: self.get_last_ai_reply_element() != old_text
        )
            return True
        except TimeoutException:
            return False
        
    # 이전 답변 (<) 버튼 찾기
    def get_previous_reply_button(self):
        button = self.wait.until(
        lambda d: d.find_element(
            By.CSS_SELECTOR,
            'svg[data-testid="chevron-leftIcon"]'
            # 부모요소(버튼)으로 올라가기
        ).find_element(By.XPATH, "..")
    )
        self.wait.until(lambda d: button.is_displayed() and button.is_enabled())
        return button
    
    # 이전 답변 (<) 버튼 클릭
    def click_previous_reply_button(self):
        self.get_previous_reply_button().click()

  

    # 다음 답변 (>) 버튼 찾기  
    def get_next_reply_button(self):
        button = self.wait.until(
        lambda d: d.find_element(
            By.CSS_SELECTOR,
            # (리팩토링 할 때) 클래스 이름말고 다른 요소로 구체화하기 
            # div 범위 구체적으로 (다른 버튼 요소랑 겹침)
            'div.css-4ved3l.ejxvx3b1 svg[data-testid="chevron-rightIcon"]'
        ).find_element(By.XPATH, "..")
    )
        self.wait.until(lambda d: button.is_displayed() and button.is_enabled())
        return button
    
    # 다음 답변 (>) 버튼 클릭
    def click_next_reply_button(self):
        self.get_next_reply_button().click()

 
 
 

    
class ChatReplyScroll(ChatMainPage) :
    def __init__(self, logged_in_driver):
        driver = logged_in_driver
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

#   ---------------------------
#     ai 긴 답변 올 시, 스크롤
#   ---------------------------         

   
    # 스크롤 요소 가져오기 (스크롤이 포함된 div)
    def get_scroll_container(self):
        return self.driver.find_element(
        By.CSS_SELECTOR,
       "div.css-ovflmb.eglo0y10"
    )

    # 긴 답변 받을시, 위로 스크롤
    def scroll_to_top(self, step_px=200, max_attempts=50):
        container = self.get_scroll_container()
        attempts = 0

        while attempts < max_attempts:
            scroll_top = self.get_scroll_top()
            if scroll_top <= 5:  # 0 근처로 판단 (top를 0으로 하면 오류남)
                break

            # 점진적 스크롤 (위로 천천히 스크롤 됨)
            self.driver.execute_script(f"arguments[0].scrollBy(0, -{step_px});", container)
            time.sleep(0.2)  # 렌더링 대기
            attempts += 1
        final_scroll_top = self.get_scroll_top()
        print("답변 위로 스크롤 성공!",final_scroll_top)
        return(final_scroll_top)

        # # 최종 scrollTop 값 확인
        # final_top = self.get_scroll_top()
        # print("최종 scrollTop:", final_top, flush=True)
        # return final_top
    

    # scrollTop 값 조회
    def get_scroll_top(self):
        return self.driver.execute_script(
        "return arguments[0].scrollTop;",
        self.get_scroll_container()
    )

#   ---------------------------
#     '맨 아래로 스크롤' 버튼
#   --------------------------- 

    # '맨 아래로 스크롤' 버튼 요소 가져오기 (못찾으면 none)
    def get_scroll_to_bottom_button(self):
        try:
            return self.driver.find_element(
            By.CSS_SELECTOR,
            'button[aria-label="맨 아래로 스크롤"]'
        )
        except NoSuchElementException:
            return None


    # '맨 아래로 스크롤' 버튼 활성화 여부 
    def is_scroll_to_bottom_button_enabled(self) -> bool:
        button = self.get_scroll_to_bottom_button()
        if not button:
            return False

        # 버튼이 없으면 html에 disabled라고 뜸
        # get_attribute("disabled") = none (버튼 활성화)
        # get_attribute("disabled") = '' (버튼 비활성화)
        return button.get_attribute("disabled") is None



    # '맨 아래로 스크롤' 버튼 클릭
    def click_scroll_to_bottom_button(self):
        #버튼 활성화가 True 될 때까지 기다림
        WebDriverWait(self.driver, 5).until(
        lambda d: self.is_scroll_to_bottom_button_enabled()
    )

        self.get_scroll_to_bottom_button().click()
        return True




class AIMakeImage(ChatMainPage): 
    def __init__(self, logged_in_driver):
        driver = logged_in_driver
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # 플러스 버튼 요소 가져오기 
    def get_chat_main_plus_button(self):
        svg = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button.MuiIconButton-root svg[data-testid='plusIcon']")
            )
        )
        return svg.find_element(By.XPATH, "./ancestor::button")


    # 플러스 버튼 클릭
    def click_chat_main_plus_button(self):
        button = self.get_chat_main_plus_button()
        self.driver.execute_script("arguments[0].click();", button)

    

    # '이미지 생성' 버튼 요소 가져오기
    def get_image_make_button(self):
        return self.wait.until(
        EC.element_to_be_clickable((By.XPATH, '//span[text()="이미지 생성"]'))
    )

    # 이미지 생성이 완료 될 때까지 기다림
    def wait_until_img_complete(self, timeout=100):
        wait = WebDriverWait(self.driver, timeout)

        # "이미지 생성중... "이 뜰 때까지 기다림
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.MuiCircularProgress-root")))

        # "이미지 생성중... "이 사라질 때까지 기다림
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "span.MuiCircularProgress-root")))

    # complete_element 안에 img 태그가 존재하는지 확인
    def is_reply_imgtag(self):
        try:
            # 답변 영역(complete 상태)을 기다린 후 가져오기
            complete_element = self.wait.until(
                lambda d: d.find_element(
                    By.CSS_SELECTOR, "div.elice-aichat__markdown[data-status='complete']"
                )
            )

            # complete_element 안에 img 태그 존재 확인
            imgtag = complete_element.find_element(By.XPATH, ".//img")
            return imgtag.is_displayed() # True/False 반환

        except Exception as e:
            raise AssertionError(e)

   
    # 생성된 이미지 요소 가져오기
    def get_img_element(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.elice-aichat__markdown img")
            )
        )
    
    # 부모꺼 재정의
    # 전체 답변 내용 요소 접근
    def get_ai_reply_element(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.elice-aichat__markdown")
            )
        )


    # 답변 끝 위치로 스크롤 이동 (hover 하기 위해서)
    def scroll_to_reply_end(self):
        reply = self.get_ai_reply_element() 
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'end'});",
            reply
        )


    # 이미지 hover
    def hover_reply_image(self):
        image = self.get_img_element()
        ActionChains(self.driver).move_to_element(image).perform()


    # 확대 버튼 요소 가져오기
    def get_img_zoom_button(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    '//*[local-name()="svg" and @data-testid="magnifying-glass-plusIcon"]/ancestor::button'
                )
            )
        )


    # 확대 버튼 클릭
    def click_img_zoom_button(self):
        self.scroll_to_reply_end()
        self.hover_reply_image()

        try:
            btn = self.get_img_zoom_button()
            self.driver.execute_script("arguments[0].click();", btn)
        except TimeoutException:
            raise AssertionError("확대 버튼이 나타나지 않거나 클릭 불가 상태")
        except WebDriverException as e:
            raise AssertionError(f"확대 버튼 클릭 중 오류 발생: {e}")

        
        # 확대 모달이 열렸는지 판단 (T/F)
    def is_image_zoom_modal_open(self):
        try:
            self.wait.until(
                 EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "div[role='dialog']")
                )
            )
            return True
        except:
            return False

    # 확대된 이미지 X 버튼 요소 가져오기
    def get_img_x_button(self):
         return self.wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[.//*[local-name()="svg" and @data-testid="xmarkIcon"]]'))
    )

    # 확대된 이미지 X 버튼 클릭
    def click_img_x_button(self):
        try:
            self.get_img_x_button().click()
        except TimeoutException:
            raise AssertionError("확대된 이미지 X 버튼이 나타나지 않거나 클릭 불가 상태")
        except WebDriverException as e:
            raise AssertionError(f"확대된 이미지 X 버튼 클릭 중 오류 발생: {e}")

    # 확대 모달이 닫힐 때까지 기다림
    def wait_until_image_modal_closed(self):
        self.wait.until(
            EC.invisibility_of_element_located((
                By.XPATH,
                '//div[@role="dialog"]'
            ))
        )

    # 이미지 하단 '다운로드' 버튼 요소 가져오기
    def get_img_download_button(self):
            self.hover_reply_image()
            return self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//*[local-name()="svg" and @data-testid="downloadIcon"]]'))
        )
    
    # 이미지 하단 '다운로드' 버튼 클릭
    def click_img_download_button(self):
        self.scroll_to_reply_end()
        self.hover_reply_image()
        try:
            self.get_img_download_button().click()
        except TimeoutException:
            raise AssertionError("이미지 다운로드 버튼이 나타나지 않거나 클릭 불가 상태")
        except WebDriverException as e:
            raise AssertionError(f"이미지 다운로드 버튼 클릭 중 오류 발생: {e}")


class EdgeCaseInput(ChatMainPage):
    def __init__(self, logged_in_driver):
        driver = logged_in_driver
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)


    # 입력창 옆 '취소' 버튼 요소 가져오기
    def get_input_cacel_button(self):
         return self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'button[aria-label="취소"]')
            )
        )
    # 입력창 옆 '취소' 버튼 클릭
    def click_input_cacel_button(self):
        try:
            self.get_input_cacel_button().click()
        except TimeoutException:
            raise AssertionError("취소 버튼이 나타나지 않거나 클릭 불가 상태")
        except WebDriverException as e:
            raise AssertionError(f"취소 버튼 클릭 중 오류 발생: {e}")

    # 내가 보낸 메세지 하단의 '수정' 버튼 요소 가져오기
    def get_message_edit_button(self):
        return self.wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@data-testid='penIcon']/ancestor::button")
            )
    )

    # 내가 보낸 메세지 하단의 '수정' 버튼 클릭
    def click_message_edit_button(self):
        try:
            self.get_message_edit_button().click()
        except TimeoutException:
            raise AssertionError("수정 버튼이 나타나지 않거나 클릭 불가 상태")
        except WebDriverException as e:
            raise AssertionError(f"수정 버튼 클릭 중 오류 발생: {e}")

    # 메세지 수정 창 요소 가져오기
    def get_message_edit_textarea(self):
        edit_textarea = self.wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "textarea[name='input']")
        )
    )
        return edit_textarea
    
    # base.page의 clear_all이 안먹어서 (React state) JS 강제 발생
    # 입력된 메세지 수정 입력창 내용 비우기
    def clear_textarea(self, element):
        self.driver.execute_script("""
            const textarea = arguments[0];
            textarea.value = '';
            textarea.dispatchEvent(new Event('input', { bubbles: true }));
            textarea.dispatchEvent(new Event('change', { bubbles: true }));
        """, element)

    # 수정된 메시지 '보내기' 버튼 요소 가져오기
    def get_edit_ok_button(self):
         return self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[.//text()[normalize-space()='보내기']]")
            )
        )
    
     # 수정된 메시지 '보내기' 버튼 클릭
    def click_edit_ok_button(self):
        try:
            self.get_edit_ok_button().click()
        except TimeoutException:
            raise AssertionError("보내기 버튼이 나타나지 않거나 클릭 불가 상태")
        except WebDriverException as e:
            raise AssertionError(f"보내기 버튼 클릭 중 오류 발생: {e}")
    
    # 수정된 메시지 '취소' 버튼 요소 가져오기
    def get_edit_cancel_button(self):
        return self.wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "form button[type='button']:first-of-type")
        )
    )

    # 수정된 메시지 '취소' 버튼 클릭하기
    def click_edit_cancel_button(self):
        try:
            self.get_edit_cancel_button().click()
        except TimeoutException:
            raise AssertionError("취소 버튼이 나타나지 않거나 클릭 불가 상태")
        except WebDriverException as e:
            raise AssertionError(f"취소 버튼 클릭 중 오류 발생: {e}")









   
        
   

