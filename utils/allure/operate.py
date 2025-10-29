import logging
import re
import subprocess
import time
import webbrowser


logger = logging.getLogger(__name__)

def start_allure_server(allure_dir):
    """
    Запускает Allure serve и возвращает URL
    """
    try:
        logger.info("Запускается сервер Allure...")
        process = subprocess.Popen(
            ["allure", "serve", allure_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        time.sleep(3)

        url_match = ""
        while True:
            line = process.stdout.readline()
            if not line:
                break
            else:
                if line.startswith("Server started at"):
                    url_match = re.search(r'http://[0-9.:]+', line)
                    break


        if url_match:
            url = url_match.group()
            logger.info(f"Получен адрес сервера Allure: {url}")
            return url
        else:
            logger.error("Не удалось найти URL в выводе Allure")
            return None

    except Exception as e:
        logger.error(f"Ошибка запуска Allure: {e}")
        return None


def open_current_report(allure_url):
    """
    Открывает Allure отчет в браузере
    """
    try:
        logger.info("Открытие отчета Allure в браузере...")
        webbrowser.open(allure_url)
    except Exception as e:
        logger.error(f"❌ Ошибка открытия отчета: {e}")
