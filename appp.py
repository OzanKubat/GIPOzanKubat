from email import header
from tkinter import Variable
import pandas as pd  
import plotly.express as px
import streamlit as st

#import _ as _

st.set_page_config(
    page_title="GIP Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"}
    )

# ---- SIDEBAR ----
st.sidebar.header("Gelieve hier te filteren:")
boekjaar = st.sidebar.radio(
    "Selecteer boekjaar:",
    ("Boekjaar 1","Boekjaar 2","Boekjaar 3"),
    index=0
)

st.subheader('Samenstelling Totale Activa', anchor=None)
#######################################################################################
# ---- READ EXCEL ACTIVA ----
#######################################################################################
@st.cache
def get_activa_from_excel():
    df = pd.read_excel(
        io="data/AnalyseReynaers.xlsx",
        engine="openpyxl",
        sheet_name="verticale analyse balans",
        usecols="A:E",
        nrows=100,
        header=2
    )

    # filter row on column value
    activa = ["VASTE ACTIVA","VLOTTENDE ACTIVA"]
    df = df[df['ACTIVA'].isin(activa)]

    return df

df_activa = get_activa_from_excel()
df_activa = df_activa.round({"Boekjaar 1":2, "Boekjaar 2":2, "Boekjaar 3":2})
st.write(df_activa)



st.subheader('Samenstelling Passiva', anchor=None)
#######################################################################################
# ---- READ EXCEL PASSIVA ----
#######################################################################################
@st.cache
def get_passiva_from_excel():
    df = pd.read_excel(
        io="data/AnalyseReynaers.xlsx",
        engine="openpyxl",
        sheet_name="verticale analyse balans",
        usecols="A:E",
        nrows=100,
        header=50
    )

#change headers
# filter row on column value
    passiva = ["EIGEN VERMOGEN","VOORZIENINGEN EN UITGESTELDE BELASTINGEN","SCHULDEN"]
    df = df[df['PASSIVA'].isin(passiva)]

    return df

df_passiva = get_passiva_from_excel()
df_passiva = df_passiva.round({"Boekjaar 1":2, "Boekjaar 2":2, "Boekjaar 3":2})
st.write(df_passiva)


st.subheader('Rentabiliteit Eigen Vermogen', anchor=None)
#######################################################################################
#READ EXCEL FOR REV CHART
#######################################################################################
@st.cache
def get_rev_from_excel():
    df = pd.read_excel(
        io="data/AnalyseReynaers.xlsx",
        engine="openpyxl",
        sheet_name="REV",
        usecols="A:D",
        nrows=10,
        header=1
    )
    # change column names
    df.columns = ["Type","Boekjaar 1","Boekjaar 2","Boekjaar 3"]
    # filter row on column value
    rev = ["REV"]
    df = df[df["Type"].isin(rev)]

    df = df.T #Transponeren
    df = df.rename(index={"Boekjaar 1":"1","Boekjaar 2":"2",
                    "Boekjaar 3":"3"})
    df = df.iloc[1: , :] # Drop first row 
    df.insert(0,"Boekjaar",["Boekjaar 1","Boekjaar 2",
                    "Boekjaar 3"],True)
    df.columns = ["Boekjaar","REV"] # change column names
    df = df.astype({'Boekjaar':'string','REV':'float64'})
    
    return df

df_rev = get_rev_from_excel()
df_rev = df_rev.round({"Boekjaar 1":2, "Boekjaar 2":2, "Boekjaar 3":2})
st.write(df_rev)

fig = px.line(df_rev, x="Boekjaar", y=["REV"], markers=True)
fig.update_layout({
'plot_bgcolor': 'rgba(0, 0, 0, 0)',
'paper_bgcolor': 'rgba(0, 0, 0, 0)',})

fig.update_traces(line=dict(width=3))
st.plotly_chart(fig, use_container_width=True)


st.subheader('Liquiditeit', anchor=None)

#######################################################################################
#READ EXCEL LIQUIDITEIT
#######################################################################################
@st.cache
def get_liq_from_excel():
    liq = pd.read_excel(
        io="data/AnalyseReynaers.xlsx",
        engine="openpyxl",
        sheet_name="Liquiditeit",
        usecols="A:D",
        nrows=20,
        header=1
    )

    liq.columns= ["type","Boekjaar 1","Boekjaar 2", "Boekjaar 3"]
    type= ['Liquiditeit in ruime zin','Liquiditeit in enge zin']
    liq= liq[liq['type'].isin(type)]

    liq = liq.T #Transponeren
    liq = liq.rename(index={"Boekjaar 1":"1","Boekjaar 2":"2",
                    "Boekjaar 3":"3"})
    liq = liq.iloc[1: , :] # Drop first row 
    liq.insert(0,"Boekjaar",["Boekjaar 1","Boekjaar 2",
                    "Boekjaar 3"],True)
    liq.columns = ["Boekjaar","Liquiditeit in ruime zin","Liquiditeit in enge zin"] # change column names
    liq = liq.astype({'Boekjaar':'string','Liquiditeit in ruime zin':'float64','Liquiditeit in enge zin':'float64'})
    
    return liq


df_liq = get_liq_from_excel()
df_liq = df_liq.round({"Boekjaar 1":2, "Boekjaar 2":2, "Boekjaar 3":2})
st.write(df_liq)


fig = px.line(df_liq, x="Boekjaar", y=["Liquiditeit in ruime zin", "Liquiditeit in enge zin"], markers=True, range_y=[0,2.6])
fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)',})

fig.update_traces(line=dict(width=3))
st.plotly_chart(fig, use_container_width=True)


st.subheader('Solvabiliteit', anchor=None)
#######################################################################################
#READ EXCEL SOLVABILITEIT
#######################################################################################
@st.cache
def get_solv_from_excel():
    solv = pd.read_excel(
        io="data/AnalyseReynaers.xlsx",
        engine="openpyxl",
        sheet_name="Solvabiliteit",
        usecols="A:D",
        nrows=20,
        header=0
    )
    #change headers
    solv.columns = ["Type","Boekjaar 1","Boekjaar 2","Boekjaar 3"]
    # filter row on column value
    componenten = ["EIGEN VERMOGEN","TOTAAL VAN DE PASSIVA","Solvabiliteit"]
    solv = solv[solv['Type'].isin(componenten)]

    return solv

df_solv = get_solv_from_excel()
df_solv = df_solv.round({"Boekjaar 1":2, "Boekjaar 2":2, "Boekjaar 3":2})
st.write(df_solv)


#######################################################################################
#READ EXCEL KLANT EN LEVERANCIERSKREDIET
#######################################################################################
@st.cache
def get_kredieten_from_excel():
    kredieten = pd.read_excel(
        io="data/AnalyseReynaers.xlsx",
        engine="openpyxl",
        sheet_name="KlantLevKrediet",
        usecols="A:D",
        nrows=20,
        header=1
    )

    liq.columns= ["type","Boekjaar 1","Boekjaar 2", "Boekjaar 3"]
    type= ['type,','Klantenkrediet','Leverancierskrediet']
    liq= liq[liq['type'].isin(type)]

    liq = liq.T #Transponeren
    liq = liq.rename(index={"Boekjaar 1":"1","Boekjaar 2":"2",
                    "Boekjaar 3":"3"})
    liq = liq.iloc[1: , :] # Drop first row 
    liq.insert(0,"Boekjaar",["Boekjaar 1","Boekjaar 2",
                    "Boekjaar 3"],True)
    liq.columns = ["Boekjaar","Klantenkrediet","Leverancierskrediet"] # change column names
    liq = liq.astype({'Boekjaar':'string','Liquiditeit in ruime zin':'float64','Liquiditeit in enge zin':'float64'})
    
    return liq

#fig = px.bar(df_klantlev, x=['Klanntenkrediet', 'Levkrediet', 'Tot aant dagen...', '...'],
        #orientation='h',
        #barmode='group',
        #title='klantlevkrediet',
        #range_x=[],
        #labels={'value', 'aant dagen'}
        #text_auto=True
#fig.update_traces()
#st.plotly_chart(fig, use_container_width=True)

#to update colors of lines, xaxis yaxis titles, etc search in streamlit
#fig.update_layout(xaxis_title="")






fig_activa = px.pie(df_activa, 
            values=boekjaar, 
            names='ACTIVA',
            title=f'Samenstelling activa {boekjaar}'            
            )
fig_activa.update_traces(textfont_size=20, pull=[0, 0.2], marker=dict(line=dict(color='#000000', width=2)))
fig_activa.update_layout(legend = dict(font = dict(size = 20)), title = dict(font = dict(size = 30)))
fig_activa.show()









#HIDE STREAMLIT STYLE
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)