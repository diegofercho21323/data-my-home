from dash import Input, Output
from models.model_handler import ModelHandler
import plotly.graph_objs as go


def register_callbacks(app):
    # Callback existente para la predicción
    @app.callback(
        [
            Output("output-container", "children"),
            Output("bar-chart", "figure"),
            Output("line-chart", "figure"),
            Output("status-bar-chart", "figure"),
        ],
        [
            Input("departamento-input", "value"),
            Input("programa-input", "value"),
            Input("año-input", "value"),
            Input("presupuesto-input", "value"),
            Input("valor-subsidio-input", "value"),
        ],
    )
    def actualizar_prediccion(departamento, programa, año, presupuesto, valor_subsidio):
        handler = ModelHandler(departamento)
        # Evaluar el modelo con el conjunto de prueba
        handler.evaluate_model()
        df_year = handler.df[handler.df["Año"] == año - 1]
        deficit_promedio = df_year["Déficit Viviendas"].mean()

        # Verificar si el déficit promedio es cero
        if deficit_promedio == 0:
            return (
                "Déficit de viviendas es cero para el año seleccionado. No es posible calcular el impacto.",
                {},
                {},
                {},
            )

        prediccion = handler.predict(programa, año, presupuesto, deficit_promedio)
        impacto = (prediccion / deficit_promedio) * 100

        mensaje = [
            f"Predicción de Hogares Beneficiados: {int(prediccion)} ",
            f"Impacto en el Déficit Habitacional: {impacto:.2f}%",
        ]

        bar_fig = go.Figure(
            data=[
                go.Bar(name="Déficit Viviendas", x=[año], y=[deficit_promedio]),
                go.Bar(name="Hogares Beneficiados", x=[año], y=[prediccion]),
            ]
        )
        bar_fig.update_layout(
            title="Déficit vs Hogares Beneficiados",
            xaxis_title="Año",
            yaxis_title="Número de Hogares",
            barmode="group",
        )

        line_fig = go.Figure(
            data=[
                go.Scatter(
                    x=[año],
                    y=[impacto],
                    mode="lines+markers",
                    name="Impacto en Déficit",
                )
            ]
        )
        line_fig.update_layout(
            title="Impacto en el Déficit Habitacional",
            xaxis_title="Año",
            yaxis_title="Impacto (%)",
        )

        estado_counts = handler.df["Categoría Estado"].value_counts()
        status_bar_fig = go.Figure(
            data=[
                go.Bar(
                    x=estado_counts.index,
                    y=estado_counts.values,
                    name="Estado de Postulación",
                )
            ]
        )

        status_bar_fig.update_layout(
            title="Distribución de Estados de Postulación",
            xaxis_title="Estado de Postulación",
            yaxis_title="Número de Subsidios",
            barmode="group",
        )

        return mensaje, bar_fig, line_fig, status_bar_fig

    # Callback para subsidios ejecutados por año
    @app.callback(
        Output("subsidios-ejecutados-por-año", "figure"),
        Input("departamento-input", "value"),
    )
    def subsidios_ejecutados_por_año(departamento):
        # Cargar el modelo del departamento
        handler = ModelHandler(departamento)

        # Evaluar el modelo con el conjunto de prueba
        handler.evaluate_model()

        # Filtrar subsidios ejecutados ("Asignados") por año
        subsidios_ejecutados = handler.df[handler.df["Categoría Estado"] == "Ejecutado"]
        subsidios_por_año = subsidios_ejecutados.groupby("Año")["Hogares"].sum()

        # Crear gráfico de barras
        fig = go.Figure(
            data=[
                go.Bar(
                    x=subsidios_por_año.index,
                    y=subsidios_por_año.values,
                    name="Hogares Asignados",
                )
            ]
        )
        fig.update_layout(
            title="Subsidios Ejecutados por Año",
            xaxis_title="Año",
            yaxis_title="Número de Hogares Asignados",
        )

        return fig

    # Callback para mostrar la diferencia entre Senso Hogares y Senso Viviendas por año
    @app.callback(
        Output("diferencia-senso-hogares-viviendas", "figure"),
        Input("departamento-input", "value"),
    )
    def diferencia_senso_hogares_viviendas(departamento):
        # Cargar el modelo del departamento
        handler = ModelHandler(departamento)
        # Evaluar el modelo con el conjunto de prueba
        handler.evaluate_model()

        # Agrupar por año y calcular la diferencia entre Senso Hogares y Senso Viviendas
        handler.df["Diferencia Senso"] = (
            handler.df["Senso Hogares"] - handler.df["Senso Viviendas"]
        )
        diferencia_por_año = handler.df.groupby("Año")["Diferencia Senso"].sum()

        # Crear gráfico de barras
        fig = go.Figure(
            data=[
                go.Bar(
                    x=diferencia_por_año.index,
                    y=diferencia_por_año.values,
                    name="Diferencia Senso Hogares vs Viviendas",
                )
            ]
        )
        fig.update_layout(
            title="Diferencia entre Senso Hogares y Senso Viviendas por Año",
            xaxis_title="Año",
            yaxis_title="Diferencia (Hogares - Viviendas)",
        )

        return fig
