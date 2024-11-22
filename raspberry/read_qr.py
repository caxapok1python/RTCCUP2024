import cv2
import pyzbar.pyzbar as zbar
from typing import Optional


def find_qr_code(camera_index: int = 0) -> Optional[str]:
    """
    Ищет QR-код с камеры и возвращает его содержимое.

    :param camera_index: Индекс камеры для захвата видео (по умолчанию 0).
    :return: Строка с данными из QR-кода или None, если QR-код не найден.
    """
    # Открытие видеопотока с указанной камеры
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Ошибка: Не удалось открыть камеру.")
        return None

    print("Видеопоток запущен. Поиск QR-кода...")

    try:
        while True:
            # Считываем кадр с камеры
            ret, img = cap.read()
            if not ret:
                print("Ошибка: Не удалось получить кадр с камеры.")
                break

            # Декодируем QR-коды в кадре
            decoded_objects = zbar.decode(img)

            # Если QR-коды найдены
            if decoded_objects:
                data = decoded_objects[0].data.decode()  # Извлекаем данные из первого QR-кода
                print("QR-код найден:", f"'{data}'")
                return data
    finally:
        # Освобождаем ресурс камеры
        cap.release()
        print("Видеопоток завершён.")

    return None


if __name__ == "__main__":
    qr_data = find_qr_code()
    if qr_data:
        print("Содержимое QR-кода:", qr_data)
    else:
        print("QR-код не найден.")
