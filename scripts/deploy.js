/**
 * Script Deploy - Blockchain Charity System
 * ===========================================
 *
 * Deploy hợp đồng TuThien lên blockchain
 *
 * Cách chạy:
 *   Local:   npx hardhat run scripts/deploy.js
 *   Sepolia: npx hardhat run scripts/deploy.js --network sepolia
 *
 * Yêu cầu (nếu deploy lên Sepolia):
 *   - SEPOLIA_RPC_URL trong .env
 *   - PRIVATE_KEY trong .env
 *   - Đủ Sepolia ETH trong ví
 */

import { network } from "hardhat";

async function main() {
  console.log("╔═══════════════════════════════════════════════╗");
  console.log("║   🚀 BLOCKCHAIN CHARITY SYSTEM - DEPLOY      ║");
  console.log("╚═══════════════════════════════════════════════╝\n");

  // Kết nối network
  const { ethers } = await network.connect();
  const [deployer] = await ethers.getSigners();

  const networkName = network.name || "hardhat (local)";
  console.log(`🔗 Network: ${networkName}`);
  console.log(`👤 Deployer: ${deployer.address}`);

  const balance = await ethers.provider.getBalance(deployer.address);
  console.log(`💰 Balance: ${ethers.formatEther(balance)} ETH\n`);

  // Thông tin chiến dịch
  const CAMPAIGN_NAME = "Quỹ Từ Thiện Minh Bạch";
  const CAMPAIGN_DESCRIPTION =
    "Hệ thống quyên góp từ thiện minh bạch trên Blockchain - Mọi giao dịch đều được ghi nhận vĩnh viễn";

  console.log(`📋 Campaign: ${CAMPAIGN_NAME}`);
  console.log(`📝 Description: ${CAMPAIGN_DESCRIPTION}\n`);

  // Deploy contract
  console.log("⏳ Deploying TuThien contract...");

  const tuThien = await ethers.deployContract("TuThien", [
    CAMPAIGN_NAME,
    CAMPAIGN_DESCRIPTION,
  ]);
  await tuThien.waitForDeployment();

  const contractAddress = tuThien.target;

  console.log(`\n✅ TuThien deployed successfully!`);
  console.log(`📍 Contract Address: ${contractAddress}`);
  console.log(`🔗 Network: ${networkName}`);

  // Hiển thị link Etherscan nếu deploy trên Sepolia
  if (network.name === "sepolia") {
    console.log(`\n🔍 Etherscan: https://sepolia.etherscan.io/address/${contractAddress}`);
    console.log(`\n📌 Để verify contract trên Etherscan:`);
    console.log(`   npx hardhat verify --network sepolia ${contractAddress} "${CAMPAIGN_NAME}" "${CAMPAIGN_DESCRIPTION}"`);
  }

  console.log("\n╔═══════════════════════════════════════════════╗");
  console.log("║   ✅ DEPLOY HOÀN TẤT                         ║");
  console.log("╚═══════════════════════════════════════════════╝");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("❌ Deployment failed:", error);
    process.exit(1);
  });
