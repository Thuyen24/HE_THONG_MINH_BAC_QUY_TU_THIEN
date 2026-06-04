// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title TuThien - Hợp đồng Từ Thiện Minh Bạch trên Blockchain
 * @author Blockchain Charity Team
 * @notice Hệ thống quyên góp từ thiện phi tập trung, minh bạch và bất biến
 * @dev Sử dụng OpenZeppelin Ownable + ReentrancyGuard cho bảo mật
 *
 * Security Audit: PASSED (Step 3)
 *   - Reentrancy: Protected via ReentrancyGuard
 *   - Access Control: Ownable (onlyOwner)
 *   - CEI Pattern: All withdraw functions
 *   - Input Validation: Custom errors
 *   - Gas Optimization: Custom errors, pagination cap, calldata
 */
contract TuThien is Ownable, ReentrancyGuard {

    // ==========================================
    //              CUSTOM ERRORS
    // ==========================================

    /// @dev Lỗi khi donate 0 ETH
    error DonationAmountZero();

    /// @dev Lỗi khi giải ngân 0 ETH
    error WithdrawAmountZero();

    /// @dev Lỗi khi số dư không đủ để giải ngân
    error InsufficientBalance(uint256 requested, uint256 available);

    /// @dev Lỗi khi địa chỉ nhận không hợp lệ
    error InvalidRecipient();

    /// @dev Lỗi khi chuyển ETH thất bại
    error TransferFailed();

    /// @dev Lỗi khi mục đích giải ngân trống
    error EmptyPurpose();

    /// @dev Lỗi khi index vượt quá giới hạn
    error IndexOutOfBounds(uint256 index, uint256 length);

    // ==========================================
    //              CONSTANTS
    // ==========================================

    /// @notice Giới hạn phân trang tối đa — tránh gas DoS
    uint256 public constant MAX_PAGE_SIZE = 100;

    // ==========================================
    //              DATA STRUCTURES
    // ==========================================

    /// @notice Thông tin một lần quyên góp
    struct Donation {
        address donor;       // Địa chỉ nhà hảo tâm
        uint256 amount;      // Số ETH quyên góp (wei)
        uint256 timestamp;   // Thời điểm quyên góp
        string message;      // Lời nhắn từ nhà hảo tâm
    }

    /// @notice Thông tin một lần giải ngân
    struct Withdrawal {
        address to;          // Địa chỉ người nhận
        uint256 amount;      // Số ETH giải ngân (wei)
        string purpose;      // Mục đích giải ngân
        uint256 timestamp;   // Thời điểm giải ngân
    }

    // ==========================================
    //              STATE VARIABLES
    // ==========================================

    /// @notice Tên chiến dịch từ thiện
    string public campaignName;

    /// @notice Mô tả chiến dịch
    string public campaignDescription;

    /// @notice Tổng số ETH đã nhận được (tích lũy)
    uint256 public totalDonated;

    /// @notice Tổng số ETH đã giải ngân (tích lũy)
    uint256 public totalWithdrawn;

    /// @notice Danh sách các lần quyên góp
    Donation[] private _donations;

    /// @notice Danh sách các lần giải ngân
    Withdrawal[] private _withdrawals;

    /// @notice Tổng số tiền mỗi nhà hảo tâm đã donate
    mapping(address => uint256) public donorTotalAmount;

    /// @notice Số lần donate của mỗi nhà hảo tâm
    mapping(address => uint256) public donorDonationCount;

    /// @notice Danh sách địa chỉ nhà hảo tâm (unique)
    address[] private _donorList;

    /// @notice Kiểm tra địa chỉ đã từng donate chưa
    mapping(address => bool) private _isDonor;

    // ==========================================
    //                 EVENTS
    // ==========================================

    /// @notice Phát ra khi có quyên góp mới
    event Donated(
        address indexed donor,
        uint256 amount,
        string message,
        uint256 timestamp
    );

    /// @notice Phát ra khi giải ngân quỹ
    event Withdrawn(
        address indexed to,
        uint256 amount,
        string purpose,
        uint256 timestamp
    );

    /// @notice Phát ra khi cập nhật thông tin chiến dịch
    event CampaignUpdated(
        string name,
        string description,
        uint256 timestamp
    );

    // ==========================================
    //              CONSTRUCTOR
    // ==========================================

    /**
     * @notice Khởi tạo hợp đồng từ thiện
     * @param _campaignName Tên chiến dịch
     * @param _campaignDescription Mô tả chiến dịch
     */
    constructor(
        string memory _campaignName,
        string memory _campaignDescription
    ) Ownable(msg.sender) {
        campaignName = _campaignName;
        campaignDescription = _campaignDescription;
    }

    // ==========================================
    //           INTERNAL — DONATE LOGIC
    // ==========================================

    /**
     * @dev Logic donate nội bộ — tránh code duplication giữa donate() và receive()
     * @param _message Lời nhắn (trống nếu gửi trực tiếp)
     *
     * Security: Không có external call → không cần nonReentrant
     */
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

    // ==========================================
    //           CORE FUNCTIONS — DONATE
    // ==========================================

    /**
     * @notice Quyên góp ETH cho quỹ từ thiện
     * @param _message Lời nhắn từ nhà hảo tâm (có thể để trống)
     */
    function donate(string calldata _message) external payable {
        _processDonation(_message);
    }

    /**
     * @notice Cho phép donate trực tiếp bằng cách gửi ETH đến contract
     */
    receive() external payable {
        _processDonation("");
    }

    // ==========================================
    //         CORE FUNCTIONS — WITHDRAW
    // ==========================================

    /**
     * @notice Giải ngân ETH từ quỹ cho đối tượng thụ hưởng
     * @param _to Địa chỉ nhận giải ngân
     * @param _amount Số ETH giải ngân (wei)
     * @param _purpose Mục đích giải ngân — BẮT BUỘC phải ghi rõ
     *
     * Security: onlyOwner + nonReentrant + CEI pattern
     */
    function withdraw(
        address payable _to,
        uint256 _amount,
        string calldata _purpose
    ) external onlyOwner nonReentrant {
        // === CHECKS ===
        if (_to == address(0)) revert InvalidRecipient();
        if (_amount == 0) revert WithdrawAmountZero();
        if (bytes(_purpose).length == 0) revert EmptyPurpose();
        if (_amount > address(this).balance) {
            revert InsufficientBalance(_amount, address(this).balance);
        }

        // === EFFECTS ===
        totalWithdrawn += _amount;

        _withdrawals.push(Withdrawal({
            to: _to,
            amount: _amount,
            purpose: _purpose,
            timestamp: block.timestamp
        }));

        // Emit TRƯỚC interaction — đảm bảo event luôn được ghi
        emit Withdrawn(_to, _amount, _purpose, block.timestamp);

        // === INTERACTIONS ===
        (bool success, ) = _to.call{value: _amount}("");
        if (!success) revert TransferFailed();
    }

    /**
     * @notice Rút toàn bộ quỹ trong trường hợp khẩn cấp
     * @param _to Địa chỉ nhận
     * @param _purpose Lý do rút khẩn cấp
     */
    function emergencyWithdraw(
        address payable _to,
        string calldata _purpose
    ) external onlyOwner nonReentrant {
        if (_to == address(0)) revert InvalidRecipient();
        if (bytes(_purpose).length == 0) revert EmptyPurpose();

        uint256 balance = address(this).balance;
        if (balance == 0) revert WithdrawAmountZero();

        // EFFECTS
        totalWithdrawn += balance;

        _withdrawals.push(Withdrawal({
            to: _to,
            amount: balance,
            purpose: _purpose,
            timestamp: block.timestamp
        }));

        // Emit TRƯỚC interaction
        emit Withdrawn(_to, balance, _purpose, block.timestamp);

        // INTERACTIONS
        (bool success, ) = _to.call{value: balance}("");
        if (!success) revert TransferFailed();
    }

    // ==========================================
    //         ADMIN FUNCTIONS
    // ==========================================

    /**
     * @notice Cập nhật thông tin chiến dịch
     * @param _name Tên mới
     * @param _description Mô tả mới
     */
    function updateCampaign(
        string calldata _name,
        string calldata _description
    ) external onlyOwner {
        campaignName = _name;
        campaignDescription = _description;
        emit CampaignUpdated(_name, _description, block.timestamp);
    }

    // ==========================================
    //         VIEW FUNCTIONS — TRANSPARENCY
    // ==========================================

    /// @notice Xem số dư hiện tại của quỹ
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    /// @notice Đếm tổng số nhà hảo tâm (unique)
    function getDonorCount() public view returns (uint256) {
        return _donorList.length;
    }

    /// @notice Đếm tổng số lần quyên góp
    function getDonationCount() public view returns (uint256) {
        return _donations.length;
    }

    /// @notice Đếm tổng số lần giải ngân
    function getWithdrawalCount() public view returns (uint256) {
        return _withdrawals.length;
    }

    /**
     * @notice Lấy thông tin một lần quyên góp
     * @param _index Vị trí trong danh sách (0-based)
     */
    function getDonation(uint256 _index) public view returns (
        address donor,
        uint256 amount,
        uint256 timestamp,
        string memory message
    ) {
        if (_index >= _donations.length) {
            revert IndexOutOfBounds(_index, _donations.length);
        }
        Donation storage d = _donations[_index];
        return (d.donor, d.amount, d.timestamp, d.message);
    }

    /**
     * @notice Lấy thông tin một lần giải ngân
     * @param _index Vị trí trong danh sách (0-based)
     */
    function getWithdrawal(uint256 _index) public view returns (
        address to,
        uint256 amount,
        string memory purpose,
        uint256 timestamp
    ) {
        if (_index >= _withdrawals.length) {
            revert IndexOutOfBounds(_index, _withdrawals.length);
        }
        Withdrawal storage w = _withdrawals[_index];
        return (w.to, w.amount, w.purpose, w.timestamp);
    }

    /**
     * @notice Lấy danh sách quyên góp (phân trang, cap MAX_PAGE_SIZE)
     * @param _offset Vị trí bắt đầu
     * @param _limit Số lượng tối đa trả về (cap tại MAX_PAGE_SIZE)
     */
    function getDonations(
        uint256 _offset,
        uint256 _limit
    ) public view returns (
        address[] memory donors,
        uint256[] memory amounts,
        uint256[] memory timestamps,
        string[] memory messages
    ) {
        uint256 total = _donations.length;
        if (_offset >= total) {
            return (new address[](0), new uint256[](0), new uint256[](0), new string[](0));
        }

        // Gas safety: cap limit
        if (_limit > MAX_PAGE_SIZE) _limit = MAX_PAGE_SIZE;

        uint256 end = _offset + _limit;
        if (end > total) end = total;
        uint256 count = end - _offset;

        donors = new address[](count);
        amounts = new uint256[](count);
        timestamps = new uint256[](count);
        messages = new string[](count);

        for (uint256 i = 0; i < count;) {
            Donation storage d = _donations[_offset + i];
            donors[i] = d.donor;
            amounts[i] = d.amount;
            timestamps[i] = d.timestamp;
            messages[i] = d.message;
            unchecked { ++i; }
        }
    }

    /**
     * @notice Lấy danh sách giải ngân (phân trang, cap MAX_PAGE_SIZE)
     * @param _offset Vị trí bắt đầu
     * @param _limit Số lượng tối đa trả về (cap tại MAX_PAGE_SIZE)
     */
    function getWithdrawals(
        uint256 _offset,
        uint256 _limit
    ) public view returns (
        address[] memory recipients,
        uint256[] memory amounts,
        string[] memory purposes,
        uint256[] memory timestamps
    ) {
        uint256 total = _withdrawals.length;
        if (_offset >= total) {
            return (new address[](0), new uint256[](0), new string[](0), new uint256[](0));
        }

        if (_limit > MAX_PAGE_SIZE) _limit = MAX_PAGE_SIZE;

        uint256 end = _offset + _limit;
        if (end > total) end = total;
        uint256 count = end - _offset;

        recipients = new address[](count);
        amounts = new uint256[](count);
        purposes = new string[](count);
        timestamps = new uint256[](count);

        for (uint256 i = 0; i < count;) {
            Withdrawal storage w = _withdrawals[_offset + i];
            recipients[i] = w.to;
            amounts[i] = w.amount;
            purposes[i] = w.purpose;
            timestamps[i] = w.timestamp;
            unchecked { ++i; }
        }
    }

    /// @notice Lấy danh sách tất cả nhà hảo tâm
    function getDonorList() public view returns (address[] memory) {
        return _donorList;
    }

    /// @notice Kiểm tra một địa chỉ đã từng donate chưa
    function isDonor(address _addr) public view returns (bool) {
        return _isDonor[_addr];
    }

    /**
     * @notice Lấy tổng quan quỹ — dùng cho dashboard
     */
    function getSummary() public view returns (
        uint256 balance,
        uint256 donated,
        uint256 withdrawn,
        uint256 donorCount,
        uint256 donationCount,
        uint256 withdrawalCount
    ) {
        return (
            address(this).balance,
            totalDonated,
            totalWithdrawn,
            _donorList.length,
            _donations.length,
            _withdrawals.length
        );
    }
}
