import streamlit as st
from agent import initialize_chatbot, handle_input


agent_executor = initialize_chatbot()


def get_agent(user_input):
    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []


    output, chat_history = handle_input(agent_executor, user_input, st.session_state['chat_history'])


    st.session_state['chat_history'] = chat_history

    return output

if __name__ == "__main__":

    st.title("Vietstock Chat")
    st.write("---")

    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Đang tìm câu trả lời..."):
                try:
                    response = get_agent(prompt)

                    placeholder = st.empty()
                    full_response = ""
                    for _, item in enumerate(response):
                        full_response += item
                    placeholder.markdown(full_response)

                    st.session_state.messages.append({"role": "assistant", "content": full_response})

                except Exception as e:
                    st.error("Gặp sự cố. Vui lòng thử lại.")
                    st.session_state.messages.append({"role": "assistant", "content": "Gặp sự cố. Vui lòng thử lại."})
