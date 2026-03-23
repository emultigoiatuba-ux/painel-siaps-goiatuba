import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gestão SIAPS Goiatuba", layout="wide")

@st.cache_data
def load_data():
    file = 'dados.xlsx' 
    # Tentamos ler o arquivo. Se falhar, avisamos o usuário.
    try:
        df_raw = pd.read_excel(file)
        header_idx = 0
        for i, row in df_raw.iterrows():
            if "INE" in str(row.values) or "NOME DA EQUIPE" in str(row.values):
                header_idx = i + 1
                break
        df = pd.read_excel(file, skiprows=header_idx)
        # Limpar colunas
        df.columns = [str(c).strip() for c in df.columns]
        # Converter pontuação para número (essencial para o gráfico)
        df['PONTUAÇÃO'] = pd.to_numeric(df['PONTUAÇÃO'].astype(str).str.replace(',', '.'), errors='coerce')
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")
        return None

df = load_data()

if df is not None:
    media_mun = df['PONTUAÇÃO'].mean()
    st.title("🏥 Painel SIAPS - Goiatuba")

    # Ranking Top 3
    st.subheader("🏆 Pódio de Desempenho")
    top3 = df.sort_values('PONTUAÇÃO', ascending=False).head(3)
    c1, c2, c3 = st.columns(3)
    for i, (idx, row) in enumerate(top3.iterrows()):
        with [c1, c2, c3][i]:
            st.metric(f"{i+1}º Lugar", row['NOME DA EQUIPE'], f"{row['PONTUAÇÃO']:.2f} pts")

    # Gráfico
    st.subheader("📊 Comparativo Municipal")
    fig = px.bar(df, x='NOME DA EQUIPE', y='PONTUAÇÃO', color='PONTUAÇÃO', color_continuous_scale='RdYlGn')
    fig.add_hline(y=media_mun, line_dash="dot", line_color="red", annotation_text="Média Mun.")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Por favor, verifique se o arquivo 'dados.xlsx' foi enviado corretamente para o GitHub.")
