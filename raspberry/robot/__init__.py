from math import atan2, degrees
from typing import Tuple

import pyfirmata

# Импорт оборудования и программного обеспечения
from .hardware import Motor, Chassis
from .software import Camera


class Robot:
    """
    Класс для управления роботом, включая моторы и камеру.
    """

    def __init__(self, serial: str = '/dev/ttyUSB0', camera_offset_x: float = 0.0):
        """
        Инициализация робота.

        :param serial: Порт для подключения платы Arduino.
        :param camera_offset_x: Смещение камеры от центра робота по оси X (в мм или см).
        """
        self.camera = None  # Камера робота
        self.chassis = None  # Шасси робота
        self.right = None  # Правый мотор
        self.left = None  # Левый мотор
        self.board = pyfirmata.Arduino(serial)  # Плата Arduino
        self.camera_offset_x = camera_offset_x  # Смещение камеры по X
        print("[+] Communication Successfully started")

    def setup_motors(self, left: Tuple[int, int, int], right: Tuple[int, int, int], max_power: float = 0.5, k: float = 1.0):
        """
        Настройка моторов робота.

        :param left: Пины (inA, inB, PWM) для левого мотора.
        :param right: Пины (inA, inB, PWM) для правого мотора.
        :param max_power: Максимальная мощность моторов.
        :param k: Коэффициент чувствительности поворота.
        """
        self.left = Motor(self.board, *left)
        self.right = Motor(self.board, *right)
        self.chassis = Chassis(self.left, self.right, max_power, k)

    def setup_camera(self, camera_number: int = 0):
        """
        Настройка камеры робота.

        :param camera_number: Индекс камеры, подключённой к компьютеру.
        """
        self.camera = Camera(camera_number)

    def stop(self):
        """
        Останавливает робота, включая моторы и камеру.
        """
        self.chassis.set_power(0, 0)
        if self.camera:
            self.camera.stop()


class Callback:
    """
    Класс для обработки обратных вызовов, связанных с движением робота.
    """

    def __init__(self, robot: Robot):
        """
        Инициализация обработчика обратных вызовов.

        :param robot: Экземпляр робота.
        """
        self.robot = robot

    def calculate_angle(self, line_center: Tuple[int, int]) -> float:
        """
        Вычисляет угол отклонения линии с учётом смещения камеры.

        :param line_center: Координаты центра линии (x, y) относительно рабочей области камеры.
        :return: Угол в градусах.
        """
        # Вычисляем абсолютные координаты линии в кадре
        alc_x = int((self.robot.camera.width - self.robot.camera.work_width) / 2) + line_center[0]
        alc_y = self.robot.camera.work_pos + line_center[1]

        # Разница между центром робота (учитывая смещение камеры) и центром линии
        dx = self.robot.camera.width // 2 - alc_x + self.robot.camera_offset_x
        dy = self.robot.camera.height - alc_y

        # Угол между линией и центром робота
        angle = degrees(atan2(dx, dy))
        return angle

    def follow_line(self, *args):
        """
        Управляет движением робота, следуя линии.

        :param args: Аргументы, содержащие информацию о линии.
        """
        if not args or not args[0]:
            print("Линия не обнаружена.")
            return

        line_center = args[0][0]  # Получаем центр линии из аргументов
        print(f"Центр линии: {line_center}, Центр кадра: {self.robot.camera.work_width // 2}")

        # Вычисляем угол поворота
        angle = self.calculate_angle(line_center)
        print(f"Вычисленный угол (с учётом смещения камеры): {angle}")

        # Управляем шасси робота
        self.robot.chassis.direction(angle)
