import streamlit as st
from llama_index.llms.groq import Groq
from llama_index.core.agent import ReActAgent
from llama_index.core import Settings
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec

# page config
st.set_page_config(page_title="Financial ChatBot", page_icon=":space_invader:",
                   layout="centered", initial_sidebar_state="auto", menu_items=None)


# sidebar
with st.sidebar:
    st.subheader(
        "🤖 :orange-background[0xZee] Financial ChatBot", divider="orange")
    st.subheader("🔐 GROQ INFERENCE API", divider="grey")
    if ("GROQ_API" in st.secrets and st.secrets['GROQ_API'].startswith('gsk_')):
        st.success(':white_check_mark: GROQ API ')
        api_key = st.secrets['GROQ_API']
    else:
        api_key = st.text_input('Enter your Groq API Key', type='password')
        if not (api_key.startswith('gsk_') and len(api_key) == 56):
            st.warning("Enter a Valid GROQ API key")
        else:
            st.success('GROQ API Key Provided')


st.subheader("📊 :orange[Financial] ChatBot Agent 🏦", divider="blue")

#
if api_key:
    try:
        # Set chat engin
        if "chat_engine" not in st.session_state:
            try:
                Settings.llm = Groq(model="llama3-8b-8192",
                                    temperature=0.2, api_key=api_key)
                finance_tools = YahooFinanceToolSpec().to_tool_list()
                chat_engine = ReActAgent.from_tools(
                    finance_tools, verbose=True)
                st.session_state["chat_engine"] = chat_engine
            except Exception as e:
                st.error(f"error occurred in setting chat engine : {e}")
        # Initialize the chat messages history
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant",
                    "content": "Ask me a question or tell me what comes in your mind !"}
            ]
        # Display the prior chat messages
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        # Chat session controls
        with st.sidebar:
            st.subheader("⚙️ CHAT SESSION PARAM.", divider="grey")
            if st.button("Clear Chat Session", use_container_width=True, type="primary"):
                st.session_state["messages"] = [
                    {"role": "assistant", "content": ":sparkles: Hi, I'm here to help, How can I assist you today ? :star:"}]
            if st.button("Clear Chat Memory", use_container_width=True, type="secondary"):
                st.session_state["chat_engine"].reset()

        # PROMPTING for user input and save to chat history
        if prompt := st.chat_input("Your question"):
            # add_to_message_history("user", prompt)
            st.session_state["messages"].append(
                {"role": "user", "content": str(prompt)})

            # Display the new question immediately after it is entered
            with st.chat_message("user"):
                st.write(prompt)
            # If last message is not from assistant, generate a new response
            # if st.session_state["messages"][-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                response = st.session_state["chat_engine"].stream_chat(prompt)
                response_str = ""
                response_container = st.empty()
                for token in response.response_gen:
                    response_str += token
                    response_container.markdown(response_str)
                # st.write(response.source)
                st.session_state["messages"].append(
                    {"role": "assistant", "content": str(response.response)})

            # Save the state of the generator
            st.session_state["response_gen"] = response.response_gen
        #
        #
    except Exception as e:
        st.error(f"error occurred in chat session : {e}")
