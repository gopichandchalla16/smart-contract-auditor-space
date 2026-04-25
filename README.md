---
title: Smart Contract Auditor
emoji: 🔍
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: true
---

# 🔍 Smart Contract Auditor — GRPO-Trained AI Agent

[![Model](https://img.shields.io/badge/🤗%20Model-Qwen2.5--3B--GRPO-blue)](https://huggingface.co/Gopichand0516/smart-contract-audit-qwen-grpo)
[![Training](https://img.shields.io/badge/GRPO-10.9x%20Improvement-orange)](https://github.com/gopichandchalla16/smart-contract-audit-env)
[![GitHub](https://img.shields.io/badge/GitHub-smart--contract--audit--env-black?logo=github)](https://github.com/gopichandchalla16/smart-contract-audit-env)

> A Gradio UI demo for the **GRPO-trained Qwen2.5-3B smart contract audit agent**. The model was trained with reinforcement learning (GRPO + QLoRA) and achieved a **10.9× reward improvement** from baseline 0.030 → final 0.329 over 200 steps.

---

## 📊 Training Results

| Metric | Value |
|---|---|
| Baseline Reward | 0.030 |
| Final Reward | **0.329** |
| Improvement | **10.9×** |
| Training Steps | 200 |
| Model | Qwen2.5-3B-Instruct + QLoRA |
| Trainable Params | 18.4M / 1.03B (1.78%) |

---

## 🚀 How to Use

1. Paste any Solidity smart contract into the input box
2. Click **Audit Contract**
3. The GRPO-trained model will analyze for vulnerabilities:
   - Reentrancy attacks
   - Missing access control
   - Oracle manipulation
   - tx.origin misuse
   - Unchecked return values

---

## 🔗 Links

- **Model:** https://huggingface.co/Gopichand0516/smart-contract-audit-qwen-grpo
- **Training Env:** https://github.com/gopichandchalla16/smart-contract-audit-env
- **Colab Notebook:** https://colab.research.google.com/drive/1TPfiFJC9rGpS8ZBETGL5XSUXf-Xltsd6?usp=drive_link

---

## 👤 Author

**Gopichand Challa** — [GitHub](https://github.com/gopichandchalla16) · [HuggingFace](https://huggingface.co/Gopichand0516) · [@GopichandAI](https://twitter.com/GopichandAI)

Built for the **Meta OpenEnv Hackathon (Scaler × Meta PyTorch)** — April 2026
