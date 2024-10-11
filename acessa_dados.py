import os
import streamlit as st
from openpyxl import load_workbook
import xlwings as xw
import pandas as pd


def listar_pedidos():
    options = list([""])

    arquivos = [f for f in os.listdir(st.session_state.pasta_pedidos) if f.endswith('.xlsx')]

    for nome_arquivo in arquivos:
        # if nome_arquivo.endswith('.xlsx'):
        options.append(f"{nome_arquivo}")
        
    return options

def ler_dados_pedido():
    # Arquivo de destino
    caminho_arquivo = f'{st.session_state.pasta_pedidos}/{(st.session_state.arquivo_selecionado)}'

    # Carregar o arquivo de origem
    workbook = load_workbook(caminho_arquivo, data_only = True)
    worksheet = workbook.worksheets[1]  # Selecionar a segunda aba

    # Copiar os valores das células do arquivo fonte para células do arquivo destino
    if st.session_state.leuarquivo == False:
        st.session_state['num_pedido'] = worksheet['O7'].value
        st.session_state['nome_cliente'] = worksheet['B18'].value
        st.session_state['valor_compra'] = worksheet['W48'].value
        st.session_state['porcentagem_nota'] = worksheet['D63'].value * 100
        st.session_state['base_icms'] = worksheet['AH48'].value
        st.session_state['base_pis_cofins'] = worksheet['AI48'].value
        st.session_state['base_irpj_csll'] = worksheet['AJ48'].value
        st.session_state['imposto_represado'] = worksheet['AL48'].value
        st.session_state['percent_imposto_represado'] = worksheet['B68'].value * 100
        st.session_state['verba_marketing'] = worksheet['C81'].value
        st.session_state['percent_verba_marketing'] = worksheet['E66'].value * 100
        st.session_state['frete_sp'] = worksheet['Y48'].value
        st.session_state['valor_extra'] = worksheet['C74'].value
        st.session_state['valor_venda'] = worksheet['H81'].value
        st.session_state['lucro_liquido'] = worksheet['H72'].value
        st.session_state['margem_liquida'] = worksheet['H73'].value * 100
        st.session_state['preco_ton'] = worksheet['H66'].value
        st.session_state['represamento_previsto'] = worksheet['C79'].value
        st.session_state['percent_represamento_previsto'] = worksheet['D79'].value
        st.session_state['percent_comissao'] = worksheet['B74'].value * 100

        st.session_state['item'] = worksheet['A27'].value
        st.session_state['Quant.'] = worksheet['B27'].value
        st.session_state['Peso'] = worksheet['C27'].value
        st.session_state['Peso Total'] = worksheet['D27'].value
        st.session_state['Modelo'] = worksheet['F27'].value

        # Carregar a planilha do Excel
        file_path = f'{st.session_state.pasta_pedidos}/{(st.session_state.arquivo_selecionado)}'
        sheet_name = 'PROPOSTA EDITAVEL'  # Altere para o nome da aba que deseja usar

        # Ler o intervalo de dados da planilha
        df = pd.read_excel(file_path, sheet_name=sheet_name, usecols='A:F', skiprows=26, nrows=21, index_col=0)

        # Filtrar as linhas onde a coluna B não é vazia
        df_filtrado = df[df['Quant.'].notna()]

        # Função para formatar os números
        def formatar_numero(x):
            if isinstance(x, (int, float)):
                return f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            return x

        # Aplicar a formatação a todas as células do DataFrame
        st.session_state.df_formatado = df_filtrado.applymap(formatar_numero)

    st.session_state.leuarquivo = True

    return True

def atualizar_dados():
    # Copiar os valores das células do arquivo fonte para células do arquivo destino
    st.session_state.preco_ton = st.session_state.preco_ton
    st.session_state.porcentagem_nota = st.session_state.porcentagem_nota
    st.session_state.percent_comissao = st.session_state.percent_comissao
    st.session_state.percent_imposto_represado = st.session_state.percent_imposto_represado
    st.session_state.percent_verba_marketing = st.session_state.percent_verba_marketing

    st.session_state.num_pedido = st.session_state.num_pedido
    st.session_state.nome_cliente = st.session_state.nome_cliente
    st.session_state.valor_compra = st.session_state.valor_compra
    st.session_state.base_icms = st.session_state.base_icms
    st.session_state.base_pis_cofins = st.session_state.base_pis_cofins
    st.session_state.base_irpj_csll = st.session_state.base_irpj_csll
    st.session_state.imposto_represado = st.session_state.imposto_represado
    st.session_state.verba_marketing = st.session_state.verba_marketing
    st.session_state.frete_sp = st.session_state.frete_sp
    st.session_state.valor_extra = st.session_state.valor_extra
    st.session_state.valor_venda = st.session_state.valor_venda
    st.session_state.lucro_liquido = st.session_state.lucro_liquido
    st.session_state.represamento_previsto = st.session_state.represamento_previsto
    st.session_state.percent_represamento_previsto = st.session_state.percent_represamento_previsto
    
    # Arquivo de destino
    caminho_arquivo = f'{st.session_state.pasta_pedidos}/{(st.session_state.arquivo_selecionado)}'

    # Abrir Excel no modo invisível
    with xw.App(visible=False) as app:
        app.display_alerts = False  # Desabilitar alertas do Excel
        wb = app.books.open(f'{st.session_state.pasta_pedidos}/{st.session_state.arquivo_selecionado}')
        ws = wb.sheets[1]

        # Atualizar os valores
        # st.write(ws.range['H66'].value)
        ws.range('H66').value = st.session_state.preco_ton
        ws.range('D63').value = st.session_state.porcentagem_nota / 100
        ws.range('B74').value = st.session_state.percent_comissao / 100
        ws.range('B68').value = st.session_state.percent_imposto_represado / 100
        ws.range('E66').value = st.session_state.percent_verba_marketing / 100

        # Recalcular fórmulas
        wb.app.calculate()

        # Atualizar o valor total
        # st.session_state.total = ws.range('C2').value

        # Salvar e fechar
        wb.save()
        wb.close()

    st.session_state.leuarquivo = False
    ler_dados_pedido()



