import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import networkx as nx

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

archivo = 'informacion_carreteras.txt'
def construir_grafo(archivo):
    G = nx.Graph()
    with open(archivo,'r',encoding='utf-8') as file:
        next(file)
        for line in file:
            origen, destino, distancia = line.strip().split(',')
            G.add_edge(origen.strip(),destino.strip(), weight = float(distancia.strip()))
    return G

grafo = construir_grafo(archivo)
nodos = list(grafo.nodes())

# Definir las opciones para los dropdowns
opciones_dropdown_1 = [
    {'label': nodo, 'value': nodo}for nodo in nodos]
    

opciones_dropdown_2 = [
    {'label': nodo, 'value': nodo}for nodo in nodos]


# Diseño de la aplicación Dash
app.layout = html.Div([
    html.H1("Ruta mas Corta",style={'font-weight': 'bold'}),
    
    html.Label("Ciudad de Partida:",style={'font-weight': 'bold'}),
    dcc.Dropdown(
        id='dropdown-inicio',
        options=opciones_dropdown_1,
        value='',
        style={'width': '50%'},
    ),
    
    html.Label("Ciudad de Llegada",style={'font-weight': 'bold'}),
    dcc.Dropdown(
        id='dropdown-llegada',
        options=opciones_dropdown_2,
        value='',
        style={'width': '50%'},
    ),
    
    html.Div(id='resultado-seleccion')
], style={'backgroundColor': 'lightblue','padding': '20px'})



# Definir callback para actualizar el resultado en función de la selección de los dropdowns
@app.callback(
    Output('resultado-seleccion', 'children'),
    [Input('dropdown-inicio', 'value'),
     Input('dropdown-llegada', 'value')]
)
def actualizar_resultado(valor_dropdown_1, valor_dropdown_2):
    if valor_dropdown_1 and valor_dropdown_2:
        ruta_mas_corta, distancia_total = calcular_ruta_mas_corta(grafo, valor_dropdown_1, valor_dropdown_2)
        if len(ruta_mas_corta) > 2:
            mensaje = 'La ruta no es directa'
            return mensaje + f', la ruta más corta es: {" -> ".join(ruta_mas_corta)}, con una distancia de: {distancia_total} KM'
        else: 
            return f'La ruta más corta es: {" -> ".join(ruta_mas_corta)}, con una distancia de: {distancia_total} KM'
    else:
        return ''
    
def calcular_ruta_mas_corta(grafo, origen, destino):
    ruta_mas_corta = nx.shortest_path(grafo, origen, destino, weight='weight')
    distancia_total = nx.shortest_path_length(grafo, origen, destino, weight='weight')
    return ruta_mas_corta, distancia_total

# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run(debug=True)
