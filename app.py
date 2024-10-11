import streamlit as st
import pandas as pd
import mensagem as msg
import funcoes as fnc
import acessa_dados as dados


if 'pasta_pedidos' not in st.session_state:
    st.session_state.pasta_pedidos = 'datasets/pedidos'

if 'leuarquivo' not in st.session_state:
    st.session_state.leuarquivo = False

# Funções para cada página
def page_home():
    st.title("Página Inicial")
    st.write("Bem-vindo ao nosso aplicativo!")
    st.divider()

def page_propostas():
    st.title("Propostas")
    # Lógica para gerar a proposta
    st.write("Nesta página, você poderá gerar uma proposta personalizada.")
    # Formulário ou outras interações para gerar a proposta
    st.divider()

def page_pedidos():
    options = dados.listar_pedidos()

    st.session_state.arquivo_selecionado = st.sidebar.selectbox(
            "Selecione o pedido",
            options        
        )
    
    dados_pedido = ''
    
    if st.session_state.arquivo_selecionado:
        st.session_state.leuarquivo = False
        dados_pedido = dados.ler_dados_pedido()

    if dados_pedido:
        fnc.exibir_dados()
        carregar_input_text()
    else:
        st.session_state.carregarinput = False
        st.success(msg.mensagem(3))

def page_fechamento():
    st.title("Fechamento")
    # Lógica para fechar o pedido
    st.write("Nesta página você poderá visualizar o fechamento.")
    # Relatório de fechamento

    st.divider()

def carregar_input_text():
    st.session_state.carregarinput = True
    return True

def main():
    with st.sidebar:
        col_1, col_2, col_3, col_4, col_5 = st.columns(5)
        with col_2:
            st.image('./img/logo-tahara-600.png', width=170)

    if not st.session_state.get("logged_in", False):
        fnc.exibe_login()
    else:
        # Sidebar com as opções de navegação
        options = list(["Home", "Propostas", "Pedidos"])

        if st.session_state.nivel_acesso == 1:
            options.append("Fechamento")

        page = st.sidebar.selectbox(
            "Navegação",
            options        
        )

        # Exibir a página selecionada
        if page == "Home":
            page_home()
        elif page == "Propostas":
            page_propostas()
        elif page == "Pedidos":
            page_pedidos()
        elif page == "Fechamento":
            page_fechamento()
        
        if 'exibirdados' not in st.session_state:
            st.session_state.exibirdados = False
        elif st.session_state.exibirdados == True:
            # st.subheader(f"No. Pedido: {st.session_state["num_pedido"]} - Cliente: {st.session_state["nome_cliente"]}", divider="gray")
            st.markdown(f"#### No. Pedido: {st.session_state["num_pedido"]} - Cliente: {st.session_state["nome_cliente"]}")

            fnc.plotar_grafico()

            st.divider()
            
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("##### Valor Compra")
                st.markdown(f"R$ {fnc.formatarMoeda(st.session_state["valor_compra"])}")

                st.markdown("##### Repres. Previsto")
                st.markdown(f"R$ {fnc.formatarMoeda(st.session_state["represamento_previsto"])}")

                st.markdown("##### Preço/TON")
                st.markdown(f"R$ {fnc.formatarMoeda(st.session_state["preco_ton"])}")

                st.markdown("##### Base ICMS")
                st.markdown(f"R$ {fnc.formatarMoeda(st.session_state["base_icms"])}")
            
                st.markdown("##### Lucro Líquido")
                st.markdown(f"R$ {fnc.formatarMoeda(st.session_state["lucro_liquido"])}")
            
            with col2:
                st.markdown("##### Valor Venda")
                st.markdown(f"R$ {fnc.formatarMoeda(st.session_state["valor_venda"])}")

                st.markdown("##### % Repres. Previsto")
                st.markdown(f"{fnc.formatarPercentual(st.session_state["percent_represamento_previsto"])}%")

                st.markdown("##### % Verba Marketing")
                st.markdown(f"{fnc.formatarMoeda(st.session_state["percent_verba_marketing"])}%")

                st.markdown("##### Base PIS/Cofins")
                st.markdown(f"R$ {fnc.formatarMoeda(st.session_state["base_pis_cofins"])}")

                st.markdown("##### Margem Líquida")
                st.markdown(f"{fnc.formatarPercentual(st.session_state["margem_liquida"])}%")
            
            with col3:
                st.markdown("##### % Nota")
                st.markdown(f"{fnc.formatarPercentual(st.session_state["porcentagem_nota"])}%")

                st.markdown("##### % Imp. Represado")
                st.markdown(f"{fnc.formatarPercentual(st.session_state["percent_imposto_represado"])}%")

                st.markdown("##### % Comissão")
                st.markdown(f"{fnc.formatarPercentual(st.session_state["percent_comissao"])}%")

                st.markdown("##### Base IRPJ/CSLL")
                st.markdown(f"R$ {fnc.formatarMoeda(st.session_state["base_irpj_csll"])}")
            
            st.divider()

            st.markdown('#### Lista de produtos')
            st.write(st.session_state.df_formatado)

        if 'carregarinput' not in st.session_state:
            st.session_state.carregarinput = False
        elif st.session_state.carregarinput == True:
            with st.sidebar:
                st.number_input("Preço/TON", key="preco_ton", on_change=dados.atualizar_dados)
                st.number_input("% Nota", key="porcentagem_nota", on_change=dados.atualizar_dados)
                st.number_input("% Comissão", key="percent_comissao", on_change=dados.atualizar_dados)
                st.number_input("% Represado", key="percent_imposto_represado", on_change=dados.atualizar_dados)
                st.number_input("% Verba Marketing", key="percent_verba_marketing", on_change=dados.atualizar_dados)

        st.sidebar.button("Logout", on_click=fnc.log_out)

# Execução principal
if __name__ == "__main__":
  st.set_page_config(
      page_title="TAHARA",
      page_icon="🔺"
  )
  main()