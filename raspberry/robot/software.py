import cv2
import os


class Camera:
    def __init__(self, video_source=0, save_video=True, output_dir="./output"):
        """
        Инициализация трекера линии.
        :param video_source: источник видео (номер камеры или путь к видеофайлу).
        :param save_video: сохранять ли видео в файл.
        :param output_dir: папка для сохранения изображений и видео.
        """
        self.cap = cv2.VideoCapture(video_source)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.blur = 13
        self.dt = 100  # Базовый порог (можно настроить автоматически)
        self.work_pos = int(self.height * 0.8)
        self.work_width = int(self.width * 0.6)
        self.work_height = 40
        self.output_dir = output_dir
        self.save_video = save_video

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        if self.save_video:
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter(
                f"{self.output_dir}/output.mp4",
                self.fourcc,
                20.0,
                (self.width, self.height)
            )
            self.mask_writer = cv2.VideoWriter(
                f"{self.output_dir}/mask.mp4",
                self.fourcc,
                20.0,
                (self.width, self.height)
            )

    def calculate_center(self, moments):
        """
        Вычисляет центр линии на основе моментов.
        :param moments: моменты изображения.
        :return: координаты центра линии (x, y) или None.
        """
        if moments['m00'] > 2000:  # Минимальная площадь линии
            x = int(moments["m10"] / moments["m00"])
            y = int(moments["m01"] / moments["m00"])
            return x, y
        return None

    def process_frame(self, frame):
        """
        Обрабатывает кадр, выделяя линию и её центр.
        :param frame: входное изображение.
        :return: обработанный кадр, маска, центр линии.
        """
        # Обрезаем рабочую область
        crop = frame[self.work_pos:self.work_pos + self.work_height,
                     (self.width - self.work_width) // 2:(self.width + self.work_width) // 2]

        # Преобразуем в серый и размываем
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (self.blur, self.blur), 0)

        # Адаптивный порог
        mask = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 15)
        mask = cv2.bitwise_not(mask)

        # Вычисляем моменты
        moments = cv2.moments(mask)
        center = self.calculate_center(moments)

        # Отображаем центр на оригинальном кадре
        if center:
            cx, cy = center
            # Преобразуем координаты в глобальные для всего кадра
            global_x = (self.width - self.work_width) // 2 + cx
            global_y = self.work_pos + cy
            cv2.circle(frame, (global_x, global_y), 5, (0, 255, 0), -1)
            cv2.putText(frame, f"Center: ({global_x}, {global_y})", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

        return frame, mask, center

    def track(self, callback=print):
        """
        Основной метод для запуска трекера.
        """

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("[!] Проблемы с чтением кадра.")
                break

            # Обрабатываем текущий кадр
            processed_frame, mask, center = self.process_frame(frame)

            callback(center)

            # Отображаем результат
            cv2.imshow("Original with Line Center", processed_frame)
            cv2.imshow("Mask", mask)

            # Сохраняем маску и оригинальный кадр
            # cv2.imwrite(f"{self.output_dir}/frame_{frame_count}.png", processed_frame)
            # cv2.imwrite(f"{self.output_dir}/mask_{frame_count}.png", mask)

            # Сохраняем видео, если включено
            if self.save_video:
                self.out.write(processed_frame)
                # self.mask_writer.write(mask)


            # Управление с клавиатуры
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):  # Выход
                break

        self.stop()

    def stop(self):
        """
        Освобождает ресурсы камеры и закрывает окна.
        """
        self.cap.release()
        if self.save_video:
            self.out.release()
        cv2.destroyAllWindows()
        print("[+] Трекер остановлен.")


if __name__ == "__main__":
    tracker = Camera(video_source=0, save_video=True, output_dir="./output")
    tracker.track()
