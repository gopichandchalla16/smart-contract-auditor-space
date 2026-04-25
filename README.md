---
title: Smart Contract Auditor
emoji: 🛡️
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: true
license: apache-2.0
short_description: AI-powered Solidity smart contract security auditor trained with GRPO RL
---

# 🛡️ Smart Contract Auditor — GRPO AI Agent

An AI-powered smart contract security auditor built with **GRPO Reinforcement Learning**.

## Model
- **Base:** Qwen2.5-1.5B-Instruct
- **Fine-tuned with:** GRPO (Group Relative Policy Optimization)
- **Reward improvement:** 0.030 → 0.329 (**10.9x**)
- **Training time:** 85.7 minutes

## What it detects
- Reentrancy Attacks
- Integer Overflow/Underflow
- Access Control Issues
- Unchecked Return Values
- And more...

Built at **Meta OpenEnv Hackathon 2026** by [Gopichand0516](https://huggingface.co/Gopichand0516)
