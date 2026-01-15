'''
작성자 : 신윤아
'''
import pytest
import logging
from pages.ppt_page import PptPage
import time


class TestPPT:
    # -------------------------------------
    # AHCT-T56 PPT 생성 페이지 정상이동 
    # -------------------------------------
    def test_goPPT(self,login_once):
        page = PptPage(login_once)
        page.go_to_ppt()
        assert page.is_ppt_page_opened(), "❌ PPT 생성 페이지로 이동하지 못함"
        logging.info("✅ PPT 생성 페이지 이동 완료")
    # -------------------------------------------- 
    # AHCT-T57 PPT 주제 입력 유효성 검증
    # -------------------------------------------- 
    def test_ppttitle(self,login_once):
        page = PptPage(login_once)
        
        #공백
        page.input_title("")
        assert not page.is_create_enabled(),"❌ PPT 주제 공백 입력시 생성버튼 활성화"
        logging.info("✅주제 공백 입력 → 생성 버튼 비활성화")
        
        #1글자
        page.input_title("가")
        assert page.is_create_enabled,"❌ PPT 주제 1자 입력시 생성버튼 비활성화"
        logging.info("✅주제 1자 입력 → 생성 버튼 활성화")
        
        # 500자
        page.input_title("가" * 500)
        assert page.is_create_enabled(),"❌ PPT 주제 500자 입력시 생성버튼 활성화"
        logging.info("✅주제 500자 입력 → 생성 버튼 활성화")
        
        # 501자
        page.input_title("가" * 501)
        assert not page.is_create_enabled(),"❌ PPT 주제 501자 입력시 생성버튼 활성화"
        logging.info("✅주제 501자 입력 → 생성 버튼 비활성화")
        
    # -------------------------------------------- 
    # AHCT-T58 PPT 지시사항 입력 유효성 검증
    # --------------------------------------------    
    def test_pptinstruction(self,login_once):
        page = PptPage(login_once)
        page.input_title("가")
        #공백
        page.input_instruction("")
        assert page.is_create_enabled(),"❌ PPT생성 지시사항 미입력시 생성버튼 비활성화"
        logging.info("✅지시사항 공백 입력 → 생성 버튼 활성화")
        
        # 2000자
        page.input_instruction("가" * 2000)
        assert page.is_create_enabled(),"❌ PPT생성 지시사항 2000자 생성버튼 비활성화"
        logging.info("✅지시사항 2000자 입력 → 생성 버튼 활성화")
        
        # 2001자
        page.input_instruction("가" * 2001)
        assert not page.is_create_enabled(),"❌ PPT생성 지시사항 2001자 생성버튼 비활성화"
        logging.info("✅지시사항 2001자 입력 → 생성 버튼 비활성화")
        
        # 입력한 지시사항 지우기
        page.input_instruction("")
    # -------------------------------------------- 
    # AHCT-T59 ~ AHCT-T64
    # PPT 슬라이드 수 입력  숫자 유효성 검증
    # --------------------------------------------           
    #숫자 0입력
    def test_ppt_input0_slides(self,login_once):
        page = PptPage(login_once)
        page.input_slide("0")
        slide_value = page.get_slide_text()
        assert slide_value in ("",None),"❌ 슬라이드 수 입력값이 0으로 저장되지 않음"
        assert page.is_create_enabled(),"❌ 슬라이드 수 0 입력 시 생성 버튼이 비활성화됨"
        logging.info("✅ 슬라이드 수 0 입력 → 생성 버튼 활성화")
    
    #숫자 1입력    
    def test_ppt_input1_slides(self,login_once):
        page = PptPage(login_once)   
    
        page.input_slide("1")
        slide_value = page.get_slide_text()
        assert slide_value == "1","❌ 슬라이드 수 입력값이 1로 저장되지 않음"
        assert not page.is_create_enabled(),"❌ 슬라이드 수 1 입력 시 생성 버튼이 활성화됨"
        logging.info("✅ 슬라이드 수 1 입력 → 생성 버튼 비활성화")
    
    #숫자 3입력    
    def test_ppt_input3_slides(self,login_once):
        page = PptPage(login_once)
        page.input_slide("3")
        assert page.is_create_enabled(),"❌ 슬라이드 수 3입력 시 생성 버튼이 활성화됨"
        logging.info("✅ 슬라이드 수 3입력 → 생성 버튼 활성화")
    
    #숫자 50입력  
    def test_ppt_input51_slides(self,login_once):
        page = PptPage(login_once)   
        page.input_slide("50")
        assert page.is_create_enabled(),"❌ 슬라이드 수 50입력 시 생성 버튼이 활성화됨"
        logging.info("✅ 슬라이드 수 50입력 → 생성 버튼 활성화")
        
    #숫자 51입력  
    def test_ppt_input51_slides(self,login_once):
        page = PptPage(login_once)   
        page.input_slide("51") 
        assert not page.is_create_enabled(),"❌ 슬라이드 수 51입력 시 생성 버튼이 활성화됨"
        logging.info("✅ 슬라이드 수 51입력 → 생성 버튼 비활성화")
    
    #글자 입력
    def test_ppt_input_slides_text(self,login_once):
        page = PptPage(login_once)
        
        page.input_slide("가")
        slide_value = page.get_slide_text()
        assert slide_value in ("",None),"❌ 슬라이드 수 글자 입력 됨"
        assert page.is_create_enabled(),"❌ 슬라이드 수 글자 입력 시 생성 버튼이 비활성화됨"
        logging.info("✅ 슬라이드 수 글자 입력 → 텍스트 지워지고, 생성 버튼 활성화")
        
    # -------------------------------------------- 
    # AHCT-T65 ~ AHCT-T69 
    # PPT 섹션수 입력 유효성 검증
    # --------------------------------------------  
    #숫자 0입력
    def test_ppt_input_section_0(self,login_once):
        page = PptPage(login_once)
        page.input_section("0")
        section_value = page.get_section_text()
        assert section_value in ("",None),"❌ 섹션 수 입력값이 0으로 저장되지 않음"
        assert page.is_create_enabled(),"❌ 섹션 수 0 입력 시 생성 버튼이 비활성화됨"
        logging.info("✅ 섹션 수 0 입력 → 생성 버튼 활성화")
    
    #숫자 1입력    
    def test_ppt_input_section_1(self,login_once):
        page = PptPage(login_once)   
    
        page.input_section("1")
        section_value = page.get_section_text()
        assert section_value == "1","❌ 섹션 수 입력값이 1로 저장되지 않음"
        assert page.is_create_enabled(),"❌ 섹션 수 입력 시 생성 버튼이 비활성화됨"
        logging.info("✅ 섹션 수 1 입력 → 생성 버튼 활성화")
    
    #숫자 8입력    
    def test_ppt_input_section_8(self,login_once):
        page = PptPage(login_once)   
    
        page.input_section("8")
        section_value = page.get_section_text()
        assert section_value == "8","❌ 섹션 수 입력값이 8로 저장되지 않음"
        assert page.is_create_enabled(),"❌ 섹션 수 입력 시 생성 버튼이 비활성화됨"
        logging.info("✅ 섹션 수 8 입력 → 생성 버튼 활성화")
    
    #숫자 9입력    
    def test_ppt_input_section_9(self,login_once):
        page = PptPage(login_once)   
    
        page.input_section("9")
        section_value = page.get_section_text()
        assert section_value == "9","❌ 섹션 수 입력값이 9로 저장되지 않음"
        assert not page.is_create_enabled(),"❌ 섹션 수 입력 시 생성 버튼이 비활성화됨"
        logging.info("✅ 섹션 수 9 입력 → 생성 버튼 활성화")
        #값 초기화
        page.input_section("")
    # -------------------------------------------- 
    # AHCT-T70 PPT 심층조사 모드 토글 버튼 on/off
    # --------------------------------------------     
    def test_ppt_toggle_on_off(self,login_once):
        page = PptPage(login_once)
        
        if page.is_simple_mode_on():
            page.toggle_onoff()
        assert not page.is_simple_mode_on(), "❌ 심층조사 OFF 실패"
        logging.info("✅ 심층 조사 모드 off → 토글 비활성화")
        # ON으로 변경
        page.toggle_onoff()
        assert page.is_simple_mode_on(), "❌ 심층조사 ON 실패"
        logging.info("✅ 심층 조사 모드 on → 토글 활성화")
    
    # -------------------------------------------- 
    # AHCT-T71 PPT 자동생성 버튼 클릭
    # --------------------------------------------            
    def test_ppt_create(self,login_once):
        page = PptPage(login_once)
        
        page.input_title("강아지")
        page.input_instruction("강아지 종에 대해 알려줘")
        page.click_create()
        page.recreate_btn_click()
        time.sleep(2)
        assert page.is_stop_enable,"❌ PPT를 자동생성하고 있지 않음"
        logging.info("✅PPT생성 중입니다.")
        
        #멈춰주어야 다음 테스트 수행
        page.click_stop()
    # -------------------------------------------- 
    # AHCT-T73 PPT 자동생성 중지 버튼 클릭
    # -------------------------------------------- 
    def test_ppt_stop(self, login_once):
        page = PptPage(login_once)

        page.wait_generation_closed()

        page.input_title("강아지")
        page.input_instruction("강아지 종에 대해 알려줘")

        page.click_create()
        page.recreate_btn_click()

        page.click_stop()

        assert page.get_stop_message() == "요청에 의해 답변 생성을 중지했습니다."
        logging.info("✅ PPT 생성 중지 정상 동작")