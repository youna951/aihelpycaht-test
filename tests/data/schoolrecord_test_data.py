LESSONPLAN_COMMENT_CASES=[
    ("", True, "공백"),
    ("가", True, "1자"),
    ("가"*5000, True, "5000자"),
    ("가"*5001, True, "5001자"),
    
]

FILE_UPLOAD_CASES = [
    ("files/school_record/test_xlsx.xlsx", True, "xlsx 허용"),
    ("files/school_record/test_xls.xls", True, "xls 허용"),

    ("files/school_record/test_docs.docx", False, "docx 비허용"),
    ("files/school_record/test_hwp.hwp", False, "hwp 비허용"),
    ("files/school_record/test_pdf.pdf", False, "pdf 비허용"),
    ("files/school_record/test_ppt.pptx", False, "pptx 비허용"),
    ("files/test_100MB.xlsx", False, "100MB이상 비허용"),
]