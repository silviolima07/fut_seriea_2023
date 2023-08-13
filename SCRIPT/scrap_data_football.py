# -*- coding: utf-8 -*-
"""scrap_data_football.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16uIF-PNDlEzFi3EUFSxgwcWpH-Vbo578
"""

# Importando as bibliotecas necessarias
import pandas as pd

import requests
from bs4 import BeautifulSoup

from random import randint
from time import sleep

def get_version():
    """
    Funcao get_version retorna a data de criacao do arquivo csv.
    Return: data
    """
    URL = "https://www.football-data.co.uk/brazil.php"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all("i")
    for link in links:
        #print(link, "-",link.text)
        version_data = str(link).replace('<i>Last updated:','').replace('</i>', '').strip()
    print('Última atualização:',version_data)
    return

def get_data():
    """
    Funcao get_data traz o dataset csv.
    Return: csv
    """
    URL = "https://www.football-data.co.uk/brazil.php"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    # Extrair a linha que tem a string CSV, exatamente onde tem a url para baixar o arquivo csv.
    links = soup.find_all("a")
    for link in links:
        if link.text == 'CSV':
            #print(link, "-",link.text)
            link_csv = str(link).replace('<a href="','').replace('">CSV</a>', '')
    #print(link_csv)

    url = 'https://www.football-data.co.uk/'

    url_csv = url+link_csv

    df = pd.read_csv(url_csv)
    return df

def get_gols(time, df):
    """
      Funcao get_gols o total de gols que um time fez ou levou.
      input: time (string), df (dataframe)
      return: int
    """
    gols_marcados = 0
    gols_levados = 0
    #print("\nSeason:", season)
    for index, row in df.iterrows():
        if row['Home'] == time:
            gols_marcados    = int(gols_marcados + row['HG'])
            gols_levados = int(gols_levados + row['AG'])
        elif row['Away'] == time:
            gols_marcados    = int(gols_marcados + row['AG'])
            gols_levados = int(gols_levados + row['HG'])
    #print(time.upper())
    print("\tTotal gols marcados:",int(gols_marcados))
    print("\tTotal gols levados:",int(gols_levados))
    return (gols_marcados, gols_levados)

def get_resultados(time, df):
    """
      Funcao get_resultados retorna o total de vitorias, derrotas e empates de um time.
      Traz também os times que ele enfrentou e a pontuação no momento.
      Input: time (string), df (dataframe)
      Return: int e string
    """
    jogo = 1
    vitorias = 0
    lista_v = []
    empates = 0
    lista_e = []
    derrotas = 0
    lista_d = []
    lista_placar_v = []
    lista_placar_d = []
    lista_placar_e = []
    for index, row in df.iterrows():
        #print("\n\nAno:", row['Season'])
        # VITORIAS
        if row['Home'] == time and row['HG'] > row['AG']:
            # Jogo em casa
            vitorias    = int(vitorias + 1)
            placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
            #print("\n",row['Season'],"- VITORIA em CASA -->", placar)
            lista_placar_v.append(placar) # Placar da vitoria em  casa
            lista_v.append(row['Away']) # Time visitante que perdeu
        elif row['Away'] == time and row['AG'] > row['HG']:
            # Jogo visitante
            vitorias    = int(vitorias + 1)
            lista_v.append(row['Home']) # Time da casa que perdeu
            placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
            #print("\n",row['Season'],"- VITORIA FORA de CASA -->", placar)
            lista_placar_v.append(placar) # Placar da vitoria como visitane

        # DERROTAS
        elif row['Home'] == time and row['HG'] < row['AG']:
            # Jogo em casa
            derrotas     = int(derrotas + 1)
            lista_d.append(row['Away'])
            placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
            #print("\n",row['Season'],"- DERROTA em CASA -->", placar)
            lista_placar_d.append(placar) # Placar da derrota em casa
        elif row['Away'] == time and row['AG'] < row['HG']:
            # Jogo como visitante
            derrotas     = int(derrotas + 1)
            lista_d.append(row['Home'])# Time da casa que ganhou
            placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
            #print("\n",row['Season'],"- DERROTA FORA de  CASA -->", placar)
            lista_placar_d.append(placar)

        # EMPATES
        elif row['Home'] == time and row['HG'] == row['AG'] and row['Res'] == 'D':
            # Jogo em casa
            empates = int(empates +1)
            lista_e.append(row['Away']) # Time visitante com quem empatou
            placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
            #print("\n",row['Season'],"- EMPATE em CASA -->", placar)
            lista_placar_e.append(placar) # Placar do empate em casa

        elif row['Away'] == time and row['HG'] == row['AG'] and row['Res'] == 'D':
            # Jogo como visitante
            empates = int(empates +1)
            lista_e.append(row['Home']) # Time da casa com quem empatou
            placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
            #print("\n",row['Season'],"- EMPATE FORA de CASA -->", placar)
            lista_placar_e.append(placar)

        jogo = jogo +1


    pontos = vitorias*3 + empates
    #print(time.upper())
    #print("\tTotal vitorias",int(vitorias))
    lista_v = str(lista_v).replace("'",'').replace('[','').replace(']','')
    #print("\tVitoria contra:", lista_v)

    #print("\tTotal derrotas:",derrotas)
    lista_d = str(lista_d).replace("'",'').replace('[','').replace(']','')
    #print("\tDerrota para:",lista_d)

    #print("\tTotal empates:",empates)
    lista_e = str(lista_e).replace("'",'').replace('[','').replace(']','')
    #print("\tEmpate com:",lista_e)
    #placar = row['Home']+'-'+str(row['HG'])+'X'+str(row['AG'])+'-'+(row['Away'])
    #lista_placar_e.append(placar)

    #print("\tPontos:", pontos)
    return (vitorias, derrotas, empates, pontos, lista_v, lista_d, lista_e, lista_placar_v, lista_placar_d, lista_placar_e)

df = get_data()

df.fillna(0, inplace=True)

df['HG'] = df.HG.astype('int')
df['AG'] = df.AG.astype('int')

lista_gols_marcados = []
lista_gols_levados = []
int_vitorias = []
int_derrotas = []
int_empates = []
int_pontos = []
l_vitorias = []
l_derrotas = []
l_empates = []
l_seasons = []
l_times = []
l_placar_v = []
l_placar_d = []
l_placar_e = []

# Lista com os anos dos dados na base
seasons = list(df['Season'])
seasons = list(set(seasons))
#seasons = [2023]
for season in seasons:
    sleep(randint(1,3))

    print("\n\nSeason:", season)
    temp_df = df.loc[df.Season == season]
    times = list(temp_df['Home'])
    times = list(set(times))
    #times = ['Santos'] # Para testar com apenas um time
    n=1

    for time in times:

        print('\n',n,'-',time)
        n = n+1
        l_seasons.append(season)
        l_times.append(time)
        marcados, levados = get_gols(time, temp_df)
        lista_gols_marcados.append(marcados)
        lista_gols_levados.append(levados)

        vitorias, derrotas, empates, pontos, lista_v, lista_d, lista_e, lista_placar_v, lista_placar_d, lista_placar_e = get_resultados(time, temp_df)
        int_vitorias.append(vitorias)
        int_derrotas.append(derrotas)
        int_empates.append(empates)
        int_pontos.append(pontos)
        #l_vitorias.append([lista_v])
        l_vitorias = lista_v
        l_derrotas.append([lista_d])
        l_empates.append([lista_e])
        l_placar_v.append(lista_placar_v)
        l_placar_d.append(lista_placar_d)
        l_placar_e.append(lista_placar_e)

data = {'season':l_seasons,
        'times': l_times,
        'pontos':int_pontos,
        'gols_marcados':lista_gols_marcados,
        'gols_levados':lista_gols_levados,
        'vitorias': int_vitorias,
        'derrotas':int_derrotas,
        'empates':int_empates,
        'time_ganhou': l_vitorias,
        'time_derrota': l_derrotas,
        'time_empate': l_empates ,
        'placar_vitoria': l_placar_v,
        'placar_derrota': l_placar_d,
        'placar_empate': l_placar_e}

df_br = pd.DataFrame(data)

df_br.sort_values(by='pontos', ascending=False)

# df_br.time_ganhou
# lista = []

# for i in df_br.time_ganhou:
#   for x in i:
#     print(x)
#     lista.append(x)

# print(lista)

df_br.to_csv("../CSV/dados_2012_2023.csv")





