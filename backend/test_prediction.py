from app.agents.prediction_agent.prediction_agent import PredictionAgent
from app.agents.prediction_agent.models.prediction_request import PredictionRequest

request = PredictionRequest(
    table_name="FACT_PRIX_INDICES",
    date_column="annee",
    target_column="prix_moyen",
    forecast_horizon=5
)

agent = PredictionAgent()

result = agent.predict(request)

print(result)