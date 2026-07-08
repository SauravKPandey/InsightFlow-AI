from framework.exceptions.insightflow_exception import InsightFlowException


class ConfigurationException(InsightFlowException):

    def __init__(self, message: str):

        super().__init__(
            message=message,
            error_code="CONFIG-001",
            component="Configuration"
        )