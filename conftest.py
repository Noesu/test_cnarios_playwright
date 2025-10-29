import logging
import os
import shutil

from utils.allure import start_allure_server, open_current_report

logger = logging.getLogger(__name__)

def pytest_sessionstart(session):
    """Выполняется перед началом тестовой сессии"""
    session.allure_dir = session.config.getoption("--alluredir")
    if os.path.exists(session.allure_dir):
        logger.info(f"Удаляются результаты предыдущих тестов в папке {session.allure_dir}")
        shutil.rmtree(session.allure_dir)

    logger.info(f"Создается новая папка {session.allure_dir}...")
    os.makedirs(session.allure_dir, exist_ok=True)


def pytest_sessionfinish(session):
    """Вызывается ПОСЛЕ завершения всех тестов, ПЕРЕД выходом"""
    allure_dir = session.allure_dir
    if not os.path.exists(allure_dir):
        logger.warning("Папка с результатами не найдена")
        return

    if not os.listdir(allure_dir):
        logger.warning("Нет результатов тестов для отчета")
        return

    report_url = start_allure_server(allure_dir)
    open_current_report(report_url)