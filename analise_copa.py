import pandas as pd
from jupyter_dash import JupyterDash
from dash import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.io as pio
pio.templates.default = "ggplot2"

df_Partidas = pd.read_csv("matches_1930_2022.csv").fillna(0)
matrizPartidas = df_Partidas.values.tolist()

df_Ranking = pd.read_csv("fifa_ranking_2022-10-06.csv")
matrizRanking = df_Ranking.values.tolist()

df_Copas = pd.read_csv("world_cup.csv")
matrizCopas = df_Copas.values.tolist()

#Preparação Gráfico 1
paises=[]
for line in matrizPartidas:
  if line[20] not in paises:
    paises.append(line[20])
def function_estadios(pais):
  estadio=[]
  for line in matrizPartidas:
    if line[20] == (pais):
      if line[13] not in estadio:
        estadio.append(line[13])
  return estadio

#Preparação Gráfico 4
confederacoes=[]
for line in matrizRanking:
  if line[2] not in confederacoes:
    confederacoes.append(line[2])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = JupyterDash(__name__,external_stylesheets=external_stylesheets)

app.layout = html.Div([

#Primeiro Gráfico
    html.H2('Quantidade de espectadores nos estádios em cada partida.', style={'text-align': 'center', 'margin-top':'25px', 'color':'black'}),
    dcc.Dropdown(paises,id='drop_paises', value='Brazil',style={'margin-top': '10px'}),
    dcc.Dropdown(function_estadios('Brazil'),value='Estádio Governador Magalhães Pinto, Belo Horizonte',id='drop_estadios',style={'margin-top': '10px'}),
    html.Div([dcc.Graph(id='graph1', style={'margin-bottom': '50px'})]),

#Segundo Gráfico
    html.H2('Proporção de gols marcados e recebidos de cada seleção.', style={'text-align': 'center', 'margin-top':'5px', 'color':'black'}),
    dcc.Input(id='input_pais', value='Brazil', type='text', style={'margin-bottom':'10px'}),
    html.Div([dcc.Graph(id='graph2')]),

#Terceiro Gráfico
    html.H2('Melhores jogadores em cada edição da Copa do Mundo', style={'text-align': 'center', 'margin-top':'5px', 'color':'black'}),
    dcc.Slider(min=1,max=22,step=1,value=10, id='slider_top_player'),
    html.Div([dcc.Graph(id='graph3',style={'margin-bottom': '50px'})]),

#Quarto Gráfico
    html.H2('Ranking das seleções de cada confederação.', style={'text-align': 'center', 'margin-top':'5px', 'color':'black'}),
    dcc.Dropdown(confederacoes,value='CONMEBOL',id='drop_Conf'),
    html.Div([dcc.Graph(id='graph4')]),


#Quinto Gráfico
    html.H2('Relação de vitórias e empates dos duelos.', style={'text-align': 'center', 'margin-top':'5px', 'color':'black'}),
    dcc.Input(id='input_Pais_A', value='Brazil', type='text'),
    dcc.Input(id='input_Pais_B', value='Argentina', type='text'),
    html.Div([dcc.Graph(id='graph5')])

])
#Callback Primeiro Gráfico:
@app.callback(
    Output(component_id='drop_estadios', component_property='options'),
    Input(component_id='drop_paises', component_property='value')
)
def mudar_Dropdown(pais_drop):
  return function_estadios(pais_drop)

@app.callback(
    Output(component_id='graph1',component_property='figure'),
    Input(component_id='drop_estadios',component_property='value')
)
def grafico1(estadio):
  times=[]
  gente=[]
  turno=[]
  for line in matrizPartidas:
    if line[13] == estadio:
      gente.append(line[12])
      times.append(f'{line[0]} vs {line[1]}')
      turno.append(line[15])
  graph_01=px.line(x=times[::-1], y=gente[::-1], labels=dict(x="Partidas", y="Presença" ))
  graph_01.update_traces(mode="markers+lines", hovertemplate=turno);
  return graph_01

#Callback Segundo Gráfico:
@app.callback(
    Output(component_id='graph2', component_property='figure'),
    Input(component_id='input_pais', component_property='value')
    )
def grafico2(pais_input):
  gols_graf2=[0,0]
  for i in matrizPartidas:
    if i[0]== str(pais_input):
      gols_graf2[0] += (i[2])
      gols_graf2[1] += (i[5])
    elif i[1] == str(pais_input):
      gols_graf2[0] += (i[5])
      gols_graf2[1] += (i[2])
  graph_02=px.pie(values=gols_graf2, names=('Marcados','Recebidos'),color=('Marcados','Recebidos'),
             color_discrete_map={'Marcados':"#03c03c", 'Recebidos':"#f52020"},hole=.2)
  graph_02.update_traces(textposition='inside', textinfo='percent+label',hovertemplate=None,pull=[0.1]);
  graph_02.update_layout(title={'text':f'Seleção escolhida: {pais_input}',
                           'y':0.95,'x':0.45});
  return graph_02

#Callback Terceiro Gráfico:
@app.callback(
    Output(component_id='graph3', component_property='figure'),
    Input(component_id='slider_top_player', component_property='value')
    )
def grafico3(valor_Slider):
  jogadores_gols = []
  for linha in matrizCopas:
    jogador, gol = linha[5].split(" - ")
    jogadores_gols.append([f"{jogador}, {linha[0]}", int(gol)])
  jogadores_gols.sort(key=lambda lista: lista[1])
  jogadores_gols = jogadores_gols[len(jogadores_gols)-(valor_Slider):]
  jogadores = []
  gols = []
  for indice in jogadores_gols:
    jogadores.append(indice[0])
    gols.append(indice[1])
  graph_03 = px.bar(x=gols, y=jogadores, labels=dict(x="Gols", y="Jogadores, ano" ), orientation='h', text=gols,
               color=jogadores, color_discrete_sequence=('#efbbff','#d896ff','#be29ec','#800080','#660066'))
  graph_03.update_traces(textposition='inside',hovertemplate=None);
  graph_03.update_layout(title={'text':f'{valor_Slider} Melhores jogadores.'});
  return graph_03

#Callback Quarto Gráfico
@app.callback(
    Output(component_id='graph4', component_property='figure'),
    Input(component_id='drop_Conf', component_property='value'),

)
def grafico4(confederacao):
  selecoes=[]
  pontos=[]
  for line in matrizRanking:
    if line[2] == confederacao:
      selecoes.append(line[0])
      pontos.append(int(line[5]))
  graph_04=px.bar(x=selecoes,y=pontos, color=selecoes,labels=dict(x="Seleções", y="Pontos" ), color_discrete_sequence=('#23272a','#99aab5'))
  graph_04.update_traces(hovertemplate=None);
  return graph_04

#Callback Quinto Gráfico
@app.callback(
    Output(component_id='graph5', component_property='figure'),
    Input(component_id='input_Pais_A', component_property='value'),
    Input(component_id='input_Pais_B', component_property='value')
)
def grafico5(paisA,paisB):
  listaVDE=[0,0,0]
  for line in matrizPartidas:
    if paisA == line[0] and paisB ==line[1]:
      if line[2] > line[5]:
          listaVDE[0]+=1
      elif line[5] > line[2]:
        listaVDE[1]+=1
      else:
        listaVDE[2]+=1
    elif paisA == line[1] and paisB==line[0]:
      if line[5] > line[2]:
          listaVDE[0]+=1
      elif line[2] > line[5]:
        listaVDE[1]+=1
      else:
        listaVDE[2]+=1
  graph_05=px.pie(values=listaVDE,names=[paisA, paisB,'Empate'], color=[paisA, paisB,'Empate'], color_discrete_map={f'{paisA}':'#008744',f'{paisB}':'#0057e7 ','Empate':'#ffa700'})
  graph_05.update_traces(textposition='inside', textinfo='percent+label',hovertemplate=None,pull=[0,0,0.1])
  graph_05.update_layout(title={'text':f'Quantidade total de partidas: {listaVDE[0]+listaVDE[1]+listaVDE[2]}','y':0.95,'x':0.45});
  return graph_05



if __name__ == '__main__':
    app.run_server(debug=True)