import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import time

sns.set()  

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    st.pyplot(fig=plt)
    return None

st.set_page_config(
    page_title='SINASC Rondônia',
    layout='centered'
)
# st.write('# Análise SINASC de Rondônia')
st.badge('Análise SINASC de Rondônia', icon=':material/check:', color='green')

sinasc = pd.read_csv('./input/SINASC_RO_2019.csv')

sinasc.DTNASC = pd.to_datetime(sinasc.DTNASC)

min_data = sinasc.DTNASC.min()
max_data = sinasc.DTNASC.max()

# st.write(min_data)
# st.write(max_data)


datas = pd.DataFrame(sinasc.DTNASC.unique(), columns=['DTNASC'])
datas.sort_values(by='DTNASC', inplace=True, ignore_index=True)

data_inicial = st.sidebar.date_input('Data inicial', value=min_data, min_value=min_data, max_value=max_data)
data_final = st.sidebar.date_input('Data final', value=max_data, min_value=min_data, max_value=max_data)

st.sidebar.write('Data Inicial = ', data_inicial)
st.sidebar.write('Data Final = ', data_final)

sinasc_df = sinasc[(sinasc['DTNASC'] <= pd.to_datetime(data_final)) & (sinasc['DTNASC'] >= pd.to_datetime(data_inicial))]

if st.sidebar.checkbox('média idade mãe por data'):
    plota_pivot_table(sinasc_df, 'IDADEMAE', 'DTNASC', 'mean', 'média idade mãe por data', 'data nascimento')
if st.sidebar.checkbox('média idade mãe por sexo'):
    (plota_pivot_table(sinasc_df, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae','data de nascimento','unstack'))
if st.sidebar.checkbox('média peso bebe'):
    (plota_pivot_table(sinasc_df, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe','data de nascimento','unstack'))
if st.sidebar.checkbox('PESO mediano'):
    (plota_pivot_table(sinasc_df, 'PESO', 'ESCMAE', 'median', 'PESO mediano','escolaridade mae','sort'))
if st.sidebar.checkbox('apgar1 médio'):
    (plota_pivot_table(sinasc_df, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio','gestacao','sort'))

_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""
col1, col2, col3 = st.columns(3)



def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)


c = st.container(width=450, height=100)


if col1.button("Texto em cascata"):
    c.write_stream(stream_data)

col2.link_button('Link Google', 'https://google.com')

col3.link_button('Link YouTube', 'https://youtube.com')

col1.write(sinasc_df['DTNASC'])
col2.write(sinasc_df['IDADEMAE'])
col3.write(sinasc_df['APGAR1'])


st.code('print("Olá, mundo!")')


slider = st.slider(
    label='Escolha um valor', min_value=1,
    max_value=100, value=50, key='my_slider')