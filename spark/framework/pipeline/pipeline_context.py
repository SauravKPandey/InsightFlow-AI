from dataclasses import dataclass


@dataclass
class PipelineContext:
    """
    Carries execution metadata throughout the pipeline.
    """

    entity_name: str

    batch_id: int

    layer: str

    silver_table: str

    dlq_table : str

    execution_mode: str = "LIVE"