from dash import Dash
from components.layout import create_layout
from callbacks.main_callbacks import register_callbacks

# Crear la instancia de la aplicación Dash
app = Dash(__name__)
app.title = "Optimización de Subsidios de Vivienda"

# Configurar el layout
app.layout = create_layout()

# Registrar los callbacks
register_callbacks(app)

# Ejecutar el servidor
if __name__ == "__main__":
    app.run_server(debug=True)
