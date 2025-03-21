import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------------------------------------------------------------
# ESTILO

st.set_page_config(layout="wide",page_icon="📊",page_title="Estoque Focal")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html = True)

st.title("📊 Demostrativo de Estoque",anchor=False)

card1, card2, card3, card4 = st.columns([1,1,1,1])
col1, col2 = st.columns([1,2])
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
df_pa = df_pa[["PRODUTO", "DESCRIÇÃO","ML","TIPO","LOCAL"]]

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
outlet = outlet[["PRODUTO", "DESCRIÇÃO","ML","TIPO","LOCAL"]]

# -------------------------------------------------------------------------------------------
# DATAFRAME EMPILHADO

df = pd.concat([df_pa,outlet],ignore_index=True)

df_agrupado = df.groupby(["PRODUTO"])["ML"].sum().reset_index()

qtd_pa = df.query('TIPO == "PA"')

qtd_pa = qtd_pa["ML"].sum()

qtd_outlet = df.query('TIPO == "OUTLET"')

qtd_outlet = qtd_outlet["ML"].sum()

qtd_artigos = df_agrupado.shape[0]

qtd_localizacoes = df["LOCAL"].unique().shape[0]

# -------------------------------------------------------------------------------------------
# PATETICS CHARTS
df_agrupado = df_agrupado.sort_values(by="ML",ascending=False)
df = df.sort_values(by="ML",ascending=False)


# bar_chart = px.bar(df_agrupado,x="ML",y="PRODUTO",orientation="h",text=df_agrupado["ML"])
# bar_chart.update_traces(showlegend=False,textfont=dict(size=50,color='#FFFFFF'),textposition="outside")

with col1:
    st.dataframe(df_agrupado,use_container_width=True,hide_index=True)
with col2:
    df = df[["DESCRIÇÃO","ML","TIPO","LOCAL"]]
    st.dataframe(df,use_container_width=True,hide_index=True)
# -------------------------------------------------------------------------------------------


with card1:
    st.metric("Tipos Artigos",f'{qtd_artigos}')

with card2:
    st.metric("Qtd Localizações",qtd_localizacoes)


with card3:
    st.metric("PA",f'{qtd_pa:,.2f}'.replace(',', 'temp').replace('.', ',').replace('temp', '.'))

with card4:
    st.metric("Outlet",f'{qtd_outlet:,.2f}'.replace(',', 'temp').replace('.', ',').replace('temp', '.'))


# -------------------------------------------------------------------------------------------

if st.button("Atualizar 🔁"):
    st.cache_data.clear(),
    st.rerun()


#-----------------------------------------------------------------------------------------------------
#ESTILIZACAO

borda = """
    <style>

    [data-testid="stColumn"]
    {
    background-color: #0B1548;
    border-radius: 15px;
    padding: 10px;
    box-shadow: 5px 3px 5px rgba(0, 0, 0, 0.3);
    text-align: center;
    color: #ffffff;
    }
    </style>

    """

st.markdown(borda, unsafe_allow_html=True)  

borda = """
    <style>

    [data-testid="stHeading"]
    {
    color: #0B1548;
    }
    </style>

    """

st.markdown(borda, unsafe_allow_html=True)  