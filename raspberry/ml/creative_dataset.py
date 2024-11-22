import cv2
import os
import sys
import logging
from typing import Dict

# Настройка логирования
log_file = "dataset_creation.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

# Словарь для управления клавишами
keys: Dict[str, int] = {
    "shot": ord("s"),  # Клавиша для создания снимка
    "next": ord("n"),  # Клавиша для перехода к следующему классу
    "quit": ord("q")   # Клавиша для выхода из программы
}

# Классы дорожных знаков
classes: Dict[str, int] = {"left": 100, "right": 100, "stop": 100, "nothing": 70}

# Классы знаков опасности
# classes: Dict[str, int] = {"explosive": 35, "blasting_agent": 35, "flammable_gas": 35, "non-flammable_gas": 35, "flammable_liquid": 35, "inhalation_hazard": 35,
#                            "flammable_solid": 35, "dangerous_wet": 35, "combustible": 35, "oxidizer": 35, "poison": 35, "infectious": 35, "radioactive": 35,
#                            "corrosive": 35, "nothong": 35}

# Директория для сохранения набора данных
dataset_dir: str = "traffic/dataset"
# dataset_dir: str = "danger-signes/dataset"

# Настройка камеры
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)



def ensure_dataset_dir(directory: str):
    """
    Проверяет, существует ли директория для набора данных, и создаёт её, если нет.

    :param directory: Путь к директории.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created dataset directory: {directory}")
    else:
        logging.info(f"Dataset directory already exists: {directory}")


def shot(name: str, cnt: int, image: cv2.Mat):
    """
    Делает снимок и сохраняет его в директорию.

    :param name: Название класса (например, "left").
    :param cnt: Текущий номер снимка.
    :param image: Кадр, полученный с камеры.
    """
    image_resized = cv2.resize(image, (720, 480))
    filepath = os.path.join(dataset_dir, f"{name}.{cnt}.png")
    cv2.imwrite(filepath, image_resized)
    logging.info(f"Captured image: {filepath} ({cnt + 1}/{classes[name]})")


def read_traffic_sign(name: str, num: int):
    """
    Читает изображения для определённого дорожного знака и сохраняет их.

    :param name: Название дорожного знака (например, "left").
    :param num: Количество снимков, которые нужно сделать.
    """
    cnt = 0
    logging.info(f"Starting capture for class: {name}")

    while cnt < num:
        ret, image = cam.read()
        if not ret:
            logging.warning("Camera frame not captured. Retrying...")
            continue

        # Изменение размера изображения для отображения
        image_resized = cv2.resize(image, (720, 480))
        cv2.imshow("Camera", image_resized)

        key = cv2.waitKey(1) & 0xFF

        if key == keys["quit"]:
            logging.info("Exiting...")
            cam.release()
            cv2.destroyAllWindows()
            sys.exit(0)
        elif key == keys["shot"]:
            shot(name, cnt, image)
            cnt += 1
        elif key == keys["next"]:
            logging.info(f"Moving to the next class from: {name}")
            return


def main():
    """
    Основная функция для сбора набора данных.
    """
    logging.info("Dataset creation process started.")
    ensure_dataset_dir(dataset_dir)

    for sign in classes:
        read_traffic_sign(sign, classes[sign])
        logging.info(f"Finished capturing for sign: {sign}")

    logging.info("Dataset creation complete.")
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        cam.release()
        cv2.destroyAllWindows()
        sys.exit(1)
