from app.agents.prediction_agent.prediction_agent import (
    PredictionAgent,
)
from app.agents.prediction_agent.prediction_request import (
    PredictionRequest,
)


def main() -> None:

    print()

    print("=" * 60)
    print("PREDICTION AGENT COMPLETE TEST")
    print("=" * 60)

    # ==========================================================
    # HISTORICAL DATA
    # ==========================================================

    rows = [
        {"year": 2018, "value": 100},
        {"year": 2019, "value": 115},
        {"year": 2020, "value": 130},
        {"year": 2021, "value": 145},
        {"year": 2022, "value": 160},
        {"year": 2023, "value": 180},
        {"year": 2024, "value": 200},
    ]

    # ==========================================================
    # REQUEST
    # ==========================================================

    request = PredictionRequest(
        target_column="value",
        time_column="year",
        forecast_horizon=3,
        rows=rows,
    )

    # ==========================================================
    # AGENT
    # ==========================================================

    agent = PredictionAgent()

    response = agent.predict(
        request=request,
    )

    # ==========================================================
    # RESULT
    # ==========================================================

    print()
    print(response)
    print()


if __name__ == "__main__":
    main()