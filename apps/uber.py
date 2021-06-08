import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import os

def app():

    st.title('**Uber a Lyft v Bostnu**')


    from PIL import Image
    im_container = st.beta_container()
    #img = Image.open('uber lyft.png')
    #img = Image.open(os.path.join(r'C:\Users\petr\Desktop\pr\uber lyft.png'))
    #with im_container:
    #    st.image(img)
    img = Image.open('apps/obrazek/uber lyft.PNG')    
    with im_container:
        st.image(img)


    st.subheader('''
    Dataset ke zpracování je dostupný zde:
    https://www.kaggle.com/brllrb/uber-and-lyft-dataset-boston-ma
    Dataset je dle autora ideální zejména pro sestavení modelu lineární regrese.
    Model sestavovat nebudu.
    Popíšu zde, čím se Uber odlišuje od Lyftu.
    K úpravě dat napíšu skript v Pythonu a použiji tyto knihovny:
    - numpy,
    - pandas,
    - seaborn,
    - matplotlib,
    - pillow.

    ''')

    @st.cache
    def fetch_data():
        df = pd.read_csv('uber_lyft.csv')
        return df

    df = fetch_data()

    if st.checkbox('Ukaž výchozí dataset'):
        radky = (df.shape)
        st.write('Počet řádků a  sloupců:', radky)
        st.subheader('Data pro zpracování')
        st.write(df.head(10))

    chybejici_hodnoty = st.beta_container()
    with chybejici_hodnoty:
        st.subheader(' Zobrazím si chybějící hodnoty')
        fig = plt.figure()
        sns.heatmap(df.isnull(), cbar=False)
        st.pyplot(fig)
        st.text('Z grafu je vidět, že nám chybí data ve sloupečku "price"')


    st.text('Uložím si jen ty hodnoty, kde mi nechybí cena')

    df=df[df['price'].isnull()==False]
    df.shape

    st.info("""I po vyčištění dat mi zbylo v datasetu 637 976 řádků a 11 sloupců.
            Data jsou v rozmezí od 26.11. do 18.12.2018. Postupně budu souborem procházet
            a klást si otázky týkající se Uberu a Lyftu.
            Na ně si odpovím především grafickou formou, a rovněž letmým komentářem.
    """)

    vic_zakazniku = st.beta_container()
    with vic_zakazniku:
        st.subheader('Zjistím kdo v Bostnu vozí víc zákazníků Uber nebo Lyft?')
        fig = plt.figure()
        sns.countplot(x = df['cab_type'], palette= 'GnBu')
        plt.xlabel('')
        plt.title('Kdo má v Bostnu víc cestujících', fontsize=18)
        st.pyplot(fig)
        st.text('V absolutním počtu za sledované období vykonal Uber víc cest než Lyft')


    kolik_zakazniku = st.beta_container()
    with kolik_zakazniku:
        st.subheader('Chci vidět kolik vozí zákazníků UBER x LYFT')
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index(['datetime'], inplace=True)

        #Zjistim z datetime, zdali mám víkend nebo ne a dál si upravím data pro vyplotování
        df["day_of_week"]  = df.index.day_name()
        df.sort_index(inplace=True)
        df = df.assign(pocet = 1)
        df_uber = df[df['cab_type'] == 'Uber']
        df_lyft = df[df['cab_type'] == 'Lyft']
        df_uber_pocet = df_uber[['pocet']].groupby(level=0).count()
        df_lyft_pocet = df_lyft[['pocet']].groupby(level=0).count()
        df_uber_pocet = df_uber_pocet.resample('d').sum()
        df_lyft_pocet = df_lyft_pocet.resample('d').sum()
        # vyplotuji
    
        figure, ax1 = plt.subplots()
        figure.set_size_inches(15,6)

        sns.lineplot(data = df_uber_pocet, x = df_uber_pocet.index, y = 'pocet', ax = ax1, label ='Uber')
        sns.lineplot(data = df_lyft_pocet, x = df_lyft_pocet.index, y = 'pocet', ax = ax1, label = 'Lyft')
        plt.title('Počet zákázníků UBER vs. LYFT', fontsize=18)
        plt.xlabel('');
        plt.xticks(rotation=60)
        st.pyplot(figure)

    st.header('Zobrazím si průměrnou ujetou vzdálenost a cenu')
    st.text('Data použiji z těchto upravených údajů:')
    st.text(df.head())


    ujeta_vzdalenost = st.beta_container()
    with ujeta_vzdalenost:
        st.subheader('Zobrazím si boxplot, abych viděl průměrné ceny a také odlehlé hodnoty')
        # vyplotuji
        fig =  plt.figure()
        sns.boxplot(x = 'cab_type', y = 'price', data = df)
        plt.title('Průměrná cena a odlehlé hodnoty UBER vs. LYFT', fontsize = 14);
        plt.grid()
        plt.xlabel('')
        st.pyplot(fig)
        st.text("""
            Medián ceny obou taxislužeb se nachází pod hodnotou 20 dolarů.
            Uber má míň odlehlých hodnot oproti Lyftu.
        """)


    ujeta_vzdalenost = st.beta_container()
    with ujeta_vzdalenost:
        st.subheader('Nyní chci vidět průměrnou ujetou vzdálenost, také zde si naprogramuji boxplot')
        # vyplotuji
        fig =  plt.figure()
        sns.boxplot(x = 'cab_type', y = 'price', data = df)
        plt.title('Průměrná cena a odlehlé hodnoty UBER vs. LYFT', fontsize = 14);
        plt.grid()
        plt.xlabel('')
        st.pyplot(fig)
        st.text("""
            Co se týká ujeté vzdálenosti je situace víceméně vyrovnaná.
            Nepatrně víc toho ujede Uber, přičemž má také o něco vyšší variabilitu v najetých vzdálenostech. 
            Zde se situace tedy oproti ceně otočila.
        """)


    poptavka_den = st.beta_container()
    with poptavka_den:
        st.subheader('Zajímá mě, jak se vyvíjí poptávka v průběhu dne')
        #st.info('Jak vypadá zdrojový kód?')
        with st.beta_expander('Podívat se na kód'):
            st.code("""
                # zde si upravím kód pro následné vyplotování
                zatizeni_po_hodine = df[['hour', 'cab_type', 'pocet']].groupby(['hour', 'cab_type']).size()
                zatizeni_po_hodine = pd.DataFrame(zatizeni_po_hodine)
                # unstacknu multiindex
                zatizeni_po_hodine = zatizeni_po_hodine.unstack(1) 
                zatizeni_po_hodine = zatizeni_po_hodine[0]
                # přehazuji si pořadí sloupců, aby mi seděla barva liny
                zatizeni_po_hodine = zatizeni_po_hodine[['Uber', 'Lyft']] 
                # zobrazím
                fig, ax = plt.subplots(figsize=(12,8))
                zatizeni_po_hodine.plot(ax = ax, linewidth = 2)
                ax.set_ylabel('Počet zákazníků')
                ax.set_xlabel('')
                ax.set_title('Vytíženost v průběhu dne UBER vs. LYFT', fontsize=14)
                plt.xticks([0,2,4,6,8,10,12,14,16,18,20,22])
                ax.legend()   
                st.pyplot(fig)
                st.text('''
                Největší průměrná vytíženost (špička) nastává jak pro Uber tak pro Lyft k půlnoci,
                přičemž Uber v Bostnu dominuje.
                ''')
            """)


        # zde si upravím kód pro následné vyplotování
        zatizeni_po_hodine = df[['hour', 'cab_type', 'pocet']].groupby(['hour', 'cab_type']).size()
        zatizeni_po_hodine = pd.DataFrame(zatizeni_po_hodine)
        # unstacknu multiindex
        zatizeni_po_hodine = zatizeni_po_hodine.unstack(1) 
        zatizeni_po_hodine = zatizeni_po_hodine[0]
        # přehazuji si pořadí sloupců, aby mi seděla barva liny
        zatizeni_po_hodine = zatizeni_po_hodine[['Uber', 'Lyft']] 
        # zobrazím
        fig, ax = plt.subplots(figsize=(12,8))
        zatizeni_po_hodine.plot(ax = ax, linewidth = 2)
        ax.set_ylabel('Počet zákazníků')
        ax.set_xlabel('')
        ax.set_title('Vytíženost v průběhu dne UBER vs. LYFT', fontsize=18)
        plt.xticks([0,2,4,6,8,10,12,14,16,18,20,22])
        ax.legend()   
        st.pyplot(fig)
        st.text("""
        Největší průměrná vytíženost (špička) nastává jak pro Uber tak pro Lyft k půlnoci,
        přičemž Uber v Bostnu dominuje.
        """)


    prehled_hodin = st.beta_container()
    with prehled_hodin:
        st.subheader('Chci souhrnný, detailnější přehled vývoje poptávky během týdne po hodinách')
        # upravim kod
        df.reset_index(inplace=True)
        df1 = df.copy()
        df1['datetime'] = df1['datetime'].dt.strftime('%Y-%m-%d')
        df1['datetime'] = pd.to_datetime(df1['datetime'])
        df1.set_index('datetime', inplace = True)
        df1['day_of_week'] = pd.Categorical(df1['day_of_week'],
                                            categories = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],
                                            ordered = True)
        hour_weekday = df1.groupby(['day_of_week', 'hour']).count()['pocet'].unstack()  
        # vyplotuji kod
        fig =  plt.figure()
        sns.heatmap(hour_weekday,
            cmap = 'YlGnBu',
            linecolor = 'white',
            linewidth = .2
            )
        plt.title('Rozložení počtu cestujících z hlediska dne a hodiny', fontsize = 14)
        st.pyplot(fig)
        st.text("""
            Graf zobrazuje rozložení počtu cestujících v průběhu týdne od pondělí do neděle.
            Den je rozložen na ose x po hodinách. 
            Průměrně jsou taxi-přepravci nejvytíženější v pondělí takřka po celý den. 
            Špičky je dosaženo na přelomu pondělí a úterý.
            Nejmíň práce mají od půlnoci do devaté hodiny ráno ve středu.
        """)


    vyvoj_poptavky = st.beta_container()
    with vyvoj_poptavky:
        st.subheader('Zobrazím vývoj poptávky po taxi v průběhu času v absolutních číslech')
        # upravim si kod
        df2 = df1.groupby('datetime')['cab_type'].value_counts().unstack()    
        # vyplotuji kod
        fig, ax =  plt.subplots()
        df2 = df2[['Uber', 'Lyft']]
        df2.plot.bar(figsize = (16,6), rot = 60, ax = ax);
        plt.title('Počet zákazníků UBER x LYFT v jednotlivých dnech', fontsize = 18)
        plt.xlabel('')
        st.pyplot(fig)
        st.text("""
            Z grafu je patrno, že ani v jeden den neměl Lyft víc cest v jednom dni jak Uber.
        """)


    vytizenost_po_dni = st.beta_container()
    with vytizenost_po_dni:
        st.subheader('Chci vidět vytíženost v jednotlivých dnech týdne')  
        # vyplotuji 
        #fig =  plt.figure()
        fig = plt.figure(figsize = (20,11))
        ax1 = plt.subplot2grid((2,2), (0,0), fig = fig)
        ax2 = plt.subplot2grid((2,2), (0,1), fig = fig)

        sns.histplot(df1['day_of_week'], ax = ax1, color = 'orange')
        ax1.set_xlabel('')
        ax1.set_title('Celkový počet cestujících taxíkem v průběhu týdne', fontsize = 18)
        ax1.set_xticklabels(labels = ['Monday', 'Tuesday', 'Wednesday', 'Thurstday', 'Friday', 'Saturday', 'Sunday'], rotation = 40)

        df2 = df1.groupby('day_of_week')['cab_type'].value_counts().unstack()#.plot.bar()
        df2 = df2[['Uber', 'Lyft']]
        df2.plot.bar(ax = ax2, rot = 40)
        ax2.set_xlabel('')
        ax2.set_title('UBER vs. LYFT', fontsize = 18);

        st.pyplot(fig)
        st.text("""
            Co do počtu cest, respektive cestujících v průběhu týdne, 
            tak průměrně je nejvytíženějším dnem úterý, následuje pondělí. 
            Nejklidnějším dnem je v souhrnu středa.
        """)



    cena = st.beta_container()
    with cena:
        st.subheader('Jak se vyvíjí cena?')
        # upravim si kod - vyfiltruji si jen zvlast uber, zvlast lyft
        filter_ub = df1['cab_type'] == 'Uber'
        data_uber = df1.loc[filter_ub]
        filter_ly = df1['cab_type'] == 'Lyft'
        data_lyft = df1.loc[filter_ly]
        # spocitam smerodatne odchylky
        (round(data_uber['price'].std(),2))
        (round(data_lyft['price'].std(),2))
        # vyplotuji kod
        fig, ax =  plt.subplots()
        plt.hist(data_uber['price'],
        bins= 50,
        color= 'g',
        alpha=.5,
        label='Cena Uber')
        plt.legend()
        plt.hist(data_lyft['price'],
        bins= 50,
        color= 'r',
        alpha=.5,
        label='Cena Lyft')
        plt.legend()
        plt.title('Rozložení ceny UBER vs. LYFT', fontsize= 14);

        st.pyplot(fig)
        st.text("""
            Zde vidíme, do jaké míry se překryvají ceny obou konkurentů, 
            podíváme-li se na jejich rozložení... 
            Ve více jak desetitisících případech si Lyft naúčtoval cenu, 
            za kterou Uber vůbec nejezdil. Přečemž dle rozdělení Uber jezdí za všechny možné ceny, 
            přibližně od 5 dolarů až do 50, 
            kdežto u Lyftu jsou z rozdělení patrné jisté mezery 
            (intervaly ceny, která se v tom rozmezí od 5 do 50 dolarů nevyskytuje).
        """)


    prehled_ceny = st.beta_container()
    with prehled_ceny:
        #vyplotuji si histogramy vedle sebe
        fig, axis = plt.subplots(1,2, figsize= (17,6))

        a=sns.histplot(data_uber['price'],
        bins= 100,
        color= 'g',
        ax = axis[0]).set(title= 'UBER')
                    
        sns.histplot(data_lyft['price'],
        bins= 100,
        color= 'r',
        ax = axis[1]).set(title= 'LYFT')

        fig.suptitle('Rozložení ceny', fontsize= 20);

        st.pyplot(fig)
        st.text("""
        Dle rozložení je nejtypyčtější cenou pro Uber cena kolem 10 dolarů. 
        Pro Lyft je to cena kolem 20 dolarů. 
        Dle směrodatné odchylky se ceny víc liší u Lyftu jsou více 'rozmanitější'.
        """)

        st.info('Směrodatná odchylka Uber:   8.56')
        st.info('Směrodatná odchylka Lyft:   10.02')

    with st.beta_expander('Teorie k směrodatné odchylce'):
        st.text('Směrodatnou odchylku lze spočítat dle následujícího vzorce:')
        r'''
        $$s = \sqrt{\frac{1}{N-1}\sum_{i=1}^N(x_i-\bar{x})^2}$$
        '''
        st.text('''
        Směrodatná odchylka říká, jak moc se od sebe liší pozorované veličiny v souboru hodnot.
        Přičemž, čím větší je směrodatná odchylka, tím víc se pozorované veličiny od sebe odlišují.
        ''')
        st.markdown('Zdroj: _https://cs.wikipedia.org/wiki/Sm%C4%9Brodatn%C3%A1_odchylka_')

    prum_cena = st.beta_container()
    with prum_cena:
        # zobrazeni prumerne ceny
        fig = plt.figure()
        sns.barplot(x= 'cab_type', y= 'price', data= df1)
        plt.title('Průměrná cena', fontsize= 18)
        plt.xlabel('');
        st.pyplot(fig)
        st.text('Uber jezdí průměrně za 15.5 dolarů. Lyft pak za bezmála 17.5 dolaru.')



    cena_vzdalenost = st.beta_container()
    with cena_vzdalenost:
        st.subheader('Jak se vyvíjí cena u Uberu vs. Lyftu v závislosti na ujeté vzdálenosti?')
        # vyberu z datasetu jen 100 vzorků
        df1 = df.copy()
        df1_vzorek = df1.sample(100)
        df1_vzorek = df1_vzorek.copy()
        # zobrazeni prumerne ceny
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plt.figure()
        sns.lmplot(x= 'distance', y= 'price', data= df1_vzorek, hue= 'cab_type')
        plt.title('Vztah mezi vzdáleností a cenou', fontsize= 18);
        st.pyplot()
        #st.set_option('deprecation.showPyplotGlobalUse', False)
        st.text("""
        Graf popisuje vztah mezi ujetou vzdáleností a cenou. 
        Zde jsem pro vykreslení regresních přímek použil funkci "sample". 
        Ta z celeho datasetu vybere náhodně 100 řádku.
        Proto se sklon přímek bude s každým načtením měnit.
        Ten kdo bude mít křivku strmější, u toho roste cena v zavíslosti na ujeté vzdálenosti 
        rychleji než u druhého.
        """)

    cena_tyden = st.beta_container()
    with cena_tyden:
        st.subheader('Jaká je cena v průběhu týdne?')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        # zobrazeni prumerne ceny
        plt.figure(figsize= (15,6))
        st.set_option('deprecation.showPyplotGlobalUse', False)
        sns.set_style('dark')
        sns.set_context('talk')
        sns.stripplot(x= 'day_of_week', y= 'price', data= df1_vzorek, hue= 'cab_type', jitter= True, dodge= True)
        plt.xlabel('')
        plt.title('Cena v průběhu týdne Uber vs. Lyft', fontsize= 18);
        st.pyplot()
        st.text("""
        Vesměs byly z náhodného výběru v průběhu celého týdne pozorovány nižší průměrné ceny u Lyftu...
        (potvrzjí to náhodné testovací výběru pro 1000 vzorků)
        """)


    vzdalenost_tyden = st.beta_container()
    with vzdalenost_tyden:
        st.subheader('Jak se mění ujetá vzdálenost v průběhu týdne')
        #st.set_option('deprecation.showPyplotGlobalUse', False)
        # zobrazeni prumerne ceny
        fig = plt.figure(figsize= (15,6))
        sns.barplot(x= 'day_of_week', y= 'distance', data= df1, hue= 'cab_type')
        plt.xlabel('')
        plt.title('Ujetá vzdálenost v průběhu týdne Uber vs. Lyft', fontsize= 18);
        st.pyplot(fig)
        st.text("""
        Průměrně ujede větší vzdálenost Uber od pondělí do středy. 
        Ve čtvrtek jsou na tom obě taxislužby stejně. V pátek a sobotu toho ujede v průměru víc Lyft. 
        A v neděli je o něco víc žádanější Uber.
        """)


    mista = st.beta_container()
    with mista:
        st.subheader('Odkud se v Bostnu jezdí?')
        # zobrazim mista na mape
        #st.map(df)
        st.text("""
            Jak patrno, naše data obsahují jen údaje o místech, 
            která se až na jedno nachází především kolem centra Bostnu.
            Záznamy v datasetu poskytují dle souřadnic jen dvanáct 12 míst.
        """)


    st.map(df)





