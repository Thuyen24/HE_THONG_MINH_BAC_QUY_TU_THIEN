"""Phần 1: Thiết lập trang bìa, Chương 1 và Chương 2 của báo cáo Đồ án tốt nghiệp bằng tiếng Việt có dấu"""
from doc_helpers import *

def build_cover(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Cm(0)
    fmt_run(p.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\nTRƯỜNG ĐẠI HỌC ĐẠI NAM"), bold=True)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(40)
    p.paragraph_format.first_line_indent = Cm(0)
    fmt_run(p.add_run("KHOA CÔNG NGHỆ THÔNG TIN"), bold=True)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(50)
    p.paragraph_format.first_line_indent = Cm(0)
    fmt_run(p.add_run("----------***----------"), bold=True)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.first_line_indent = Cm(0)
    fmt_run(p.add_run("BÁO CÁO ĐỒ ÁN MÔN HỌC"), bold=True)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(80)
    p.paragraph_format.first_line_indent = Cm(0)
    fmt_run(p.add_run("ĐỀ TÀI: ỨNG DỤNG CÔNG NGHỆ BLOCKCHAIN TRONG VIỆC MINH BẠCH HÓA QUY TRÌNH KÊU GỌI VÀ GIẢI NGÂN VỐN TỪ THIỆN"), bold=True)
    
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(4)
    p.paragraph_format.space_after = Pt(100)
    p.paragraph_format.first_line_indent = Cm(0)
    fmt_run(p.add_run(
        "Giảng viên hướng dẫn : TS. Trần Đăng Công\n"
        "Sinh viên thực hiện   : Đỗ Văn Thuyên\n"
        "Lớp                    : Công nghệ thông tin\n"
        "Khóa                   : 2022 - 2026"
    ), bold=True)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Cm(0)
    fmt_run(p.add_run("HÀ NỘI - 2026"), bold=True)
    doc.add_page_break()

def build_preface(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.first_line_indent = Cm(0)
    p.paragraph_format.keep_with_next = True
    fmt_run(p.add_run("LỜI NÓI ĐẦU"), size=14, bold=True)

    add_body(doc,
        "Trong đời sống xã hội Việt Nam, tinh thần tương thân tương ái và hoạt động thiện nguyện luôn là những nét đẹp văn hóa truyền thống vô cùng quý báu. "
        "Hằng năm, hàng nghìn chiến dịch kêu gọi quyên góp được phát động nhằm hỗ trợ đồng bào gặp thiên tai, bão lũ, trẻ em vùng cao và các hoàn cảnh khó khăn. "
        "Tuy nhiên, sự phát triển bùng nổ của các hoạt động từ thiện tự phát cũng kéo theo những thách thức lớn về quản lý, mà nổi cộm nhất là khủng hoảng niềm tin từ công chúng. "
        "Các phương thức sao kê tài khoản ngân hàng thủ công hoặc quản lý dữ liệu trên hệ thống cơ sở dữ liệu tập trung đã lộ rõ những lỗ hổng chí tử về tính xác thực, khả năng chỉnh sửa dữ liệu trái phép và sự thiếu minh bạch trong khâu giải ngân.")

    add_body(doc,
        "Trước bối cảnh đó, việc tìm kiếm một giải pháp kỹ thuật khách quan, không thể can thiệp bởi con người để giám sát luồng tiền quyên góp trở thành một yêu cầu cấp thiết. "
        "Công nghệ Blockchain (chuỗi khối) với các tính chất phi tập trung, bất biến, minh bạch và tự động hóa thông qua Hợp đồng thông minh (Smart Contract) nổi lên như một câu trả lời hoàn hảo. "
        "Nhận thức được tầm quan trọng của vấn đề này, em đã quyết định lựa chọn nghiên cứu đề tài: \"Ứng dụng công nghệ Blockchain trong việc minh bạch hóa quy trình kêu gọi và giải ngân vốn từ thiện\" cho đồ án của mình. "
        "Hệ thống xây dựng bao gồm một Smart Contract Solidity bảo mật và giao diện ứng dụng phi tập trung (DApp) kết nối trực tiếp với ví điện tử MetaMask, cho phép công khai 100% dòng tiền quyên góp và các chiến dịch rút tiền giải ngân thời gian thực.")

    add_body(doc,
        "Để hoàn thành đồ án này, trước hết em xin bày tỏ lòng biết ơn sâu sắc tới Ban Giám hiệu, Ban chủ nhiệm Khoa Công nghệ thông tin Trường Đại học Đại Nam đã tạo điều kiện học tập tốt nhất cho em trong suốt những năm vừa qua. "
        "Đặc biệt, em xin gửi lời cảm ơn chân thành và sâu sắc nhất tới thầy giáo hướng dẫn - TS. Trần Đăng Công, người đã dành nhiều thời gian định hướng, hướng dẫn tận tình, chỉ bảo những kiến thức chuyên môn quý báu cũng như phương pháp luận khoa học để em có thể hoàn thành đề tài một cách trọn vẹn nhất.")

    add_body(doc,
        "Dù đã dành nhiều thời gian nghiên cứu và nỗ lực hoàn thiện đề tài với tinh thần nghiêm túc nhất, song do giới hạn về mặt thời gian và kinh nghiệm thực tiễn, đồ án chắc chắn không tránh khỏi những thiếu sót ngoài ý muốn. "
        "Em rất kính mong nhận được những ý kiến đóng góp, phê bình quý báu từ các thầy, cô giáo trong Hội đồng chấm đồ án để đề tài nghiên cứu này ngày càng hoàn thiện hơn và có khả năng ứng dụng cao hơn trong thực tiễn xã hội.")

    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sign.paragraph_format.space_before = Pt(24)
    p_sign.paragraph_format.space_after = Pt(6)
    p_sign.paragraph_format.first_line_indent = Cm(0)
    p_sign.paragraph_format.right_indent = Cm(1.0)
    fmt_run(p_sign.add_run("Hà Nội, năm 2026\nSinh viên thực hiện\n\n\nĐỗ Văn Thuyên"), size=13, bold=True)

    doc.add_page_break()

def build_ch1(doc):
    add_chapter(doc, "CHƯƠNG 1: TỔNG QUAN VỀ CÔNG NGHỆ BLOCKCHAIN VÀ THỰC TRẠNG QUỸ TỪ THIỆN")

    add_h1(doc, "1.1. Lịch sử hình thành và khái niệm cốt lõi của Blockchain")
    add_h2(doc, "1.1.1. Lịch sử hình thành và nguồn gốc lý thuyết")
    add_body(doc,
        "Lịch sử của công nghệ Blockchain không bắt đầu từ sự ra đời đột ngột của Bitcoin vào năm 2008, mà là kết quả của nhiều thập kỷ nghiên cứu trong các lĩnh vực mật mã học, mạng máy tính và hệ thống phân tán. "
        "Nền móng đầu tiên được đặt ra vào năm 1982 bởi nhà mã hóa David Chaum với đề xuất về các hệ thống máy tính thiết lập, duy trì và tin tưởng bởi các nhóm đối lập. "
        "Ý tưởng này hướng tới việc tạo dựng một cấu trúc dữ liệu liên kết mà không cần sự hiện diện của một bên thứ ba làm trung gian đáng tin cậy. "
        "Năm 1991, Stuart Haber và W. Scott Stornetta đã giới thiệu công trình nghiên cứu về việc thiết lập một chuỗi các khối dữ liệu được bảo mật bằng mật mã nhằm mục đích gắn nhãn thời gian cho các tài liệu số hóa, ngăn chặn việc sửa đổi thời gian hiển thị hoặc thay đổi nội dung tài liệu. "
        "Đến năm 1992, họ tích hợp cây Merkle vào thiết kế này, cho phép gộp nhiều tài liệu vào trong một khối duy nhất để tối ưu hóa hiệu năng lưu trữ và kiểm tra tính toàn vẹn của dữ liệu một cách nhanh chóng.")
    add_body(doc,
        "Tuy nhiên, các hệ thống tiền điện tử và sổ cái số hóa trước năm 2008 đều gặp phải một rào cản chí tử: Vấn đề chi tiêu lặp chi (Double-Spending Problem) và Bài toán các vị tướng Byzantine (Byzantine Generals Problem). "
        "Tháng 10 năm 2008, một nhân vật hoặc nhóm nhân vật ẩn danh dưới bí danh Satoshi Nakamoto đã xuất bản sách trắng có tiêu đề \"Bitcoin: A Peer-to-Peer Electronic Cash System\". "
        "Công trình này đã giải quyết triệt để vấn đề Double-Spending mà không cần đến bên thứ ba trung gian bằng cách kết hợp mạng ngang hàng (P2P), mật mã học bất đối xứng, hàm băm mật mã và một cơ chế đồng thuận mang tính đột phá dựa trên lý thuyết trò chơi gọi là Proof of Work (Bằng chứng công việc). "
        "Kể từ đó, công nghệ Blockchain đã phát triển qua nhiều giai đoạn khác nhau: từ Blockchain 1.0 tập trung vào tiền tệ kỹ thuật số đơn thuần, Blockchain 2.0 với sự xuất hiện của hợp đồng thông minh trên nền tảng Ethereum, đến các thế hệ Blockchain 3.0 và 4.0 tập trung vào khả năng mở rộng, khả năng tương tác liên chuỗi và ứng dụng thực tế trong các lĩnh vực kinh tế, xã hội và quản trị.")
    add_note(doc, "Hình 1.1. Tiến trình lịch sử phát triển của công nghệ Blockchain qua các thời kỳ")
    add_prompt_blockquote(doc, 'A professional horizontal timeline diagram showcasing the history of Blockchain technology on a pure solid white background. It shows key milestones: "1982: David Chaum proposal", "1991: Linked blocks & time-stamping by Haber & Stornetta", "1992: Merkle Tree integration", "2008: Bitcoin Whitepaper by Satoshi Nakamoto (Blockchain 1.0)", "2015: Ethereum & Smart Contracts (Blockchain 2.0)", and "Present: Scalability & Web3 DApps (Blockchain 3.0/4.0)". Minimalist flat vector style, straight academic font, perfectly centered with generous white safety margins on all sides. --ar 16:9')

    add_h2(doc, "1.1.2. Khái niệm cốt lõi của Blockchain")
    add_body(doc,
        "Về mặt bản chất kỹ thuật, Blockchain là một sổ cái phi tập trung, phân tán và được bảo mật bằng mật mã. Cấu trúc dữ liệu của Blockchain bao gồm một chuỗi liên tục các khối chứa thông tin giao dịch, trong đó mỗi khối mới được liên kết mật thiết với khối trước đó thông qua giá trị băm mật mã của khối tiền nhiệm. "
        "Hệ thống vận hành dựa trên cơ chế đồng thuận phân tán của các máy tính tham gia mạng lưới, loại bỏ hoàn toàn nhu cầu về một tổ chức quản trị trung tâm.")
    
    add_body(doc, "Các đặc trưng cốt lõi cấu thành nên sức mạnh của hệ thống Blockchain bao gồm:")
    add_list_item(doc, "A. Sổ cái phân tán (Distributed Ledger Technology - DLT): Trong kiến trúc cơ sở dữ liệu truyền thống, dữ liệu được lưu trữ tập trung tại một hoặc một nhóm máy chủ. Trái lại, với sổ cái phân tán, cơ sở dữ liệu được sao chép, chia sẻ và đồng bộ hóa trên hàng ngàn hoặc hàng triệu máy tính độc lập (nút - nodes) ngang hàng trên toàn cầu. Điều này giúp ngăn chặn hoàn toàn rủi ro mất mát dữ liệu do thiên tai, hỏng hóc thiết bị hoặc tấn công mạng.")
    add_list_item(doc, "B. Tính phi tập trung (Decentralization): Không một tổ chức, chính phủ hay tập đoàn nào sở hữu mạng lưới Blockchain công khai. Quyền kiểm soát được phân chia đều cho toàn bộ cộng đồng thông qua quy tắc giao thức phần mềm. Mọi quyết định thay đổi hệ thống đều phải thông qua cơ chế đồng thuận.")
    add_list_item(doc, "C. Tính bất biến (Immutability): Dữ liệu một khi đã được ghi vào Blockchain và đạt đến một độ sâu khối nhất định thì hầu như không thể bị sửa đổi, làm giả hoặc xóa bỏ. Nếu một kẻ tấn công muốn thay đổi một giao dịch cũ, họ buộc phải tính toán lại toàn bộ hàm băm của khối đó và tất cả các khối tiếp theo, đồng thời chiếm quyền kiểm soát trên 51% sức mạnh tính toán của toàn mạng lưới - một điều bất khả thi về mặt tài chính và công nghệ.")

    add_h1(doc, "1.2. Mật mã học trong Blockchain")
    add_h2(doc, "1.2.1. Phân tích sâu về mặt toán học của Hàm băm SHA-256")
    add_body(doc,
        "Thuật toán SHA-256 (Secure Hash Algorithm 256-bit) đóng vai trò cốt lõi trong việc đảm bảo tính toàn vẹn và bất biến của dữ liệu trên Blockchain. "
        "Về mặt cấu trúc toán học, SHA-256 lấy một thông báo đầu vào có độ dài bất kỳ (tối đa là 2^64 - 1 bit), phân tách thông báo này thành các khối dữ liệu 512-bit thông qua cơ chế đệm (padding) và thực thi 64 vòng lặp nén tuần tự. "
        "Thuật toán dựa trên các phép toán nhị phân cơ bản bao gồm phép dịch bit (rotation), phép dịch phải (shift right), phép logic AND, OR, XOR và phép cộng module 2^32. "
        "Đầu ra của hàm băm luôn là một chuỗi 256 bit (tương đương 64 ký tự ở hệ cơ số 16 hexadecimal), bất kể kích thước đầu vào lớn hay nhỏ.")
    add_body(doc,
        "Hàm băm SHA-256 sở hữu ba tính chất toán học tối quan trọng giúp bảo vệ hệ thống sổ cái:\n"
        "1. Cơ chế một chiều (One-way property): Đối với bất kỳ dữ liệu đầu vào X nào, việc tính toán giá trị băm H = SHA-256(X) là vô cùng nhanh chóng và tốn rất ít tài nguyên. Tuy nhiên, nếu chỉ biết giá trị băm H, việc tìm ngược lại dữ liệu gốc X là bất khả thi về mặt toán học. Kẻ tấn công chỉ có thể sử dụng phương pháp duyệt thử sai (brute-force) với độ phức tạp tính toán lên tới 2^256 phép thử - vượt quá khả năng xử lý của toàn bộ siêu máy tính trên thế giới cộng lại trong hàng triệu năm.\n"
        "2. Tính chất chống đụng độ (Collision resistance): Việc tìm ra hai đầu vào khác nhau X và Y sao cho SHA-256(X) = SHA-256(Y) là cực kỳ khó khăn. Điều này đảm bảo rằng mỗi khối dữ liệu trên Blockchain có một dấu vân tay số duy nhất.\n"
        "3. Hiệu ứng thác đổ (Avalanche Effect): Đây là thuộc tính quy định rằng khi có một thay đổi vô cùng nhỏ ở dữ liệu đầu vào (dù chỉ là thay đổi 1 bit), giá trị băm đầu ra sẽ thay đổi một cách toàn bộ, ngẫu nhiên và không thể dự đoán trước.")
    add_body(doc, "Ví dụ, khi băm chuỗi ký tự \"Donate\" (chữ D viết hoa), ta thu được giá trị băm hexadecimal:")
    add_formula(doc, "SHA-256(\"Donate\") = 82f8da8a 36ba4e73 b22e1b12 b5982855 16c878e1 b6f8a230 1a2e3cd8 35c1871a")
    add_body(doc, "Tuy nhiên, nếu ta chỉ thay đổi chữ 'D' thành chữ 'd' thường:")
    add_formula(doc, "SHA-256(\"donate\") = ca978112 ca1bbdca fac231b3 9a23dc4d a786effe b59db210 6a1fb423 d2426002")
    add_body(doc,
        "Sự thay đổi nhỏ ở đầu vào đã tạo ra hai kết quả hoàn toàn khác biệt. "
        "Thuộc tính toán học này ngăn chặn tuyệt đối việc kẻ tấn công thực hiện kỹ thuật đảo ngược hoặc sửa đổi thông tin giao dịch từ thiện mà không làm hỏng toàn bộ liên kết băm của chuỗi khối.")
    add_note(doc, "Hình 1.2. Minh họa hiệu ứng thác đổ (Avalanche Effect) của hàm băm SHA-256")
    add_prompt_blockquote(doc, 'A professional technical diagram illustrating the Avalanche Effect of the SHA-256 cryptographic hash function on a pure solid white background. On the left side, the input string "Donate" is hashed to show its 64-character hexadecimal value. On the right side, the input string "donate" (with a minor 1-character difference) is hashed to show a completely different, unrelated hexadecimal value. Distinct arrows show that a single bit change triggers a complete change in the entire output hash. Minimalist flat vector style, straight academic font, perfectly centered with generous white safety margins on all sides. --ar 16:9')

    add_h2(doc, "1.2.2. Chi tiết thuật toán Chữ ký số ECDSA (Mật mã đường cong Elliptic)")
    add_body(doc,
        "Thuật toán ECDSA (Elliptic Curve Digital Signature Algorithm) được sử dụng để xác thực quyền sở hữu tài sản và tính toàn vẹn của các giao dịch quyên góp cũng như giải ngân trên mạng lưới Blockchain. "
        "ECDSA dựa trên độ khó của bài toán lôgarit rời rạc trên đường cong Elliptic để đảm bảo an toàn thông tin.")
    add_body(doc, "Trong Ethereum, đường cong Elliptic được chuẩn hóa dưới tên gọi secp256k1, được định nghĩa bởi phương trình toán học:")
    add_formula(doc, "y^2 = x^3 + 7 (modulo p)")
    add_body(doc,
        "Trong đó, p là một số nguyên tố cực lớn xác định giới hạn của trường hữu hạn (p = 2^256 - 2^32 - 977). "
        "Khóa bí mật (Private Key) thực chất là một số nguyên ngẫu nhiên d được chọn trong khoảng [1, n-1] (với n là bậc của điểm gốc G trên đường cong). "
        "Khóa công khai (Public Key) đại diện bởi một tọa độ điểm P(x, y) trên đường cong, thu được từ phép nhân điểm:")
    add_formula(doc, "P = d * G")
    add_body(doc, "Nhờ tính chất toán học của phép nhân điểm trên đường cong Elliptic, việc tính toán P từ d là rất dễ dàng, nhưng việc tìm ngược lại d từ P là một bài toán bất khả thi (bài toán logarit rời rạc).")
    
    add_body(doc, "Quy trình ký duyệt giao dịch từ thiện diễn ra như sau:")
    add_list_item(doc, "1. Hệ thống frontend của ứng dụng tính toán mã băm e của nội dung giao dịch (bao gồm thông tin ví gửi, ví nhận, số tiền và nội dung).")
    add_list_item(doc, "2. Ví MetaMask của người dùng sinh ngẫu nhiên một số k trong khoảng [1, n-1] và tính toán điểm R = k * G. Tọa độ trục hoành x của điểm R được gán cho thành phần r của chữ ký số.")
    add_list_item(doc, "3. Thành phần s của chữ ký được tính toán theo công thức: s = k^-1 * (e + r * d) (modulo n). Chữ ký số xuất ra là bộ đôi giá trị (r, s).")
    add_list_item(doc, "4. Khi giao dịch được gửi lên mạng lưới, các nút kiểm tra tính hợp lệ bằng cách tính toán điểm R' = (e * s^-1) * G + (r * s^-1) * P. Nếu tọa độ trục hoành của điểm R' trùng khớp với giá trị r trong chữ ký, giao dịch được xác nhận là hợp lệ. Cơ chế này bảo vệ người dùng khỏi việc bị đánh cắp tài sản hoặc bị giả mạo chữ ký giao dịch.")
    add_note(doc, "Hình 1.3. Mô hình toán học của thuật toán chữ ký số ECDSA trên đường cong secp256k1")
    add_prompt_blockquote(doc, 'A professional mathematical diagram illustrating the ECDSA digital signature algorithm on the secp256k1 elliptic curve (y^2 = x^3 + 7) on a pure solid white background. It displays the elliptic curve graph, showing private key \'d\' generating public key \'P = d * G\' via point multiplication, and the signature verification formula using point \'R\' on the curve. Clear geometric lines, mathematical equations, straight academic font, perfectly centered with generous white safety margins on all sides. --ar 16:9')

    add_h2(doc, "1.2.3. Thực trạng từ thiện tại Việt Nam và Lỗ hổng CSDL tập trung")
    add_body(doc,
        "Trong những năm gần đây, hoạt động kêu gọi quyên góp tự phát tại Việt Nam đã trải qua những giai đoạn khủng hoảng niềm tin nghiêm trọng. "
        "Các vụ việc tranh cãi liên quan đến hoạt động \"sao kê\" tài khoản ngân hàng của các cá nhân đứng ra kêu gọi đã phơi bày những hạn chế chí tử của hệ thống tài chính tập trung.")
    add_body(doc,
        "Báo cáo sao kê ngân hàng truyền thống (dưới dạng bản in giấy hoặc file PDF) hoàn toàn không có tính bất biến. "
        "Với công nghệ chỉnh sửa hình ảnh hiện đại hoặc các phần mềm can thiệp PDF chuyên dụng, việc sửa đổi số liệu, làm giả số dư hoặc ẩn đi các giao dịch nhận tiền lớn là điều vô cùng dễ dàng. "
        "Quan trọng hơn, các hệ quản trị cơ sở dữ liệu tập trung (Centralized Database như SQL Server, MySQL, Oracle) lưu trữ thông tin giao dịch của ngân hàng hoặc ứng dụng từ thiện Web2 luôn tồn tại quyền tối cao (Root/Superuser) của Quản trị viên (DBA). "
        "Một DBA hoặc một hacker chiếm được quyền kiểm soát máy chủ cơ sở dữ liệu có thể thực hiện lệnh UPDATE hoặc DELETE trực tiếp để thay đổi số liệu trong bảng dữ liệu mà không để lại bất kỳ vết kiểm toán bất biến nào. "
        "Điều này khiến cho việc kiểm soát tài chính từ thiện hoàn toàn phụ thuộc vào sự tự giác đạo đức của các cá nhân và tổ chức, thiếu đi một cơ chế ràng buộc kỹ thuật khách quan và độc lập.")

    add_compare_table(doc,
        "Bảng 1.1. So sánh mô hình quản lý dữ liệu Tập trung và Phi tập trung trong từ thiện",
        ["Tiêu chí so sánh", "Mô hình Tập trung (CSDL truyền thống / SQL)", "Mô hình Phi tập trung (Sổ cái Blockchain)"],
        [
            ["Tính minh bạch", "Thấp. Dữ liệu chỉ người quản trị mới xem được. Cộng đồng không thể tự do kiểm chứng trực tiếp.", "Rất cao. Mọi giao dịch được ghi công khai trên sổ cái phân tán, bất kỳ ai cũng có thể kiểm chứng."],
            ["Khả năng chỉnh sửa", "Dễ dàng. Quản trị viên (DBA) có quyền UPDATE/DELETE trực tiếp mà không để lại vết kiểm toán.", "Gần như không thể. Dữ liệu đã ghi vào block được bảo vệ bởi hàm băm liên kết và cơ chế đồng thuận mạng lưới."],
            ["Rủi ro gian lận", "Cao. Người kêu gọi có thể sửa đổi số liệu, ẩn giao dịch hoặc làm giả báo cáo sao kê ngân hàng.", "Cực thấp. Mọi thay đổi trạng thái đều yêu cầu chữ ký số hợp lệ và sự đồng thuận của các nút mạng."],
            ["Tốc độ xử lý", "Nhanh (mili-giây). Giao dịch được xử lý ngay lập tức bởi máy chủ trung tâm.", "Chậm hơn (vài giây đến vài phút). Giao dịch phải chờ quá trình đồng thuận và đóng gói khối."],
            ["Khả năng chịu lỗi", "Kém. Nếu máy chủ trung tâm gặp sự cố hoặc bị tấn công, toàn bộ hệ thống sẽ ngưng hoạt động.", "Cực tốt. Hệ thống vẫn vận hành bình thường ngay cả khi phần lớn các nút mạng gặp sự cố kỹ thuật."],
            ["Độ tin cậy", "Dựa trên uy tín cá nhân hoặc tổ chức quản lý trung gian.", "Dựa trên thuật toán toán học và cơ chế mật mã học khách quan."],
        ]
    )
    add_note(doc, "Hình 1.4. Sơ đồ mô tả lỗ hổng chỉnh sửa dữ liệu của kiến trúc cơ sở dữ liệu tập trung")
    add_prompt_blockquote(doc, 'A professional systems engineering diagram illustrating the security vulnerabilities of a centralized database architecture on a pure solid white background. It shows a central server housing an SQL database, where an administrator (DBA) or an external hacker with root privileges uses direct UPDATE or DELETE commands to manipulate donation transaction records without generating immutable audit trails. Minimalist flat vector style, straight academic font, perfectly centered with generous white safety margins on all sides. --ar 16:9')

    add_h1(doc, "1.3. Nền tảng Ethereum, Hợp đồng thông minh và Ứng dụng phi tập trung (DApp)")
    add_body(doc,
        "Ethereum ra mắt vào năm 2015, mở ra kỷ nguyên Blockchain 2.0 bằng cách biến sổ cái thanh toán đơn thuần thành một Máy tính ảo toàn cầu phi tập trung (Ethereum Virtual Machine - EVM). "
        "Hợp đồng thông minh (Smart Contract) là các chương trình máy tính tự thực thi trên EVM, đảm bảo tính khách quan tuyệt đối. "
        "Ứng dụng phi tập trung (DApp) là mô hình ứng dụng kết nối trực tiếp frontend của người dùng đến blockchain thông qua ví Web3 (nhu MetaMask) thay vì máy chủ API tập trung.")
    add_body(doc,
        "EVM hoạt động như một máy tính trạng thái (State Machine), trong đó mỗi giao dịch hợp lệ làm thay đổi trạng thái toàn cục của mạng lưới. "
        "Mỗi chương trình chạy trên EVM được đo lường bằng đơn vị Gas - đại diện cho lượng tính toán cần thiết để thực thi từng chỉ lệnh. "
        "Người gửi giao dịch phải trả phí Gas này cho các validator để duy trì hoạt động bảo mật của mạng lưới.")
    add_note(doc, "Hình 1.5. So sánh kiến trúc Web2 truyền thống với kiến trúc Web3 DApp phi tập trung")
    add_prompt_blockquote(doc, 'A professional architectural comparison diagram between a traditional Web2 client-server model and a Web3 decentralized application (DApp) model on a pure solid white background. On the left, the Web2 model shows "Client Browser -> Central Web Server -> Centralized Database". On the right, the Web3 model shows "Client Browser + MetaMask -> frontend hosted -> Ethereum Smart Contract -> Decentralized Ledger". Minimalist flat vector style, straight academic font, perfectly centered with generous white safety margins on all sides. --ar 16:9')

    add_h1(doc, "1.4. Phân tích chi tiết về các thế hệ cơ chế đồng thuận trong Blockchain")
    add_body(doc,
        "Cơ chế đồng thuận là trái tim của mọi mạng lưới blockchain, giải quyết bài toán làm thế nào để hàng triệu nút mạng độc lập đạt được sự nhất trí về một trạng thái duy nhất của sổ cái mà không cần bên trung gian. "
        "Thế hệ đầu tiên là Proof of Work (PoW) - Bằng chứng công việc. Trong PoW, các thợ đào phải giải một câu đố toán học cực kỳ khó nhằm tìm ra một số nonce thỏa mãn điều kiện độ khó của mạng lưới. "
        "Quy trình này tiêu tốn một lượng năng lượng điện và năng lực phần cứng khổng lồ, nhưng lại cung cấp độ bảo mật cực cao nhờ tính chất bất đối xứng: việc giải đố rất khó nhưng việc kiểm chứng kết quả lại vô cùng dễ dàng.")
    add_body(doc,
        "Để giải quyết vấn đề tiêu thụ năng lượng của PoW, cơ chế Proof of Stake (PoS) - Bằng chứng cổ phần đã ra đời. PoS thay thế việc khai thác bằng năng lượng phần cứng bằng việc đặt cọc (staking) tài sản kỹ thuật số. "
        "Những người xác thực (validators) được lựa chọn để đóng gói khối mới dựa trên tỷ lệ tài sản họ khóa lại làm tài sản thế chấp. Nếu họ có hành vi gian lận hoặc phá hoại mạng lưới, tài sản thế chấp này sẽ bị phạt nặng (slashing). "
        "Ethereum đã chuyển đổi thành công từ PoW sang PoS vào tháng 9 năm 2022 thông qua sự kiện lịch sử \"The Merge\", giúp giảm hơn 99.95% lượng điện năng tiêu thụ toàn mạng lưới.")
    add_body(doc,
        "Bên cạnh PoW và PoS, các cơ chế đồng thuận khác như Proof of Authority (PoA) hay Delegated Proof of Stake (DPoS) cũng được ứng dụng rộng rãi trong các mạng lưới riêng tư hoặc liên minh. "
        "PoA hoạt động dựa trên uy tín của các nút được phê duyệt trước, giúp tối ưu hóa đáng kể tốc độ xử lý giao dịch và loại bỏ phí gas đắt đỏ, rất phù hợp cho các dự án từ thiện thử nghiệm hoặc mạng lưới chính phủ quản lý.")

    add_h1(doc, "1.5. Tổng quan về các cuộc tấn công bảo mật phổ biến trên mạng lưới Blockchain")
    add_body(doc,
        "Mặc dù công nghệ Blockchain mang lại độ an toàn và tính minh bạch vượt trội so với cơ sở dữ liệu truyền thống, hệ thống vẫn phải đối mặt với các nguy cơ bảo mật ở các cấp độ khác nhau. "
        "Ở cấp độ giao thức mạng lưới, cuộc tấn công 51% (51% Attack) xảy ra khi một thực thể hoặc nhóm thợ đào kiểm soát hơn 50% sức mạnh băm (hashing power) hoặc lượng cổ phần staking của mạng lưới. "
        "Khi đạt được quyền lực này, kẻ tấn công có thể ngăn cản giao dịch mới, đảo ngược các giao dịch đã thực hiện trong thời gian họ kiểm soát mạng lưới và thực hiện hành vi chi tiêu hai lần (double-spending).")
    add_body(doc,
        "Ở cấp độ hợp đồng thông minh, các lỗ hổng bảo mật thường xuất phát từ sai sót trong mã nguồn do lập trình viên thiết kế. "
        "Lỗ hổng tái nhập (Reentrancy) là một trong những lỗi nghiêm trọng nhất, từng gây ra vụ hack The DAO nổi tiếng vào năm 2016 dẫn đến việc phân tách chuỗi Ethereum. "
        "Lỗ hổng này xảy ra khi một hợp đồng thông minh thực hiện chuyển tiền đến một hợp đồng bên ngoài trước khi cập nhật số dư nội bộ của mình. "
        "Hợp đồng bên ngoài có thể gọi ngược lại hàm rút tiền một cách đệ quy, thực hiện rút tiền liên tục cho đến khi cạn kiệt tài sản của hợp đồng mục tiêu.")
    add_body(doc,
        "Các lỗ hổng khác bao gồm tràn số (integer overflow/underflow) đối với các phiên bản Solidity cũ dưới 0.8.0, lỗi phụ thuộc mốc thời gian (timestamp dependence) khi lập trình viên sử dụng block.timestamp cho các hàm ngẫu nhiên, và lỗi phân quyền truy cập (access control failure) khi không thiết lập bộ lọc modifier phù hợp cho các hàm quản trị quan trọng. "
        "Do đó, việc kiểm toán an toàn (security audit) và kiểm thử kỹ lưỡng trước khi đưa hợp đồng lên mạng chính là bắt buộc để bảo vệ dòng tiền quyên góp của cộng đồng.")
    
    doc.add_page_break()

def build_ch2(doc):
    add_chapter(doc, "CHƯƠNG 2: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG QUỸ TỪ THIỆN MINH BẠCH")

    add_h1(doc, "2.1. Phân tích yêu cầu hệ thống")
    add_h2(doc, "2.1.1. Yêu cầu chức năng")
    add_body(doc, "Hệ thống từ thiện minh bạch được phân tích thiết kế hướng đến hai tác nhân chính:")
    add_list_item(doc, "- Nhà hảo tâm (Donors): Kết nối ví MetaMask, xem số dư quỹ hiện tại, gửi quyên góp ETH kèm lời nhắn, xem lịch sử giao dịch quyên góp của mình và toàn bộ hệ thống.")
    add_list_item(doc, "- Ban quản trị chiến dịch (Owner): Thực hiện rút tiền giải ngân cho các đối tượng thụ hưởng với địa chỉ ví và mục đích cụ thể, sử dụng chức năng rút khẩn cấp khi cần thiết.")
    add_note(doc, "Hình 2.1. Biểu đồ Use Case tổng thể của hệ thống minh bạch từ thiện Blockchain")
    add_prompt_blockquote(doc, 'A professional software engineering Use Case diagram for a transparent blockchain-based charity crowdfunding system on a pure solid white background. It shows two main actors: "Donor" on the left and "Campaign Owner" on the right. System use cases include: "Donate ETH", "View Campaign Info", "View Donation History", and "Request Withdrawal (owner only)", with lines connecting actors to use cases. Minimalist flat vector style, straight academic font, perfectly centered with generous white safety margins on all sides. --ar 16:9')

    add_h2(doc, "2.1.2. Yêu cầu phi chức năng")
    add_body(doc,
        "Các yêu cầu phi chức năng bao gồm: Bảo mật cao chống tấn công Reentrancy (tái nhập), tối ưu hóa Gas fee trong Smart Contract bằng cách sử dụng Custom Errors (lỗi tùy chỉnh), giao diện tải nhanh độ trễ thấp và tự động cập nhật số liệu thời gian thực thông qua sự kiện (Events).")

    add_h1(doc, "2.2. Phân tích chi tiết Kiến trúc 3 lớp của ứng dụng DApp từ thiện")
    add_body(doc,
        "Kiến trúc của ứng dụng phi tập trung (DApp) giải quyết triệt để bài toán Single Point of Failure bằng cách phân rã hệ thống thành 3 lớp hoạt động độc lập nhưng liên kết chặt chẽ:")
    add_list_item(doc, "1. Lớp giao diện người dùng (Frontend Presentation Layer): Sử dụng HTML/CSS/JavaScript thuần túy. Lớp này chịu trách nhiệm hiển thị Dashboard số liệu trực quan, tiếp nhận các thao tác nhập liệu từ nhà hảo tâm (nhập số tiền, nội dung lời nhắn) và hiển thị lịch sử giao dịch. Frontend hoàn toàn không lưu trữ cơ sở dữ liệu nội bộ mà chuyển giao trạng thái thông qua các component phản ứng động.")
    add_list_item(doc, "2. Lớp kết nối Web3 (Integration/Middleware Layer): Đóng vai trò là cầu nối dịch ngôn ngữ giữa trình duyệt web và các khối blockchain. MetaMask đóng vai trò là một Wallet Provider, lưu trữ an toàn khóa bí mật và cung cấp API window.ethereum vào trình duyệt. Thư viện Ethers.js v6 tiếp nhận API này để tạo các kết nối JSON-RPC chuẩn. Khi người dùng click Donate, Ethers.js đóng gói tham số, MetaMask hiện popup yêu cầu ký duyệt và gửi transaction đã ký lên mạng lưới.")
    add_list_item(doc, "3. Lớp logic và Lưu trữ Blockchain (Storage & Logic Layer): Bao gồm Smart Contract chạy trực tiếp trên EVM. Toàn bộ tài sản (ETH) quyên góp được khóa trực tiếp trong địa chỉ của hợp đồng thông minh. Các biến trạng thái lưu trữ trên Blockchain được cập nhật thông qua quá trình đồng thuận toàn mạng lưới, đảm bảo tính bất biến và công khai.")
    add_note(doc, "Hình 2.2. Sơ đồ kiến trúc 3 lớp của Blockchain Charity DApp")
    add_prompt_blockquote(doc, 'A professional software architecture diagram showing the 3-layer architecture of the Blockchain Charity DApp on a pure solid white background. The three layers are: "1. Presentation Layer (ReactJS, TailwindCSS, MetaMask Interface)", "2. Integration Layer (Ethers.js v6, JSON-RPC Provider)", and "3. Blockchain Layer (Ethereum Sepolia Testnet, Solidity Smart Contract, EVM)". Clear layer separations, directional arrows, minimalist flat vector style, straight academic font, perfectly centered with generous white safety margins on all sides. --ar 16:9')

    add_h1(doc, "2.3. Thiết kế luồng hoạt động (Workflow)")
    add_body(doc,
        "Hệ thống vận hành thông qua các quy trình tuần tự chặt chẽ. Khi quyên góp, giao dịch được ký bởi khóa bí mật của người dùng, chuyển đến EVM để xử lý và khóa tiền trực tiếp trong hợp đồng. "
        "Khi giải ngân, EVM sẽ chạy qua các chốt chặn kiểm tra: Quyền sở hữu (onlyOwner), Số dư khả dụng, tính hợp lệ của địa chỉ ví nhận và độ dài của chuỗi mô tả mục đích giải ngân.")
    add_note(doc, "Hình 2.3. Sơ đồ tuần tự mô tả chi tiết luồng hoạt động Quyên góp")
    add_prompt_blockquote(doc, 'A professional UML Sequence Diagram illustrating the Donation workflow of the Web3 charity application on a pure solid white background. It shows lifelines for "Donor (User)", "Frontend (React)", "MetaMask", and "TuThien Smart Contract". Steps include: "1. Click Donate", "2. Request signature", "3. Approve transaction on MetaMask", "4. Send transaction to Blockchain", "5. Execute donate() function", and "6. Emit Donated event to Frontend". Minimalist flat vector style, straight academic font, perfectly centered with generous white safety margins on all sides. --ar 16:9')
    add_note(doc, "Hình 2.4. Sơ đồ tuần tự mô tả chi tiết luồng hoạt động Giải ngân quỹ")
    add_prompt_blockquote(doc, 'A professional UML Sequence Diagram illustrating the Withdrawal (disbursement) workflow of the Web3 charity application on a pure solid white background. Lifelines shown: "Campaign Owner", "Frontend (React)", "MetaMask", and "TuThien Smart Contract". Steps include: "1. Request withdrawal with recipient and purpose", "2. Check owner role", "3. Sign transaction on MetaMask", "4. Call withdraw() function", "5. Update totalWithdrawn state", "6. Transfer ETH to recipient", and "7. Emit Withdrawn event". Minimalist flat vector style, straight academic font, perfectly centered with generous white safety margins on all sides. --ar 16:9')

    add_h1(doc, "2.4. Phân tích Thiết kế logic và Cấu trúc dữ liệu trong Smart Contract")
    add_body(doc,
        "Smart Contract TuThien.sol được thiết kế tối ưu hóa cấu trúc dữ liệu lưu trữ để hạn chế tối đa số lượng ghi (SSTORE) - hoạt động tiêu tốn gas nhiều nhất trên mạng Ethereum.")
    add_body(doc,
        "A. Biến địa chỉ định danh (address): Sử dụng kiểu dữ liệu address để lưu trữ thông tin Owner của chiến dịch. Khi deploy hợp đồng, biến này được thiết lập bằng địa chỉ của người khởi tạo và bảo vệ bằng modifier onlyOwner.")
    add_body(doc,
        "B. Cấu trúc dữ liệu Struct: Sử dụng hai struct Donation và Withdrawal để nhóm các dữ liệu có liên quan lại với nhau, giúp mã nguồn sạch và dễ quản lý khi truyền nhận dữ liệu dạng mảng động.")

    add_compare_table(doc,
        "Bảng 2.1. Cấu trúc dữ liệu Struct Donation trong Smart Contract",
        ["Trường dữ liệu", "Kiểu dữ liệu", "Mô tả chi tiết"],
        [
            ["donor", "address", "Địa chỉ ví công khai của người gửi tiền quyên góp"],
            ["amount", "uint256", "Số tiền quyên góp tính bằng đơn vị wei (1 ETH = 10^18 wei)"],
            ["timestamp", "uint256", "Mốc thời gian Unix Epoch ghi nhận từ biến block.timestamp"],
            ["message", "string", "Lời nhắn gửi kèm từ nhà hảo tâm"],
        ]
    )
    add_compare_table(doc,
        "Bảng 2.2. Cấu trúc dữ liệu Struct Withdrawal trong Smart Contract",
        ["Trường dữ liệu", "Kiểu dữ liệu", "Mô tả chi tiết"],
        [
            ["to", "address", "Địa chỉ ví của bên thụ hưởng nhận tiền giải ngân"],
            ["amount", "uint256", "Số tiền giải ngân tính bằng đơn vị wei"],
            ["purpose", "string", "Mô tả chi tiết mục đích sử dụng tiền giải ngân (tối thiểu 10 ký tự)"],
            ["timestamp", "uint256", "Mốc thời gian thực hiện giao dịch giải ngân"],
        ]
    )

    add_body(doc, "C. Cơ chế ánh xạ Mapping: Để quản lý số tiền đóng góp của từng ví, hợp đồng thiết lập cấu trúc:")
    add_formula(doc, "mapping(address => uint256) public donorTotalAmount")
    add_body(doc,
        "Mapping hoạt động giống như một bảng băm (Hash Table) với độ phức tạp truy xuất O(1). "
        "Khi nhà hảo tâm quyên góp, giá trị băm của địa chỉ ví msg.sender sẽ được dùng để định vị trực tiếp ô nhớ chứa số tiền đóng góp lũy kế trên blockchain mà không cần duyệt qua toàn bộ danh sách, giúp tiết kiệm tối đa lượng gas thực thi trong máy ảo EVM.")
    add_note(doc, "Hình 2.5. Sơ đồ cấu trúc lớp (Class Diagram) và mối quan hệ thừa kế của Smart Contract TuThien")
    add_prompt_blockquote(doc, 'A professional UML Class Diagram showcasing the Solidity Smart Contract "TuThien" inheritance structure and members on a pure solid white background. It shows the main class "TuThien" inheriting from OpenZeppelin\'s "Ownable" and "ReentrancyGuard". Inside "TuThien", it lists private state variables (campaignName, campaignDescription, totalDonated, totalWithdrawn), structs (Donation, Withdrawal), and public methods (donate, withdraw, getDetails). Minimalist flat vector style, straight academic font, perfectly centered with generous white safety margins on all sides. --ar 16:9')

    add_h1(doc, "2.5. Phân tích so sánh các ngôn ngữ phát triển Hợp đồng thông minh phổ biến")
    add_body(doc,
        "Hiện nay, có nhiều ngôn ngữ lập trình được sử dụng để xây dựng hợp đồng thông minh tùy thuộc vào nền tảng blockchain mục tiêu. "
        "Solidity là ngôn ngữ phổ biến nhất, được thiết kế chuyên biệt cho Ethereum Virtual Machine (EVM). "
        "Cú pháp của Solidity chịu ảnh hưởng mạnh mẽ bởi C++, Python và JavaScript, giúp các lập trình viên truyền thống dễ dàng tiếp cận. "
        "Solidity là ngôn ngữ hướng đối tượng, tĩnh và hỗ trợ cơ chế kế thừa đa hình phức tạp, rất phù hợp cho việc xây dựng các ứng dụng tài chính và quản lý quỹ từ thiện phi tập trung.")
    add_body(doc,
        "Ngôn ngữ thứ hai là Vyper, cũng chạy trên EVM nhưng được thiết kế với mục tiêu tối ưu hóa tính an toàn bảo mật và khả năng đọc mã. "
        "Vyper loại bỏ hoàn toàn các tính năng phức tạp của Solidity như kế thừa, nạp chồng toán tử, đệ quy vô hạn và hàm kiểm tra kiểu động. "
        "Nhờ vậy, mã nguồn Vyper dễ kiểm toán và giảm thiểu nguy cơ xuất hiện các lỗ hổng bảo mật ẩn, tuy nhiên lại làm giảm tính linh hoạt khi xây dựng các cấu trúc ứng dụng lớn.")
    add_body(doc,
        "Đối với các blockchain thế hệ mới như Solana hay Polkadot, Rust và Go lại là những ngôn ngữ chủ đạo. "
        "Rust mang lại hiệu năng thực thi cực kỳ cao và khả năng quản lý bộ nhớ an toàn tuyệt đối mà không cần bộ thu gom rác (garbage collector). "
        "Tuy nhiên, độ dốc học tập của Rust là rất lớn so với Solidity. "
        "Trong khuôn khổ đề tài này, việc lựa chọn Solidity là giải pháp tối ưu nhất do hệ sinh thái Ethereum có tính phổ biến cao, tài liệu hỗ trợ phong phú và khả năng tương thích tuyệt vời với ví MetaMask.")

    add_h1(doc, "2.6. Thiết kế giải pháp phân quyền và kiểm toán dòng tiền trong Smart Contract")
    add_body(doc,
        "Để đảm bảo dòng tiền từ thiện được sử dụng đúng mục đích và ngăn ngừa tuyệt đối nguy cơ thất thoát tài sản, hệ thống được tích hợp các cơ chế kiểm toán tự động ngay tại lớp hợp đồng thông minh. "
        "Cơ chế thứ nhất là phân quyền quản trị dựa trên chuẩn Ownable. Khi hợp đồng được khởi tạo trên blockchain, địa chỉ ví thực hiện deploy sẽ được lưu vĩnh viễn vào biến owner. "
        "Các hàm nhạy cảm như giải ngân (withdraw) sẽ được đính kèm modifier onlyOwner để chặn đứng mọi nỗ lực truy cập phi pháp từ các tài khoản không có thẩm quyền.")
    add_body(doc,
        "Cơ chế thứ hai là kiểm toán dòng tiền công khai. Mọi giao dịch quyên góp hay giải ngân đều bắt buộc phải phát đi một sự kiện (Event) tương ứng là Donated hoặc Withdrawn lên nhật ký sự kiện của mạng lưới (EVM logs). "
        "Nhật ký này là bất biến và không thể bị sửa đổi bởi bất kỳ ai, kể cả chủ dự án. "
        "Frontend của DApp sẽ sử dụng các sự kiện này để tự động dựng lại toàn bộ lịch sử thu chi mà không cần qua bất kỳ máy chủ API trung gian nào, giúp các nhà hảo tâm thực hiện giám sát độc lập dòng tiền mọi lúc mọi nơi.")
    
    doc.add_page_break()
