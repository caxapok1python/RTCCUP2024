import cv2
from typing import List, Optional


# Список значений порога для бинаризации
dts = [10, 20, 30, 40, 50]


def apply_dt(dt: int, img: cv2.Mat) -> cv2.Mat:
    """
    Применяет пороговую бинаризацию к изображению.

    :param dt: Значение порога для бинаризации.
    :param img: Входное изображение в формате BGR.
    :return: Бинаризованное изображение.
    """
    # Преобразование изображения в оттенки серого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Применение размытия для снижения шумов
    gray = cv2.GaussianBlur(gray, (13, 13), 0)
    # Применение бинаризации с инверсией
    _, thrsh1 = cv2.threshold(gray, dt, 255, cv2.THRESH_BINARY_INV)
    return thrsh1


def autoconf_dt(img: cv2.Mat) -> int:
    """
    Автоматически определяет подходящее значение порога для бинаризации.

    :param img: Входное изображение в формате BGR.
    :return: Оптимальное значение порога.
    """
    dt = []  # Список подходящих значений порога
    height, width, _ = img.shape  # Размеры изображения

    # Координаты и размеры области анализа
    work_pos = 400
    work_width = 245
    work_height = 20

    # Размер размытия
    blur = 13

    # Обрезка области анализа
    crop = img[work_pos:work_pos + work_height,
               (width - work_width) // 2: (width + work_width) // 2]

    # Преобразование обрезанной области в оттенки серого и размытие
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (blur, blur), 0)

    # Поиск подходящего значения порога
    for i in range(0, 256):
        _, thrsh1 = cv2.threshold(gray, i, 255, cv2.THRESH_BINARY_INV)
        m = cv2.moments(thrsh1)["m00"]  # Площадь белых пикселей

        # Проверка, соответствует ли площадь заданному диапазону
        if 255 * work_height * 30 < m < 255 * work_height * 60:
            dt.append(i)

    # Возвращение медианного значения, если список не пуст
    if dt:
        return dt[len(dt) // 2]

    # Возвращение значения по умолчанию, если список пуст
    return 115


def main() -> None:
    """
    Основная функция для работы с камерой и бинаризацией изображений.
    """
    # Открытие видеопотока с камеры
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру.")
        return

    print("Запущено. Нажмите 'q', чтобы выйти.")
    try:
        while True:
            # Считываем кадр с камеры
            ret, image = cap.read()
            if not ret:
                print("Ошибка: не удалось получить кадр с камеры.")
                break

            # Определение области анализа
            height, width, _ = image.shape
            work_pos = 400
            work_width = 245
            work_height = 20
            blur = 13
            crop = image[work_pos:work_pos + work_height,
                         (width - work_width) // 2: (width + work_width) // 2]
            crop = cv2.GaussianBlur(crop, (blur, blur), 0)

            # Сохранение текущего кадра
            cv2.imwrite("../tmp/colored.png", image)
            print("Размер области анализа:", crop.shape)

            # Применение различных значений порога
            for i in dts:
                th = apply_dt(i, crop)
                cv2.imwrite(f"../tmp/{i}.png", th)

            # Автоматическое определение порога
            dt = autoconf_dt(image)
            th = apply_dt(dt, crop)

            # Отображение изображения с автоматически настроенным порогом
            cv2.imshow("Автоматическая бинаризация", th)
            cv2.imwrite(f"../tmp/autoconf_{dt}.png", th)

            # Выход по нажатию клавиши 'q'
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        # Освобождение ресурсов
        cap.release()
        cv2.destroyAllWindows()
        print("Видеопоток завершён.")


if __name__ == "__main__":
    main()
