import dash
import pandas as pd
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

# Inicializando app e definindo stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Carregando dados
data = pd.read_csv('active_fire_with_locations_bugged.csv')
region_counters = data['region'].value_counts()

# Criando gráfico de barras
fig = go.Figure(go.Bar(x=region_counters.index, y=region_counters.values))
fig.update_layout(xaxis_title="Regiões", yaxis_title="Contagem de focos")

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
    dcc.Graph(id='fig1',
    		  figure=fig)
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)