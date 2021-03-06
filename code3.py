import dash
import datetime
import pandas as pd
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

# Inicializando app e definindo stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Carregando e transformando dados
data = pd.read_csv('active_fire_with_locations_bugged.csv')
region_counters = data['region'].value_counts()
state_counters = data['state'].value_counts()
data['acq_date'] = data['acq_date'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
data['month'] = data['acq_date'].apply(lambda x: x.month)
counters_by_region_and_month = pd.DataFrame(data.groupby(['month', 'region'])['region'].count())
counters_by_region_and_month.columns = ['counter']
counters_by_region_and_month = counters_by_region_and_month.reset_index()
regions = counters_by_region_and_month['region'].unique()

# Criando gráficos de barras
fig = go.Figure(go.Bar(x=region_counters.index, y=region_counters.values))
fig.update_layout(xaxis_title="Regiões", yaxis_title="Contagem de focos")
fig2 = go.Figure(go.Bar(x=state_counters.index, y=state_counters.values))
fig2.update_layout(xaxis_title="Estados", yaxis_title="Contagem de focos")
fig3 = go.Figure()
for region in regions:
    line_data = counters_by_region_and_month[counters_by_region_and_month['region'] == region]
    fig3.add_trace(go.Scatter(x=line_data['month'],
                              y=line_data['counter'],
                              mode='lines',
                              name=region))
fig3.update_layout(xaxis_title="Meses", yaxis_title="Contagem de focos")

# Definindo layout da página
app.layout = html.Div(children=[
    html.H1(
        children='Focos de Incêndio no Brasil',
        style={
            'textAlign': 'center',
        }
    ),
    html.H3(
        children='De janeiro a junho de 2020',
        style={
            'textAlign': 'center',
        }
    ),
    html.Div(children=[dcc.Graph(id='fig1',figure=fig)],
             style={'width': '50%', 'float': 'left'}),
    html.Div(children=[dcc.Graph(id='fig3',figure=fig3)],
             style={'marginLeft': '50%'}),
    dcc.Graph(id='fig2',
              figure=fig2)
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)