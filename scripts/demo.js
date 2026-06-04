/**
 * Script Demo — Tương tác với TuThien contract trên local
 * Chạy: npx hardhat run scripts/demo.js
 */
import { network } from "hardhat";

async function main() {
  console.log("╔═══════════════════════════════════════════════╗");
  console.log("║   🎯 DEMO — Blockchain Charity System        ║");
  console.log("╚═══════════════════════════════════════════════╝\n");

  // Hardhat 3: ethers is accessed via network.connect()
  const { ethers } = await network.connect();

  const [owner, donor1, donor2, recipient] = await ethers.getSigners();

  console.log("👤 Owner:", owner.address);
  console.log("💰 Donor 1:", donor1.address);
  console.log("💰 Donor 2:", donor2.address);
  console.log("🎁 Recipient:", recipient.address);

  // Deploy
  console.log("\n📝 Deploying TuThien contract...");
  const tuThien = await ethers.deployContract("TuThien", [
    "Quỹ Từ Thiện Minh Bạch",
    "Demo hệ thống quyên góp từ thiện trên Blockchain",
  ]);
  await tuThien.waitForDeployment();
  console.log("✅ Contract deployed tại:", tuThien.target);

  // Donate
  console.log("\n─── 💰 DONATE ───────────────────────────────");
  await (await tuThien.connect(donor1).donate("Ủng hộ trẻ em vùng cao", { value: ethers.parseEther("1.0") })).wait();
  console.log("✅ Donor 1 đã donate 1 ETH — 'Ủng hộ trẻ em vùng cao'");

  await (await tuThien.connect(donor2).donate("Chung tay vì cộng đồng", { value: ethers.parseEther("0.5") })).wait();
  console.log("✅ Donor 2 đã donate 0.5 ETH — 'Chung tay vì cộng đồng'");

  await (await tuThien.connect(donor1).donate("Lần 2", { value: ethers.parseEther("0.3") })).wait();
  console.log("✅ Donor 1 đã donate thêm 0.3 ETH");

  // Summary
  console.log("\n─── 📊 TỔNG QUAN QUỸ ────────────────────────");
  const s = await tuThien.getSummary();
  console.log(`   💵 Số dư hiện tại:   ${ethers.formatEther(s[0])} ETH`);
  console.log(`   📥 Tổng đã nhận:     ${ethers.formatEther(s[1])} ETH`);
  console.log(`   📤 Tổng đã giải ngân: ${ethers.formatEther(s[2])} ETH`);
  console.log(`   👥 Số nhà hảo tâm:   ${s[3]}`);
  console.log(`   📋 Số lần donate:    ${s[4]}`);

  // Withdraw
  console.log("\n─── 💸 GIẢI NGÂN ────────────────────────────");
  await (await tuThien.connect(owner).withdraw(recipient.address, ethers.parseEther("0.8"), "Hỗ trợ xây trường học vùng cao")).wait();
  console.log("✅ Owner giải ngân 0.8 ETH → Recipient");

  // After
  console.log("\n─── 📊 SAU GIẢI NGÂN ────────────────────────");
  const s2 = await tuThien.getSummary();
  console.log(`   💵 Số dư còn lại:    ${ethers.formatEther(s2[0])} ETH`);
  console.log(`   📤 Tổng đã giải ngân: ${ethers.formatEther(s2[2])} ETH`);

  // History
  console.log("\n─── 📋 LỊCH SỬ QUYÊN GÓP ───────────────────");
  const count = await tuThien.getDonationCount();
  for (let i = 0; i < count; i++) {
    const d = await tuThien.getDonation(i);
    console.log(`   #${i + 1} | ${d[0].slice(0, 8)}... | ${ethers.formatEther(d[1])} ETH | "${d[3]}"`);
  }

  console.log("\n╔═══════════════════════════════════════════════╗");
  console.log("║   ✅ DEMO HOÀN TẤT — Contract hoạt động OK!  ║");
  console.log("╚═══════════════════════════════════════════════╝");
}

main().then(() => process.exit(0)).catch((e) => { console.error("❌", e); process.exit(1); });
