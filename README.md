## Streamlit ChatBot app to provide Real-time Financial Stock data

### Overview
`Zee-Fin-Bot` is a financial chatbot application that provides real-time data analysis and decision-making capabilities. It integrates a Groq-powered Llama model, Yahoo Finance tools, and the ReAct Agent to deliver a comprehensive financial analysis experience.

### Components
- **Groq-powered Llama Model**: Utilizes the `llama3-8b-8192` model for advanced data processing and analysis.
- **Yahoo Finance Tools**: Offers access to real-time financial data for analysis.
- **ReAct Agent**: Employs the chat engine for interactive decision-making based on the financial data.

### Requirements
- Python 3.6 or higher
- Streamlit
- Groq
- ReAct Agent

### Installation
- replace your GROQ API Key in `.streamlit/secrets.toml`
- To install the necessary packages and run the app, run the following commands in your terminal:
```bash
pip install -r requirements.txt
streamlit run main.py


