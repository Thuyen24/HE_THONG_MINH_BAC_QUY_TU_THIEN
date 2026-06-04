import os, sys
sys.path.insert(0, os.path.dirname(__file__))

try:
    import docx
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])

from docx import Document
from docx.shared import Cm, Pt

from gen_part1 import build_cover, build_preface, build_ch1, build_ch2
from gen_part2 import build_ch3, build_ch4, build_refs

def main():
    doc = Document()
    # Page setup - Decree 30
    for s in doc.sections:
        s.top_margin = Cm(2.0)
        s.bottom_margin = Cm(2.0)
        s.left_margin = Cm(3.0)
        s.right_margin = Cm(1.5)
        s.page_width = Cm(21.0)
        s.page_height = Cm(29.7)
    # Default style
    st = doc.styles['Normal']
    st.font.name = 'Times New Roman'
    st.font.size = Pt(13)
    st.paragraph_format.line_spacing = 1.5
    st.paragraph_format.space_before = Pt(6)
    st.paragraph_format.space_after = Pt(6)

    build_cover(doc)
    build_preface(doc)
    build_ch1(doc)
    build_ch2(doc)
    build_ch3(doc)
    build_ch4(doc)
    build_refs(doc)

    paths = [
        r"d:\DAIHOCDAINAM\Blockchain-Charity-System\docs\DoAn_BlockchainCharity.docx",
        r"d:\Blockchain-Charity-System\docs\DoAn_BlockchainCharity.docx",
    ]
    for p in paths:
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            doc.save(p)
            print(f"SUCCESS: {p}")
        except Exception as e:
            print(f"WARNING: {p}: {e}")

if __name__ == "__main__":
    main()
