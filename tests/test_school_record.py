'''
작성자 : 신윤아
'''
import os
import pytest
import logging
from pages.school_life_record_page import SchoolLifeRecordPage
from tests.data.schoolrecord_test_data import *

class Test_School_Record:
    # -------------------------------------
    # AHCT-T115 세부 특기사항 페이지 정상 이동
    # -------------------------------------
    def test_go_schoolrecord(self,login_once_with_download):
        page = SchoolLifeRecordPage(login_once_with_download)
        page.go_to_record()
        page.wait_record_page_loaded()
        assert page.is_record_page_opened(),"❌세부 특기사항 페이지로 이동하지 못함"
        logging.info("✅ 세부 특기사항 페이지 이동 완료")
   
    # -------------------------------------
    # AHCT-T120 세부 특기사항 입력양식 다운받기
    # -------------------------------------    
    def test_download_form(self, login_once_with_download):
        page = SchoolLifeRecordPage(login_once_with_download)

        file_name = "student_evaluation_template.xlsx"
        file_path = page.download_form_and_wait(file_name)

        assert os.path.exists(file_path), f"❌ {file_name} 파일이 존재하지 않습니다."

        logging.info(f"✅ 양식 {file_name} 다운로드 완료")
    
    # -------------------------------------
    # AHCT-T121 세부 특기사항 성취기준 검색하기
    # ------------------------------------- 
    def test_go_kice(self,login_once_with_download):
        page = SchoolLifeRecordPage(login_once_with_download)
        page.go_to_KICE() #assert Page안에 넣어줬습니다
        logging.info("✅ 성취기준 사이트 새 창 검증 완료")
        
     # -------------------------------------
    # AHCT-T116 세부 특기사항 학교 드롭박스 내용 검증
    # -------------------------------------
    def test_school_dropdown(self, login_once_with_download):
        page = SchoolLifeRecordPage(login_once_with_download)
        school_level = page.get_dropdown_option("SCHOOL_DROPBOX")
        expexted_school = ["초등","중등","고등"] 
        assert school_level == expexted_school,(f"❌ 학교 선택 불일치 | 기대값={expexted_school}, 실제값={school_level}")
        logging.info("✅ 학교 드롭박스 학교 옵션 검증 완료")
        #드롭박스 값 선택해야 요소찾기 가능
        page.select_el()
     # --------------------------------------------------
    # AHCT-T117 세부 특기사항 학교 초등 선택시 과목 드롭박스 내용 검증
    # --------------------------------------------------
    def test_subject_dropdown_el(self,login_once_with_download):
        page = SchoolLifeRecordPage(login_once_with_download)
        page.select_el()
        subject_option = page.get_dropdown_option("SUBJECT_DROPBOX")
        expected_subject = [
            "국어","영어","수학","사회","과학","도덕","음악","미술","체육","실과"]
        assert subject_option == expected_subject,(f"❌ 과목 옵션 불일치 | 기대={expected_subject}, 실제={subject_option}")
        logging.info("✅ 초등 선택 시 과목 드롭박스 검증 완료")
        #국어선택
        page.select_subject()
    
    # --------------------------------------------------
    # AHCT-T118 세부 특기사항 학교 중등 선택시 과목 드롭박스 내용 검증
    # --------------------------------------------------
    def test_subject_dropdown_mid(self,login_once_with_download):
        page = SchoolLifeRecordPage(login_once_with_download)
        page.select_mid()
        subject_option = page.get_dropdown_option("SUBJECT_DROPBOX")
        expected_subject = [
            "국어","영어","수학","사회","과학","정보","도덕","기술·가정","음악","미술","체육"]
        assert subject_option == expected_subject,(f"❌ 과목 옵션 불일치 | 기대={expected_subject}, 실제={subject_option}")
        logging.info("✅ 중등 선택 시 과목 드롭박스 검증 완료")
        #국어선택
        page.select_subject()
        
    # --------------------------------------------------
    # AHCT-T119 세부 특기사항 학교 고등 선택시 과목 드롭박스 내용 검증
    # --------------------------------------------------
    def test_subject_dropdown_high(self,login_once_with_download):
        page = SchoolLifeRecordPage(login_once_with_download)
        page.select_high()
        subject_option = page.get_dropdown_option("SUBJECT_DROPBOX")
        expected_subject = [
            "국어","영어","수학","사회","과학","한국사","정보","제2외국어/한문","기술·가정","예술","체육"]
        assert subject_option == expected_subject,(f"❌ 과목 옵션 불일치 | 기대={expected_subject}, 실제={subject_option}")
        logging.info("✅ 고등 선택 시 과목 드롭박스 검증 완료")
        #국어선택
        page.select_subject()
        
    # --------------------------------------------------
    # AHCT-T133 ~ AHCT-T135 세부 특기사항 추가입력 유효성 검증
    # --------------------------------------------------
    @pytest.mark.parametrize(
        "comment,expected_enable,desc",
        LESSONPLAN_COMMENT_CASES
    )
    def test_input_textarea(self,login_once_with_download,comment,expected_enable,desc):
        page = SchoolLifeRecordPage(login_once_with_download)
        page.input_textarea(comment)
        actual = page.is_create_enabled()

        assert actual == expected_enable, (
            f"❌ 추가입력 {desc} 입력 시 생성 버튼 상태 불일치 | "
            f"기대={expected_enable}, 실제={actual}"
        )

        logging.info(f"✅ 추가입력 {desc} 입력 → 생성 버튼 {'활성화' if expected_enable else '비활성화'}")
    
    # --------------------------------------------------
    # AHCT-T122 ~ AHCT-T126 
    # 세부 특기사항 파일첨부(클릭)
    # -------------------------------------------------- 
    @pytest.mark.parametrize(
        "file_path,expected_success, desc",
        FILE_UPLOAD_CASES
    )
    def test_click_file_upload(self, login_once_with_download, file_path, expected_success, desc):
        page = SchoolLifeRecordPage(login_once_with_download)
        page.click_upload()
        page.upload_file(file_path)
        
        file_name = os.path.basename(file_path)
        uploaded = page.is_file_uploaded(file_name)

        assert uploaded == expected_success, (
            f"❌ {desc} | 파일명 표시 여부 불일치 "
            f"(기대={expected_success}, 실제={uploaded})"
        )
        logging.info(f"✅ {desc} 파일 업로드 UI 검증 완료")
        
    # ----------------------------------------------------------
    # AHCT-T136 세부 특기사항 파일첨부 후 생성 버튼 클릭
    # ----------------------------------------------------------
    def test_createbtn(self,login_once_with_download):
        page = SchoolLifeRecordPage(login_once_with_download)
        page.upload_file_data()
        page.input_textarea("")
        page.click_create_button()
        page.click_recreate_button()
        assert page.is_stop_enable,"❌ 세부 특기사항 자동생성하고 있지 않음"
        logging.info("✅세부 특기사항 생성 중입니다.")
        
    # ----------------------------------------------------------
    # AHCT-T139 세부 특기사항 생성 버튼 클릭 후 생성결과 다운로드
    # ----------------------------------------------------------
    def test_get_result(self,login_once_with_download):
        page = SchoolLifeRecordPage(login_once_with_download)
        page.wait_get_result()
        assert page.is_result_download_enabled(),"❌ 세부 특기사항 다운로드불가"
        logging.info("✅세부 특기사항 다운로드 가능")
        
        
    # ----------------------------------------------------------
    # AHCT-T138 세부 특기사항 결과 생성 후 정지 버튼 클릭
    # ----------------------------------------------------------
    def test_stopbtn(self,login_once_with_download):
        page = SchoolLifeRecordPage(login_once_with_download)
        page.upload_file_data()
        page.click_create_button()
        page.click_recreate_button()
        page.click_stop()
        assert page.get_stop_message() == "요청에 의해 답변 생성을 중지했습니다."
        logging.info("✅ 세부 특기사항 생성 중지 정상 동작")
    
    
        