from framework.exceptions.insightflow_exception import InsightFlowException


class ValidationException(InsightFlowException):

    def __init__(self, message: str):

        super().__init__(
            message=message,
            error_code="VALIDATION-001",
            component="Normalizer"
        )