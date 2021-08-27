import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import chart_studio.plotly as py
import plotly.graph_objects as go
import chart_studio.plotly as py
import chart_studio
chart_studio.tools.set_credentials_file(username='petrhanulik', api_key='DM1dA4eDt2dEIRzfWsXG')
import streamlit as st
from PIL import Image

def app():


    st.title('UNIVERSITY RANKING IN THE UK')
    st.text("""

    """)
    st.subheader('BI & Data Visualization Case Study')

    st.markdown('__Context description:__')
    st.text("""
    UK Higher Education (HE) market has undergone a major change 
    after students started paying for the tuition.
    Students now paying considerable amount annually have become “Customers” of Universities
    who have to make sure they provide students with the best service possible
    for their money paid.
    This creates challenges for many institutions.
    Well-recognized university institution is going though the change process
    to find a new way of working with their with data
    to derive value and management-relevant information. 
    """)

    st.text("""
    Analysis needs to be done to discover which areas
    in the institution may have the most positive impact on ranking.
    This analysis will be used to influence University’s business strategy... 
    """)


    st.markdown('*University of Cambridge:*')
    im_container = st.beta_container()
    img = Image.open('cambridge.jpg')    
    with im_container:
        st.image(img)

    st.markdown('*University of Oxford:*')
    im_container = st.beta_container()
    img = Image.open('oxford.jpg')    
    with im_container:
        st.image(img)

    @st.cache(allow_output_mutation=True)
    def fetch_data():
        df = pd.read_excel('rank.xlsx', engine='openpyxl')
        return df

    df = fetch_data()



    st.subheader('Dataset to be analysed:')
    st.text("""

    """)
    st.write(df.head())

    st.warning('I wanna see missing values in dataset:')
    st.write(df.isna().any())

    st.text('I am interested in the shape of datasets and the header')
    st.markdown('__(rows, columns__)')

    st.write(df.shape)
    st.write(df.head())

    df1 = df.copy()
    df1 = df1[df1['Ranking Year']==2015]
    df1 = df1.dropna()
    df1 = df1.sort_values('Ranking')
    df1 = df1[:20]

    st.subheader('What determines the ranking most??')
    st.write((df[['Institution', 'Ranking Year', 'Guardian score/100', 'NSS Teaching (%)', 'NSS Overall (%)', 'Expenditure per student / 10', 'Student:staff ratio', 'Career prospects (%)', 'Ranking']].sort_values('Ranking')[:10]) )
    st.text("""
    It´s for sure that "Guardian score" determinates Ranking over with other factors.
    OK, but what else? which factors have a strong influence on the ranking in the evaluation? What else determinates ranking?
        """)

    df.drop(['Ranking Year'],axis=1, inplace=True) # delete column with Ranking Year
    df.corr()
    df = df.sort_values('Ranking')
    df['NSS Teaching (%)'] = df['NSS Teaching (%)'].rank(ascending=False)     # is student satisfied with teaching
    df['NSS Overall (%)'] = df['NSS Overall (%)'].rank(ascending=False)       # overall satisfaction
    df['Expenditure per student / 10'] = df['Expenditure per student / 10'].rank(ascending=False)
    df['Student:staff ratio'] = df['Student:staff ratio'].rank()              # the smaller the number the better is UNI in ranking number of students per member of teaching staff
    df['Career prospects (%)'] = df['Career prospects (%)'].rank(ascending=False)
    df['Value added score/10'] = df['Value added score/10'].rank(ascending=False) 
    ##The value-added score compares students' individual degree results with their entry qualifications, 
    ##to show how effective the teaching is. It is given as a rating out of 10
    ##
    df['Entry Tariff'] = df['Entry Tariff'].rank(ascending=False)             #scores of students - UCAS Tariff points translate your qualifications and grades into a numerical value
    df['NSS Feedback (%)'] = df['NSS Feedback (%)'].rank(ascending=False)

    koreluj = st.beta_container()
    with koreluj:
        fig = plt.figure(figsize=(13,7))
        sns.heatmap(df.corr(),annot=True)
        st.pyplot(fig)
        st.text('The picture gives me an overview of correlation between ranking and other factors.')
        st.text("""
        But strong correlation between ranking and Engry tariff doesn't mean
        that Entry tariff causes great ranking.
            """)

    st.subheader('I wanna plot selected factors for 2015')
    st.text('To see how much factors change based on the ranking by first 20 universities')



    tr1 = go.Scatter(
                    x = df1['Ranking'],
                    y = df1['NSS Teaching (%)'],
                    mode = 'lines+markers',
                    name = 'National students survey Teaching',
                    marker = dict(color='green'),
                                  text=df1['Institution']
                    )

    tr2 = go.Scatter(
                    x = df1['Ranking'],
                    y = df1['NSS Overall (%)'],
                    mode = 'lines',
                    name = 'National students survey Overall',
                    marker = dict(color='blue'),
                                  text=df1['Institution']
                    )
    tr3 = go.Scatter(
                    x = df1['Ranking'],
                    y = df1['Expenditure per student / 10'],
                    mode = 'lines+markers',
                    name = 'Expenditure per student',
                    marker = dict(color='black'),
                                  text=df1['Institution']
                    )

    tr4 = go.Scatter(
                    x = df1['Ranking'],
                    y = df1['NSS Overall (%)'],
                    mode = 'lines',
                    name = 'National students survey Overall',
                    marker = dict(color='yellow'),
                                  text=df1['Institution']
                    )
    tr5 = go.Scatter(
                    x = df1['Ranking'],
                    y = df1['Student:staff ratio'],
                    mode = 'lines+markers',
                    name = 'Student:staff ratio',
                    marker = dict(color='orange'),
                                  text=df1['Institution']
                    )

    tr6 = go.Scatter(
                    x = df1['Ranking'],
                    y = df1['Career prospects (%)'],
                    mode = 'lines',
                    name = 'Career prospects',
                    marker = dict(color='red'),
                                  text=df1['Institution']
                    )

    tr7 = go.Scatter(
                    x = df1['Ranking'],
                    y = df1['NSS Feedback (%)'],
                    mode = 'lines+markers',
                    name = 'NSS Feedback',
                    marker = dict(color='purple'),
                                  text=df1['Institution']
                    )

    data=[tr1, tr2, tr3, tr4, tr5, tr6, tr7]
    layout=dict(title='Selected Factors vs Ranking',
                xaxis=dict(title='Ranking', ticklen=5, zeroline=False)
               )

    fig=dict(data=data, layout=layout)
    st.plotly_chart(fig)


    st.subheader('Where I´m standing in selected attributes (Edinburgh vs. Others) 2015')
    st.text("""To see how much factors change based on the ranking by first 20 universities
    Attributes:

    - NSS Overall (Student Satisfaction)
    - Student/Staff ratio,
    - Expenditure per student.
    """)


    data=[
         {
             'x':df1['Ranking'],
             'y':df1['Student:staff ratio'],
             'mode':'markers',
             'text':df1['Institution'],
             'marker':{
                 'color':df1['NSS Overall (%)'],                     # color scaling represent overall satisfaction
                 'size':df1['Expenditure per student / 10'],         #expenditure_student,
                 'showscale':True
             },
         }   
    ]

    layout = go.Layout(
        title='Edingurgh vs. competition',
        xaxis=dict(
            title='Ranking'
        ),
        yaxis=dict(
            title='Student/staff ratio'
        ) ) 
    fig=go.Figure(layout=layout,data=data) 
    st.plotly_chart(fig)

    st.markdown(' __NSS Overall (Student Satisfaction)__ is displayed in color - the lighter the better ')
    st.markdown(' __Expenditure per student__ is represented by the size of the cycle  - the bigger the higher the expenses ')


    st.subheader('Now I wanna see my position in terms of:')
    st.text("""

    - National student survey Teaching
    - Entry Tariff
    - Ranking... (of course)
    """)
    st.text('Entry tariffs could be solid measure. Higher tariff => higher quality of applicants...')


    barva=df1['Career prospects (%)']
    #velikost=df1['Expenditure per student / 10'] 

    data=go.Scatter3d(
        x=df1['Ranking'],
        y=df1['NSS Teaching (%)'],
        z=df1['Entry Tariff'],
        mode='markers',
        text=df1['Institution'],
        marker= dict(
             size=10,
             color=barva,
             colorscale= 'amp',
             autocolorscale=False

            #['blue', 'green', 'red', 'yellow', 'purple']
        )
    )

    layout=go.Layout(
        margin={
           'l':0,
           'r':0,
           'b':0,
           't':0
        }
    )
    fig=go.Figure(data=data, layout=layout)
    st.plotly_chart(fig)

    st.markdown('__Now I´m able to see my position in terms of 4 metrics:__')   
    st.text("""
    1.Ranking.......................x axis
    2.Satisfaction with teaching....y axis 
    3.Entry tariff..................z axis
    4.Career prospects..............color (the darker the better)
    """)


    st.subheader('Who improved over the period 2013-2015 most?')
    st.text('Editing and operations on data:')
    st.info('Now a script was written to get the 5 top improvers between 2013 and 2015 ')

    df2 = pd.read_excel('rank.xlsx')
    df2013 = df2[df2['Ranking Year']==2013]
    df2015 = df2[df2['Ranking Year']==2015]
    df2013 = df2013.set_index('Institution')
    df_new = df2015.set_index('Institution').join(df2013[['Ranking']], rsuffix='_2013')
    df_new['Zlepseni/zhorseni'] = df_new['Ranking'] - df_new['Ranking_2013']
    df_new = df_new.sort_values('Zlepseni/zhorseni', ascending=False)
    df2 = df2.set_index(['Institution', 'Ranking Year'])


    st.text('And there you go:')
    st.markdown('The best improver is __*Cardiff Met*__. Improved in ranking table by 32 positions.')
    st.write(df_new.head())


    st.subheader('I wanna see graphicly (on the first glance) in which areas is the improvement significant...')


    uni_selection = ['Cardiff Met', 'West London', 'Anglia Ruskin', 'Birmingham City', 'Aberystwyth']
    src = df2.loc[uni_selection, ['NSS Teaching (%)', 'NSS Overall (%)', 'Expenditure per student / 10', 'Student:staff ratio', 'Career prospects (%)', 'Value added score/10', 'NSS Feedback (%)']]

    df_improvers = src.unstack(0).sort_index(ascending=False)
    df_improvers.head()

    st.markdown('__Development of individual attributes in the years 2013 to 2015 in the table:__')
    st.write(df_improvers.head())

    st.markdown('__Development of individual attributes in the years 2013 to 2015 in the chart :__')

    fig, ax = plt.subplots(figsize=(18,11))
    df_improvers.plot(ax = ax, title='FACTORS from 2013 to 2015', linewidth=3, grid=True, xticks=(2013,2014,2015), legend=False)
    #df.plot(kind='bar', stacked=True, rot=0, figsize=(10,6), legend=False, zorder=3)
    #plt.grid(zorder=0)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    st.pyplot(fig)

    st.write("""
    There where the lines rise the steepest (the fastest)...
    those are the key areas the Edinbourgh University should focus on
    and improve in those.
    """)


    st.subheader('I want see Cardiff Met - factors by factors graphicly')
    st.text('Remember Cardiff Met is Uni with the biggest improvement...')

    cardiff_met = df2.loc[['Cardiff Met']]
    cardiff_met = cardiff_met.reset_index()
    cardiff_met = cardiff_met.drop(['Ranking (Prev)'], axis=1)
    cardiff_met = cardiff_met.drop(['Ranking Change'], axis=1)
    cardiff_met = cardiff_met.drop(['Institution'], axis=1)
    cardiff_met.set_index('Ranking Year', inplace=True)
    st.write(cardiff_met)


    fig, ax = plt.subplots(figsize=(14,12))
    cardiff_met.plot.area(ax = ax, subplots=True)
    st.pyplot(fig)



    st.text('A different point of view...:')

    fig, ax = plt.subplots(figsize=(15, 16))
    cardiff_met.plot.barh(ax = ax, subplots=True)
    st.pyplot(fig)

    st.text("""
    My recommendation is increase the entry tariff, 
    entry tariff have potention to attract better students.
    """)

    st.text("""
    And improve quality of teaching.
    There has been significant improvement in quality of teaching...
    which then goes hand in hand with how student perceive career prospects.
    """)













