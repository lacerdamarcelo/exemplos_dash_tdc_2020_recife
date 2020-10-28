import dash
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Inicializando app e definindo stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Carregando e transformando dados
data = pd.read_csv('active_fire_with_locations_bugged.csv')
region_counters = data['region'].value_counts()
data['acq_date'] = data['acq_date'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
data['month'] = data['acq_date'].apply(lambda x: x.month)
data['week_in_the_year'] = data['acq_date'].apply(lambda x: ((x - datetime.datetime(2020, 1, 1)).days // 7) + 1)
counters_by_region_and_month = pd.DataFrame(data.groupby(['month', 'region'])['region'].count())
counters_by_region_and_month.columns = ['counter']
counters_by_region_and_month = counters_by_region_and_month.reset_index()
counters_by_region_and_week_in_the_year = pd.DataFrame(data.groupby(['week_in_the_year', 'region'])['region'].count())
counters_by_region_and_week_in_the_year.columns = ['counter']
counters_by_region_and_week_in_the_year = counters_by_region_and_week_in_the_year.reset_index()
regions = counters_by_region_and_week_in_the_year['region'].unique()
regions = counters_by_region_and_month['region'].unique()
counters_by_region_and_week_in_the_year['cumsum'] = counters_by_region_and_week_in_the_year['counter'].cumsum()
counters_by_region_and_week_in_the_year['cumsum'] = None
cum_sum = counters_by_region_and_week_in_the_year[counters_by_region_and_week_in_the_year['region'] == regions[0]]['counter'].cumsum()
for region in regions[1:]:
    cum_sum = pd.concat([cum_sum, counters_by_region_and_week_in_the_year[counters_by_region_and_week_in_the_year['region'] == region]['counter'].cumsum()])
counters_by_region_and_week_in_the_year['cumsum'] = cum_sum

# Criando gráficos de barras
fig = px.bar(counters_by_region_and_week_in_the_year, x='cumsum', y='region', animation_frame='week_in_the_year',
             color='cumsum', orientation='h')
fig.update_layout(xaxis_title="Regiões", yaxis_title="Contagem de focos",
                  yaxis={'categoryorder':'total ascending'})
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
    dcc.Graph(id='fig2')
    ]
)

# Gráfico fig2 atualizado por callback.
@app.callback(
    Output(component_id='fig2', component_property='figure'),
    [Input(component_id='fig1', component_property='selectedData')]
)
def plot_fig2(selectedData):
    if selectedData is None:
        region_filter = regions
    else:
        region_filter = [selected_dict['y'] for selected_dict in selectedData['points']]
    state_counters = data[data['region'].isin(region_filter)]['state'].value_counts()
    fig2 = go.Figure(go.Bar(x=state_counters.index, y=state_counters.values))
    fig2.update_layout(xaxis_title="Estados", yaxis_title="Contagem de focos")
    return fig2

if __name__ == '__main__':
    app.run_server(debug=True)