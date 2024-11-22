import sys
from robot import Robot, Callback

def main():
    """
    Основная функция для запуска робота с параметрами, переданными через аргументы командной строки.
    """
    try:
        # Убедимся, что переданы нужные аргументы
        if len(sys.argv) < 4:
            print("[!] Usage: python script.py <max_power> <k>")
            return

        # Создаем объект робота
        print("[+] Initializing robot...")
        robot = Robot('/dev/ttyUSB0')  # Измените на '/dev/tty.usbmodem14201' для MacBook

        # Настройка моторов (порты, максимальная мощность, коэффициент K)
        max_power = float(sys.argv[2])
        k = float(sys.argv[3])
        robot.setup_motors((3, 7, 5), (2, 4, 6), max_power=max_power, k=k)
        print(f"[+] Motors configured: max_power={max_power}, k={k}")

        # Настройка камеры
        robot.setup_camera(0)
        print("[+] Camera configured.")

        # Настройка обратного вызова и запуск трекинга линии
        callback = Callback(robot)
        print("[+] Starting line tracking...")
        robot.camera.track(callback.follow_line)

    except KeyboardInterrupt:
        print("\n[!] Program interrupted by user.")

    except Exception as e:
        print(f"[!] An error occurred: {e}")

    finally:
        # Останавливаем робота и освобождаем ресурсы
        print("[+] Robot stopped. Exiting program.")

if __name__ == "__main__":
    main()
