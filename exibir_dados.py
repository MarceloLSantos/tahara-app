import streamlit as st

def exibir_dados():
    st.session_state.exibirdados = True
    return True

def carregar_input_text():
    st.session_state.carregarinput = True
    return True