import streamlit as st
import pandas as pd

# --------------------------------------------------------------------------------------------------------
# ESTILO

st.set_page_config(layout="wide",page_icon="📊",page_title="Estoque Focal")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)

st.title("📊 Demostrativo de Estoque",anchor=False)

card1, card2, card3 = st.columns([1,1,1])
# --------------------------------------------------------------------------------------------------------
# LINKS PARA O ESTOQUE

url_pa = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS4eL_StwXZnZrikVfRucRYOO_stX6InEBMSNUIyF_e8r0aKN-ACp4u0QFVJ8JgyFGMu7ra1J7Fwaaw/pub?gid=905962302&single=true&output=csv"
url_outlet = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS4eL_StwXZnZrikVfRucRYOO_stX6InEBMSNUIyF_e8r0aKN-ACp4u0QFVJ8JgyFGMu7ra1J7Fwaaw/pub?gid=872414139&single=true&output=csv"


# --------------------------------------------------------------------------------------------------------
# CARREGAR ESTOQUE PA

@st.cache_data
def load_pa():
    df = pd.read_csv(url_pa)
    return df

df_pa = load_pa()
df_pa["ML"] = df_pa["ML"].str.replace(",", ".").astype(float)
df_pa["TIPO"] = "PA"

df_pa['PRODUTO'] = df_pa['DESCRIÇÃO'].str.split().str[:1].str.join(' ')
df_pa = df_pa[["PRODUTO", "DESCRIÇÃO","ML","TIPO"]]

# --------------------------------------------------------------------------------------------------------
# CARREGAR ESTOQUE OUTLET

@st.cache_data
def load_outlet():
    df = pd.read_csv(url_outlet)
    return df

outlet = load_outlet()
outlet["ML"] = outlet["ML"].str.replace(",", ".").astype(float)
outlet["TIPO"] = "OUTLET"

outlet['PRODUTO'] = outlet['DESCRIÇÃO'].str.split().str[:1].str.join(' ')
outlet = outlet[["PRODUTO", "DESCRIÇÃO","ML","TIPO"]]

# -------------------------------------------------------------------------------------------
# DATAFRAME EMPILHADO

df = pd.concat([df_pa,outlet],ignore_index=True)

df_agrupado = df.groupby(["PRODUTO"])["ML"].sum().reset_index()

qtd_pa = df.query('TIPO == "PA"')

qtd_pa = qtd_pa["ML"].sum()

qtd_outlet = df.query('TIPO == "OUTLET"')

qtd_outlet = qtd_outlet["ML"].sum()

qtd_artigos = df_agrupado.shape[0]


# -------------------------------------------------------------------------------------------

with card1:
    st.metric("Tipos Artigos",qtd_artigos)

with card2:
    st.metric("Soma Pa",qtd_pa)

with card3:
    st.metric()

# -------------------------------------------------------------------------------------------

if st.button("Atualizar 🔁"):
    st.cache_data.clear(),
    st.rerun()