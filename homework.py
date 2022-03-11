class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
        self,
        training_type,
        duration,
        distance,
        speed,
        calories,
    ) -> None:
        self.training_type = training_type
        self.duration = '%.3f' % duration
        self.distance = '%.3f' % distance
        self.speed = '%.3f' % speed
        self.calories = '%.3f' % calories

    def get_message(self):
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration} ч.; '
            f'Дистанция: {self.distance} км; Ср. скорость: '
            f'{self.speed} км/ч; '
            f'Потрачено ккал: {self.calories}.'
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN = 60
    type = ''

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return float(self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return float(self.get_distance() / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.type,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    type = 'Running'
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.coeff_calorie_1 *
                self.get_mean_speed() -
                self.coeff_calorie_2
            ) *
            self.weight / self.M_IN_KM *
            self.duration * self.MIN
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    type = 'SportsWalking'
    coeff_calorie_1 = 0.035
    coeff_calorie_2 = 0.029

    def __init__(
        self, action: int,
        duration: float,
        weight: float,
        height: int,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            self.coeff_calorie_1 * self.weight +
            (self.get_mean_speed()**2 // self.height) *
            self.coeff_calorie_2 * self.weight
        ) * self.duration * self.MIN


class Swimming(Training):
    """Тренировка: плавание."""
    type = 'Swimming'
    LEN_STEP = 1.38
    coeff_calorie_1 = 1.1
    coeff_calorie_2 = 2

    def __init__(
        self, action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() +
             self.coeff_calorie_1) *
            self.coeff_calorie_2 * self.weight
        )

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool /
            self.M_IN_KM / self.duration
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    return dic[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


dic = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)