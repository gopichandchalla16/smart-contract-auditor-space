import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load model and tokenizer from HF Hub
MODEL_ID = "Gopichand0516/smart-contract-audit-qwen-grpo"
BASE_MODEL = "unsloth/qwen2.5-1.5b-instruct-unsloth-bnb-4bit"

tokenizer = None
model = None

def load_model():
    global tokenizer, model
    if model is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto"
        )
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, MODEL_ID)
        model.eval()
    return tokenizer, model

SYSTEM_PROMPT = """You are an expert smart contract security auditor specializing in Solidity vulnerabilities.
Analyze the provided smart contract and identify:
1. Vulnerability type and name
2. Severity level (Critical/High/Medium/Low)
3. Exact location in code
4. Potential impact/exploit scenario
5. Recommended fix with corrected code

Be precise, technical, and thorough."""

EXAMPLE_CONTRACTS = {
    "Reentrancy Attack": """pragma solidity ^0.8.0;

contract Vulnerable {
    mapping(address => uint) public balances;
    
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }
    
    function withdraw() public {
        uint amount = balances[msg.sender];
        (bool ok,) = msg.sender.call{value: amount}("");
        balances[msg.sender] = 0;  // State updated AFTER external call
    }
}""",
    "Integer Overflow": """pragma solidity ^0.7.0;

contract Token {
    mapping(address => uint256) public balances;
    
    function transfer(address to, uint256 amount) public {
        require(balances[msg.sender] >= amount);
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
    
    function mint(uint256 amount) public {
        balances[msg.sender] += amount;  // Unchecked overflow
    }
}""",
    "Access Control Missing": """pragma solidity ^0.8.0;

contract Ownable {
    address public owner;
    
    constructor() {
        owner = msg.sender;
    }
    
    function withdrawAll() public {
        payable(msg.sender).transfer(address(this).balance);
    }
    
    function setOwner(address newOwner) public {
        owner = newOwner;  // Anyone can become owner!
    }
}"""
}

def audit_contract(solidity_code, max_tokens, temperature):
    if not solidity_code.strip():
        return "⚠️ Please paste a Solidity smart contract to audit."
    
    try:
        tok, mdl = load_model()
        
        prompt = f"""<|im_start|>system
{SYSTEM_PROMPT}<|im_end|>
<|im_start|>user
Audit this Solidity smart contract for security vulnerabilities:

```solidity
{solidity_code}
```
<|im_end|>
<|im_start|>assistant
"""
        inputs = tok(prompt, return_tensors="pt").to(mdl.device)
        
        with torch.no_grad():
            outputs = mdl.generate(
                **inputs,
                max_new_tokens=int(max_tokens),
                temperature=float(temperature),
                do_sample=temperature > 0.1,
                pad_token_id=tok.eos_token_id,
                eos_token_id=tok.eos_token_id,
            )
        
        generated = outputs[0][inputs["input_ids"].shape[1]:]
        result = tok.decode(generated, skip_special_tokens=True)
        return result.strip()
        
    except Exception as e:
        return f"❌ Error during audit: {str(e)}"

def load_example(example_name):
    return EXAMPLE_CONTRACTS.get(example_name, "")

with gr.Blocks(
    title="Smart Contract Auditor — GRPO AI Agent",
    theme=gr.themes.Base(
        primary_hue="green",
        secondary_hue="blue",
        neutral_hue="gray",
        font=gr.themes.GoogleFont("JetBrains Mono"),
    ).set(
        body_background_fill="#0d1117",
        body_text_color="#c9d1d9",
        block_background_fill="#161b22",
        block_border_color="#30363d",
        input_background_fill="#0d1117",
        button_primary_background_fill="#238636",
        button_primary_text_color="white",
    )
) as demo:

    gr.HTML("""
    <div style="text-align:center; padding:20px; background:linear-gradient(135deg,#0d1117,#161b22); border:1px solid #30363d; border-radius:10px; margin-bottom:20px;">
        <h1 style="color:#00ff88; font-size:2em; margin:0;">🛡️ Smart Contract Auditor</h1>
        <p style="color:#8b949e; margin:8px 0;">AI-Powered Solidity Vulnerability Detection via GRPO Reinforcement Learning</p>
        <div style="margin-top:10px;">
            <span style="background:#21262d; border:1px solid #30363d; border-radius:20px; padding:4px 12px; font-size:12px; color:#58a6ff; margin:4px;">🤗 Qwen2.5-1.5B + GRPO</span>
            <span style="background:#21262d; border:1px solid #30363d; border-radius:20px; padding:4px 12px; font-size:12px; color:#3fb950; margin:4px;">📈 10.9x Reward Improvement</span>
            <span style="background:#21262d; border:1px solid #30363d; border-radius:20px; padding:4px 12px; font-size:12px; color:#f78166; margin:4px;">⚡ Meta OpenEnv Hackathon 2026</span>
        </div>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📋 Load Example")
            example_dropdown = gr.Dropdown(
                choices=list(EXAMPLE_CONTRACTS.keys()),
                label="Choose a vulnerable contract",
                value=None
            )
            load_btn = gr.Button("📂 Load Example", size="sm")

            gr.Markdown("### ⚙️ Settings")
            max_tokens = gr.Slider(minimum=100, maximum=600, value=350, step=50, label="Max Output Tokens")
            temperature = gr.Slider(minimum=0.1, maximum=1.0, value=0.1, step=0.1, label="Temperature")

            gr.Markdown("""
### 🔍 Detects
- 🔴 Reentrancy Attacks
- 🟠 Integer Overflow
- 🟡 Access Control Issues
- 🟡 Unchecked Return Values
- 🟢 Gas Optimization Issues

### 📊 Training Stats
| Metric | Value |
|--------|-------|
| Base Model | Qwen2.5-1.5B |
| Algorithm | GRPO |
| Steps | 200 |
| Reward | 0.030 → 0.329 |
| Improvement | **10.9x** |
""")

        with gr.Column(scale=2):
            gr.Markdown("### 📝 Paste Solidity Contract")
            solidity_input = gr.Code(
                language="javascript",
                label="Solidity Smart Contract",
                placeholder="pragma solidity ^0.8.0;\n\ncontract MyContract {\n    // Paste your contract here...\n}",
                lines=18,
            )
            audit_btn = gr.Button("🔍 Run Security Audit", variant="primary", size="lg")
            gr.Markdown("### 🛡️ Audit Report")
            output = gr.Textbox(label="AI Security Analysis", lines=18, show_copy_button=True)

    gr.HTML("""
    <div style="text-align:center; margin-top:20px; padding:16px; border-top:1px solid #30363d; color:#8b949e; font-size:12px;">
        Built by <a href="https://huggingface.co/Gopichand0516" style="color:#58a6ff;">Gopichand0516</a> |
        Model: <a href="https://huggingface.co/Gopichand0516/smart-contract-audit-qwen-grpo" style="color:#58a6ff;">smart-contract-audit-qwen-grpo</a> |
        Meta OpenEnv Hackathon 2026
    </div>
    """)

    load_btn.click(fn=load_example, inputs=[example_dropdown], outputs=[solidity_input])
    audit_btn.click(fn=audit_contract, inputs=[solidity_input, max_tokens, temperature], outputs=[output])

if __name__ == "__main__":
    demo.launch()
