import { defineConfig } from "hardhat/config";
import hardhatToolboxMochaEthers from "@nomicfoundation/hardhat-toolbox-mocha-ethers";
import dotenv from "dotenv";

dotenv.config();

// Kiểm tra PRIVATE_KEY có phải hex hợp lệ không (tránh crash khi dùng placeholder)
const privateKey = process.env.PRIVATE_KEY || "";
const isValidKey = /^(0x)?[0-9a-fA-F]{64}$/.test(privateKey);

/**
 * Hardhat 3 Configuration
 * Project: Blockchain Charity Transparency System
 *
 * Sử dụng:
 * - Solidity 0.8.24 với optimizer
 * - Sepolia testnet cho testing
 * - Etherscan để verify contract
 */
export default defineConfig({
  plugins: [hardhatToolboxMochaEthers],

  solidity: {
    version: "0.8.24",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
      evmVersion: "paris",
    },
  },

  networks: {
    // Sepolia Testnet — chỉ kích hoạt khi có private key hợp lệ
    ...(isValidKey
      ? {
          sepolia: {
            type: "http",
            url: process.env.SEPOLIA_RPC_URL || "https://rpc.sepolia.org",
            accounts: [privateKey.startsWith("0x") ? privateKey : `0x${privateKey}`],
            chainId: 11155111,
          },
        }
      : {}),
  },
});
