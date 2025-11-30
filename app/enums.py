from enum import Enum

class Frequence(str, Enum):
    """
    Freqûencia de execução de um hábito

    Attributes:
        DAILY: Executado diariamente
        WEEKLY: Executado semanalmente
        MONTHLY: Executado mensalmente
    """

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

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
