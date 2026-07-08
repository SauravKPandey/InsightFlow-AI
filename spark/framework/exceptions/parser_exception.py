from framework.exceptions.insightflow_exception import InsightFlowException


class ParserException(InsightFlowException):

    def __init__(self, message: str):

        super().__init__(
            message=message,
            error_code="PARSE-001",
            component="DebeziumParser"
        )