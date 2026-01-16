from enum import Enum

class Status(str, Enum):
    """
    Status de conclusão de um hábito

    Attributes:
        FINISHED: Atividade concluída
        PARTIALLY: Atividade parcialmente concluída
        UNFINISHED: Atividade não concluída
    """

    FINISHED = "completed"
    PARTIALLY = "partially"
    UNFINISHED = "unfinished"
