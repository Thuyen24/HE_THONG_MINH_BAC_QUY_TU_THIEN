/**
 * Blockchain Charity System — Frontend App
 * Kết nối MetaMask + tương tác TuThien contract
 *
 * Fix v2:
 *  - Expose tất cả hàm lên window rõ ràng sau DOMContentLoaded
 *  - Kiểm tra network ID, tự động yêu cầu đổi sang Hardhat localhost
 *  - Hiển thị lỗi chi tiết hơn (bao gồm custom errors từ contract)
 *  - Thêm nút "Thử lại" khi loadData thất bại
 *  - Xử lý trường hợp MetaMask đang ở sai mạng
 */
import { CONTRACT_ADDRESS, CONTRACT_ABI } from './contract.js';

// ── Constants ────────────────────────────────────────────────
const RPC_URL         = "http://127.0.0.1:8545";
const HARDHAT_CHAIN_ID = "0x7a69";  // 31337 decimal = Hardhat localhost

let provider, signer, contract, userAddress;
let isOwnerFlag = false;

// Read-only provider — dùng để load dữ liệu mà không cần MetaMask
let readProvider = null;
let readContract = null;

function initReadProvider() {
  try {
    readProvider = new ethers.JsonRpcProvider(RPC_URL);
    readContract = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, readProvider);
    return true;
  } catch (e) {
    console.warn("Read provider init failed:", e.message);
    return false;
  }
}

// ── Decode custom errors từ contract ────────────────────────
function decodeError(e) {
  const msg = e?.reason || e?.data?.message || e?.message || "Lỗi không xác định";
  const fullStr = JSON.stringify(e) + msg;

  if (msg.includes("DonationAmountZero") || msg.includes("value out-of-range"))
    return "Số ETH phải lớn hơn 0.";
  if (msg.includes("user rejected") || msg.includes("ACTION_REJECTED"))
    return "Bạn đã huỷ giao dịch trong MetaMask.";
  if (msg.includes("insufficient funds"))
    return "Số dư ví không đủ để thực hiện giao dịch.";
  if (msg.includes("network") || msg.includes("could not detect"))
    return "Không kết nối được với mạng blockchain. Hãy chắc chắn Hardhat node đang chạy.";
  if (msg.includes("nonce"))
    return "Lỗi nonce. Hãy reset account trong MetaMask (Settings → Advanced → Reset Account).";
  // Withdraw-specific errors
  if (fullStr.includes("OwnableUnauthorizedAccount"))
    return "Chỉ tài khoản Owner mới có quyền giải ngân. Hãy kết nối đúng ví Owner.";
  if (fullStr.includes("InsufficientBalance"))
    return "Số dư quỹ không đủ để giải ngân số tiền này.";
  if (fullStr.includes("InvalidRecipient"))
    return "Địa chỉ người nhận không hợp lệ (không được là 0x0).";
  if (fullStr.includes("EmptyPurpose"))
    return "Mục đích giải ngân không được để trống.";
  if (fullStr.includes("WithdrawAmountZero"))
    return "Số ETH giải ngân phải lớn hơn 0.";
  if (fullStr.includes("TransferFailed"))
    return "Giao dịch chuyển ETH thất bại. Kiểm tra địa chỉ người nhận.";

  return msg.length > 120 ? msg.slice(0, 120) + "..." : msg;
}

// ── Kiểm tra và chuyển MetaMask sang Hardhat localhost ──────
async function ensureCorrectNetwork() {
  if (!window.ethereum) return false;
  try {
    const chainId = await window.ethereum.request({ method: "eth_chainId" });
    if (chainId === HARDHAT_CHAIN_ID) {
      updateNetworkBadge(true);
      return true;
    }

    updateNetworkBadge(false);

    try {
      // Thu 1: switch sang mạng đã có
      await window.ethereum.request({
        method: "wallet_switchEthereumChain",
        params: [{ chainId: HARDHAT_CHAIN_ID }],
      });
    } catch (switchErr) {
      if (switchErr.code === 4902) {
        // Mạng chưa có → thêm vào MetaMask rồi switch
        await window.ethereum.request({
          method: "wallet_addEthereumChain",
          params: [{
            chainId: HARDHAT_CHAIN_ID,
            chainName: "Hardhat Localhost 8545",
            nativeCurrency: { name: "Ether", symbol: "ETH", decimals: 18 },
            rpcUrls: ["http://127.0.0.1:8545"],
          }],
        });
        // Sau khi add, switch thại lần 2
        await window.ethereum.request({
          method: "wallet_switchEthereumChain",
          params: [{ chainId: HARDHAT_CHAIN_ID }],
        });
      } else {
        throw switchErr;
      }
    }

    // Xác nhận lại sau khi switch
    const newChain = await window.ethereum.request({ method: "eth_chainId" });
    const ok = newChain === HARDHAT_CHAIN_ID;
    updateNetworkBadge(ok);
    if (!ok) showToast("⚠️ Vẫn chưa đúng mạng. Hãy chọn \"Hardhat Localhost\" trong MetaMask.", "error");
    return ok;
  } catch (e) {
    if (e.code === 4001) {
      showToast("Đã huỷ đổi mạng.", "info");
    } else {
      showToast("Lỗi đổi mạng: " + decodeError(e), "error");
    }
    updateNetworkBadge(false);
    return false;
  }
}

function updateNetworkBadge(isCorrect) {
  const badge = document.getElementById("networkBadge");
  if (!badge) return;
  if (isCorrect) {
    badge.textContent = "⚡ Hardhat";
    badge.className   = "network-badge ok";
  } else {
    badge.textContent = "⚠️ Sai mạng";
    badge.className   = "network-badge wrong";
  }
  badge.style.display = "flex";
}

// ── Cập nhật UI Wallet Panel ─────────────────────────────────
async function updateWalletUI(address) {
  const connectBtn  = document.getElementById("connectBtn");
  const walletPanel = document.getElementById("walletPanel");
  const walletShort = document.getElementById("walletShort");

  // Ẩn nút connect, hiện wallet panel
  if (connectBtn)  connectBtn.style.display  = "none";
  if (walletPanel) walletPanel.style.display = "flex";
  if (walletShort) walletShort.textContent   = address.slice(0, 7) + "..." + address.slice(-5);

  // Lấy số dư ví
  await refreshWalletBalance();

  // Mở khoá nút donate
  const donateBtn = document.getElementById("donateBtn");
  if (donateBtn) {
    donateBtn.disabled  = false;
    donateBtn.innerHTML = `
      <svg class="icon" viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
      <span>Donate ngay</span>
    `;
  }

  // Kiểm tra nếu là Owner thì hiện panel giải ngân
  // (checkOwner được định nghĩa ở cuối file — dùng setTimeout để đảm bảo hoisting)
  setTimeout(() => { if (typeof checkOwner === "function") checkOwner(); }, 0);
}



async function refreshWalletBalance() {
  const balEl = document.getElementById("walletBalance");
  if (!balEl || !provider || !userAddress) return;
  try {
    const bal = await provider.getBalance(userAddress);
    balEl.textContent = parseFloat(ethers.formatEther(bal)).toFixed(4) + " ETH";
  } catch { /* ignore */ }
}

// ── Copy địa chỉ ─────────────────────────────────────────────
async function copyAddress() {
  if (!userAddress) return;
  try {
    await navigator.clipboard.writeText(userAddress);
    showToast("Đã copy: " + userAddress.slice(0, 10) + "...", "success");
  } catch {
    showToast("Không thể copy địa chỉ.", "error");
  }
}

// ── Đổi ví (Switch Wallet) ───────────────────────────────────
async function switchWallet() {
  if (!window.ethereum) {
    showToast("MetaMask chưa cài đặt!", "error");
    return;
  }

  const btn = document.getElementById("switchBtn");
  if (btn) {
    btn.classList.add("switching");
    btn.innerHTML = '<span class="spinner" style="border-color:rgba(8,145,178,0.3);border-top-color:var(--primary-light)"></span> <span>Đang mở...</span>';
  }

  try {
    // Yêu cầu MetaMask hiển thị popup chọn tài khoản
    // wallet_requestPermissions buộc MetaMask mở lại account picker
    await window.ethereum.request({
      method: "wallet_requestPermissions",
      params: [{ eth_accounts: {} }],
    });

    // Sau khi user chọn xong, lấy account mới
    const accounts = await window.ethereum.request({ method: "eth_accounts" });
    if (accounts.length === 0) {
      showToast("Không có tài khoản nào được chọn.", "error");
      return;
    }

    const newAddress = accounts[0];
    if (newAddress.toLowerCase() === userAddress?.toLowerCase()) {
      showToast("Vẫn đang dùng ví: " + newAddress.slice(0, 8) + "...", "info");
      return;
    }

    // Cập nhật state
    userAddress = newAddress;
    provider    = new ethers.BrowserProvider(window.ethereum);
    signer      = await provider.getSigner();
    contract    = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, signer);

    await updateWalletUI(newAddress);
    showToast("✅ Đã chuyển sang: " + newAddress.slice(0, 8) + "..." + newAddress.slice(-6), "success");
    loadData();
  } catch (e) {
    if (e.code === 4001) {
      showToast("Đã huỷ chọn tài khoản.", "info");
    } else {
      showToast("Lỗi đổi ví: " + decodeError(e), "error");
    }
  } finally {
    if (btn) {
      btn.classList.remove("switching");
      btn.innerHTML = `
        <svg class="icon" style="width:15px;height:15px" viewBox="0 0 24 24"><path d="M7 16V4m0 0L3 8m4-4 4 4"/><path d="M17 8v12m0 0 4-4m-4 4-4-4"/></svg>
        <span>Đổi ví</span>
      `;
    }
  }
}

// ── Kết nối ví ──────────────────────────────────────────────
async function connectWallet() {
  try {
    if (!window.ethereum) {
      showToast("Vui lòng cài đặt MetaMask!", "error");
      return;
    }

    // Kết nối ví TRƯỚC (không block bởi mạng)
    await window.ethereum.request({ method: "eth_requestAccounts" });
    provider    = new ethers.BrowserProvider(window.ethereum);
    signer      = await provider.getSigner();
    userAddress = await signer.getAddress();
    contract    = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, signer);

    // Hiện wallet panel ngay lập tức (nút Đổi ví + Thoát)
    await updateWalletUI(userAddress);
    showToast("Đã kết nối: " + userAddress.slice(0, 8) + "...", "success");

    // Kiểm tra mạng SAU khi đã hiện UI
    ensureCorrectNetwork().catch(() => {});

    // Lắng nghe thay đổi account (KHÔNG reload — cập nhật trực tiếp)
    window.ethereum.on("accountsChanged", async (accounts) => {
      if (accounts.length === 0) { disconnectWallet(); return; }
      const newAddr = accounts[0];
      userAddress   = newAddr;
      provider      = new ethers.BrowserProvider(window.ethereum);
      signer        = await provider.getSigner();
      contract      = new ethers.Contract(CONTRACT_ADDRESS, CONTRACT_ABI, signer);
      await updateWalletUI(newAddr);
      showToast("Đã chuyển sang: " + newAddr.slice(0, 8) + "..." + newAddr.slice(-6), "info");
      loadData();
    });
    window.ethereum.on("chainChanged", () => location.reload());

    loadData();
  } catch (e) {
    showToast("Lỗi kết nối: " + decodeError(e), "error");
  }
}



// ── Donate ──────────────────────────────────────────────────
async function donate() {
  if (!contract || !signer) {
    showToast("Vui lòng kết nối ví trước!", "error");
    return;
  }

  const amountInput = document.getElementById("donateAmount");
  const msgInput    = document.getElementById("donateMessage");
  const amount      = amountInput?.value?.trim();
  const message     = msgInput?.value?.trim() || "";

  if (!amount || isNaN(parseFloat(amount)) || parseFloat(amount) <= 0) {
    showToast("Vui lòng nhập số ETH hợp lệ (> 0)!", "error");
    return;
  }

  const btn = document.getElementById("donateBtn");
  if (btn) {
    btn.disabled  = true;
    btn.innerHTML = '<span class="spinner"></span> <span>Đang xử lý...</span>';
  }

  try {
    // Kiểm tra mạng một lần nữa trước khi gửi
    const networkOk = await ensureCorrectNetwork();
    if (!networkOk) {
      if (btn) { btn.disabled = false; btn.innerHTML = resetDonateBtnHTML(); }
      return;
    }

    const weiValue = ethers.parseEther(amount);
    console.log("[Donate] amount:", amount, "ETH |", weiValue.toString(), "wei");

    const tx = await contract.donate(message, { value: weiValue });
    showToast("Giao dịch đang được xác nhận...", "info");
    const receipt = await tx.wait();
    console.log("[Donate] tx confirmed:", receipt.hash);

    showToast(`✅ Donate ${parseFloat(amount).toFixed(4)} ETH thành công!`, "success");
    if (amountInput) amountInput.value = "";
    if (msgInput)    msgInput.value    = "";
    loadData();
  } catch (e) {
    console.error("[Donate] Error:", e);
    showToast("❌ " + decodeError(e), "error");
  }

  if (btn) {
    btn.disabled  = false;
    btn.innerHTML = resetDonateBtnHTML();
  }
}

function resetDonateBtnHTML() {
  return `
    <svg class="icon" viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
    <span>Donate ngay</span>
  `;
}

// ── Tab Switching ────────────────────────────────────────────
function switchTab(tab) {
  const donationList   = document.getElementById("donationList");
  const withdrawalList = document.getElementById("withdrawalList");
  const tabDonations   = document.getElementById("tabDonations");
  const tabWithdrawals = document.getElementById("tabWithdrawals");

  if (tab === "donations") {
    if (donationList)   donationList.style.display   = "block";
    if (withdrawalList) withdrawalList.style.display  = "none";
    if (tabDonations)   tabDonations.classList.add("active");
    if (tabWithdrawals) tabWithdrawals.classList.remove("active");
  } else {
    if (donationList)   donationList.style.display   = "none";
    if (withdrawalList) withdrawalList.style.display  = "block";
    if (tabDonations)   tabDonations.classList.remove("active");
    if (tabWithdrawals) tabWithdrawals.classList.add("active");
  }
}

// ── Load Data ────────────────────────────────────────────────
async function loadData() {
  if (!readContract) {
    console.warn("readContract chưa sẵn sàng — bỏ qua loadData.");
    return;
  }

  try {
    const c = readContract;

    // Campaign info
    const [name, desc] = await Promise.all([c.campaignName(), c.campaignDescription()]);
    const nameEl = document.getElementById("campaignName");
    const descEl = document.getElementById("campaignDesc");
    if (nameEl) nameEl.textContent = name;
    if (descEl) descEl.textContent = desc;

    // Summary — getSummary() trả về 6 giá trị:
    // [balance, totalDonated, totalWithdrawn, donorCount, donationCount, withdrawalCount]
    const summary = await c.getSummary();
    setText("balance",        formatETH(summary[0]));
    setText("totalDonated",   formatETH(summary[1]));
    setText("totalWithdrawn", formatETH(summary[2]));
    setText("donorCount",     summary[3].toString());

    // Donations (hiển thị 20 gần nhất)
    const donationCount = Number(summary[4]);
    const donationList  = document.getElementById("donationList");
    if (donationList) {
      if (donationCount === 0) {
        donationList.innerHTML = emptyStateHTML("Chưa có quyên góp nào");
      } else {
        const start = Math.max(0, donationCount - 20);
        const limit = donationCount - start;
        const data  = await c.getDonations(start, limit);
        let html = "";
        for (let i = limit - 1; i >= 0; i--) {
          const addr = data.donors[i];
          const amt  = ethers.formatEther(data.amounts[i]);
          const time = new Date(Number(data.timestamps[i]) * 1000).toLocaleString("vi-VN");
          const msg  = data.messages[i] || "(không có lời nhắn)";
          html += historyItemHTML(addr, amt, msg, time, "donate");
        }
        donationList.innerHTML = html;
      }
    }

    // Withdrawals
    const withdrawalCount = Number(summary[5]);
    const withdrawalList  = document.getElementById("withdrawalList");
    if (withdrawalList) {
      let html = "";

      // Nếu là Owner → hiện form giải ngân inline
      if (isOwnerFlag) {
        const bal = await c.getBalance();
        html += buildInlineWithdrawForm(parseFloat(ethers.formatEther(bal)).toFixed(4));
      }

      if (withdrawalCount === 0) {
        html += emptyStateHTML("Chưa có giải ngân nào");
      } else {
        const start = Math.max(0, withdrawalCount - 20);
        const limit = withdrawalCount - start;
        const data  = await c.getWithdrawals(start, limit);
        for (let i = limit - 1; i >= 0; i--) {
          const addr    = data.recipients[i];
          const amt     = ethers.formatEther(data.amounts[i]);
          const time    = new Date(Number(data.timestamps[i]) * 1000).toLocaleString("vi-VN");
          const purpose = data.purposes[i];
          html += historyItemHTML(addr, amt, purpose, time, "withdraw");
        }
      }
      withdrawalList.innerHTML = html;
    }
  } catch (e) {
    console.error("loadData error:", e);
    // Hiển thị thông báo lỗi + nút thử lại trong danh sách
    const donationList = document.getElementById("donationList");
    if (donationList) {
      donationList.innerHTML = `
        <div class="empty-state">
          <svg class="icon icon-xl" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <p>Không kết nối được blockchain.<br><small>Hãy chắc chắn <code>npx hardhat node</code> đang chạy.</small></p>
          <button class="btn-connect" style="margin-top:12px" onclick="window._loadData()">Thử lại</button>
        </div>`;
    }
  }
}

// ── Helpers ──────────────────────────────────────────────────
function formatETH(val) {
  return parseFloat(ethers.formatEther(val)).toFixed(4) + " ETH";
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function historyItemHTML(addr, amt, msg, time, type) {
  const sign = type === "donate" ? "+" : "-";
  return `<div class="history-item">
    <div class="history-left">
      <div class="history-addr">${addr.slice(0, 8)}...${addr.slice(-6)}</div>
      <div class="history-msg">${msg}</div>
    </div>
    <div class="history-right">
      <div class="history-amount ${type}">${sign}${parseFloat(amt).toFixed(4)} ETH</div>
      <div class="history-time">${time}</div>
    </div>
  </div>`;
}

function buildInlineWithdrawForm(balanceETH) {
  return `<div class="inline-withdraw-form">
    <div class="inline-withdraw-header">
      <svg class="icon" viewBox="0 0 24 24"><path d="M12 22V2M7 17l5 5 5-5"/></svg>
      <span>Giải ngân quỹ</span>
      <span class="inline-balance">${balanceETH} ETH khả dụng</span>
    </div>
    <div class="inline-withdraw-fields">
      <div class="form-group" style="margin-bottom:10px">
        <input class="form-input" type="text" id="inlineWithdrawTo"
          placeholder="Địa chỉ nhận (0x...)" spellcheck="false" autocomplete="off">
      </div>
      <div class="inline-withdraw-row">
        <div class="form-group" style="margin-bottom:10px;flex:1">
          <input class="form-input" type="number" id="inlineWithdrawAmount"
            placeholder="Số ETH" step="0.001" min="0.0001">
        </div>
        <div class="form-group" style="margin-bottom:10px;flex:2">
          <input class="form-input" type="text" id="inlineWithdrawPurpose"
            placeholder="Mục đích giải ngân (tối thiểu 10 ký tự)">
        </div>
      </div>
      <button class="btn-inline-withdraw" id="inlineWithdrawBtn" onclick="window.inlineWithdraw()">
        <svg class="icon" style="width:16px;height:16px" viewBox="0 0 24 24"><path d="M12 22V2M7 17l5 5 5-5"/></svg>
        Thực hiện Giải Ngân
      </button>
    </div>
  </div>`;
}

function emptyStateHTML(message) {
  return `<div class="empty-state">
    <svg class="icon icon-xl" viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M2 10h20"/></svg>
    <p>${message}</p>
  </div>`;
}

function showToast(msg, type) {
  const t = document.getElementById("toast");
  if (!t) return;
  t.textContent = msg;
  t.className   = `toast ${type} show`;
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove("show"), 4000);
}

// ── Expose to window ─────────────────────────────────────────
window.connectWallet    = connectWallet;
window.donate           = donate;
window.switchTab        = switchTab;
window.switchWallet     = switchWallet;
window.copyAddress      = copyAddress;
window.disconnectWallet = disconnectWallet;
window._loadData        = loadData;
window.previewWithdraw  = previewWithdraw;
window.withdraw         = withdraw;
window.cancelPreview    = cancelPreview;
window.inlineWithdraw   = inlineWithdraw;

// ── Inline Withdraw (từ tab Giải ngân) ──────────────────────
async function inlineWithdraw() {
  if (!contract || !signer) {
    showToast("Vui lòng kết nối ví Owner trước!", "error");
    return;
  }

  const to      = document.getElementById("inlineWithdrawTo")?.value?.trim();
  const amount  = document.getElementById("inlineWithdrawAmount")?.value?.trim();
  const purpose = document.getElementById("inlineWithdrawPurpose")?.value?.trim();

  if (!to || !to.startsWith("0x") || to.length !== 42) {
    showToast("Địa chỉ người nhận không hợp lệ (0x... 42 ký tự).", "error"); return;
  }
  if (!amount || parseFloat(amount) <= 0) {
    showToast("Số ETH giải ngân phải lớn hơn 0.", "error"); return;
  }
  if (!purpose || purpose.length < 10) {
    showToast("Mục đích giải ngân quá ngắn (tối thiểu 10 ký tự).", "error"); return;
  }

  const networkOk = await ensureCorrectNetwork();
  if (!networkOk) {
    showToast("Vui lòng chuyển MetaMask sang đúng mạng!", "error");
    return;
  }

  const btn = document.getElementById("inlineWithdrawBtn");
  if (btn) { btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> Đang xử lý...'; }

  try {
    const weiAmount = ethers.parseEther(amount);
    console.log("[InlineWithdraw] to:", to, "| amount:", amount, "ETH | purpose:", purpose);

    const tx = await contract.withdraw(to, weiAmount, purpose);
    showToast("Giao dịch giải ngân đang xác nhận...", "info");
    await tx.wait();

    showToast(`✅ Đã giải ngân ${parseFloat(amount).toFixed(4)} ETH thành công!`, "success");

    // Reset form
    document.getElementById("inlineWithdrawTo").value = "";
    document.getElementById("inlineWithdrawAmount").value = "";
    document.getElementById("inlineWithdrawPurpose").value = "";

    loadData();
    checkOwner();
  } catch (e) {
    console.error("[InlineWithdraw] Error:", e);
    showToast("❌ " + decodeError(e), "error");
  }

  if (btn) {
    btn.disabled = false;
    btn.innerHTML = `
      <svg class="icon" style="width:16px;height:16px" viewBox="0 0 24 24"><path d="M12 22V2M7 17l5 5 5-5"/></svg>
      Thực hiện Giải Ngân
    `;
  }
}

// ── Thoát ví (Disconnect) ────────────────────────────────────
function disconnectWallet() {
  // Xoá state
  provider    = null;
  signer      = null;
  contract    = null;
  userAddress = null;

  // Ẩn wallet panel, hiện lại nút connect
  const walletPanel = document.getElementById("walletPanel");
  const connectBtn  = document.getElementById("connectBtn");
  const networkBadge = document.getElementById("networkBadge");

  if (walletPanel) walletPanel.style.display = "none";
  if (connectBtn)  connectBtn.style.display  = "flex";
  if (networkBadge) networkBadge.style.display = "none";

  // Ẩn panel giải ngân (Owner)
  const withdrawPanel = document.getElementById("withdrawPanel");
  if (withdrawPanel) withdrawPanel.style.display = "none";

  // Khoá lại nút donate
  const donateBtn = document.getElementById("donateBtn");
  if (donateBtn) {
    donateBtn.disabled  = true;
    donateBtn.innerHTML = `
      <svg class="icon" viewBox="0 0 24 24"><path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><circle cx="18" cy="12" r="2"/></svg>
      <span>Kết nối ví để donate</span>
    `;
  }

  // Xoá listener cũ (tránh duplicate)
  if (window.ethereum) {
    window.ethereum.removeAllListeners?.("accountsChanged");
    window.ethereum.removeAllListeners?.("chainChanged");
  }

  showToast("Đã ngắt kết nối ví.", "info");
}


// ============================================================
// GIAI NGAN (WITHDRAW) — Chi danh cho Owner
// ============================================================

// Kiem tra owner va hien/an panel giai ngan
async function checkOwner() {
  if (!readContract) return;
  try {
    const ownerAddr = await readContract.owner();
    console.log("[checkOwner] Contract owner:", ownerAddr);
    console.log("[checkOwner] Current wallet:", userAddress);

    // Hien dia chi owner o panel
    const ownerEl = document.getElementById("ownerAddr");
    if (ownerEl) ownerEl.textContent = ownerAddr;

    // Cap nhat so du contract trong panel
    const balEl = document.getElementById("contractBalance");
    if (balEl) {
      const bal = await readContract.getBalance();
      balEl.textContent = parseFloat(ethers.formatEther(bal)).toFixed(4) + " ETH";
    }

    // Chi hien panel neu vi dang ket noi la owner
    const panel = document.getElementById("withdrawPanel");
    if (userAddress && ownerAddr.toLowerCase() === userAddress.toLowerCase()) {
      console.log("[checkOwner] ✅ Wallet IS owner — showing panel");
      isOwnerFlag = true;
      if (panel) panel.style.display = "block";
      // Reload data to inject inline withdraw form
      loadData();
    } else {
      console.log("[checkOwner] ❌ Wallet is NOT owner — hiding panel");
      isOwnerFlag = false;
      if (panel) panel.style.display = "none";
    }
  } catch (e) {
    console.warn("checkOwner error:", e.message);
  }
}

// Xem truoc truoc khi gui giao dich
function previewWithdraw() {
  const to      = document.getElementById("withdrawTo")?.value?.trim();
  const amount  = document.getElementById("withdrawAmount")?.value?.trim();
  const purpose = document.getElementById("withdrawPurpose")?.value?.trim();

  // Validate
  if (!to || !to.startsWith("0x") || to.length !== 42) {
    showToast("Địa chỉ người nhận không hợp lệ (phải là 0x... 42 ký tự).", "error");
    return;
  }
  if (!amount || isNaN(parseFloat(amount)) || parseFloat(amount) <= 0) {
    showToast("Số ETH giải ngân phải lớn hơn 0.", "error");
    return;
  }
  if (!purpose || purpose.length < 10) {
    showToast("Mục đích giải ngân quá ngắn (tối thiểu 10 ký tự).", "error");
    return;
  }

  // Hien preview
  document.getElementById("previewTo").textContent      = to.slice(0, 10) + "..." + to.slice(-8);
  document.getElementById("previewAmount").textContent  = parseFloat(amount).toFixed(4) + " ETH";
  document.getElementById("previewPurpose").textContent = purpose;

  document.getElementById("withdrawPreview").style.display = "block";
  document.getElementById("previewBtn").style.display      = "none";
  document.getElementById("withdrawBtn").style.display     = "flex";
  document.getElementById("cancelPreviewBtn").style.display = "inline-flex";
}

// Huy preview, quay lai form
function cancelPreview() {
  document.getElementById("withdrawPreview").style.display  = "none";
  document.getElementById("previewBtn").style.display       = "flex";
  document.getElementById("withdrawBtn").style.display      = "none";
  document.getElementById("cancelPreviewBtn").style.display = "none";
}

// Thuc hien giai ngan
async function withdraw() {
  if (!contract || !signer) {
    showToast("Vui lòng kết nối ví Owner trước!", "error");
    return;
  }

  const to      = document.getElementById("withdrawTo")?.value?.trim();
  const amount  = document.getElementById("withdrawAmount")?.value?.trim();
  const purpose = document.getElementById("withdrawPurpose")?.value?.trim();

  // Validate lan cuoi
  if (!to || !to.startsWith("0x") || to.length !== 42) {
    showToast("Địa chỉ không hợp lệ.", "error"); return;
  }
  if (!amount || parseFloat(amount) <= 0) {
    showToast("Số ETH không hợp lệ.", "error"); return;
  }
  if (!purpose || purpose.length < 10) {
    showToast("Mục đích quá ngắn.", "error"); return;
  }

  // Kiểm tra mạng trước khi gửi
  const networkOk = await ensureCorrectNetwork();
  if (!networkOk) {
    showToast("Vui lòng chuyển MetaMask sang đúng mạng!", "error");
    return;
  }

  const btn = document.getElementById("withdrawBtn");
  const cancelBtn = document.getElementById("cancelPreviewBtn");
  if (btn) { btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> <span>Đang xử lý...</span>'; }
  if (cancelBtn) cancelBtn.disabled = true;

  try {
    const weiAmount = ethers.parseEther(amount);
    console.log("[Withdraw] to:", to, "| amount:", amount, "ETH | purpose:", purpose);
    console.log("[Withdraw] signer address:", await signer.getAddress());

    const tx = await contract.withdraw(to, weiAmount, purpose);
    showToast("Giao dịch giải ngân đang xác nhận...", "info");
    const receipt = await tx.wait();
    console.log("[Withdraw] confirmed:", receipt.hash);

    showToast(`✅ Đã giải ngân ${parseFloat(amount).toFixed(4)} ETH thành công!`, "success");

    // Reset form
    document.getElementById("withdrawTo").value      = "";
    document.getElementById("withdrawAmount").value  = "";
    document.getElementById("withdrawPurpose").value = "";
    cancelPreview();

    // Cap nhat so lieu
    loadData();
    checkOwner();
  } catch (e) {
    console.error("[Withdraw] Error:", e);
    showToast("❌ " + decodeError(e), "error");
  }

  if (btn) {
    btn.disabled = false;
    btn.innerHTML = `
      <svg class="icon" style="width:16px;height:16px" viewBox="0 0 24 24"><path d="M12 22V2M7 17l5 5 5-5"/></svg>
      <span>Xác nhận Giải Ngân</span>
    `;
  }
  if (cancelBtn) cancelBtn.disabled = false;
}


// ── Khởi động ────────────────────────────────────────────────
initReadProvider();
loadData();
