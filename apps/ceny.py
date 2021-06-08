#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import matplotlib.pyplot as plt 

def app():


    st.title('Ceny vybraných surovin, akcií a bitcoinu')


    st.subheader('\n')

    st.success('''
    Data byla získána z historických přehledů na Yahoo Finance \n
    za období od roku 2015 do roku 2020
    ''')

    with st.beta_expander('ÚVOD'):
        st.text('''
        - K porovnání vývoje cen v jednotlivých letech jsem naprogramoval tutu aplikaci
        - Obsahuje aktiva, která mě zajímala
        - Jednotlivé soubory byly staženy jako csv
        - Následně spojeny do jednoho souboru v Excelu a importovány zpět do csv formátu
        - V Pythonu převedeny na DataFrame a dále upravována pro vyplotování v Plotly
        - Komodita nazvana "Med" je "Měď" chem. zn. Cu
        - Ceny jsou uvedeny v USD
        ''')

    col1, col2 = st.beta_columns(2)
    img1 = Image.open('apps/obrazek/ropa.jpg')
    img2 = Image.open('apps/obrazek/zlato.jpg')
    with col1:
        st.image(img1, use_column_width=True)
    with col2:
        st.image(img2, use_column_width=True)


    col3, col4 = st.beta_columns(2)
    img3 = Image.open('apps/obrazek/airbus.jpg')
    img4 = Image.open('apps/obrazek/bitcoin.jpg')
    with col3:
        st.image(img3, use_column_width=True)
    with col4:
        st.image(img4, use_column_width=True)

    # nactu si data
    @st.cache
    def load():
        df = pd.read_csv('ceny4.csv', index_col = 'Date')
        #df['Date'] = pd.to_datetime(df['Date']) # když to odkomentuji dělá to nehezké krivky v plotly musím v read_csv nechat index_col
        #df = df.set_index('Date')

        #df = df.dropna()
        #df['Close'] = df['Close'].astype(float)
        #df['Close'] = round(df['Close'], 2)

        
        jmena_titulu = df.columns[:-1]

        return df, jmena_titulu

    df, jmena_titulu = load()

    st.sidebar.title('Data k zobrazení')

    # pri zakliknutí se zobrazi dataframe
    ukaz = st.sidebar.checkbox(label='Zobraz dataset')

    if ukaz:
        st.write(df)


    # zde zkusím dostat slider oboustranný
    st.subheader('Přehled aktiv v jednotlivých letech')

    #roky = [2015, 2016, 2017, 2018, 2019, 2020]                            # původně stejné rozhraní jako multiselekt
    #year = st.multiselect(label='Vyber rozsah', options=roky)              # původně stejné rozhraní jako multiselekt
    slid = st.slider('Vyber rozsah:', 
                    #options=[2015, 2016, 2017, 2018, 2019, 2020],
                    #value=[2015,  2020], 1)
                    2015, 2020, (2015,2020))

    #df = df[df['Date'].dt.year == year]

    #st.subheader('Data pro rok(y) {}'.format(slid))                         # popis k  multiselekt
    #st.write('Vybraný rozsah:', year, year[0], year[1])


    st.subheader('Výběr titulů k zobrazení vývoje ceny')

    vyber = st.multiselect(label='Vyber si aktiva k porovnání', options=jmena_titulu)

    #st.text(vyber)

    #df = df[df['rok'].isin(year)]   # původně stejné rozhraní jako multiselekt

    df = (df.query(f"rok.between{slid}"))

    vyber_aktiv = df[vyber]


    if not vyber_aktiv.empty:

        plotly_graf = px.line(data_frame=vyber_aktiv,
                            x=vyber_aktiv.index,
                            y=vyber,
                            title= 'Vývoj ceny v čase')

        st.plotly_chart(plotly_graf)

    #st.write(vyber_aktiv)

    #slid= st.slider('vyber rok', 
    #                #options=[2015, 2016, 2017, 2018, 2019, 2020],
    # #               #value=[2015,  2020], 1)
    #                2015, 2020, (2015,2020))
    #
    #st.write('Rozsah je:', slid)
    #st.write(df)
    #st.write(df.query(f"rok.between{slid}"))


    #zkusím do barchartu
    st.subheader('Základní statistiky')
    if not vyber_aktiv.empty:   
        popis_dat = (vyber_aktiv.describe())
        statistiky = popis_dat.iloc[[1,3,7]]
        st.write(statistiky)
        stat = statistiky.unstack().swaplevel(1).unstack()
        #fig = plt.subplots()
        #stat.plot.bar()
        #st.pyplot()
        fig,ax = plt.subplots()
        stat.plot.bar(ax=ax)
        st.pyplot(fig)













