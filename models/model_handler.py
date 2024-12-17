import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class ModelHandler:
    def __init__(self, departamento):
        self.departamento = departamento
        self.pipeline = None
        self.df = None
        self.df_test = None
        self.load_data()
        self.train_model()

    def load_data(self):
        # Cargar el dataset de entrenamiento del departamento
        train_path = f"./data/train_departament/train_{self.departamento}.csv"
        test_path = f"./data/test_departament/test_{self.departamento}.csv"

        # Cargar datos
        self.df = pd.read_csv(train_path)
        self.df_test = pd.read_csv(test_path)

        # Crear la columna de déficit de viviendas
        self.df["Déficit Viviendas"] = (
            self.df["Senso Hogares"] - self.df["Senso Viviendas"]
        )
        self.df_test["Déficit Viviendas"] = (
            self.df_test["Senso Hogares"] - self.df_test["Senso Viviendas"]
        )

        # Crear categoría del estado de postulación
        self.df["Categoría Estado"] = self.df["Estado de Postulación"].apply(
            self.categorize_postulation_status
        )
        self.df_test["Categoría Estado"] = self.df_test["Estado de Postulación"].apply(
            self.categorize_postulation_status
        )

    @staticmethod
    def categorize_postulation_status(status):
        if "Asignado" in status:
            return "Ejecutado"
        elif "Renuncia" in status or "Vencido" in status:
            return "No Ejecutado"
        else:
            return "Pendiente"

    def train_model(self):
        # Entrenar el modelo para el departamento
        X = self.df[
            [
                "Programa",
                "Año",
                "Valor Asignado",
                "Déficit Viviendas",
                "Categoría Estado",
            ]
        ]
        y = self.df["Hogares"]

        cat_features = ["Programa", "Categoría Estado"]
        num_features = ["Año", "Valor Asignado", "Déficit Viviendas"]

        # Escalar las características numéricas
        num_pipeline = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())

        cat_pipeline = make_pipeline(
            SimpleImputer(strategy="most_frequent"),
            OneHotEncoder(handle_unknown="ignore"),
        )

        full_pipeline = ColumnTransformer(
            [("num", num_pipeline, num_features), ("cat", cat_pipeline, cat_features)]
        )

        self.pipeline = make_pipeline(
            full_pipeline,
            RandomForestRegressor(n_estimators=150, random_state=26, max_depth=20),
        )
        self.pipeline.fit(X=X, y=y)

    def evaluate_model(self):
        # Evaluar el modelo con los datos de prueba
        X_test = self.df_test[
            [
                "Programa",
                "Año",
                "Valor Asignado",
                "Déficit Viviendas",
                "Categoría Estado",
            ]
        ]
        y_test = self.df_test["Hogares"]

        # Realizar predicciones
        y_pred = self.pipeline.predict(X_test)

        # Calcular las métricas de evaluación
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        print(f"Evaluación del Modelo:")
        print(f"Mean Absolute Error: {mae}")
        print(f"Mean Squared Error: {mse}")
        print(f"R2 Score: {r2}")

    def predict(self, programa, año, presupuesto, deficit):
        # Predecir hogares beneficiados con un nuevo conjunto de datos
        input_data = pd.DataFrame(
            {
                "Programa": [programa],
                "Año": [año],
                "Valor Asignado": [presupuesto],
                "Déficit Viviendas": [deficit],
                "Categoría Estado": ["Pendiente"],
            }
        )
        return self.pipeline.predict(input_data)[0]
