import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(page_title="Ações B3", layout="centered")
st.title("📈 Visualizador de Ações da B3")

# Lista de ações disponíveis
acoes_disponiveis = [
    "VALE3.SA", "PETR4.SA", "ITUB4.SA", "BBAS3.SA", "BBDC4.SA",
    "MGLU3.SA", "WEGE3.SA", "SUZB3.SA", "PRIO3.SA", "SMFT3.SA",
    "ELET3.SA", "ELET6.SA", "B3SA3.SA", "ABEV3.SA", "LREN3.SA",
    "BPAC11.SA", "GGBR4.SA", "CIEL3.SA", "KLBN11.SA", "RAIL3.SA"
]

# Mapeamento de nomes
nomes_empresas = {
    "VALE3.SA": "Vale",
    "PETR4.SA": "Petrobras PN",
    "ITUB4.SA": "Itaú Unibanco",
    "BBAS3.SA": "Banco do Brasil",
    "BBDC4.SA": "Bradesco",
    "MGLU3.SA": "Magazine Luiza",
    "WEGE3.SA": "WEG",
    "SUZB3.SA": "Suzano",
    "PRIO3.SA": "PetroRio",
    "SMFT3.SA": "Smart Fit",
    "ELET3.SA": "Eletrobras ON",
    "ELET6.SA": "Eletrobras PN",
    "B3SA3.SA": "B3",
    "ABEV3.SA": "Ambev",
    "LREN3.SA": "Lojas Renner",
    "BPAC11.SA": "BTG Pactual",
    "GGBR4.SA": "Gerdau",
    "CIEL3.SA": "Cielo",
    "KLBN11.SA": "Klabin",
    "RAIL3.SA": "Rumo"
}

# Filtros
st.sidebar.header("Filtros")
selecionadas = st.sidebar.multiselect("Escolha as ações", acoes_disponiveis, default=acoes_disponiveis[:5])

# Filtro de datas
hoje = datetime.today()
inicio = st.sidebar.date_input("Data inicial", hoje - timedelta(days=30))
fim = st.sidebar.date_input("Data final", hoje)

# Buscar dados
try:
    dados = yf.download(selecionadas, start=inicio, end=fim)["Close"]
    dados = dados.dropna(how="all")

    if dados.empty:
        st.warning("Não há dados disponíveis para esse período.")
    else:
        # Gráfico de linha
        st.subheader("📉 Evolução dos Preços")
        st.line_chart(dados)

        # Tabela de preços e variação
        st.subheader("📊 Tabela de Preço Atual e Variação")

        tabela = []
        for acao in selecionadas:
            serie = dados[acao].dropna()
            nome = nomes_empresas.get(acao, "—")
            if len(serie) >= 2:
                preco_inicial = serie.iloc[0]
                preco_final = serie.iloc[-1]
                variacao = preco_final / preco_inicial - 1
                tabela.append({
                    "Código": acao,
                    "Empresa": nome,
                    "Preço Inicial": f"R$ {preco_inicial:.2f}",
                    "Preço Atual": f"R$ {preco_final:.2f}",
                    "Variação (%)": f"{variacao * 100:.2f}%",
                    "Status": "🔼 Alta" if variacao > 0 else "🔽 Baixa" if variacao < 0 else "⏸️ Estável"
                })
            else:
                tabela.append({
                    "Código": acao,
                    "Empresa": nome,
                    "Preço Inicial": "—",
                    "Preço Atual": "—",
                    "Variação (%)": "—",
                    "Status": "Dados insuficientes"
                })

        df_tabela = pd.DataFrame(tabela)
        st.dataframe(df_tabela, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao buscar dados: {e}")