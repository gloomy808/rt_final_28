import pickle
import time
import pytest
from pages.auth import *
from selenium.webdriver.common.by import By
from pages.settings import valid_phone, valid_login, valid_password, \
    invalid_ls, valid_email, valid_pass_reg, fake_email

@pytest.mark.reg
@pytest.mark.positive

def test_menu_type_autoriz(browser):
    """Проверка названия табов в меню выбора типа авторизации."""
    try:
        page = AuthPage(browser)
        menu = [page.tub_phone.text, page.tub_email.text, page.tub_login.text, page.tub_ls.text]
        for i in range(len(menu)):
            assert "Номер" in menu
            assert 'Почта' in menu
            assert 'Логин' in menu
            assert 'Лицевой счёт' in menu
    except AssertionError:
        print('Ошибка в имени таба Меню типа аутентификации')




@pytest.mark.positive
@pytest.mark.xfail
@pytest.mark.parametrize('username', [valid_phone, valid_email, valid_login, invalid_ls],
                         ids=['phone', 'email', 'login', 'ls'])
def test_active_tab(browser, username):
    """Тест смены полей ввода при смене типа авторизации."""
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_password)
    if username == valid_phone:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Телефон'
    elif username == valid_email:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Почта'
    elif username == valid_login:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Логин'
    else:
        assert browser.find_element(*AuthLocators.AUTH_ACTIVE_TAB).text == 'Лицевой счет'



@pytest.mark.reg
@pytest.mark.positive
def test_reg_page_open(browser):
    """ Проверка страницы регистрации  """
    page = AuthPage(browser)
    page.enter_reg_page()

    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'


@pytest.mark.auth
@pytest.mark.positive
@pytest.mark.parametrize('username', [valid_phone, valid_login],
                         ids=['valid phone', 'valid login'])
def test_auth_page_phone_login_valid(browser, username):
    """Проверка авторизации по номеру телефона/логину и паролю + проверка
    автоматического переключения табов тел/логин"""
    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_password)
    page.btn_click_enter()

    assert page.get_relative_link() == '/account_b2c/page'


@pytest.mark.auth
@pytest.mark.positive
def test_auth_page_email_valid(browser):
    """Проверка авторизации по почте и паролю"""
    page = AuthPage(browser)
    page.enter_username(valid_email)
    page.enter_password(valid_pass_reg)
    # time.sleep(20)     # на случай появления Captcha, необходимости ее ввода вручную
    page.btn_click_enter()
    page.driver.save_screenshot('auth_by_email.png')


    assert page.get_relative_link() == '/account_b2c/page'

@pytest.mark.auth
@pytest.mark.positive
def test_VK_btn(browser):
    """Проверка авторизации по кнопки VK"""
    page = OtherPage(browser)
    page.vk_click()

    assert page.get_relative_link() == '/authorize'

@pytest.mark.auth
@pytest.mark.positive
def test_google_btn(browser):
    """Проверка авторизации по кнопки googl"""
    page = OtherPage(browser)
    page.gogl_click()

    assert page.get_relative_link() == '/o/oauth2/auth/identifier'

@pytest.mark.auth
@pytest.mark.positive
def test_mail_btn(browser):
    """Проверка авторизации по кнопки mail"""
    page = OtherPage(browser)
    page.mail_click()

    assert page.get_relative_link() == '/oauth/authorize'

@pytest.mark.auth
@pytest.mark.positive
def test_ok_btn(browser):
    """Проверка авторизации по кнопки ok"""
    page = OtherPage(browser)
    page.ok_click()

    assert page.get_relative_link() == '/dk'


@pytest.mark.auth
@pytest.mark.positive
def test_ya_btn(browser):
    """Проверка авторизации по кнопки яндекс"""
    page = OtherPage(browser)
    page.ya_click()

    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/authenticate'

@pytest.mark.auth
@pytest.mark.positive
def test_vost_pass(browser):
    """проверка кнопки востоновления пороля"""
    page = OtherPage(browser)
    page.vos_pass()

    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/reset-credentials'