import streamlit as st
import plotly.express as px
import pandas as pd

from resource import state_t, death_t, hospital, icu, clusters
from utils import generate_line_chart, generate_medical_chart

single_state_list = state_t.loc[:, ~state_t.columns.isin(['Total', 'Date'])].columns.values.tolist()

st.title('Malaysia Covid Data with Streamlit')

st.title('Summary')

latest_date = state_t['Date'][-1]

## Summary
st.text(f'Showing data on: {latest_date}')

death_s = pd.DataFrame(death_t[death_t['Date'] == latest_date].T).reset_index()
death_s.columns = ['State', 'Deaths']
cluster_s = clusters[clusters.status == 'active']['state'].value_counts().reset_index()
cluster_s.columns = ['State', 'Active Clusters']
summary = pd.DataFrame(state_t.loc[:, ~state_t.columns.isin(['Date', 'Total'])].reset_index(drop=True).tail(1).T).reset_index()
summary.columns = ['State', 'Cases']

summarized_dataframe = summary.merge(death_s, how='left', on='State').reset_index(drop=True).set_index('State') # merge 1: death
summarized_dataframe = summarized_dataframe.merge(cluster_s, how='left', on='State').set_index('State') # merge 2: clusters
summarized_dataframe['Active Clusters'] = summarized_dataframe['Active Clusters'].fillna(0).astype(int) # change cluster data type float -> int
summarized_dataframe = summarized_dataframe.append(summarized_dataframe.sum().rename('Total'))

st.dataframe(summarized_dataframe)
st.text('Active Cluster count does not include clusters which involve multiple regions simultaneously')

## Cases and Deaths
container = st.sidebar.container()
all = st.sidebar.checkbox("Select All")
 
if all:
    selected_options = container.multiselect("Cases and Deaths",
         single_state_list, single_state_list)
else:
    selected_options =  container.multiselect("Cases and Deaths",
        single_state_list)

st.title('Cases')
if selected_options:
    
    fig = generate_line_chart(state_t, selected_options)
    st.plotly_chart(fig)
else:

    st.text('<--- Pick a State')

st.title('Deaths')
if selected_options:
    
    fig = generate_line_chart(death_t, selected_options)
    st.plotly_chart(fig)
else:

    st.text('<--- Pick a State')


## Medical
st.title('Medical')
selected_radio = st.sidebar.selectbox('Medical and Clusters (Single State):', single_state_list)
st.markdown(f'You have chosen **{selected_radio}**.')
if selected_radio:
    hospital_one = hospital[hospital.state == selected_radio]
    hospital_cols = hospital.loc[:, ~hospital.columns.isin(['date', 'state'])].columns.tolist()

    fig = generate_medical_chart(hospital_one, hospital_cols)    
    st.plotly_chart(fig)

    icu_one = icu[icu.state == selected_radio]
    icu_cols = icu.loc[:, ~icu.columns.isin(['date', 'state'])].columns.tolist()

    fig = generate_medical_chart(icu_one, icu_cols)    
    st.plotly_chart(fig)


## CLusters
st.title('Clusters')
if selected_radio:
    
    cluster_one = clusters[(clusters.status == 'active') & (clusters.state.str.contains(selected_radio))]
    cluster_category = cluster_one.category.value_counts().reset_index().set_index('index')

    if len(cluster_one) > 0:
        st.text('Currently Active')
        st.dataframe(cluster_one)
        st.dataframe(cluster_category)
    else:
        st.text('No Data')

    cluster_one = clusters[(clusters.status == 'ended') & (clusters.state.str.contains(selected_radio))]
    cluster_category = cluster_one.category.value_counts().reset_index().set_index('index')

    if len(cluster_one) > 0:
        st.text('Historical')
        st.dataframe(cluster_one)
        st.dataframe(cluster_category)
    else:
        st.text('No Data')


st.text('Data Source: https://github.com/MoH-Malaysia/covid19-public')