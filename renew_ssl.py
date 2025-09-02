import subprocess
import time
import os
import logging


RENEW_INTERVAL_DAYS = 90  # 3 месяца

def init_logger(name: str, log_mod: str = 'a'):
    name = name.split('.')[-1]
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Настройка обработчика и форматировщика для записи в файл
    file_handler = logging.FileHandler(f"logs/{name}.log", mode=log_mod, encoding='utf-8')
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Настройка обработчика для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


logger = init_logger(__name__)
def renew_certificate():
    while True:
        try:
            # Выполняем команду Certbot для перевыпуска сертификата
            logger.info(f"Запуск процесса обновления сертификата")
            subprocess.run(["certbot", "renew", "--quiet"], check=True)
            logger.info(f"Сертификат перевыпущен")
        except subprocess.CalledProcessError as e:
            logger.error(f"Ошибка при перевыпуске: {e}")
        
        # Ждем 3 месяца
        time.sleep(RENEW_INTERVAL_DAYS * 24 * 60 * 60)

if __name__ == "__main__":
    renew_certificate()
