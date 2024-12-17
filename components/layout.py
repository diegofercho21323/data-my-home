from dash import html, dcc

departament_options = {
    5: "ANTIOQUIA",
    8: "ATLÁNTICO",
    11: "BOGOTÁ, D.C.",
    13: "BOLÍVAR",
    15: "BOYACÁ",
    17: "CALDAS",
    18: "CAQUETÁ",
    19: "CAUCA",
    20: "CESAR",
    23: "CÓRDOBA",
    25: "CUNDINAMARCA",
    27: "CHOCÓ",
    41: "HUILA",
    44: "LA GUAJIRA",
    47: "MAGDALENA",
    50: "META",
    52: "NARIÑO",
    54: "NORTE DE SANTANDER",
    63: "QUINDÍO",
    66: "RISARALDA",
    68: "SANTANDER",
    70: "SUCRE",
    73: "TOLIMA",
    76: "VALLE DEL CAUCA",
    81: "ARAUCA",
    85: "CASANARE",
    86: "PUTUMAYO",
    88: "ARCHIPIÉLAGO DE SAN ANDRÉS, PROVIDENCIA Y SANTA CATALINA",
    91: "AMAZONAS",
    94: "GUAINÍA",
    95: "GUAVIARE",
    97: "VAUPÉS",
    99: "VICHADA",
}
# dcc.Dropdown(
#                         id="departamento-input",
#                         options=[
#                             {
#                                 "label": value,
#                                 "value": label,
#                             }
#                             for label, value in departament_options.items()
#                         ],
#                         value="5",  # Departamento por defecto
#                     ),

from dash import dcc, html


def create_layout():
    return html.Div(
        [
            html.H1(
                "Optimización de Subsidios de Vivienda", style={"textAlign": "center"}
            ),
            # Pestañas para mostrar diferentes vistas
            dcc.Tabs(
                [
                    # Pestaña para subsidios generales (ya existente)
                    dcc.Tab(
                        label="Predicción de Subsidios",
                        children=[
                            html.Div(
                                [
                                    # Entradas para el usuario
                                    html.Div(
                                        [
                                            html.Label("Departamento:"),
                                            dcc.Dropdown(
                                                id="departamento-input",
                                                options=[
                                                    {
                                                        "label": value,
                                                        "value": label,
                                                    }
                                                    for label, value in departament_options.items()
                                                ],
                                                value="5",  # Departamento por defecto
                                            ),
                                            html.Label("Programa:"),
                                            dcc.Dropdown(
                                                id="programa-input",
                                                options=[
                                                    {
                                                        "label": "Mi Casa Ya",
                                                        "value": "Mi Casa Ya",
                                                    },
                                                    {"label": "VIPA", "value": "VIPA"},
                                                    {
                                                        "label": "Ahorro Programado",
                                                        "value": "Ahorro Programado",
                                                    },
                                                    {
                                                        "label": "Nuevo Programa",
                                                        "value": "Nuevo Programa",
                                                    },
                                                ],
                                                value="Nuevo Programa",
                                            ),
                                            html.Label("Año:"),
                                            dcc.Input(
                                                id="año-input",
                                                type="number",
                                                value=2025,
                                            ),
                                            html.Label("Presupuesto Total (COP):"),
                                            dcc.Input(
                                                id="presupuesto-input",
                                                type="number",
                                                value=4000000000,
                                            ),
                                            html.Label(
                                                "Valor Subsidio por Hogar (COP):"
                                            ),
                                            dcc.Input(
                                                id="valor-subsidio-input",
                                                type="number",
                                                value=12000000,
                                            ),
                                        ],
                                        style={"margin": "20px"},
                                    ),
                                    # Resultado de predicción
                                    html.Div(
                                        id="output-container",
                                        style={"margin": "20px", "fontSize": "20px"},
                                    ),
                                    # Gráficos
                                    html.Div(
                                        [
                                            dcc.Graph(id="bar-chart"),
                                            dcc.Graph(id="line-chart"),
                                            dcc.Graph(
                                                id="status-bar-chart"
                                            ),  # Gráfico de estado de postulación
                                        ]
                                    ),
                                ]
                            )
                        ],
                    ),
                    # Nueva Pestaña para Subsidios Ejecutados por Año
                    dcc.Tab(
                        label="Subsidios Ejecutados por Año",
                        children=[
                            html.Div(
                                [
                                    # Gráfico de subsidios ejecutados por año
                                    dcc.Graph(id="subsidios-ejecutados-por-año"),
                                    # Gráfico de la diferencia entre Senso Hogares y Senso Viviendas
                                    dcc.Graph(id="diferencia-senso-hogares-viviendas"),
                                ]
                            )
                        ],
                    ),
                ]
            ),
        ]
    )
