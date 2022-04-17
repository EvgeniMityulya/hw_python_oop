from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str  # тип тренировки
    duration: float     # длительность тренировки в часах
    distance: float     # дистанция в км
    speed: float        # скорость в км/ч
    calories: float     # калории

    def get_message(self) -> str:
        return ("Тип тренировки: {training_type}; "
                "Длительность: {duration:.3f} ч.; "
                "Дистанция: {distance:.3f} км; "
                "Ср. скорость: {speed:.3f} км/ч; "
                "Потрачено ккал: {calories:.3f}.".format(**asdict(self)))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int           # количество совершённых действий
    duration_hour: float  # длительность тренировки в часах
    weight: float         # вес спортсмена

    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60
    LEN_STEP: ClassVar[float] = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_hour

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return NotImplementedError(f"Ошибка в {type(self).__name__}")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_hour,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEEP_SUBTRAHEND: float = 20

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                - self.CALORIES_MEAN_SPEEP_SUBTRAHEND) * self.weight
                / self.M_IN_KM * self.duration_hour * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_MULTIPLIER_1: float = 0.035
    WEIGHT_MULTIPLIER_2: float = 0.029
    SQUARE: int = 2

    def __init__(self,
                 action: int,       # количество шагов
                 duration: float,   # время тренировки в часах
                 weight: float,     # вес пользователя
                 height) -> None:   # рост пользователя
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.WEIGHT_MULTIPLIER_1 * self.weight +
                (self.get_mean_speed() ** self.SQUARE // self.height)
                * self.WEIGHT_MULTIPLIER_2 * self.weight)
                * self.duration_hour * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    MEAN_SPEED_SUMMAND: float = 1.1
    MEAN_SPEED_MULTIPLIER: float = 2

    def __init__(self,
                 action: int,               # количество гребков
                 duration: float,           # время в часах
                 weight: float,             # вес пользователя
                 length_pool: float,        # длина бассейна в м
                 count_pool: int) -> None:  # сколько раз переплыл бассейн
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration_hour)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.MEAN_SPEED_SUMMAND)
                * self.MEAN_SPEED_MULTIPLIER * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_id: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    if workout_type in training_id:
        return training_id[workout_type](*data)
    raise ValueError("Тренировка не обнаружена.")


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),  # плавание
        ('RUN', [15000, 1, 75]),        # бег
        ('WLK', [9000, 1, 75, 180]),    # ходьба
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
