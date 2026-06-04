import re
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_bg(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    
    # Top border
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), '4')
    top.set(qn('w:space'), '0')
    top.set(qn('w:color'), 'CCCCCC')
    tblBorders.append(top)
    
    # Bottom border
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')
    bottom.set(qn('w:space'), '0')
    bottom.set(qn('w:color'), 'CCCCCC')
    tblBorders.append(bottom)
    
    # Inside horizontal border
    insideH = OxmlElement('w:insideH')
    insideH.set(qn('w:val'), 'single')
    insideH.set(qn('w:sz'), '4')
    insideH.set(qn('w:space'), '0')
    insideH.set(qn('w:color'), 'E5E7EB')
    tblBorders.append(insideH)
    
    tblPr.append(tblBorders)

def fmt_run(run, size=13, bold=False, italic=False):
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic

def add_chapter(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.first_line_indent = Cm(0) # KHÔNG thụt lề tiêu đề Chương
    p.paragraph_format.keep_with_next = True
    fmt_run(p.add_run(text.upper()), size=14, bold=True) # Tiêu đề chương cỡ 14, in đậm, căn giữa

def add_h1(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12) # Before: 12pt
    p.paragraph_format.space_after = Pt(6)   # After: 6pt
    p.paragraph_format.first_line_indent = Cm(0) # KHÔNG thụt lề tiêu đề mục nhỏ
    p.paragraph_format.keep_with_next = True
    fmt_run(p.add_run(text), size=13, bold=True, italic=False) # Cỡ 13, in đậm, đứng thẳng, căn trái

def add_h2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12) # Before: 12pt
    p.paragraph_format.space_after = Pt(6)   # After: 6pt
    p.paragraph_format.first_line_indent = Cm(0) # KHÔNG thụt lề tiêu đề mục nhỏ
    p.paragraph_format.keep_with_next = True
    fmt_run(p.add_run(text), size=13, bold=True, italic=False) # Cỡ 13, in đậm, đứng thẳng, căn trái

def add_body(doc, text):
    p = doc.add_paragraph()
    
    # Kiểm tra tự động các chuỗi kỹ thuật để tránh Justify Spacing Error
    tech_patterns = [
        r"SHA-256", r"ECDSA", r"y\^2", r"P\s*=\s*d", r"s\s*=\s*k\^-1", r"R'\s*=",
        r"mapping\(", r"msg\.value", r"msg\.sender", r"payable", r"withdraw", r"donate",
        r"0x", r"Hash", r"SHA", r"EVM", r"Ethers\.js", r"Hardhat", r"OpenZeppelin",
        r"MetaMask", r"Solidity", r"Ownable", r"ReentrancyGuard", r"nonce", r"signature",
        r"\"[^\"]+\"", r"'[^']+'"
    ]
    is_technical = any(re.search(pat, text, re.IGNORECASE) for pat in tech_patterns)
    
    if is_technical:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT # Căn lề trái nếu chứa ký tự kỹ thuật/mã băm/công thức
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY # Căn đều hai bên nếu thuần chữ
        
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.first_line_indent = Cm(1.27) # Thụt lề đầu dòng 1.27cm
    fmt_run(p.add_run(text), size=13)
    return p

def add_list_item(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT # Căn lề trái hoàn toàn cho danh sách gạch đầu dòng
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.first_line_indent = Cm(0) # TUYỆT ĐỐI KHÔNG thụt lề
    p.paragraph_format.left_indent = Cm(0)       # Căn sát lề trái
    fmt_run(p.add_run(text), size=13) # Cỡ 13 cho danh sách liệt kê
    return p

def add_formula(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER      # Căn giữa công thức/mã băm
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.first_line_indent = Cm(0) # KHÔNG thụt lề
    fmt_run(p.add_run(text), size=13, italic=True) # Cỡ 13, in nghiêng
    return p

def add_note(doc, text):
    # Cấu hình chú thích hình ảnh: Chữ in thường, In đậm (Bold), cỡ chữ 13, căn giữa trang, KHÔNG in nghiêng, không thụt lề
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.first_line_indent = Cm(0)
    fmt_run(p.add_run(text), size=13, bold=True, italic=False)
    return p

def add_compare_table(doc, title, headers, rows):
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.first_line_indent = Cm(0)
    fmt_run(p_title.add_run(title), size=12, bold=True, italic=True)

    ncols = len(headers)
    table = doc.add_table(rows=1 + len(rows), cols=ncols)
    table.autofit = True
    set_table_borders(table)
    
    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        set_cell_bg(cell, "F1F5F9")
        set_cell_margins(cell)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.first_line_indent = Cm(0)
        r = p.add_run(h)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)
        
    # Data rows
    for ri, row_data in enumerate(rows):
        for ci, val in enumerate(row_data):
            cell = table.rows[ri + 1].cells[ci]
            set_cell_margins(cell)
            if ri % 2 == 1:
                set_cell_bg(cell, "F9FAFB")
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.first_line_indent = Cm(0)
            r = p.add_run(val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
            if ci == 0:
                r.font.bold = True
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)
    p_after.paragraph_format.first_line_indent = Cm(0)

def add_test_table(doc, tc_num, title, steps, expected, actual, status):
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.paragraph_format.first_line_indent = Cm(0)
    fmt_run(p_title.add_run(f"Kịch bản kiểm thử {tc_num}: {title}"), size=12, bold=True)

    table = doc.add_table(rows=6, cols=2)
    table.autofit = False
    table.columns[0].width = Cm(4.0)
    table.columns[1].width = Cm(12.5)
    set_table_borders(table)
    
    fields = [
        ("Mã kịch bản", f"TC-0{tc_num}"),
        ("Tên chức năng", title),
        ("Các bước thực hiện", steps),
        ("Kết quả kỳ vọng", expected),
        ("Kết quả thực tế", actual),
        ("Trạng thái", status)
    ]
    for idx, (fn, fv) in enumerate(fields):
        c0 = table.rows[idx].cells[0]
        c1 = table.rows[idx].cells[1]
        set_cell_margins(c0)
        set_cell_margins(c1)
        set_cell_bg(c0, "F1F5F9")
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(4)
        p0.paragraph_format.space_after = Pt(4)
        p0.paragraph_format.first_line_indent = Cm(0)
        r0 = p0.add_run(fn)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(11)
        r0.font.bold = True
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(4)
        p1.paragraph_format.space_after = Pt(4)
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.first_line_indent = Cm(0)
        r1 = p1.add_run(fv)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        if fn == "Trạng thái":
            r1.font.bold = True
            r1.font.color.rgb = RGBColor(16, 185, 129) if "PASS" in fv else RGBColor(239, 68, 68)
            
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)
    p_after.paragraph_format.first_line_indent = Cm(0)

def add_prompt_blockquote(doc, prompt_text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.left_indent = Cm(1.0)
    p.paragraph_format.right_indent = Cm(1.0)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.first_line_indent = Cm(0)
    
    # Left border simulation in python-docx: italicized, centered text block with custom labels
    run_label = p.add_run("Prompt for Bing Creator: ")
    fmt_run(run_label, size=11, bold=True, italic=True)
    
    run_content = p.add_run(prompt_text)
    fmt_run(run_content, size=11, bold=False, italic=True)
    return p
