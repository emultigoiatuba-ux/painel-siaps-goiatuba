import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gestão SIAPS Goiatuba", layout="wide")

def load_data():
    file = 'dados.xlsx' 
    df_raw = pd.read_excel(file)
    header_idx = 0
    for i, row in df_raw.iterrows():
        if "INE" in row.values:
            header_idx = i + 1
            break
    df = pd.read_excel(file, skiprows=header_idx)
    df.columns = [str(c).strip() for c in df.columns]
    df['PONTUAÇÃO'] = pd.to_numeric(df['PONTUAÇÃO'].astype(str).str.replace(',', '.'), errors='coerce')
    return df

try:
    df = load_data()
    media_mun = df['PONTUAÇÃO'].mean()

    st.title("🏥 Monitoramento SIAPS - Goiatuba")
    
    # Ranking
    st.subheader("🥇 Top 3 Equipes do Mês")
    top3 = df.sort_values('PONTUAÇÃO', ascending=False).head(3)
    c1, c2, c3 = st.columns(3)
    for i, (idx, row) in enumerate(top3.iterrows()):
        with [c1, c2, c3][i]:
            st.success(f"{i+1}º: {row['NOME DA EQUIPE']}")
            st.metric("Pontuação", f"{row['PONTUAÇÃO']:.2f}")

    # Gráfico
    st.subheader("📊 Desempenho Geral vs Média Municipal")
    fig = px.bar(df, x='NOME DA EQUIPE', y='PONTUAÇÃO', color='PONTUAÇÃO', color_continuous_scale='RdYlGn')
    fig.add_hline(y=media_mun, line_dash="dot", line_color="red", annotation_text=f"Média: {media_mun:.2f}")
    st.plotly_chart(fig, use_container_width=True)

    # Feedback WhatsApp
    st.divider()
    eq = st.selectbox("Selecione para Feedback:", df['NOME DA EQUIPE'].unique())
    d_eq = df[df['NOME DA EQUIPE'] == eq].iloc[0]
    msg = f"*FEEDBACK SIAPS*\n*Equipe:* {eq}\n*Pontuação:* {d_eq['PONTUAÇÃO']:.2f}\n*Ação:* Resolver {d_eq['PESSOAS SEM CRITÉRIO']} cadastros pendentes!"
    st.text_area("Texto para WhatsApp:", msg)

except Exception as e:
    st.error(f"Aguardando o arquivo 'dados.xlsx'. Certifique-se de que ele foi enviado ao GitHub.")
