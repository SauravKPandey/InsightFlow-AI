class InsightFlowException(Exception):
    """
    Base exception for the InsightFlow framework.
    """

    def __init__(
        self,
        message: str,
        error_code: str,
        component: str
    ):
        super().__init__(message)

        self.message = message
        self.error_code = error_code
        self.component = component