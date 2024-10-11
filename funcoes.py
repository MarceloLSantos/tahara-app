import streamlit as st
import requests
import json
from st_pages import hide_pages
from time import sleep


def log_in():
    st.session_state["logged_in"] = True
    hide_pages([])
    st.success("Logged in!")
    sleep(0.5)

def log_out():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.session_state["logged_in"] = False
    st.success("Deslogado com sucesso")
    sleep(1.0)

def exibe_login():
    with st.sidebar:
        hide_pages(["page1", "page2" ])

        st.title("Login")
        username = st.text_input("Usuário", key="username")
        password = st.text_input("Senha", key="password", type="password")

        if st.button("Login", key="login"):
            resultado = autenticar_usuario(username, password)
            if resultado:
                st.session_state["logged_in"] = True
                hide_pages([])
                st.success("Login bem-sucedido!")
                # sleep(1.0)
            else:
                st.error("Usuário ou senha inválidos.")

def autenticar_usuario(username, password):
    st.session_state.nivel_acesso = 1
    return True

    # URL da API PHP
    url = "https://mlssistemas.com.br/tahara/api/autenticar/"

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'My Python API Script'
    }
    # Dados a serem enviados para a API
    data = {
    'username': username,
    'password': password,
    'api_python': 'tahara@api-python'
    }
    data_json = json.dumps(data)

    # Fazendo a requisição POST para a API
    response = requests.post(url, data_json, headers=headers)

    # Verificando a resposta da API
    if response.status_code == 200:
        resultado = json.loads(response.text)
        st.session_state.nivel_acesso = int(resultado['nivel_acesso'])
        return resultado
    else:
        return False

def exibir_dados():
    st.session_state.exibirdados = True
    return True

def formatarMoeda(valor):
    # return format(valor, '.2f')
    return format(valor, '_.2f').replace(".",",").replace("_",".")

def formatarPercentual(valor):
    return format(valor, '_.2f').replace(".",",").replace("_",".")

def plotar_grafico():
    valor = st.session_state.margem_liquida

    cor = 'gray'

    if valor >= 35:
        cor = '#00ff00'
    elif valor >= 30:
        cor = '#00aa00'
    elif valor >= 25:
        cor = '#ffff00'
    elif valor >= 20:
        cor = '#bbbb00'
    elif valor >= 15:
        cor = '#ff6600'
    elif valor >= 10:
        cor = '#bb6600'
    elif valor >= 5:
        cor = '#ff0000'
    elif valor >= 1:
        cor = '#990000'
    else:
        cor = 'gray'

    st.markdown(
        f'''
        <style>
            .div_parent{{
                width: 100%;
                border: 1px solid gray;
                text-align: center;
                background-color: #333333;
                border-radius: 20px;
            }}

            .format {{
                display: inline-block;
                width: 60px;
                height: 40px;
                border: 1px solid gray;
                border-radius: 5px;
                text-align: center;
            }}
        </style>
        <div class="div_parent">
            <h5>QUALIDADE DA VENDA - {formatarPercentual(valor)} Pts</h5>
            <div id="cell1" class="format" style="background-color:{(cor if valor >= 1 else 'gray')}"></div>
            <div id="cell2" class="format" style="background-color:{(cor if valor >= 5 else 'gray')}"></div>
            <div id="cell3" class="format" style="background-color:{(cor if valor >= 10 else 'gray')}"></div>
            <div id="cell4" class="format" style="background-color:{(cor if valor >= 15 else 'gray')}"></div>
            <div id="cell5" class="format" style="background-color:{(cor if valor >= 20 else 'gray')}"></div>
            <div id="cell6" class="format" style="background-color:{(cor if valor >= 25 else 'gray')}"></div>
            <div id="cell7" class="format" style="background-color:{(cor if valor >= 30 else 'gray')}"></div>
            <div id="cell8" class="format" style="background-color:{(cor if valor >= 35 else 'gray')}"></div>
        </div>

        
        ''',
        unsafe_allow_html=True
    )

# st.number_input(label="Qualidade da venda", key="qualidade", on_change=plotar_grafico)
# plotar_grafico(0)
