import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_pandas_profiling import st_profile_report

import pandas as pd
from pandas_profiling import ProfileReport

import numpy as np

import matplotlib
matplotlib.use('agg')
from tkinter import *
from mttkinter import *

import seaborn as sns

from matplotlib import pyplot
import matplotlib.pyplot as plt

from sklearn import metrics

from sklearn import datasets
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

from scipy.stats import ks_2samp
import statsmodels.formula.api as smf
import statsmodels.api as sm

from datetime import datetime

import plotly.figure_factory as ff

from PIL import Image
from io import BytesIO

st.set_page_config(page_title='Projeto 2 - Cientista de Dados EBAC', page_icon='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQlWkTPwbN4sIWlFBLTlDUnHXFNHRGqslRP6cTgzcOUdfFWxY_kS2rok5rUwCRbe3Hg-0&usqp=CAU', layout="wide", initial_sidebar_state="auto", menu_items=None)

with st.sidebar:
    
    image = Image.open('Por-Que-e-Como-Data-Science-e-Mais-do-Que-Apenas-Machine-Learning.jpg')
    st.sidebar.image(image)
    st.markdown("---")
    st.title('Projeto 2 - Cientista de Dados - EBAC')
    st.subheader('Aluno: Matheus Feldberg')
    st.markdown('[LinkedIn](https://www.linkedin.com/in/matheus-feldberg-521a93259)')
    st.markdown('[GitHub](https://github.com/math-feldberg/Mod16Ex01)')
    st.markdown("---")
         
    renda = pd.read_csv('./previsao_de_renda.csv')
    renda.drop(['Unnamed: 0', 'id_cliente'], axis=1)
    renda['posse_de_veiculo'] = renda['posse_de_veiculo'].map({True: 1,False: 0})
    renda['posse_de_imovel'] = renda['posse_de_imovel'].map({True: 1,False: 0})
    renda['data_ref'] = pd.to_datetime(renda['data_ref'])
    renda['data_ref'] = renda['data_ref'].dt.strftime('%m-%Y')   
    renda.dropna(inplace=True) 
        
    @st.cache_data

    def convert_df(renda):
                                    # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return renda.to_csv().encode('utf-8') 
    
    csv = convert_df(renda)

    st.download_button(
                                label="???? Download do Dataframe em CSV",
                                data=csv,
                                file_name='dataframe.csv',
                                mime='text/csv')
                                    
    @st.cache_data

    def to_excel(renda):
                                output = BytesIO()
                                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                                renda.to_excel(writer, index=False, sheet_name='Sheet1')
                                writer.save()
                                processed_data = output.getvalue()
                                return processed_data

    renda_xlsx = to_excel(renda)
                                
    st.download_button(
                                label='???? Download do Dataframe em EXCEL',
                                data=renda_xlsx,
                                file_name= 'dataframe.xlsx')   
        
   

with st.sidebar:
    
    selected = option_menu(
                        menu_title = 'Sum??rio',
                        options =  ['1. Etapa 1 CRISP - DM: Entendimento do neg??cio',
                        '2. Etapa 2 Crisp-DM: Entendimento dos dados',
                        '3. Etapa 3 Crisp-DM: Prepara????o dos dados',
                        '4. Etapa 4 Crisp-DM: Modelagem',
                        '5. Etapa 5 Crisp-DM: Avalia????o dos resultados',
                        '6. Etapa 6 Crisp-DM: Implanta????o'],
                        default_index=0)
    
if selected == '1. Etapa 1 CRISP - DM: Entendimento do neg??cio':
        
    st.subheader('Etapa 1 CRISP - DM: Entendimento do neg??cio')
                
    st.markdown('''Como primeira etapa do CRISP-DM, vamos entender do que se trata o neg??cio, e quais os objetivos. 
Essa ?? uma base de proponentes de cart??o de cr??dito, nosso objetivo ?? construir um modelo preditivo para 
90 em um horizonte de 12 meses) atrav??s de vari??veis que podem ser observadas na data da avalia????o do cr??dito 
(tipicamente quando o cliente solicita o cart??o).
                            
Atividades do CRISP-DM:

- Objetivos do neg??cio:
Note que o objetivo aqui ?? que o modelo sirva o mutu??rio (o cliente) para que avalie suas pr??prias decis??es, 
e n??o a institui????o de cr??dito.
- Objetivos da modelagem:
O objetivo est?? bem definido: desenvolver o melhor modelo preditivo de modo a auxiliar o mutu??rio a tomar suas 
pr??prias decis??es referentes a cr??dito.

Nessa etapa tamb??m se avalia a situa????o da empresa/segmento/assunto de modo a se entender o tamanho do p??blico, 
relev??ncia, problemas presentes e todos os detalhes do processo gerador do fen??meno em quest??o, e portanto dos dados.
Tamb??m ?? nessa etapa que se constr??i um planejamento do projeto.''')
                        
elif selected == '2. Etapa 2 Crisp-DM: Entendimento dos dados':
    
    st.header('Etapa 2 Crisp-DM: Entendimento dos dados')

    st.markdown('A segunda etapa ?? o entendimento dos dados. Foram fornecidas 13 vari??veis mais a vari??vel resposta (em negrito na tabela). O significado de cada uma dessas vari??veis se encontra na tabela.')
    st.subheader('Dicion??rio de dados')
    st.markdown('''Os dados est??o dispostos em uma tabela com uma linha para cada cliente, e uma coluna para cada vari??vel armazenando as caracter??sticas desses clientes. Colocamos uma c??pia o dicion??rio de dados (explica????o dessas vari??veis) abaixo neste notebook:


| Vari??vel                | Descri????o                                           | Tipo         |
| ----------------------- |:---------------------------------------------------:| ------------:|
| data_ref                |  Data de refer??ncia                                 | data         |
| id_cliente              |  Identifica????o do cliente                           | inteiro      |
| sexo                    |  M = 'Masculino'; F = 'Feminino'                    | M/F          |
| posse_de_veiculo        |  True = 'possui'; False = 'n??o possui'              | True/False   |
| posse_de_imovel         |  True = 'possui'; False = 'n??o possui'              | True/False   |
| qtd_filhos              |  Quantidade de filhos                               | inteiro      |
| tipo_renda              |  Tipo de renda (ex: assaliariado, aut??nomo etc)     | texto        |
| educacao                |  N??vel de educa????o (ex: secund??rio, superior etc)   | texto        |
| estado_civil            |  Estado civil (ex: solteiro, casado etc)            | texto        |
| tipo_residencia         |  Tipo de resid??ncia (ex: casa/apto, com os pais etc)| texto        |
| idade                   |  Idade em anos                                      | inteiro      |
| tempo_emprego           |  Tempo de emprego em anos                           | inteiro      |
| qt_pessoas_residencia   |  Quantidade de pessoas na resid??ncia                | inteiro      |
| **renda**               |  Renda do cliente em Reais                          | inteiro      |''')

    st.subheader('Carregando os pacotes')   

    st.markdown('?? considerada uma boa pr??tica carregar os pacotes que ser??o utilizados como a primeira coisa do programa.')

    st.markdown('Usaremos o seguinte c??digo:')
                                            
    code = '''import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_pandas_profiling import st_profile_report

import pandas as pd
from pandas_profiling import ProfileReport

import numpy as np

import matplotlib
matplotlib.use('agg')
from tkinter import *
from mttkinter import *

import seaborn as sns

from matplotlib import pyplot
import matplotlib.pyplot as plt

from sklearn import metrics

from sklearn import datasets
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

from scipy.stats import ks_2samp
import statsmodels.formula.api as smf
import statsmodels.api as sm

from datetime import datetime

import plotly.figure_factory as ff

from PIL import Image
from io import BytesIO'''

    st.code(code, language='python')

    st.subheader('Carregando os dados') 
    st.markdown('O comando pd.read_csv ?? um comando da biblioteca pandas (pd.) e carrega os dados do arquivo csv indicado para um objeto *dataframe* do pandas.')

    renda = pd.read_csv('./previsao_de_renda.csv')
    renda.head(1)

    st.dataframe(renda)

    st.markdown('Ao lado voc?? pode baixar o dataframe em formato CSV e EXCEL.')
                            
    st.subheader('Entendimento dos dados - Univariada')
    st.markdown('Nesta etapa tipicamente avaliamos a distribui????o de todas as vari??veis.')

    st.markdown('Vamos utilziar Pandas Profiling para explora????o dos dados e para garantir a qualidade dos dados.')
    
    from streamlit_pandas_profiling import st_profile_report
      
    prof = renda.profile_report()
    st_profile_report(prof)
                                     
    st.download_button(
               label='???? Download do ProfileReport', 
               data=prof.to_html(), 
               file_name='analise_renda.html')
    st.markdown("---")
           
    st.markdown('Distribui????o das vari??veis qualitativas no tempo (sexo, posse_de_veiculo, posse_de_imovel, tipo_renda, educacao, estado_civil e tipo_residencial):')
    
    renda.drop(['Unnamed: 0', 'id_cliente'], axis=1)
    renda['posse_de_veiculo'] = renda['posse_de_veiculo'].map({True: 1,False: 0})
    renda['posse_de_imovel'] = renda['posse_de_imovel'].map({True: 1,False: 0})
    renda['data_ref'] = pd.to_datetime(renda['data_ref'])
    renda['data_ref'] = renda['data_ref'].dt.strftime('%m-%Y')
    renda.head()

    st.set_option('deprecation.showPyplotGlobalUse', False)
    sns.countplot(x= renda['data_ref'],  hue = renda['sexo'], data=renda)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
    plt.xticks(rotation=45);
    st.pyplot()

    sns.countplot(x= renda['data_ref'],  hue = renda['posse_de_veiculo'], data=renda)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xticks(rotation=45);
    st.pyplot()

    sns.countplot(x= renda['data_ref'],  hue = renda['posse_de_imovel'], data=renda)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xticks(rotation=45);
    st.pyplot()
                                            
    sns.countplot(x= renda['data_ref'],  hue = renda['tipo_renda'], data=renda)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xticks( rotation=45);
    st.pyplot()

    sns.countplot(x= renda['data_ref'],  hue = renda['educacao'], data=renda)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xticks(rotation=45);
    st.pyplot()
                                            
    sns.countplot(x= renda['data_ref'],  hue = renda['estado_civil'], data=renda)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xticks(rotation=45);
    st.pyplot()

    sns.countplot(x= renda['data_ref'],  hue = renda['tipo_residencia'], data=renda)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xticks(rotation=45);
    st.pyplot()
                                                    
    st.header('Entendimento dos dados - Bivariadas')

    st.markdown('Entender a rela????o da renda representada pela vari??vel resposta (```renda```) e as demais vari??veis explicativas (demais). Para isto, vamos avaliar a capacidade econ??mica para diferentes grupos definidos pelas vari??veis explicativas para obter um modelo preditor de renda.')

    st.markdown('Plotando uma matriz de corre????o:')
    st.dataframe(renda)
    data_corr = renda.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(data_corr, annot=True, fmt='.1g', vmin=-1, vmax=1, cmap='mako', center=0)
    plt.xticks(rotation = 40)
    st.pyplot()   

elif selected == '3. Etapa 3 Crisp-DM: Prepara????o dos dados':
                            
    st.header('Etapa 3 Crisp-DM: Prepara????o dos dados')

    st.subheader('Nessa etapa realizamos tipicamente as seguintes opera????es com os dados:')

    st.markdown(''' - **sele????o**: J?? temos os dados selecionados adequadamente?
    - **limpeza**: Precisaremos identificar e tratar dados faltantes
    - **constru????o**: constru????o de novas vari??veis
    - **integra????o**: Temos apenas uma fonte de dados, n??o ?? necess??rio integra????o
    - **formata????o**: Os dados j?? se encontram em formatos ??teis?
                                    ''')

    st.markdown('''Em primeirio lugar, vamos realizar a sele????o e limpeza dos dados:
    - a vari??vel 'Unnamed: 0' apresenta valores ??nicos, logo, ?? irrelevante para o projeto.
    - a vari??vel 'id_cliente' tamb??m n??o tem valor para a an??lise pretendida porque n??o interfere em nenhuma outra vari??vel.
    - a vari??vel 'tempo_emprego' tem 17.2% de valores missing.
    - a avari??vel 'data_ref' ser?? adequada para m??s e ano.''')

    st.markdown('As colunas Unnamed: 0 e id_cliente foram exclu??das no in??cio quando plotamos os gr??ficos de distribui????o das vari??veis qualitativas pelo tempo.')

    st.markdown('Identificando e tratando os dados missing:')
    
    renda = pd.read_csv('./previsao_de_renda.csv')
    renda.head(1)

    renda.drop(['Unnamed: 0', 'id_cliente'], axis=1)
    renda['posse_de_veiculo'] = renda['posse_de_veiculo'].map({True: 1,False: 0})
    renda['posse_de_imovel'] = renda['posse_de_imovel'].map({True: 1,False: 0})
    renda['data_ref'] = pd.to_datetime(renda['data_ref'])
    renda['data_ref'] = renda['data_ref'].dt.strftime('%m-%Y')
    renda.head()
        
    st.dataframe(renda.isna().sum())

    renda.dropna(inplace=True)
    renda.isna().sum()
    st.markdown('A coluna data_ref tamb??m foi corrigida no in??ico para exibir apenas m??s/ano::')
    st.dataframe(renda)
                        
elif selected == '4. Etapa 4 Crisp-DM: Modelagem':
                        
                st.header('Etapa 4 Crisp-DM: Modelagem')

                st.markdown('''Nessa etapa que realizaremos a constru????o do modelo. Os passos t??picos s??o:
                                - Selecionar a t??cnica de modelagem
                                - Desenho do teste
                                - Avalia????o do modelo''')
                
                renda = pd.read_csv('./previsao_de_renda.csv')
                renda.head(1)

                renda.drop(['Unnamed: 0', 'id_cliente'], axis=1)
                renda['posse_de_veiculo'] = renda['posse_de_veiculo'].map({True: 1,False: 0})
                renda['posse_de_imovel'] = renda['posse_de_imovel'].map({True: 1,False: 0})
                renda['data_ref'] = pd.to_datetime(renda['data_ref'])
                renda['data_ref'] = renda['data_ref'].dt.strftime('%m-%Y')
                renda.head()
        
                renda.dropna(inplace=True)
                X = pd.get_dummies(renda.drop(['Unnamed: 0', 'id_cliente', 'data_ref'], axis=1))
                y = renda['renda']

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state = 100)
                print(X_train.shape)
                print(X_test.shape)
                print(y_train.shape)
                print(y_test.shape)

                regr_1 = DecisionTreeRegressor(max_depth=4)
                regr_2 = DecisionTreeRegressor(max_depth=3)
                regr_3 = DecisionTreeRegressor(max_depth=2)

                regr_1.fit(X_train, y_train)
                regr_2.fit(X_train, y_train)
                regr_3.fit(X_train, y_train)

                plt.rc('figure', figsize=(40, 10))
                tp = tree.plot_tree(regr_1, 
                feature_names=X.columns,  
                filled=True)
                st.pyplot()
                plt.rc('figure', figsize=(10, 5))
                tp = tree.plot_tree(regr_2, 
                feature_names=X.columns,  
                filled=True) 
                st.pyplot()
                plt.rc('figure', figsize=(10, 5))
                tp = tree.plot_tree(regr_3, 
                feature_names=X.columns,  
                filled=True) 
                st.pyplot()
                mse1 = regr_1.score(X_train, y_train)
                mse2 = regr_2.score(X_train, y_train)
                mse2 = regr_3.score(X_train, y_train)


                template = "O MSE da ??rvore de treino com profundidade={0} ??: {1:.2f}"

                st.write(template.format(regr_1.get_depth(),mse1).replace(".",","))
                st.write(template.format(regr_2.get_depth(),mse2).replace(".",","))
                st.write(template.format(regr_3.get_depth(),mse2).replace(".",","))

elif selected == '5. Etapa 5 Crisp-DM: Avalia????o dos resultados':

    st.header('Etapa 5 Crisp-DM: Avalia????o dos resultados')

    st.markdown('O modelo de ??rvore de regress??o com profundidade 4 apresentou um MSE de 0.99 tanto para os dados de treino quanto para os dados de teste e, portanto, ?? o melhor para previs??o dos dados de renda.')
                
    renda = pd.read_csv('./previsao_de_renda.csv')
    renda.head(1)

    renda.drop(['Unnamed: 0', 'id_cliente'], axis=1)
    renda['posse_de_veiculo'] = renda['posse_de_veiculo'].map({True: 1,False: 0})
    renda['posse_de_imovel'] = renda['posse_de_imovel'].map({True: 1,False: 0})
    renda['data_ref'] = pd.to_datetime(renda['data_ref'])
    renda['data_ref'] = renda['data_ref'].dt.strftime('%m-%Y')
    renda.head()
            
    renda.dropna(inplace=True)
    X = pd.get_dummies(renda.drop(['Unnamed: 0', 'id_cliente', 'data_ref'], axis=1))
    y = renda['renda']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3, random_state = 100)                           
                
    regr_1 = DecisionTreeRegressor(max_depth=4)
    regr_2 = DecisionTreeRegressor(max_depth=3)
    regr_3 = DecisionTreeRegressor(max_depth=2)

    regr_1.fit(X_test, y_test)
    regr_2.fit(X_test, y_test)
    regr_3.fit(X_test, y_test)

    plt.rc('figure', figsize=(40, 10))
    tp = tree.plot_tree(regr_1, 
    feature_names=X.columns,  
    filled=True)
    st.pyplot()

    plt.rc('figure', figsize=(10, 5))
    tp = tree.plot_tree(regr_3, 
    feature_names=X.columns,  
    filled=True) 
    st.pyplot()

    plt.rc('figure', figsize=(10, 5))
    tp = tree.plot_tree(regr_3, 
    feature_names=X.columns,  
    filled=True) 
    st.pyplot()

    mse1 = regr_1.score(X_test, y_test)
    mse2 = regr_2.score(X_test, y_test)
    mse2 = regr_3.score(X_test, y_test)
    
    template = "O MSE da ??rvore de teste com profundidade={0} ??: {1:.2f}"

    st.write(template.format(regr_1.get_depth(),mse1).replace(".",","))
    st.write(template.format(regr_2.get_depth(),mse2).replace(".",","))
    st.write(template.format(regr_3.get_depth(),mse2).replace(".",","))
                    
elif selected == '6. Etapa 6 Crisp-DM: Implanta????o':
                        
    st.header('Etapa 6 Crisp-DM: Implanta????o')

    st.markdown('Nessa etapa colocamos em uso o modelo desenvolvido, normalmente implementando o modelo desenvolvido em um motor que toma as decis??es com algum n??vel de automa????o.')
