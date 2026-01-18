from enum import Enum

class Status(str, Enum):
    """
    Status de conclusão de um hábito

    Attributes:
        COMPLETED: Atividade concluída
        PARTIALLY: Atividade parcialmente concluída
        UNFINISHED: Atividade não concluída
    """

    COMPLETED = "completed"
    PARTIALLY = "partially"
    UNFINISHED = "unfinished"
