import pyfirmata


class Motor:
    """
    Класс для управления двигателем через Arduino с использованием библиотеки pyfirmata.
    """

    def __init__(self, board: pyfirmata.Arduino, inA: int, inB: int, pwm: int):
        """
        Инициализация двигателя.

        :param board: Экземпляр pyfirmata.Arduino для управления пинами.
        :param inA: Номер цифрового пина для направления "вперёд".
        :param inB: Номер цифрового пина для направления "назад".
        :param pwm: Номер пина для управления скоростью через ШИМ.
        """
        self.inA: pyfirmata.Pin = board.digital[inA]  # Пин для направления "вперёд"
        self.inB: pyfirmata.Pin = board.digital[inB]  # Пин для направления "назад"
        self.pwm: pyfirmata.Pin = board.digital[pwm]  # Пин для ШИМ-сигнала
        self.pwm.mode = pyfirmata.PWM  # Установка пина в режим ШИМ

    def set_power(self, power: float) -> None:
        """
        Устанавливает мощность двигателя.

        :param power: Мощность двигателя в диапазоне от -1.0 до 1.0.
                      Положительное значение — вперёд, отрицательное — назад, 0 — стоп.
        """
        if power == 0:
            # Полная остановка двигателя
            self.inA.write(0)
            self.inB.write(0)
            self.pwm.write(0)
        elif power > 0:
            # Вращение вперёд
            power = abs(power)
            self.inA.write(1)  # Направление "вперёд"
            self.inB.write(0)  # Направление "назад" выключено
            self.pwm.write(power)  # Установка скорости через ШИМ
        else:
            # Вращение назад
            power = abs(power)
            self.inA.write(0)  # Направление "вперёд" выключено
            self.inB.write(1)  # Направление "назад"
            self.pwm.write(power)  # Установка скорости через ШИМ


class Chassis:
    """
    Класс для управления шасси робота с двумя моторами.
    """

    def __init__(self, left_side: Motor, right_side: Motor, max_power: float = 0.3, k: float = 1.5):
        """
        Инициализация шасси.

        :param left_side: Мотор, управляющий левой стороной.
        :param right_side: Мотор, управляющий правой стороной.
        :param max_power: Максимальная мощность, передаваемая на моторы (по умолчанию 0.3).
        :param k: Коэффициент коррекции мощности при поворотах.
        """
        self.left: Motor = left_side
        self.right: Motor = right_side
        self.k: float = k
        self.statpower: float = max_power

    def direction(self, angle: float) -> None:
        """
        Устанавливает направление движения шасси.

        :param angle: Угол поворота в диапазоне от -90 до 90.
                      Отрицательные значения — поворот влево, положительные — вправо.
        """
        sp = self.statpower  # Максимальная мощность

        # Расчёт мощности для левого и правого мотора в зависимости от угла
        if angle < 0:
            lpower = sp - (sp * abs(angle) / 90 * self.k)  # Уменьшаем мощность левого мотора
            if lpower < 0:
                lpower = 0  # Минимальная мощность — 0
            rpower = sp  # Правая сторона работает на максимальной мощности
        else:
            rpower = sp - (sp * abs(angle) / 90 * self.k)  # Уменьшаем мощность правого мотора
            if rpower < 0:
                rpower = 0  # Минимальная мощность — 0
            lpower = sp  # Левая сторона работает на максимальной мощности

        # Вывод рассчитанных мощностей в консоль (для отладки)
        print(lpower, rpower)

        # Передача рассчитанной мощности на моторы (отрицательная мощность — реверс)
        self.left.set_power(-1 * lpower)
        self.right.set_power(-1 * rpower)

    def set_power(self, lpower: float, rpower: float) -> None:
        """
        Устанавливает мощность напрямую для левого и правого мотора.

        :param lpower: Мощность для левого мотора в диапазоне от -1.0 до 1.0.
        :param rpower: Мощность для правого мотора в диапазоне от -1.0 до 1.0.
        """
        self.left.set_power(lpower)
        self.right.set_power(rpower)

    def stop(self) -> None:
        """
        Останавливает оба мотора.
        """
        self.left.set_power(0)
        self.right.set_power(0)

