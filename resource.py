import pandas as pd
import streamlit as st

@st.cache(allow_output_mutation=True)
def read_resources():
    print('Loading data...')
    state = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv')
    death = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_state.csv')
    hospital = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/hospital.csv')
    icu = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/icu.csv')
    clusters = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/clusters.csv')

    clusters.state = clusters.state.str.replace('WP Kuala Lumpur', 'W.P. Kuala Lumpur').str.replace('WP Putrajaya', 'W.P. Putrajaya').str.replace('WP Labuan', 'W.P. Labuan')

    return state, death, hospital, icu, clusters

state, death, hospital, icu, clusters = read_resources()

state_t = state.groupby('date')['cases_new'].apply(lambda state: state.reset_index(drop=True)).unstack()
state_t.columns = state['state'].unique()
state_t['Total'] = state_t.sum(axis=1)
state_t['Date'] = state_t.index

death_t = death.groupby('date')['deaths_new'].apply(lambda death: death.reset_index(drop=True)).unstack()
death_t.columns = death['state'].unique()
death_t['Total'] = death_t.sum(axis=1)
death_t['Date'] = death_t.index