import plotly.express as px
import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title='Dashboard', layout="wide")

#@st.cache_data
def load_indicators(indicators_path):
    indicators = pd.read_feather(indicators_path)    
    indicator_names = set(list(indicators.columns.str[:-5])[2:])        
    return  indicators, indicator_names

#@st.cache_data
def load_metadata(metadata_path):
    metadata = pd.read_csv(metadata_path)
    return metadata

#@st.cache_data
def load_map(map_path):
    with open(map_path) as f:
        mapa = json.load(f)    
    return mapa


metadata_indicators = load_metadata('metadata_indicators.csv')
indicators, indicator_names = load_indicators('indicators_data.feather')
mapa = load_map('mapa.geo.json')

tab1, tab2, tab3 = st.tabs(["Correlation Explorer", "Data Spacialization", "Data Sources and Definitions"])

with tab1:
    st.subheader('Explore the  data correlations between countries indicators', divider='red')
    col1, col2 = st.columns([0.25, 0.7], vertical_alignment='center')
    with col1:        
        indicator_x = st.selectbox("PLease, select the indicator ('X' axis )", indicator_names, index=1)
        indicator_y = st.selectbox("PLease, select the indicator ('Y' axis )", indicator_names, index=20)
        year = 'Mean'    
        st.caption('Observations:')
        st.caption('1-The data displayed is the simple arithmetic mean between the years of 2019-2023')        
        st.caption('2-Hover for detailed information')
        #year = st.select_slider("Please, select the year", options=["2019","2020", "2021", "2022", "2023", "Mean"], value=("Mean"),)    
    with col2:
        fig = px.scatter(indicators,x=f"{indicator_x}_{year}", y=f"{indicator_y}_{year}",hover_name="country.value")
        st.plotly_chart(fig)


with tab2:    
    col1, col2 = st.columns([0.25, 0.75],vertical_alignment='center')
    with col1:
        indicator_tab2 = st.selectbox("PLease, select the indicator to map", indicator_names, key=3 )
        year_tab2 = st.select_slider("Please, select the year", options=["2019","2020", "2021", "2022", "2023", "Mean"], value=("Mean"))
        st.caption('Observations:')
        st.caption('1-when used, Mean encompass the years 2019-2023')        
        st.caption('2-Hover for detailed information')
    
    
    with col2:
        st.subheader(f'{indicator_tab2}-{year_tab2}', divider='red')
        try:
            fig2 = px.choropleth(indicators, geojson=mapa, locations='countryiso3code', color=f'{indicator_tab2}_{year_tab2}',
            color_continuous_scale='plasma', featureidkey='properties.iso_a3', labels={f'{indicator_tab2}_{year_tab2}':'Values'},
            fitbounds='geojson',hover_name="country.value")        
            fig2.update_layout(height=600)    
            st.plotly_chart(fig2,use_container_width=True,height=600)
        except: 
            st.subheader('Not enough data for selected year/indicator. Pleas select another')
         

with tab3:
    st.subheader('Data Sources, observations, definitions', divider='red')
    st.caption('Most of the data employed in this dashboard was downloaded from the World Bank site (https://data.worldbank.org/). The data was treated and transformations like mean were applied. The table below presents the sources and defintions of the indicators.')
    st.caption('Dashboard developed for educational purposes as curricular project for undergraduate degree in Data Science in "Ampli", Brazil.')


    st.html('\n')    
    st.table(data=metadata_indicators)   
    