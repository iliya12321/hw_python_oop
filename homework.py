from dataclasses import dataclass, asdict
from typing import List, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # преодолевает за один шаг
    M_IN_KM: int = 1000  # из метров в километры
    M_IN_HOUR: int = 60  # Служит для перевода в минуты

    def __init__(self,
                 action: int,  # число шагов или гребков
                 duration: float,  # длительность тренировки в часах
                 weight: float,  # вес спортсмена
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM  # Формула дистанции

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration  # формула средней скорости

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__, self.duration,
            self.get_distance(), self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        return ((((coeff_calorie_1 * self.get_mean_speed())
            - (coeff_calorie_2))
            * (self.weight / self.M_IN_KM))
            * (self.duration * self.M_IN_HOUR))  # формула расхода каллорий


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int  # рост спортсмена
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_3: float = 0.035
        coeff_calorie_4: float = 0.029  # расчёт каллорий для спортивной ходьбы
        return (((coeff_calorie_3 * self.weight)
                + (self.get_mean_speed()**2 // self.height)
                * (coeff_calorie_4 * self.weight))
                * (self.duration * self.M_IN_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # один гребок в плавании

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,  # длинна бассейна в метрах
                 count_pool: int  # сколько раз пользователь переплыл бассейн
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (((self.length_pool * self.count_pool)
                / self.M_IN_KM) / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_5: float = 1.1  # формула расчёта каллорий
        return (self.get_mean_speed() + coeff_calorie_5) * 2 * self.weight


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in training_type:
        return training_type[workout_type](*data)
    else:
        raise ValueError(
            f'Нет такой тренировки{workout_type}.'
        )


def main(training: Training) -> InfoMessage:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)