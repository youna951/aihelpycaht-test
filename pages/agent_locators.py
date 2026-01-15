"""
created by 심다영
25-12-17 확인 완료
"""

from selenium.webdriver.common.by import By

LOCATORS = {
    # =======================================================
    # 에이전트 버튼 모음
    # =======================================================
    #에이전트 탐색 버튼
    "menu_agent_search": (By.XPATH, '//span[normalize-space(text())="에이전트 탐색"]/ancestor::li'),
    # + 만들기 버튼 
    "agent_builder_create": (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/agents/builder"]'),
    # 에이전트 첫 생성 시 활성화되는 만들기 버튼
    "btn_create": (By.XPATH, '//button[normalize-space(.)="만들기"]'),
    # 공개 범위 설정 > 나만 보기
    "scope_private": (By.XPATH, "//label[.//p[text()='나만 보기']]"),
    # 공개 범위 설정 > 기관 내 공유
    "scope_organization": (By.XPATH, '//p[text()="기관 내 공유"]'),
    # 공개 범위 설정 후 저장 버튼
    "btn_scope_save": (By.XPATH, '//button[normalize-space(.)="저장"]'),
    # 업데이트 버튼
    # 편집을 통해 들어왔을 때 활성화됨
    "btn_update": (By.XPATH, '//button[normalize-space(.)="업데이트"]'),
    # 우측에 표시되는 미리보기 새로 고침 버튼
    "btn_preview_refresh": (By.CSS_SELECTOR, 'button[aria-label="새로고침"]'),
    # 미리보기 채팅창에 텍스트 입력
    "input_preview_textarea": (By.CSS_SELECTOR,'textarea[name="input"][placeholder="메시지를 입력해 주세요."]'),
    # 미리보기 채팅창에 텍스트 입력 후 보내기
    "btn_preview_send": (By.CSS_SELECTOR, 'button[aria-label="보내기"]'),
    # 삭제 클릭 시 표시되는 삭제 버튼
    "btn_confirm_delete": (By.CSS_SELECTOR, 'div[role="dialog"] button.MuiButton-containedError'),
    # 삭제 클릭 시 표시되는 취소 버튼
    "btn_cancel_delete": (By.CSS_SELECTOR, 'div[role="dialog"] button.MuiButton-containedInherit'),
    # =======================================================
    # 에이전트 빌더 페이지 내 요소들
    # =======================================================
    # 에이전트 만들기 내 설정 버튼
    "agent_builder_settings": (By.XPATH, '//button[contains(text(), "설정")]'),
    # 설정 > 이름
    "input_agent_name": (By.CSS_SELECTOR, 'input[name="name"]'),
    # 설정 > 한줄 소개
    "input_agent_description": (By.CSS_SELECTOR, 'input[name="description"]'),
    # 설정 > 규칙
    "input_agent_rules": (By.CSS_SELECTOR, 'textarea[name="systemPrompt"]'),
    # 설정 > 지식 파일 업로드
    "input_agent_fileupload": (By.XPATH, '//label[contains(text(),"파일 업로드")]//input[@type="file"]'),
    # 설정 > 웹 검색 기능 체크박스
    "checkbox_websearch_function": (By.CSS_SELECTOR, 'input[name="toolIds"][value="web_search"]'),
    # 설정 > 웹 브라우징 체크박스
    "checkbox_webbrowsing_function": (By.CSS_SELECTOR, 'input[name="toolIds"][value="web_browsing"]'),
    # 설정 > 이미지 생성 체크박스
    "checkbox_imagegeneration_function": (By.CSS_SELECTOR, 'input[name="toolIds"][value="image_generation"]'),
    # 설정 > 코드 실행 및 데이터 분석 체크박스
    "checkbox_codeexecution_function": (By.CSS_SELECTOR, 'input[name="toolIds"][value="code_execution"]'),

    # =======================================================
    # 내 에이전트 내에 있는 요소들
    # =======================================================
    # 에이전트 탐색 > 내 에이전트
    "btn_myagent": (By.CSS_SELECTOR, 'a[href="/ai-helpy-chat/agents/mine"]'),
    # 내 에이전트에 있는 첫 번째 에이전트 카드(편집 버튼)
    "btn_first_myagent_edit": (By.XPATH, '//*[name()="svg" and @data-testid="penIcon"]/ancestor::button[1]'),
    # 내 에이전트에 있는 첫 번째 에이전트 카드(삭제 버튼)
    "btn_first_myagent_delete": (By.CSS_SELECTOR, 'button svg[data-testid="trashIcon"]'),

    # =======================================================
    # 미리보기
    # =======================================================
    # 미리보기에 표시되는 챗봇 이름
    "preview_agent_name": (By.CSS_SELECTOR, "h6.MuiTypography-h6"),
    # 미리보기 한줄 소개
    "preview_agent_decription": (By.CSS_SELECTOR, "p.MuiTypography-body1"),
    # 미리보기 시작 대화
    "preview_agent_starter": (By.CSS_SELECTOR, "button span"),
    # 미리보기에서 챗봇 답변 칸
    "preview_agent_answer": (By.CSS_SELECTOR, "p.css-dmwv96.e1d5acfy0"),
    # 업데이트 메세지
    "message_update_complete": (By.XPATH, '//button[.//svg[@data-testid="ellipsis-verticalIcon"]]'),

    # =================================================
    # 페이지 이동 및 조작
    # =================================================
    # ai 검색창에 텍스트 입력
    "input_agent_search": (By.CSS_SELECTOR, 'input[placeholder="AI 에이전트 검색"]'),

    # =================================================
    # ellipsis 메뉴 (카드 스코프)
    # =================================================
    # 템플릿: 카드(에이전트 타이틀 기반) XPath
    "card_by_title_xpath_tpl": (By.XPATH, '//a[.//*[self::p or self::span][contains(normalize-space(.), "{agent_title}")]]'),
    # 카드 내부 ellipsis 버튼 (CSS)
    "btn_ellipsis_in_card": (By.CSS_SELECTOR, 'button:has(svg[data-testid="ellipsis-verticalIcon"])'),
    # 메뉴 등장 대기용 - 편집 항목
    "menu_item_edit": (By.XPATH, '//ul//li//*[self::span or self::p][normalize-space(.)="편집"]'),

    # =================================================
    # 메뉴 항목 클릭
    # =================================================
    # ellipsis > 삭제 버튼
    "menu_item_delete": (By.XPATH, '//ul//li//*[self::span or self::p][normalize-space(.)="삭제"]'),

    # =================================================
    # 검증
    # =================================================
    "no_result_title": (By.CSS_SELECTOR, "h6.MuiTypography-subtitle1"),
    "btn_update_on_edit_page": (By.XPATH, '//button[normalize-space(.)="업데이트"]'),
    # =================================================
    # 삭제 메세지 검증
    # =================================================
    "del_message": (By.CSS_SELECTOR, 'div[role="dialog"] h2.MuiDialogTitle-root'),
    # =================================================
    # 내 에이전트 첫 번째 항목
    # =================================================
    "myagent_cards": (By.CSS_SELECTOR,'a[href^="/ai-helpy-chat/agents/"]'),
    # ===================================================
    # 공개 범위 검증
    # =======================================================
    "icon_scope_private": (By.CSS_SELECTOR, 'svg[data-testid="lockIcon"]'),
    "icon_scope_organization": (By.CSS_SELECTOR, 'svg[data-testid="buildingsIcon"]'),
}