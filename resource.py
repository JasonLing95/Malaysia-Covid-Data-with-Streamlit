import pandas as pd
import streamlit as st

@st.cache(allow_output_mutation=True)
def read_resources():
    print('Loading data...')

    # static population data
    population = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/static/population.csv')

    # malaysia data import
    malaysia_cases = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_malaysia.csv')
    malaysia_death = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_malaysia.csv')
    malaysia_vaccine_reg = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/registration/vaxreg_malaysia.csv')
    malaysia_vaccine = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_malaysia.csv')

    # state level import
    state = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/cases_state.csv')
    death = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/deaths_state.csv')
    state_reg = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/registration/vaxreg_state.csv')
    state_vaccine = pd.read_csv('https://raw.githubusercontent.com/CITF-Malaysia/citf-public/main/vaccination/vax_state.csv')

    # medical data import
    hospital = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/hospital.csv')
    icu = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/icu.csv')
    
    # clusters data import
    clusters = pd.read_csv('https://raw.githubusercontent.com/MoH-Malaysia/covid19-public/main/epidemic/clusters.csv')

    clusters.state = clusters.state.str.replace('WP Kuala Lumpur', 'W.P. Kuala Lumpur').str.replace('WP Putrajaya', 'W.P. Putrajaya').str.replace('WP Labuan', 'W.P. Labuan')
    malaysia_cases.rename(columns={'date': 'Date'}, inplace=True)
    malaysia_death.rename(columns={'date': 'Date'}, inplace=True)

    return state, death, hospital, icu, clusters, malaysia_cases, malaysia_death, malaysia_vaccine_reg, malaysia_vaccine, state_reg, population, state_vaccine

state, death, hospital, icu, clusters, malaysia_cases, malaysia_death, malaysia_vaccine_reg, malaysia_vaccine, state_reg, population, state_vaccine = read_resources()

state_t = state.groupby('date')['cases_new'].apply(lambda state: state.reset_index(drop=True)).unstack()
state_t.columns = state['state'].unique()
state_t['Total'] = state_t.sum(axis=1)
state_t['Date'] = state_t.index

single_state_list = state_t.loc[:, ~state_t.columns.isin(['Total', 'Date'])].columns.values.tolist()

death_t = death.groupby('date')['deaths_new'].apply(lambda death: death.reset_index(drop=True)).unstack()
death_t.columns = death['state'].unique()
death_t['Total'] = death_t.sum(axis=1)
death_t['Date'] = death_t.index

reg_t = state_reg.groupby('date')['total'].apply(lambda state_reg: state_reg.reset_index(drop=True)).unstack()
reg_t.columns = state_reg['state'].unique()
reg_t.rename(columns={'date': 'Date'}, inplace=True)
reg_t['Date'] = reg_t.index

for state in single_state_list:
  reg_t[state] = round((reg_t[state] / population[population.state == state]['pop'].values[0]) * 100, 2)

@st.cache()
def change_percentage(state, dose):
  dose = round((dose / population[population.state == state]['pop'].values[0]) * 100, 2)
  return str(dose) + '%'

vaccine_dos = state_vaccine[['state', 'daily_partial', 'daily_full', 'date']].sort_values('date').groupby('state').tail(1)
vaccine_dos['dose1_percent'] =  vaccine_dos.apply(lambda x: change_percentage(x['state'], x['daily_partial']), axis=1)
vaccine_dos['dose2_percent'] =  vaccine_dos.apply(lambda x: change_percentage(x['state'], x['daily_full']), axis=1)
vaccine_data_date = vaccine_dos.date.tail(1).values[0]
vaccination_df = vaccine_dos[['state', 'dose1_percent', 'dose2_percent']].set_index('state').rename(columns={'dose1_percent': 'Dose 1', 'dose2_percent': 'Dose 2'})