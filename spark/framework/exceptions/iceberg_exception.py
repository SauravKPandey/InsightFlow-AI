from framework.exceptions.insightflow_exception import InsightFlowException


class IcebergException(InsightFlowException):

    def __init__(self, message: str):

        super().__init__(
            message=message,
            error_code="ICEBERG-001",
            component="IcebergWriter"
        )