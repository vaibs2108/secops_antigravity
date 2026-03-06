---
title: SecOps Antigravity AI
emoji: 🛡️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8501
app_file: app/main.py
pinned: false
license: mit
---

# GenAI SecOps Demonstration Platform 🛡️

A simulated, enterprise-scale Cybersecurity Operations platform designed to demonstrate how **Generative AI agents** can integrate with and improve security operations.

This application generates a **synthetic, deterministic enterprise database** containing thousands of assets, alerts, and incidents entirely in-memory at runtime. It then calculates real-time operational KPIs based on this data.

Finally, it provides interfaces to invoke specialized **LangChain AI Agents** (like *Incident Triage*, *Root Cause Analysis*, and *Security Copilot*) which use the synthesized metrics as context to generate simulated analysis, applying input/output guardrails to ensure safety.

## 🚀 Features
- **Dynamic Data Generation**: Generates 10k+ assets and 20k+ alerts in seconds.
- **Deterministic KPI Engine**: Computes MTTD, MTTR, False Positive rates natively via Pandas.
- **Interactive Dashboard**: Built on Streamlit and Altair.
- **AI Agent Interventions**: LangChain-powered simulations with guardrails protecting against prompt injection.

## 💻 Local Development

1. **Clone the repository.**
2. **Set up a virtual environment and use uv/pip to install dependencies.**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables.**
   Copy `.env.example` to `.env` and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=sk-your-key-here
   MODEL_NAME=gpt-4o-mini
   ```
4. **Run the Streamlit app.**
   ```bash
   streamlit run app/main.py
   ```

## ☁️ Deploying to HuggingFace Spaces

This repository is structured specifically to support one-click deployment to HuggingFace Spaces using the **Streamlit** SDK.

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces) and select **Streamlit** as the Space SDK.
2. Push this repository's contents to the Space. HuggingFace will automatically read the `requirements.txt` and install the necessary Python dependencies.
3. **Important:** In your Hugging Face Space settings, navigate to the **Variables and secrets** section and securely add your `OPENAI_API_KEY`. The application will fail to run the AI agents without it.
4. (Optional) Set `MODEL_NAME` to a different compatible model if desired.

---
*Note: This platform is for demonstration purposes only. It does not connect to actual enterprise environments or ingest real telemetry data.*
