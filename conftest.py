import pytest
from selenium import webdriver
import time
from datetime import datetime
import pytest
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



@pytest.fixture(autouse=True)
def browser():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(executable_path="./chromedriver.exe")
    driver.set_window_size(1920, 1080)
    driver.maximize_window()
    driver.implicitly_wait(5)


    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # выполните все остальные перехватчики, чтобы получить объект отчета
    outcome = yield
    rep = outcome.get_result()

    # установите атрибут отчета для каждой фазы вызова, который может
    # вызвана "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


# проверьте, не провалился ли тест
@pytest.fixture(scope="function", autouse=True)
def test_failed_check(request):
    yield
    # request.node является "item", потому что мы используем значение по умолчанию
    # "function" scope
    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            driver = request.node.funcargs['browser']
            take_screenshot(driver, request.node.nodeid)
            print("executing test failed", request.node.nodeid)


# сделайте скриншот с названием теста, датой и временем
def take_screenshot(driver, nodeid):
    time.sleep(1)
    file_name = f'{nodeid}_{datetime.today().strftime("%Y-%m-%d_%H:%M")}.png'.replace("/", "_").replace("::", "__")
    driver.save_screenshot(file_name)