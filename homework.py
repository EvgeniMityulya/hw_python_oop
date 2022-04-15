from typing import Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,        # тип тренировки
                 duration: float,           # длительность тренировки
                 distance: float,           # дистанция
                 speed: float,              # скорость
                 calories: float) -> None:  # калории
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f"Тип тренировки: {self.training_type};"
                f" Длительность: {self.duration:.3f} ч.;"
                f" Дистанция: {self.distance:.3f} км;"
                f" Ср. скорость: {self.speed:.3f} км/ч;"
                f" Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,       # количество совершённых действий
                 duration: float,   # длительность тренировки
                 weight: float,     # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_1 * self.get_mean_speed()
                - self.coeff_calorie_2) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_weight_1: float = 0.035
    coeff_weight_2: float = 0.029
    multiplier: int = 2

    def __init__(self,
                 action: int,       # количество шагов
                 duration: float,   # время тренировки в часах
                 weight: float,     # вес пользователя
                 height) -> None:   # рост пользователя
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.coeff_weight_1 * self.weight + (self.get_mean_speed()
                ** self.multiplier // self.height) * self.coeff_weight_2
                * self.weight) * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    coeff_calorie_3: float = 1.1
    coeff_calorie_4: int = 2

    def __init__(self,
                 action: int,               # количество гребков
                 duration: float,           # время в часах
                 weight: float,             # вес пользователя
                 length_pool: float,        # длина бассейна
                 count_pool: int) -> None:  # сколько раз переплыл бассейн
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.coeff_calorie_3)
                * self.coeff_calorie_4 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_trainings: dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    if workout_type in dict_trainings:
        return dict_trainings[workout_type](*data)
    else:
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

