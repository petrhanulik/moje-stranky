#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from PIL import Image
from multiapp import MultiApp
from apps import  uber, ceny, odkazy

st.set_page_config(
        page_title='Portfolio',
        page_icon='📈',
    )

app = MultiApp()



st.markdown("""
# Prezentace mých projektů 

Zde jsou tři odkazy na mé projekty naprogramované v rámci [Engeto Datové Akademie](https://engeto.cz/datova-akademie/) \n
a nad její rámec 

* všechny skripty byly napsány v jazyce Python
""")


with st.beta_expander('Získaný Certifikát'):
        st.text('''
        Certifikát z Datové Akademie
        ''')
        im_container = st.beta_container()
    
        img = Image.open('apps/obrazek/certifikat.jpg')    
        with im_container:
            st.image(img)



app.add_app('UNIVERSITY RANKING IN THE UK', ma.app)
app.add_app('Uber vs. Lyft v Bostnu', uber.app)
app.add_app('Porovnání cen aktiv', ceny.app)
app.add_app('Odkazy na GitHub', odkazy.app)
app.run()


st.text("""
.
.
.
""")

st.write('📊')



