# 🤖 InsuraBot - AI Insurance Chatbot

InsuraBot is an AI-powered chatbot built with LangChain and LangGraph, designed to provide comprehensive insurance customer service. This chatbot can recommend insurance products, verify policy information, and track claim status in real-time.

## 📋 Table of Contents
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Agent Guide](#agent-guide)

## ✨ Key Features

### 1. **Insurance Product Recommendation** 🏆
- Personalized insurance product recommendations (health, vehicle, and home)
- Automatic premium calculation based on user parameters
- Re-ranking system for relevant results
- Email delivery for recommendations

**Available Products:**
- **Health Insurance**: Individual and family products with 10% discount for families
- **Vehicle Insurance**: All Risk (1-5 years) and TLO (1+ years), premium calculation based on vehicle age and price
- **Home Insurance**: HomeSafe Basic and HomeSafe Plus with coverage types

### 2. **Policy/Membership Information** 📄
- Check policy status based on policy number
- Complete membership insurance details
- Policy period information and payment status
- Send policy data via email

### 3. **Claim Tracking** 📝
- Check claim status by Claim ID
- Claim submission procedures
- Claim status (accepted, processing, rejected)
- Claim requirements and documentation

### 4. **Multi-Agent Architecture** 🔄
- **Product Agent**: Handles product recommendations and information
- **Policy Agent**: Manages membership and policy information
- **Claim Agent**: Handles claim information and status
- Automatic agent handoff system

### 5. **Additional Features** 🎯
- User-friendly chat interface with Streamlit
- Token usage tracking for monitoring
- Visualization of tools used
- Chat history management with thread-based conversations
- Email notifications for recommendations and information

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│          Streamlit Web Interface (app.py)                │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│     LangGraph Swarm (Multi-Agent Orchestrator)          │
│  ┌──────────────────┬──────────────────┬─────────────┐  │
│  │ Product Agent    │ Policy Agent     │ Claim Agent │  │
│  └──────────────────┴──────────────────┴─────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼─────┐ ┌─────▼────────┐ ┌──▼──────────┐
│ Qdrant      │ │  SQLite      │ │  OpenAI     │
│ (Products)  │ │  (Policy &   │ │  (LLM)      │
│             │ │   Claims)    │ │             │
└─────────────┘ └──────────────┘ └─────────────┘
```

## 📋 Prerequisites

- Python 3.8+
- OpenAI API Key
- Qdrant Cloud Account (or local Qdrant instance)
- Gmail Account (for email notifications)
- Excel files for data:
  - `claim_dataset.xlsx`: Claim data
  - `data_polis_asuransi.xlsx`: Policy data
  - Insurance product dataset (URL in environment)

## 🚀 Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd RecomInsuranceChatbot
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Initial Database (Optional)
```bash
python chatbot/import_dataset.py
```

## ⚙️ Configuration

Create a `.env` file in the root directory with the following configuration:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
CHAT_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small

# Qdrant Vector Database
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=https://your-qdrant-url:6333
QDRANT_COLLECTION_NAME=insurance_product

# Reranker Model
RERANKER_MODEL=mixedbread-ai/mxbai-rerank-large-v1

# Gmail Configuration
GMAIL_USER2=your_email@gmail.com
GMAIL_APP_PASSWORD2=your_gmail_app_password

# Dataset URL
URL_DATASET=https://url-to-your-insurance-dataset.xlsx
```

### Getting Gmail App Password:
1. Go to https://myaccount.google.com
2. Access Security Settings
3. Enable 2-Factor Authentication
4. Create App Password for Gmail
5. Use that password in `GMAIL_APP_PASSWORD2`

## 📖 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will run at http://localhost:8501

### Features in Interface

1. **Chat Input**: Type your question or command
2. **Clear Chat**: Button to clear chat history
3. **Token Usage**: Monitor API token usage
4. **Tools Call**: See which tools were used by the chatbot
5. **Example ID**: Reference IDs for testing

### Example Questions

**Product Recommendations:**
- "I want health insurance for a family of 3, I'm 35 years old"
- "I have a 2022 car worth 300 million, what insurance is good?"
- "What home insurance products are available?"

**Policy Information:**
- "I want to check my policy"
- "What's the status of my policy PLS-HEALTH-001?"
- "Show my insurance membership details"

**Claim Information:**
- "How do I file an insurance claim?"
- "Check the status of claim cl0001"
- "What are the requirements and documents for claims?"

## 📁 Project Structure

```
RecomInsuranceChatbot/
├── app.py                          # Main Streamlit application
├── test.py                         # UI test file
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
├── .env                            # Environment variables (create this)
├── claimdata.db                    # SQLite database for claims
├── policydata.db                   # SQLite database for policies
├── claim_dataset.xlsx              # Claim data source
├── data_polis_asuransi.xlsx        # Policy data source
│
└── chatbot/                        # Main package
    ├── __init__.py
    ├── chatbot.py                  # Agent orchestration & LangGraph setup
    ├── config.py                   # Configuration and LLM setup
    ├── tools.py                    # Tool definitions for agents
    ├── functions.py                # Utility functions
    └── import_dataset.py           # Data import script for database setup
```

## 🤖 Agent Guide

### Product Agent
**Responsibilities:**
- Insurance product recommendations
- Premium calculations
- Product detail information

**Special Rules:**
- Health: 10% discount for 2+ family members
- Vehicle: All Risk if 1-5 years old, TLO for 5+ years
- Home: Based on home value for premium calculation
- Don't transfer conversation if still about products

### Policy Agent
**Responsibilities:**
- Check policy status
- Membership details
- Payment information

**Flow:**
1. Request policy number if not provided
2. Display policy information
3. Offer email delivery

### Claim Agent
**Responsibilities:**
- Claim submission procedures
- Check claim status
- Requirements and documents

**Flow:**
1. Ask type of help (procedures or status)
2. If status, request Claim ID
3. Display claim information

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Web Framework** | Streamlit |
| **LLM** | OpenAI GPT-4o-mini |
| **Embedding** | OpenAI text-embedding-3-small |
| **Agent Framework** | LangChain + LangGraph |
| **Vector Database** | Qdrant |
| **Relational Database** | SQLite |
| **Re-ranking** | Sentence Transformers |
| **Monitoring** | Langfuse |
| **Email** | Gmail (SMTP) |

## 📊 Monitoring Features

### Token Usage
Check your API token usage in the sidebar:
- **Input Tokens**: Tokens from prompt
- **Output Tokens**: Tokens from response
- **Total Tokens**: Overall total

### Tools Call
Monitor which tools were called by the agent:
- search_insurance
- premi_calc_health
- premi_calc_vehicle
- premi_calc_home
- insurance_recomend_email
- policy_information
- claim_information

## 🐛 Troubleshooting

### Issue: "Connection to Qdrant failed"
- Make sure Qdrant URL and API key are correct in `.env`
- Check internet connection

### Issue: "Email not sent"
- Verify Gmail and App Password in `.env`
- Make sure Gmail account has 2FA enabled
- Check firewall SMTP access to smtp.gmail.com:587

### Issue: "Database error"
- Run `python chatbot/import_dataset.py` to reinitialize databases
- Make sure Excel dataset files are in the root directory

## 📝 Notes

- All premium values are **estimates** and not official policy values
- Chatbot uses Indonesian language for communication
- Response time depends on OpenAI and Qdrant API speed
- Chat history is stored in session memory

## 📧 Contact & Support

For questions or suggestions, please contact the development team.

---

**Version**: 1.0.0  
**Last Updated**: March 2026
