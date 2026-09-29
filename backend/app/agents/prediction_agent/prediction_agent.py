from __future__ import annotations

from app.agents.base.base_agent import BaseAgent

from app.agents.prediction_agent.feature_builder import (
    FeatureBuilder,
)
from app.agents.prediction_agent.model_selector import (
    ModelSelector,
)
from app.agents.prediction_agent.prediction_analyzer import (
    PredictionAnalyzer,
)
from app.agents.prediction_agent.prediction_engine import (
    PredictionEngine,
)
from app.agents.prediction_agent.prediction_formatter import (
    PredictionFormatter,
)
from app.agents.prediction_agent.prediction_models import (
    PredictionResult,
)
from app.agents.prediction_agent.prediction_request import (
    PredictionRequest,
)
from app.agents.prediction_agent.prediction_request_builder import (
    PredictionRequestBuilder,
)

from app.agents.sql_agent.sql_agent import (
    SQLAgent,
)

from app.models.agent_response import (
    AgentResponse,
)


__all__ = (
    "PredictionAgent",
)


class PredictionAgent(BaseAgent):
    """
    Main agent responsible for generating predictions.

    Complete workflow
    -----------------

    User Question
        ↓
    SQL Agent
        ↓
    Historical SQL Data
        ↓
    PredictionRequestBuilder
        ↓
    FeatureBuilder
        ↓
    ModelSelector
        ↓
    PredictionEngine
        ↓
    PredictionAnalyzer
        ↓
    PredictionFormatter
        ↓
    AgentResponse
    """

    def __init__(
        self,
        *,
        sql_agent: SQLAgent,
    ) -> None:
        """
        Initialize Prediction Agent components.

        Args:
            sql_agent:
                SQL Agent used to retrieve historical data.
        """

        self._sql_agent = sql_agent

        self._prediction_request_builder = (
            PredictionRequestBuilder()
        )

        self._feature_builder = (
            FeatureBuilder()
        )

        self._model_selector = (
            ModelSelector()
        )

        self._prediction_engine = (
            PredictionEngine()
        )

        self._prediction_analyzer = (
            PredictionAnalyzer()
        )

        self._prediction_formatter = (
            PredictionFormatter()
        )

    # ==========================================================
    # BASE AGENT
    # ==========================================================

    def ask(
        self,
        *,
        question: str,
        conversation_id: int,
    ) -> AgentResponse:
        """
        Process a prediction request.

        Workflow:
            User Question
                ↓
            SQL Agent
                ↓
            Historical Data
                ↓
            Prediction Request
                ↓
            Prediction Pipeline
                ↓
            AgentResponse

        Args:
            question:
                User prediction question.

            conversation_id:
                Current conversation identifier.

        Returns:
            Unified AgentResponse.
        """

        try:

            # ==================================================
            # STEP 1 - GET HISTORICAL DATA
            # ==================================================

            historical_question = (
                self._build_historical_data_question(
                    question=question,
                )
            )

            sql_response = self._sql_agent.ask(
                question=historical_question,
                conversation_id=conversation_id,
            )

            # ==================================================
            # SQL FAILURE
            # ==================================================

            if not sql_response.success:

                return AgentResponse(
                    success=False,

                    error=(
                        sql_response.error
                        or
                        "Impossible de récupérer les données "
                        "historiques nécessaires à la prédiction."
                    ),

                    answer=(
                        sql_response.answer
                        or
                        "Impossible de récupérer les données "
                        "historiques nécessaires à la prédiction."
                    ),

                    sql=sql_response.sql,

                    rows=sql_response.rows,

                    data={},
                )

            # ==================================================
            # NO DATA
            # ==================================================

            if not sql_response.rows:

                return AgentResponse(
                    success=False,

                    error=(
                        "Aucune donnée historique disponible "
                        "pour effectuer une prédiction."
                    ),

                    answer=(
                        "Je n'ai trouvé aucune donnée historique "
                        "suffisante pour générer une prédiction."
                    ),

                    sql=sql_response.sql,

                    rows=[],

                    data={},
                )

            # ==================================================
            # STEP 2 - BUILD PREDICTION REQUEST
            # ==================================================

            request = (
                self._prediction_request_builder.build(
                    question=question,
                    rows=sql_response.rows,
                )
            )

            # ==================================================
            # STEP 3 - RUN PREDICTION PIPELINE
            # ==================================================

            prediction_result = (
                self.predict(
                    request=request,
                )
            )

            # ==================================================
            # PREDICTION FAILURE
            # ==================================================

            if not prediction_result.success:

                return AgentResponse(
                    success=False,

                    error=(
                        prediction_result.error
                        or
                        "La génération de la prédiction a échoué."
                    ),

                    answer=(
                        prediction_result.error
                        or
                        "Impossible de générer une prédiction "
                        "à partir des données disponibles."
                    ),

                    sql=sql_response.sql,

                    rows=sql_response.rows,

                    data=self._build_prediction_data(
                        prediction_result=prediction_result,
                        request=request,
                        analysis={},
                    ),
                )

            # ==================================================
            # STEP 4 - ANALYZE PREDICTION
            # ==================================================

            analysis = (
                self._prediction_analyzer.analyze(
                    prediction_result=prediction_result,
                )
            )

            # ==================================================
            # STEP 5 - FORMAT RESPONSE
            # ==================================================

            answer = (
                self._prediction_formatter.format(
                    prediction_result=prediction_result,
                    analysis=analysis,
                )
            )

            # ==================================================
            # SUCCESS RESPONSE
            # ==================================================

            return AgentResponse(
                success=True,

                error=None,

                answer=answer,

                sql=sql_response.sql,

                rows=sql_response.rows,

                data=self._build_prediction_data(
                    prediction_result=prediction_result,
                    request=request,
                    analysis=analysis,
                ),
            )

        except Exception as ex:

            return AgentResponse(
                success=False,

                error=str(ex),

                answer=(
                    "Une erreur est survenue lors de la "
                    "génération de la prédiction."
                ),

                sql=None,

                rows=[],

                data={},
            )

    # ==========================================================
    # PREDICTION PIPELINE
    # ==========================================================

    def predict(
        self,
        *,
        request: PredictionRequest,
    ) -> PredictionResult:
        """
        Generate a prediction from historical data.

        Workflow:
            PredictionRequest
                ↓
            FeatureBuilder
                ↓
            ModelSelector
                ↓
            PredictionEngine
                ↓
            PredictionResult

        Args:
            request:
                Prediction request containing historical
                data and prediction configuration.

        Returns:
            Structured PredictionResult.
        """

        # ======================================================
        # STEP 1 - FEATURE PREPARATION
        # ======================================================

        prepared_rows = (
            self._feature_builder.build(
                rows=request.rows,
                time_column=request.time_column,
                target_column=request.target_column,
            )
        )

        # ======================================================
        # MINIMUM DATA VALIDATION
        # ======================================================

        if len(prepared_rows) < 2:

            raise ValueError(
                "Les données historiques sont insuffisantes "
                "pour effectuer une prédiction. "
                "Au moins 2 périodes historiques sont nécessaires."
            )

        # ======================================================
        # STEP 2 - MODEL SELECTION
        # ======================================================

        selected_model = (
            self._model_selector.select(
                rows=prepared_rows,
                time_column=request.time_column,
                target_column=request.target_column,
            )
        )

        # ======================================================
        # STEP 3 - PREDICTION
        # ======================================================

        prediction_result = (
            self._prediction_engine.predict(
                target_column=request.target_column,
                time_column=request.time_column,
                forecast_horizon=request.forecast_horizon,
                rows=prepared_rows,
            )
        )

        # ======================================================
        # CHECK PREDICTION RESULT
        # ======================================================

        if not prediction_result.success:

            raise ValueError(
                prediction_result.error
                or
                "Impossible de générer la prédiction."
            )

        # ======================================================
        # STEP 4 - MODEL METADATA
        # ======================================================

        self._add_model_metadata(
            prediction_result=prediction_result,
            selected_model=selected_model,
        )

        # ======================================================
        # RETURN RESULT
        # ======================================================

        return prediction_result

    # ==========================================================
    # RESPONSE DATA
    # ==========================================================

    @staticmethod
    def _build_prediction_data(
        *,
        prediction_result: PredictionResult,
        request: PredictionRequest,
        analysis: dict,
    ) -> dict:
        """
        Build structured prediction data.

        This data can be consumed by:
        - Frontend
        - Charts
        - Dashboards
        - Future visualization agents

        Args:
            prediction_result:
                Prediction generated by the engine.

            request:
                Prediction configuration.

            analysis:
                Prediction analysis.

        Returns:
            Structured prediction metadata.
        """

        predictions = [

            {
                "period": prediction.period,

                "predicted_value": (
                    prediction.predicted_value
                ),

                "lower_bound": (
                    prediction.lower_bound
                ),

                "upper_bound": (
                    prediction.upper_bound
                ),
            }

            for prediction
            in prediction_result.predictions

        ]

        return {

            # ==============================================
            # REQUEST
            # ==============================================

            "target_column": (
                request.target_column
            ),

            "time_column": (
                request.time_column
            ),

            "forecast_horizon": (
                request.forecast_horizon
            ),

            # ==============================================
            # MODEL
            # ==============================================

            "model_name": (
                prediction_result.model_name
            ),

            "selected_model": (
                prediction_result.metadata.get(
                    "selected_model"
                )
            ),

            # ==============================================
            # PREDICTIONS
            # ==============================================

            "predictions": predictions,

            # ==============================================
            # METRICS
            # ==============================================

            "metrics": (
                prediction_result.metrics
            ),

            # ==============================================
            # ANALYSIS
            # ==============================================

            "analysis": analysis,

            # ==============================================
            # METADATA
            # ==============================================

            "metadata": (
                prediction_result.metadata
            ),
        }

    # ==========================================================
    # PRIVATE
    # ==========================================================

    @staticmethod
    def _add_model_metadata(
        *,
        prediction_result: PredictionResult,
        selected_model: str,
    ) -> None:
        """
        Add model selection information to prediction metadata.

        Args:
            prediction_result:
                Generated prediction result.

            selected_model:
                Model selected by ModelSelector.
        """

        prediction_result.metadata[
            "selected_model"
        ] = selected_model

    @staticmethod
    def _build_historical_data_question(
        *,
        question: str,
    ) -> str:
        """
        Transform a prediction request into a historical
        data retrieval request for the SQL Agent.

        The SQL Agent must only retrieve existing historical
        data. Future predictions are generated exclusively
        by the Prediction Engine.
        """

        return f"""
La demande utilisateur est :

{question}

IMPORTANT :

Cette demande sera traitée par un système de prédiction
séparé.

Ta seule responsabilité est de récupérer les données
historiques réelles nécessaires à cette prédiction.

Tu dois :

- Identifier la donnée à prédire.
- Identifier la dimension temporelle.
- Récupérer les valeurs historiques réelles.
- Retourner suffisamment de périodes historiques.
- Trier les résultats chronologiquement.

Tu ne dois JAMAIS :

- Faire une prédiction en SQL.
- Calculer des valeurs futures.
- Générer des années futures.
- Utiliser une régression linéaire.
- Calculer slope ou intercept.
- Créer ForecastYears ou NextYears.
- Estimer des valeurs.

IMPORTANT :

Retourne uniquement les données historiques existantes
dans la base de données.

Le modèle Prophet effectuera lui-même la prédiction future.

La requête SQL doit idéalement retourner deux colonnes :

1. Une colonne temporelle.
2. Une colonne numérique correspondant à la valeur historique.

Trie toujours les résultats par ordre chronologique.
""".strip()