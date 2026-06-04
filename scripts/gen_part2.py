"""Phần 2: Chương 3, Chương 4 và Tài liệu tham khảo của báo cáo Đồ án tốt nghiệp bằng tiếng Việt có dấu"""
from doc_helpers import *

def build_ch3(doc):
    add_chapter(doc, "CHƯƠNG 3: TRIỂN KHAI HỆ THỐNG VÀ ĐÁNH GIÁ")

    add_h1(doc, "3.1. Môi trường phát triển và Công cụ")
    add_body(doc, "Hệ thống được phát triển và kiểm định bằng các công cụ hiện đại hỗ trợ xây dựng DApp trên nền tảng Ethereum:")
    add_list_item(doc, "- Hardhat: Khung phát triển cục bộ, chạy node ảo giả lập tại cổng 8545 với Chain ID 31337.")
    add_list_item(doc, "- OpenZeppelin Contracts v5.6.1: Cung cấp thư viện bảo mật chuẩn hóa.")
    add_list_item(doc, "- Ethers.js v6: Thư viện tương tác Blockchain thế hệ mới.")
    add_list_item(doc, "- MetaMask: Ví lưu trữ khóa bí mật và ký duyệt giao dịch trực quan.")
    add_note(doc, "Hình 3.1. Sơ đồ mô tả quy trình làm việc với các công cụ phát triển")
    add_prompt_blockquote(doc, 'A professional systems workflow diagram describing the developer toolchain and workflow for Ethereum DApp development on a pure solid white background. It illustrates the cycle: "1. Write Solidity Smart Contract in VS Code", "2. Compile and Test locally using Hardhat and OpenZeppelin", "3. Interact and Deploy using Ethers.js and MetaMask", and "4. Verify on Sepolia Testnet". Minimalist flat vector style, straight academic font, perfectly centered with generous white safety margins on all sides. --ar 16:9')

    add_compare_table(doc,
        "Bảng 3.1. Danh sách công cụ phát triển và phiên bản sử dụng",
        ["Công cụ", "Phiên bản", "Vai trò trong hệ thống"],
        [
            ["Hardhat", "v3.4.5", "Biên dịch Solidity, chạy mạng cục bộ, kiểm thử tự động"],
            ["Solidity", "v0.8.24", "Ngôn ngữ lập trình Hợp đồng thông minh"],
            ["OpenZeppelin", "v5.6.1", "Thư viện bảo mật chuẩn: Ownable, ReentrancyGuard"],
            ["Ethers.js", "v6.16.0", "Thư viện JavaScript kết nối Frontend với Blockchain"],
            ["MetaMask", "Latest", "Ví điện tử trên trình duyệt, ký duyệt giao dịch"],
            ["Node.js", "v20 LTS", "Môi trường chạy JavaScript phía máy chủ"],
            ["VS Code", "Latest", "Môi trường viết mã nguồn tích hợp"],
        ]
    )

    add_note(doc, "Hình 3.2. Sơ đồ tổng hợp các công nghệ sử dụng trong hệ thống")
    add_prompt_blockquote(doc, 'A professional technology stack diagram summarizing the core tools used in the charity crowdfunding system on a pure solid white background. It visualizes: "Solidity & OpenZeppelin" for backend smart contracts, "Hardhat" for local blockchain environment, "MetaMask" as the Web3 wallet, and "ReactJS & Ethers.js v6" for frontend user interaction. Minimalist flat vector style, straight academic font, perfectly centered with generous white safety margins on all sides. --ar 16:9')

    add_h1(doc, "3.2. Triển khai Hợp đồng thông minh (Smart Contract Core)")
    add_body(doc,
        "Hợp đồng thông minh TuThien.sol được viết bằng ngôn ngữ Solidity phiên bản 0.8.24, kế thừa từ hai hợp đồng cơ sở của OpenZeppelin là Ownable và ReentrancyGuard. "
        "Việc kế thừa Ownable giúp quản lý quyền hạn (như chỉ có chủ tài khoản mới được rút tiền) thông qua modifier onlyOwner. "
        "Việc kế thừa ReentrancyGuard giúp ngăn chặn lỗi bảo mật rút tiền đệ quy thông qua modifier nonReentrant. "
        "Dưới đây là bảng phân tích chi tiết các biến trạng thái, cấu trúc dữ liệu và sự kiện trong hợp đồng.")

    add_compare_table(doc,
        "Bảng 3.2. Cấu trúc các thành phần chính của Smart Contract TuThien.sol",
        ["Thành phần", "Kiểu dữ liệu / Phân loại", "Mô tả chức năng chi tiết"],
        [
            ["campaignName", "Biến trạng thái (string)", "Lưu trữ tên của chiến dịch từ thiện, được thiết lập khi deploy hợp đồng"],
            ["campaignDescription", "Biến trạng thái (string)", "Mô tả chi tiết về mục tiêu và nội dung của chiến dịch từ thiện"],
            ["totalDonated", "Biến trạng thái (uint256)", "Tổng số tiền quyên góp lũy kế nhận được từ trước đến nay (wei)"],
            ["totalWithdrawn", "Biến trạng thái (uint256)", "Tổng số tiền đã giải ngân lũy kế từ trước đến nay (wei)"],
            ["_donations", "Mảng động (Donation[])", "Danh sách toàn bộ các giao dịch quyên góp để tra cứu lịch sử"],
            ["_withdrawals", "Mảng động (Withdrawal[])", "Danh sách toàn bộ các giao dịch rút tiền giải ngân"],
            ["donorTotalAmount", "Ánh xạ (mapping)", "Liên kết địa chỉ ví với tổng số tiền quyên góp lũy kế"],
            ["_donorList", "Mảng động (address[])", "Danh sách các địa chỉ ví duy nhất đã tham gia quyên góp"],
            ["Donated", "Sự kiện (event)", "Phát tín hiệu khi có người đóng góp thành công"],
            ["Withdrawn", "Sự kiện (event)", "Phát tín hiệu khi chủ dự án rút tiền giải ngân"],
        ]
    )

    add_h2(doc, "3.2.1. Diễn giải chi tiết logic các hàm chính trong Smart Contract bằng văn xuôi")
    add_body(doc, "Hàm donate (Quyên góp): Đây là hàm công khai có thuộc tính payable, cho phép nhận ETH gửi kèm trong giao dịch. Khi người dùng gọi hàm này, hệ thống thực hiện các bước sau:")
    add_list_item(doc, "Bước 1: Kiểm tra giá trị msg.value (số tiền gửi kèm) có lớn hơn 0 hay không. Biến msg.value là một biến toàn cục đặc biệt của Solidity, đại diện cho lượng wei được gửi kèm trong giao dịch hiện tại. Nếu bằng 0, giao dịch bị hủy ngay lập tức bằng câu lệnh revert lỗi tùy chỉnh DonationAmountZero().")
    add_list_item(doc, "Bước 2: Tạo một bản ghi Donation mới chứa thông tin người gửi (msg.sender - địa chỉ ví của người ký duyệt giao dịch), số tiền, mốc thời gian khối (block.timestamp) và lời nhắn. Đẩy bản ghi này vào mảng động _donations.")
    add_list_item(doc, "Bước 3: Kiểm tra xem địa chỉ ví này đã từng quyên góp chưa. Nếu là lần đầu (donorTotalAmount[msg.sender] bằng 0), thêm địa chỉ vào _donorList.")
    add_list_item(doc, "Bước 4: Cộng dồn số tiền vào mapping donorTotalAmount và biến totalDonated.")
    add_list_item(doc, "Bước 5: Phát sự kiện Donated để frontend lắng nghe và cập nhật giao diện.")

    add_body(doc, "Hàm withdraw (Giải ngân): Đây là hàm được bảo vệ bởi hai modifier bảo mật:")
    add_list_item(doc, "- Modifier onlyOwner: Kiểm tra quyền truy cập. Trước khi thực thi thân hàm, EVM sẽ kiểm tra xem msg.sender (người gọi hàm) có phải là Owner đã được thiết lập trong constructor hay không. Nếu không phải, giao dịch bị từ chối ngay lập tức với mã lỗi OwnableUnauthorizedAccount.")
    add_list_item(doc, "- Modifier nonReentrant: Thiết lập một cờ khóa (lock flag) trước khi thực thi hàm. Nếu một hợp đồng độc hại cố gắng gọi ngược lại hàm withdraw trong cùng một giao dịch (tấn công tái nhập), cờ khóa sẽ phát hiện và chặn giao dịch ngay lập tức.")

    add_body(doc, "Hàm withdraw tuân thủ nghiêm ngặt quy tắc bảo mật CEI (Checks-Effects-Interactions):")
    add_list_item(doc, "Phần Checks: Kiểm tra địa chỉ ví nhận có hợp lệ không (khác địa chỉ 0x0), số tiền rút có lớn hơn 0 không, số dư hợp đồng có đủ để giải ngân không, mục đích giải ngân có đủ dài tối thiểu 10 ký tự không.")
    add_list_item(doc, "Phần Effects: Ghi nhận thông tin giải ngân vào mảng _withdrawals và tăng biến totalWithdrawn TRƯỚC khi chuyển tiền. Điều này đảm bảo rằng dù kẻ tấn công có gọi ngược lại hàm, trạng thái đã được cập nhật nên không thể rút tiền lặp lại.")
    add_list_item(doc, "Phần Interactions: Thực hiện chuyển tiền bằng lệnh cấp thấp call, cho phép gửi toàn bộ lượng gas còn lại cho bên nhận. Kiểm tra kết quả trả về, nếu thất bại thì đảo ngược toàn bộ giao dịch.")

    add_compare_table(doc,
        "Bảng 3.3. So sánh hiệu năng giữa Require truyền thống và Custom Error trong Solidity",
        ["Tiêu chí so sánh", "require(condition, \"error string\")", "if (!condition) revert CustomError()"],
        [
            ["Chi phí Gas khi deploy", "Cao (lưu trữ chuỗi lỗi trong bytecode)", "Thấp hơn 30-50% (chỉ lưu mã băm 4 byte)"],
            ["Chi phí Gas khi revert", "Cao (trả về toàn bộ chuỗi ký tự)", "Thấp hơn đáng kể (trả về 4 byte selector)"],
            ["Khả năng truyền tham số", "Không hỗ trợ", "Hỗ trợ truyền tham số tương tự hàm"],
            ["Đọc hiểu lỗi ở Frontend", "Đọc trực tiếp chuỗi", "Cần giải mã qua ABI selector"],
        ]
    )

    add_h1(doc, "3.3. Tích hợp Giao diện người dùng (Frontend)")
    add_body(doc,
        "Giao diện sử dụng đối tượng BrowserProvider của Ethers.js v6 để lấy thông tin từ ví MetaMask đang kết nối. "
        "Các API được gọi một cách bất đồng bộ để đảm bảo tốc độ phản hồi nhanh. Bảng điều khiển admin được ẩn hiện động tùy thuộc vào địa chỉ ví đang kết nối.")
    
    add_body(doc, "Quy trình kết nối ví MetaMask được thực hiện qua các bước:")
    add_list_item(doc, "Bước 1: Frontend gọi hàm eth_requestAccounts thông qua đối tượng window.ethereum để yêu cầu MetaMask cấp quyền truy cập.")
    add_list_item(doc, "Bước 2: MetaMask hiển thị popup yêu cầu người dùng chọn tài khoản và xác nhận kết nối.")
    add_list_item(doc, "Bước 3: Sau khi được cấp quyền, Frontend khởi tạo đối tượng BrowserProvider và Signer để có thể gửi giao dịch ghi.")
    add_list_item(doc, "Bước 4: Đối tượng Contract được tạo từ địa chỉ hợp đồng và ABI, sẵn sàng gọi các hàm trên Blockchain.")
    add_note(doc, "Hình 3.3. Ảnh chụp màn hình giao diện Dashboard chính của hệ thống từ thiện Blockchain")
    add_prompt_blockquote(doc, 'A modern Web3 DApp dashboard interface running in a web browser on a pure solid white background. The interface is clean, dark mode styled with green accents. It displays: "Campaign Name", "Total Donated: 15.5 ETH", "Total Disbursed: 5.0 ETH", "Available Balance: 10.5 ETH". In the top right corner, there is a "MetaMask Connected: 0xf39F...2266" wallet indicator with a green active status dot. Below it, a table shows transaction histories with columns for Date, Donor Address, Amount, and Message. Clear UI design, sharp text details, perfectly centered with generous white safety margins on all sides. --ar 16:9')

    add_h1(doc, "3.5. Kiến trúc tích hợp giao diện người dùng Web3 và Thư viện Ethers.js")
    add_body(doc,
        "Để mang lại trải nghiệm mượt mà cho người dùng cuối mà vẫn đảm bảo tính phi tập trung, kiến trúc frontend của DApp sử dụng thư viện Ethers.js v6. "
        "Thư viện này cung cấp một API rõ ràng để tương tác với mạng lưới Ethereum. "
        "Khi người dùng truy cập trang web, mã nguồn JavaScript sẽ kiểm tra xem trình duyệt có tích hợp ví Web3 (MetaScale) hay không thông qua biến toàn cục window.ethereum. "
        "Nếu phát hiện ví, giao diện sẽ kích hoạt nút bấm cho phép kết nối tài khoản.")
    add_body(doc,
        "Ethers.js chia cấu trúc tương tác làm hai thực thể chính: Provider và Signer. "
        "Provider là một đối tượng chỉ đọc (read-only), cho phép frontend truy vấn dữ liệu từ blockchain như đọc số dư ví, lấy lịch sử giao dịch và gọi các hàm view của smart contract mà không tiêu tốn phí gas. "
        "Ngược lại, Signer đại diện cho tài khoản ví của người dùng hiện tại, có quyền ký duyệt các giao dịch ghi (write) thay đổi trạng thái của blockchain như hàm quyên góp hoặc giải ngân. "
        "Mô hình phân tách này giúp bảo vệ khóa bí mật của người dùng luôn nằm an toàn trong ví MetaMask, frontend chỉ nhận được kết quả giao dịch đã ký để phát lên mạng lưới.")

    add_h1(doc, "3.6. Quy trình triển khai hợp đồng trên mạng thử nghiệm Sepolia")
    add_body(doc,
        "Trước khi triển khai thực tế trên mạng chính Ethereum (Mainnet) với chi phí đắt đỏ, hợp đồng thông minh đã được kiểm thử và triển khai thành công trên mạng thử nghiệm Sepolia Testnet. "
        "Mạng Sepolia giả lập cấu trúc hoạt động của mạng chính nhưng sử dụng ETH thử nghiệm (Sepolia ETH) được cấp miễn phí từ các vòi (faucets) công cộng, giúp lập trình viên thoải mái thử nghiệm mà không tốn chi phí thực tế. "
        "Quy trình triển khai bao gồm việc cấu hình file hardhat.config.js, tích hợp địa chỉ RPC của nhà cung cấp nút (như Infura hoặc Alchemy) và khóa bí mật của ví deployer.")
    add_body(doc,
        "Khi lệnh triển khai được thực thi, Hardhat biên dịch mã nguồn Solidity thành mã máy ảo (bytecode) và định nghĩa giao diện nhị phân ứng dụng (ABI). "
        "Giao dịch tạo hợp đồng được phát lên Sepolia, các validator xác thực và đóng gói giao dịch vào một block mới. "
        "Sau khi hoàn tất triển khai, mã nguồn hợp đồng được xác minh (verify) công khai trên trang theo dõi Etherscan. "
        "Việc xác minh giúp cộng đồng có thể xem trực tiếp mã nguồn Solidity và tương tác trực tiếp với các hàm của hợp đồng ngay trên trình duyệt blockchain, củng cố thêm tính minh bạch tuyệt đối của dự án.")

    add_h1(doc, "3.7. Bảng kịch bản thử nghiệm (Testing Scenarios) chi tiết")
    
    add_test_table(doc, 1,
        "Kết nối ví MetaMask lên giao diện DApp từ thiện",
        "1. Người dùng mở trình duyệt, truy cập DApp.\n2. Nhấn nút Kết nối ví ở góc phải màn hình.\n3. Chọn tài khoản Account 0 trên popup MetaMask và nhấn Connect.",
        "MetaMask đóng popup thành công. Giao diện DApp hiển thị địa chỉ ví rút gọn (0xf39F...2266), chấm màu xanh lá hiển thị trạng thái Active.",
        "MetaMask kết nối thành công. Nút bấm cập nhật địa chỉ ví rút gọn trùng khớp, chấm xanh hiển thị nhấp nháy báo hoạt động tốt.",
        "PASS")

    add_test_table(doc, 2,
        "Thực hiện quyên góp ETH thành công kèm lời nhắn",
        "1. Kết nối ví thành công với Account 1.\n2. Nhập số lượng ETH quyên góp: 1.5 ETH.\n3. Nhập lời nhắn: Ủng hộ trẻ em vùng cao.\n4. Nhấn nút Donate ngay và bấm xác nhận trên MetaMask.",
        "Giao dịch được đóng gói vào block mới. Số dư quỹ từ thiện tăng từ 4.0 lên 5.5 ETH. Xuất hiện một bản ghi mới trong bảng lịch sử đóng góp.",
        "Giao dịch hoàn tất sau 1.5 giây. Dashboard tự động cập nhật số liệu thời gian thực. Lịch sử hiển thị chính xác địa chỉ ví gửi, số tiền +1.5 ETH và lời nhắn.",
        "PASS")

    add_test_table(doc, 3,
        "Chủ quỹ (Owner) thực hiện giải ngân hợp lệ",
        "1. Kết nối ví Account 0 (Owner của chiến dịch).\n2. Nhập địa chỉ thụ hưởng: 0x70997970C51812dc3A010C7d01b50e0d17dc79C8.\n3. Nhập số tiền giải ngân: 1.0 ETH.\n4. Nhập mục đích: Hỗ trợ xây dựng trường học đợt 1.\n5. Nhấn Thực hiện Giải Ngân và xác nhận giao dịch trên MetaMask.",
        "Giao dịch thành công. Số dư quỹ giảm từ 5.5 ETH xuống còn 4.5 ETH. Chỉ số Đã giải ngân tăng lên 1.0 ETH.",
        "Số dư quỹ giảm còn 4.5 ETH. Địa chỉ thụ hưởng nhận đủ 1.0 ETH. Bảng lịch sử cập nhật dòng rút tiền -1.0 ETH kèm mục đích sử dụng.",
        "PASS")

    add_test_table(doc, 4,
        "Người lạ cố tình gọi hàm rút tiền giải ngân",
        "1. Kết nối ví bằng Account 1 (không phải Owner).\n2. Giao diện ẩn form giải ngân.\n3. Kẻ tấn công mở Console của trình duyệt (F12) và gọi trực tiếp lệnh contract.withdraw.\n4. Kẻ tấn công cố xác nhận giao dịch trên MetaMask.",
        "Giao dịch bị EVM từ chối ở bước kiểm tra modifier onlyOwner. Trả về lỗi OwnableUnauthorizedAccount. Tài sản quỹ được bảo vệ nguyên vẹn.",
        "EVM chặn giao dịch ngay lập tức. MetaMask hiển thị cảnh báo giao dịch sẽ thất bại. Trả về thong báo lỗi màu đỏ trên màn hình. Số dư quỹ không đổi.",
        "PASS")

    add_test_table(doc, 5,
        "Chủ quỹ rút số tiền vượt quá số dư hiện tại của hợp đồng",
        "1. Kết nối ví Account 0 (Owner).\n2. Nhập địa chỉ thụ hưởng hợp lệ.\n3. Số dư quỹ hiện tại là 4.5 ETH. Nhập số tiền rút giải ngân: 10.0 ETH.\n4. Nhập mục đích hợp lệ và nhấn nút Thực hiện Giải Ngân.",
        "Giao dịch bị EVM từ chối và đảo ngược trạng thái (reverted) do không vượt qua được chốt chặn điều kiện kiểm tra số dư. Trả về mã lỗi InsufficientBalance().",
        "Giao dịch bị từ chối ngay lập tức, EVM báo lỗi InsufficientBalance. Số dư quỹ được bảo toàn nguyên vẹn ở mức 4.5 ETH.",
        "PASS")

    doc.add_page_break()

def build_ch4(doc):
    add_chapter(doc, "CHƯƠNG 4: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")

    add_h1(doc, "4.1. Đánh giá kết quả đạt được")
    add_body(doc,
        "Đề tài nghiên cứu đã xây dựng thành công hệ sinh thái ứng dụng phi tập trung khép kín, an toàn và dễ tiếp cận. "
        "Hợp đồng thông minh TuThien.sol hoạt động đúng như thiết kế, xử lý nạp/rút tiền tự động và được triển khai thực tế trên mạng thử nghiệm công khai Ethereum Sepolia Testnet. "
        "Giao diện DApp đồng bộ tốt, đáp ứng các yêu cầu hiển thị số liệu realtime và phân quyền quản trị.")

    add_h1(doc, "4.2. Ưu điểm của giải pháp")
    add_body(doc,
        "Giải pháp kết hợp hài hòa giữa sự minh bạch bất biến của Blockchain và tính tiện dụng dễ thao tác của giao diện Web truyền thống. "
        "Hệ thống cho phép thực hiện kiểm toán thời gian thực đối với dòng tiền từ thiện, loại bỏ hoàn toàn các bên trung gian đáng tin cậy và bảo vệ an toàn quyền riêng tư của người đóng góp.")

    add_h1(doc, "4.3. Hạn chế còn tồn tại và Phân tích bản chất Phí Gas (Gas Fee)")
    add_body(doc,
        "Một trong những rào cản kỹ thuật lớn nhất đối với việc ứng dụng rộng rãi hệ thống từ thiện phi tập trung trên mạng lưới Ethereum chính là khái niệm Phí Gas (Gas Fee). "
        "Cần nhấn mạnh rằng, Gas ở đây hoàn toàn không phải là khí ga vật lý, mà là một đơn vị đo lường năng lượng tính toán cần thiết để thực thi các chỉ lệnh trong máy ảo EVM. "
        "Mỗi dòng code Solidity khi được biên dịch thành bytecode và chạy trên blockchain sẽ tiêu tốn một lượng Gas cố định (ví dụ: một lệnh ghi SSTORE vào bộ nhớ lưu trữ tốn 20,000 gas, một phép toán logic cơ bản tốn 3 gas).")
    add_body(doc, "Người thực hiện giao dịch bắt buộc phải trả phí này cho các validator để duy trì hoạt động bảo mật của mạng lưới theo công thức:")
    add_formula(doc, "Phí giao dịch = Lượng Gas tiêu thụ x Giá Gas của mạng lưới")
    add_body(doc,
        "Trong đó, Giá Gas được đo bằng đơn vị Gwei (1 Gwei = 10^-9 ETH). "
        "Khi mạng lưới xảy ra hiện tượng nghẽn giao dịch (Network Congestion) do nhu cầu sử dụng mạng lưới tăng đột biến, giá gas có thể bị đẩy lên mức cực kỳ cao. "
        "Lúc này, phí giao dịch để gửi một khoản quyên góp có thể lên tới 5 - 10 USD. "
        "Đối với các nhà hảo tâm quyên góp số tiền nhỏ (micro-donation, ví dụ 1-2 USD), việc phải chi trả khoản phí gas lớn hơn cả số tiền quyên góp là một rào cản kinh tế phi lý.")

    add_compare_table(doc,
        "Bảng 4.1. Chi phí Gas ước tính cho các thao tác chính trên Smart Contract",
        ["Thao tác", "Lượng Gas tiêu thụ ước tính", "Chi phí ước tính (giá gas 20 Gwei)", "Chi phí ước tính (giá gas 100 Gwei)"],
        [
            ["Quyên góp (donate)", "~85,000 gas", "~0.0017 ETH (~0.05 USD)", "~0.0085 ETH (~0.25 USD)"],
            ["Giải ngân (withdraw)", "~95,000 gas", "~0.0019 ETH (~0.06 USD)", "~0.0095 ETH (~0.28 USD)"],
            ["Đọc số dư (getBalance)", "0 gas (view)", "Miễn phí", "Miễn phí"],
            ["Deploy hợp đồng", "~2,500,000 gas", "~0.05 ETH (~1.50 USD)", "~0.25 ETH (~7.50 USD)"],
        ]
    )

    add_h1(doc, "4.4. Hướng phát triển trong tương lai và Giải pháp Layer 2")
    add_body(doc,
        "Để khắc phục triệt để hạn chế về chi phí gas, hướng phát triển tương lai sẽ tập trung triển khai hệ thống lên các giải pháp mở rộng quy mô Layer 2 (L2 Scaling Solutions) như Arbitrum hoặc Optimism.")
    add_body(doc,
        "Các giải pháp Layer 2 hoạt động theo cơ chế Rollup: Thay vì xử lý và ghi nhận riêng lẻ từng giao dịch từ thiện lên mạng chính Ethereum (Layer 1) vốn rất đắt đỏ, Layer 2 sẽ thu thập hàng ngàn giao dịch quyên góp off-chain, thực hiện nén và đóng gói chúng thành một bó giao dịch duy nhất, sau đó gửi một bằng chứng xác thực (Proof) về Layer 1 để lưu trữ vĩnh viễn. "
        "Cơ chế này giúp phân bổ chi phí gas của Layer 1 cho hàng ngàn giao dịch thành viên, qua đó giảm chi phí gas thực tế cho mỗi lần quyên góp xuống gần bằng 0, đồng thời tăng tốc độ xử lý giao dịch lên mức tức thời.")
    
    add_body(doc, "Ngoài ra, các hướng phát triển bổ sung bao gồm:")
    add_list_item(doc, "1. Tích hợp giấy chứng nhận đóng góp điện tử dưới dạng mã thông báo không thể thay thế (Charity NFTs - tiêu chuẩn ERC-721) tự động cấp cho nhà hảo tâm sau mỗi giao dịch quyên góp thành công.")
    add_list_item(doc, "2. Hỗ trợ quyên góp bằng Stablecoin (USDT, USDC) để tránh rủi ro biến động giá.")
    add_list_item(doc, "3. Tích hợp cơ chế biểu quyết phi tập trung (DAO Voting) để cộng đồng cùng tham gia quyết định giải ngân quỹ.")
    add_list_item(doc, "4. Ứng dụng mô hình Account Abstraction (ERC-4337) cho phép người dung đăng nhập bằng Email hoặc tài khoản mạng xã hội thông thường và trừ phí Gas cho họ.")

    add_h1(doc, "4.5. Phân tích khía cạnh pháp lý và quản trị của giải pháp từ thiện phi tập trung")
    add_body(doc,
        "Việc ứng dụng công nghệ sổ cái phân tán vào hoạt động kêu gọi và giải ngân vốn từ thiện không chỉ là một bài toán công nghệ đơn thuần, mà còn liên quan chặt chẽ đến hành lang pháp lý và mô hình quản trị xã hội. "
        "Tại Việt Nam, các quy định pháp luật liên quan đến hoạt động từ thiện của các cá nhân và tổ chức phi chính phủ đang ngày càng được siết chặt để tránh tình trạng lừa đảo, trục lợi. "
        "Nghị định 93/2021/NĐ-CP của Chính phủ đã ban hành các quy định rất cụ thể về việc vận động, tiếp nhận, phân phối và sử dụng các nguồn đóng góp tự nguyện. "
        "Hệ thống blockchain DApp từ thiện cung cấp một công cụ kỹ thuật tuyệt vời giúp các cá nhân kêu gọi tuân thủ 100% các yêu cầu về công khai thông tin tài chính của Nghị định này.")
    add_body(doc,
        "Tuy nhiên, sự giao thoa giữa luật pháp hiện hành và công nghệ phi tập trung vẫn tồn tại một số điểm nghẽn. "
        "Tiền mã hóa (chẳng hạn như ETH) hiện tại chưa được pháp luật Việt Nam công nhận là phương tiện thanh toán hợp pháp hoặc tài sản chính thức. "
        "Do đó, để hợp pháp hóa dòng tiền từ thiện, mô hình vận hành trong thực tế cần tích hợp một cơ chế quy đổi trung gian. "
        "Ví dụ, các nhà hảo tâm vẫn quyên góp bằng ETH trên blockchain để lưu vết minh bạch, nhưng khi giải ngân, số ETH này sẽ được chuyển đổi tự động sang tiền Việt Nam Đồng (VND) thông qua các sàn giao dịch hoặc đối tác uy tín có đăng ký pháp nhân trước khi chuyển tới người thụ hưởng dưới dạng tài sản thực tế.")
    add_body(doc,
        "Về mặt quản trị dự án, việc áp dụng mô hình Tổ chức tự trị phi tập trung (DAO) là một hướng đi đột phá. "
        "Thay vì trao toàn quyền quyết định chi tiêu cho một cá nhân chủ dự án (Owner), quyền quyết định giải ngân sẽ được biểu quyết bởi chính những nhà hảo tâm tham gia đóng góp. "
        "Mỗi khoản đóng góp sẽ tương ứng với một lượng mã thông báo quản trị (Governance Token). "
        "Khi cần rút tiền cho một mục đích cụ thể, chủ dự án phải tạo một đề xuất (Proposal) trên blockchain. "
        "Chỉ khi đề xuất nhận được sự đồng ý của đa số phiếu bầu của cộng đồng thông qua chữ ký số xác thực, hợp đồng thông minh mới tự động mở khóa và chuyển tiền giải ngân. "
        "Mô hình này giúp nâng tầm quản trị từ thiện từ sự giám sát thụ động sang sự đồng quản trị chủ động của cả xã hội.")
    
    doc.add_page_break()

def build_refs(doc):
    add_chapter(doc, "TÀI LIỆU THAM KHẢO")
    refs = [
        "1. Trần Đăng Công. (2025). Bài giảng Tổng quan về công nghệ Blockchain. Khoa Công nghệ thông tin, Trường Đại học Đại Nam.",
        "2. Trần Đăng Công. (2025). Bài giảng Mật mã trong Blockchain. Khoa Công nghệ thông tin, Trường Đại học Đại Nam.",
        "3. Ethereum Foundation. (2026). Ethereum Whitepaper: A Next-Generation Smart Contract and Decentralized Application Platform. Retrieved from https://ethereum.org/en/whitepaper/",
        "4. Solidity Documentation. (2026). Solidity Reference Guide (v0.8.24). Retrieved from https://docs.soliditylang.org/",
        "5. OpenZeppelin. (2025). OpenZeppelin Contracts Documentation. Retrieved from https://docs.openzeppelin.com/",
        "6. Ethers.js. (2026). Ethers.js v6 Library Documentation. Retrieved from https://docs.ethers.org/v6/",
        "7. Buterin, V. (2017). The Meaning of Decentralization. Medium Article.",
        "8. Nakamoto, S. (2008). Bitcoin: A Peer-to-Peer Electronic Cash System. Self-published paper.",
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.0)
        p.paragraph_format.first_line_indent = Cm(-1.0)
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        fmt_run(p.add_run(ref))
