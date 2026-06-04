# 🎓 TÀI LIỆU ÔN TẬP VẤN ĐÁP BẢO VỆ ĐỒ ÁN TỐT NGHIỆP
### Đề tài: Ứng dụng Blockchain trong việc minh bạch hóa quy trình kêu gọi và giải ngân vốn từ thiện
**Tác giả:** Đỗ Văn Thuyên — Sinh viên K16 — MSV: 1671020308  
**Đơn vị:** Khoa Công nghệ thông tin - Trường Đại học Đại Nam  
**Giáo viên hướng dẫn:** TS. Trần Đăng Công  

---

## Ⅰ. Tổng quan Luồng hoạt động hệ thống (System Workflow)

### 1. Luồng đi của Tiền (ETH) và Dữ liệu
Khi một nhà hảo tâm quyên góp tiền qua hệ thống, quy trình diễn ra tuần tự qua các lớp kiến trúc như sau:
1.  **Tương tác ở Presentation Layer (Frontend):** 
    Nhà hảo tâm nhập số tiền quyên góp (ví dụ: `0.5 ETH`) và lời nhắn gửi đi, sau đó bấm nút **"Quyên góp"**. Giao diện React/JS sử dụng thư viện `Ethers.js v6` để tạo một yêu cầu giao dịch Web3.
2.  **Ký duyệt qua Wallet Layer (MetaMask):** 
    MetaMask chặn yêu cầu này và hiển thị cửa sổ popup yêu cầu người dùng xác nhận. MetaMask hiển thị rõ lượng ETH cần gửi và ước lượng phí gas. Khi người dùng ký duyệt (Sign), MetaMask sử dụng **khóa bí mật (Private Key)** được lưu trữ an toàn trong trình duyệt để ký và phát transaction lên mạng lưới RPC Node.
3.  **Tương tác với Smart Contract trên Sepolia Testnet:** 
    Giao dịch đã ký được truyền đến mạng lưới Ethereum Sepolia. Các máy đào / Validator tiếp nhận giao dịch và đưa vào block để xử lý. EVM (Ethereum Virtual Machine) giải nén bytecode và gọi hàm `donate(string memory _message)` của hợp đồng `TuThien.sol`.
4.  **Thay đổi trạng thái và Cập nhật sổ cái (State Update):** 
    Smart contract thực hiện kiểm tra điều kiện, nếu hợp lệ sẽ cộng số dư trực tiếp vào địa chỉ ví của hợp đồng (`address(this).balance`) và ghi nhận lịch sử vào biến trạng thái (State Variables). Toàn bộ luồng tiền và lịch sử được ghi vĩnh viễn vào các Block mới của Blockchain.
5.  **Cập nhật giao diện thông qua Events:** 
    Sau khi block được confirm, Smart Contract phát ra (emit) một Event `Donated(...)`. Frontend lắng nghe sự kiện này và tự động render lại giao diện: cập nhật tổng tiền quỹ, danh sách nhà hảo tâm và bảng lịch sử giao dịch thời gian thực mà không cần người dùng tải lại trang.

### 2. Tại sao luồng này an toàn và không thể bị thao túng?
*   **Bất biến (Immutability):** Dữ liệu một khi đã ghi vào Blockchain Sepolia thì không một ai, kể cả chủ sở hữu (Owner) của hợp đồng hay lập trình viên hệ thống, có thể sửa đổi hay xóa bỏ. Không tồn tại cơ chế `UPDATE` hay `DELETE` như cơ sở dữ liệu truyền thống (SQL/NoSQL).
*   **Trustless (Không cần đặt niềm tin vào trung gian):** Tiền cứu trợ được khóa trực tiếp trong mã nguồn của Smart Contract chứ không nằm trong tài khoản ngân hàng cá nhân. Luồng tiền chỉ ra khỏi contract thông qua các quy tắc logic toán học được quy định sẵn trong hàm `withdraw`.
*   **Bảo mật Private Key:** Khóa bí mật của người dùng nằm an toàn trong ví MetaMask và không bao giờ được gửi lên server hay lộ ra ngoài, tránh việc bị giả mạo chữ ký giao dịch.

---

## Ⅱ. Phân tích sâu chức năng Quyên góp (Donate Function)

### 1. Vai trò và ý nghĩa của thuộc tính `payable`
*   **Vai trò:** Cho phép hàm tiếp nhận tiền điện tử (ở đây là đồng ETH) gửi kèm theo giao dịch.
*   **Bản chất kỹ thuật:** Trong Solidity, nếu một hàm không được khai báo từ khóa `payable` mà người dùng cố tình gửi ETH kèm theo giao dịch (giá trị `msg.value > 0`), máy ảo EVM sẽ ngay lập tức **từ chối giao dịch (revert)** để bảo vệ tiền của người dùng không bị mất oan.

### 2. Logic kỹ thuật của từng bước thực thi trong hàm `_processDonation`
Hàm quyên góp cốt lõi được cài đặt thông qua hàm nội bộ (private helper) `_processDonation`:

```solidity
function _processDonation(string memory _message) private {
    if (msg.value == 0) revert DonationAmountZero();

    // Cập nhật state
    totalDonated += msg.value;
    donorTotalAmount[msg.sender] += msg.value;
    donorDonationCount[msg.sender] += 1;

    // Thêm vào danh sách nhà hảo tâm nếu chưa có
    if (!_isDonor[msg.sender]) {
        _isDonor[msg.sender] = true;
        _donorList.push(msg.sender);
    }

    // Lưu thông tin donation
    _donations.push(Donation({
        donor: msg.sender,
        amount: msg.value,
        timestamp: block.timestamp,
        message: _message
    }));

    emit Donated(msg.sender, msg.value, _message, block.timestamp);
}
```

*   **Bước 1 (Kiểm tra đầu vào):** `if (msg.value == 0) revert DonationAmountZero();`
    Đảm bảo lượng ETH gửi vào phải lớn hơn 0. Nếu bằng 0, giao dịch bị hủy ngay lập tức để tránh làm nghẽn mạng và tốn phí gas vô ích.
*   **Bước 2 (Cập nhật số liệu lũy kế):** 
    Cộng dồn giá trị quyên góp vào tổng số tiền quỹ (`totalDonated`), tăng số dư đã quyên góp của ví gửi (`donorTotalAmount[msg.sender]`) và tăng tổng số lần quyên góp của tài khoản đó.
*   **Bước 3 (Quản lý danh sách duy nhất):** `if (!_isDonor[msg.sender])`
    Sử dụng ánh xạ kiểm tra nhanh $O(1)$ để xem ví này đã từng quyên góp chưa. Nếu chưa từng, đánh dấu lại và đưa địa chỉ ví này vào mảng `_donorList` (dùng để hiển thị danh sách nhà hảo tâm).
*   **Bước 4 (Lưu vết lịch sử):** `_donations.push(...)`
    Khởi tạo struct `Donation` chứa đầy đủ thông tin giao dịch (địa chỉ ví, số lượng wei, mốc thời gian block, lời nhắn) và đẩy vào mảng động để lưu trữ.
*   **Bước 5 (Kích hoạt Event):** `emit Donated(...)`
    Phát ra sự kiện ghi nhận giao dịch lên log của Blockchain, phục vụ cho việc cập nhật frontend theo thời gian thực.

### 3. Tối ưu Gas: Tại sao dùng `revert CustomError()` thay vì `require()`?
*   **Cú pháp cũ:** `require(msg.value > 0, "Donation amount must be greater than zero");`
*   **Bản chất hao phí gas:** Khi sử dụng `require` kèm chuỗi thông báo lỗi dạng String, Solidity bắt buộc phải biên dịch chuỗi ký tự đó và lưu giữ nó trong mã máy của hợp đồng. Điều này làm tăng kích thước bytecode (tốn gas deploy) và tốn gas thực thi để phân tích chuỗi string khi có lỗi xảy ra.
*   **Giải pháp Custom Errors:** `error DonationAmountZero();` kết hợp `revert DonationAmountZero();` chỉ biên dịch ra một mã nhận diện lỗi dài **4 byte** (chuyển đổi từ mã băm SHA-3 của tên lỗi). Điều này giúp tiết kiệm tối đa dung lượng lưu trữ của contract trên blockchain và tiết kiệm khoảng **200 - 400 gas** cho mỗi lần giao dịch thất bại.

---

## Ⅲ. Phân tích sâu chức năng Giải ngân (Withdraw Function)

### 1. Vai trò và quyền hạn tối cao
*   **Quyền hạn:** Hàm `withdraw` được bảo vệ bằng modifier `onlyOwner`. Chỉ có địa chỉ ví của Admin (người khởi tạo chiến dịch) mới được phép kích hoạt hàm này. Bất cứ ví nào khác gọi hàm sẽ bị chặn ngay lập tức.
*   **Vai trò:** Thực hiện rút một khoản ETH cụ thể từ quỹ để gửi trực tiếp đến địa chỉ thụ hưởng (nhà cung cấp vật tư, người nghèo, bệnh viện...) kèm theo mục đích rõ ràng phục vụ mục tiêu minh bạch.

### 2. Quy tắc bảo mật CEI (Checks - Effects - Interactions)
Đây là quy chuẩn bảo mật sống còn của lập trình Smart Contract để chống lại tấn công tái nhập (**Reentrancy Attack**). Hàm `withdraw` được thiết kế nghiêm ngặt theo quy trình:

```solidity
function withdraw(
    address payable _to,
    uint256 _amount,
    string calldata _purpose
) external onlyOwner nonReentrant {
    // === CHECKS (Kiểm tra điều kiện) ===
    if (_to == address(0)) revert InvalidRecipient();
    if (_amount == 0) revert WithdrawAmountZero();
    if (bytes(_purpose).length == 0) revert EmptyPurpose();
    if (_amount > address(this).balance) {
        revert InsufficientBalance(_amount, address(this).balance);
    }

    // === EFFECTS (Thay đổi trạng thái nội bộ) ===
    totalWithdrawn += _amount;

    _withdrawals.push(Withdrawal({
        to: _to,
        amount: _amount,
        purpose: _purpose,
        timestamp: block.timestamp
    }));

    emit Withdrawn(_to, _amount, _purpose, block.timestamp);

    // === INTERACTIONS (Tương tác bên ngoài) ===
    (bool success, ) = _to.call{value: _amount}("");
    if (!success) revert TransferFailed();
}
```

*   **Checks (Kiểm tra):** Xác thực đầu vào (ví nhận không rỗng, tiền rút lớn hơn 0, lý do giải ngân không để trống) và kiểm tra số dư quỹ hiện tại có đủ để giải ngân hay không.
*   **Effects (Cập nhật trạng thái):** Cập nhật tổng số tiền đã rút (`totalWithdrawn`) và ghi nhận giao dịch giải ngân vào lịch sử **TRƯỚC KHI chuyển tiền đi**.
*   **Interactions (Tương tác chuyển tiền):** Thực hiện lệnh gửi ETH thực tế ra bên ngoài thông qua lệnh `call`.

#### ⚠️ Điều gì xảy ra nếu đảo ngược thứ tự (Chuyển tiền trước, Cập nhật trạng thái sau)?
If chúng ta chuyển tiền trước bằng lệnh `call`, máy ảo EVM sẽ tạm dừng thực thi tại Smart Contract của chúng ta để chuyển luồng điều khiển sang địa chỉ ví nhận. Nếu ví nhận là một **Smart Contract độc hại**, hàm `receive()` hoặc `fallback()` của nó có thể viết mã lệnh gọi ngược lại (reenter) hàm `withdraw` của chúng ta. 
Do trạng thái số dư quỹ và lịch sử rút tiền chưa kịp cập nhật, chốt chặn kiểm tra số dư (`_amount > address(this).balance`) vẫn tiếp tục thông qua và tiền lại tiếp tục được chuyển đi. Vòng lặp đệ quy này sẽ rút cạn toàn bộ số tiền có trong quỹ từ thiện của chúng ta trong vòng một giao dịch duy nhất.

### 3. Tại sao lại dùng lệnh cấp thấp `call` thay vì `transfer` hay `send`?
Trong các phiên bản Solidity cũ, hàm `transfer` (giới hạn cứng 2300 gas) thường được khuyến nghị sử dụng vì tính an toàn. Tuy nhiên, trong Solidity hiện đại:
*   **Hạn chế của `transfer`:** Nếu ví nhận tiền là một ví Multisig (ví đa chữ ký) hoặc một Smart Contract trung gian (ví dụ: ví Gnosis Safe, ví Account Abstraction), việc xử lý nhận tiền của chúng đòi hỏi tiêu tốn nhiều hơn 2300 gas. Sử dụng `transfer` sẽ khiến giao dịch luôn bị thất bại (out of gas) và không thể chuyển tiền được.
*   **Ưu thế của `call`:** Lệnh `(bool success, ) = _to.call{value: _amount}("")` chuyển tiếp toàn bộ lượng gas còn lại của giao dịch sang ví nhận, cho phép chuyển tiền thành công tới mọi loại ví mà không sợ bị nghẽn gas. Mối nguy hiểm reentrancy của lệnh `call` đã được phòng ngừa tuyệt đối nhờ vào bổ trợ **CEI Pattern** và modifier **`nonReentrant`** của thư viện OpenZeppelin.

---

## Ⅳ. Bộ câu hỏi hiểm hóc thường gặp (Hội đồng bẫy) & Cách trả lời ăn điểm

### ❓ Câu 1 (Bẫy về tính minh bạch của Admin):
> **Thầy cô hỏi:** *"Em nói hệ thống minh bạch 100%, vậy nếu Admin (Owner) thông đồng với người thụ hưởng, rút hết tiền cứu trợ để tiêu xài cá nhân thì Blockchain làm sao ngăn cản được?"*

*   **Cách trả lời ăn điểm:**
    "Thưa thầy cô, Blockchain là công nghệ **ghi nhận lịch sử và thực thi logic khách quan**, nó không thể thay thế đạo đức con người nhưng nó **bắt buộc con người phải để lại dấu vết không thể xóa nhòa**. 
    Hàm `withdraw` yêu cầu tham số bắt buộc là mô tả mục đích giải ngân (`_purpose`). Khi Admin thực hiện rút tiền, toàn bộ địa chỉ ví nhận giải ngân, số tiền, mốc thời gian và mục đích giải ngân đều được lưu vĩnh viễn trên Blockchain. Công chúng và nhà hảo tâm có thể phát hiện ngay lập tức sự bất thường này trên trang Dashboard. 
    Để nâng cao tính bảo mật và kiểm soát quyền hạn rút tiền trong thực tế, thay vì đặt quyền sở hữu hợp đồng (`Owner`) cho một cá nhân đơn lẻ, chúng ta có thể chuyển quyền `Owner` cho một **ví đa chữ ký (Multisig Wallet - như Gnosis Safe)** do đại diện của nhiều bên (nhà tài trợ, kiểm toán, chính quyền địa phương) cùng quản lý. Khi đó, lệnh giải ngân chỉ được thực thi khi có sự ký duyệt đồng thuận của đa số thành viên."

### ❓ Câu 2 (Bẫy về Thư viện OpenZeppelin):
> **Thầy cô hỏi:** *"Tại sao em lại dùng thư viện `Ownable` và `ReentrancyGuard` của OpenZeppelin mà không tự viết? Bản chất của modifier `nonReentrant` hoạt động bên dưới như thế nào?"*

*   **Cách trả lời ăn điểm:**
    "Thưa thầy cô, OpenZeppelin là tiêu chuẩn công nghiệp được kiểm định an toàn (security audited) bởi hàng triệu lập trình viên trên thế giới. Sử dụng thư viện giúp giảm thiểu tối đa các lỗi bảo mật tiềm ẩn và tuân thủ các chuẩn chung.
    *   `Ownable` giúp phân quyền kiểm soát truy cập (Access Control) một cách chuẩn hóa thông qua biến `_owner` và modifier `onlyOwner`.
    *   Modifier `nonReentrant` của thư viện `ReentrancyGuard` hoạt động dựa trên cơ chế **khóa trạng thái (Mutex Lock)**. Bên trong thư viện, nó định nghĩa một biến trạng thái kiểu số nguyên (ví dụ: `_status`). Khi bắt đầu vào hàm có gắn `nonReentrant`, biến này được chuyển từ trạng thái `NOT_ENTERED` (1) sang `ENTERED` (2). Khi kết thúc hàm, trạng thái được chuyển về lại `NOT_ENTERED`. Nếu có bất kỳ cuộc gọi tái nhập nào cố tình gọi lại hàm khi trạng thái vẫn đang là `ENTERED`, giao dịch sẽ bị revert ngay lập tức. Cơ chế này khóa chặt mọi nỗ lực tấn công đệ quy."

### ❓ Câu 3 (Bẫy về Giới hạn Hệ thống & Gas fee):
> **Thầy cô hỏi:** *"Nếu hệ thống của em có hàng chục nghìn lượt quyên góp, việc hiển thị toàn bộ lịch sử giao dịch lên Frontend có bị lỗi gì không và Smart Contract có bị nghẽn gas không?"*

*   **Cách trả lời ăn điểm:**
    "Thưa thầy cô, nếu chúng ta viết hàm trả về toàn bộ danh sách mảng động `_donations` cùng lúc, khi số lượng phần tử tăng lên quá lớn, giao dịch truy vấn sẽ tiêu tốn quá nhiều tài nguyên máy ảo EVM và gây ra lỗi **Out of Gas (hết gas)** hoặc làm trình duyệt bị đơ.
    Để giải quyết triệt để lỗi nghẽn gas này, trong Smart Contract em đã thiết kế các hàm view hỗ trợ **phân trang (Pagination)** là `getDonations(uint256 _offset, uint256 _limit)` và `getWithdrawals(...)` kèm theo biến giới hạn tối đa `MAX_PAGE_SIZE = 100`. 
    Mỗi khi Frontend truy vấn, nó chỉ yêu cầu đọc một lượng nhỏ dữ liệu (ví dụ: 10 hoặc 20 bản ghi mỗi lần dựa trên vị trí `_offset`). Cơ chế này đảm bảo thời gian phản hồi nhanh, tiết kiệm băng thông và loại bỏ hoàn toàn nguy cơ lỗi Out of Gas khi hệ thống mở rộng quy mô."

### ❓ Câu 4 (Bẫy về tính riêng tư và lưu trữ dữ liệu):
> **Thầy cô hỏi:** *"Tại sao em không lưu luôn hình ảnh hóa đơn giải ngân hoặc các tệp chứng từ trực tiếp lên Blockchain mà chỉ lưu chuỗi mô tả string?"*

*   **Cách trả lời ăn điểm:**
    "Thưa thầy cô, lưu trữ dữ liệu trên Blockchain cực kỳ đắt đỏ vì mọi nút mạng trên toàn cầu đều phải lưu lại bản sao của dữ liệu đó. Theo ước tính, lưu trữ 1 Megabyte dữ liệu trên Ethereum có thể tốn hàng chục nghìn USD phí gas.
    Do đó, giải pháp tối ưu kiến trúc Web3 là:
    1.  Chỉ lưu trữ các dữ liệu định danh cốt lõi (Số tiền, địa chỉ ví, mốc thời gian, mã băm giao dịch) trực tiếp trên Blockchain.
    2.  Các file chứng từ nặng như ảnh hóa đơn, video giải ngân sẽ được lưu trữ phi tập trung trên mạng **IPFS (InterPlanetary File System)** hoặc các dịch vụ đám mây an toàn. Hợp đồng thông minh sẽ chỉ lưu trữ **mã băm duy nhất (CID IPFS)** của file đó để tham chiếu, vừa đảm bảo tính xác thực thông tin, vừa tối ưu chi phí vận hành hệ thống."
