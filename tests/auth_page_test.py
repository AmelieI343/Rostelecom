import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import string
import credentials

@pytest.fixture(autouse=True, scope="session")
def testing():
    pytest.driver = webdriver.Chrome('./chromedriver.exe')
    driver = pytest.driver
    #Go to login page
    driver.get('https://b2c.passport.rt.ru')

    yield

    pytest.driver.quit()

def test_login_by_phone_invalid():
    '''Проверяем поведение системы при вводе неправильного телефона'''
    driver = pytest.driver
    driver.implicitly_wait(10)

    driver.find_element(By.ID, 'username').send_keys(credentials.incorrect_phone)
    driver.find_element(By.ID, 'password').send_keys(credentials.correct_password)
    driver.find_element(By.ID, 'kc-login').click()

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'
    assert driver.find_element(By.ID, 'forgot_password').value_of_css_property('color') == "rgba(255, 79, 18, 1)"

def test_login_by_email_invalid():
    '''Проверяем поведение системы при вводе неправильного e-mail'''
    driver = pytest.driver
    driver.implicitly_wait(10)

    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.ID, 'username').send_keys(credentials.incorrect_email)
    driver.find_element(By.ID, 'password').send_keys(credentials.correct_password)
    driver.find_element(By.ID, 'kc-login').click()

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'
    assert driver.find_element(By.ID, 'forgot_password').value_of_css_property('color') == "rgba(255, 79, 18, 1)"

def test_login_by_login_invalid():
    '''Проверяем поведение системы при вводе неправильного логина'''
    driver = pytest.driver
    driver.implicitly_wait(10)

    driver.find_element(By.ID, 't-btn-tab-login').click()
    driver.find_element(By.ID, 'username').send_keys(credentials.incorrect_login)
    driver.find_element(By.ID, 'password').send_keys(credentials.correct_password)
    driver.find_element(By.ID, 'kc-login').click()

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'
    assert driver.find_element(By.ID, 'forgot_password').value_of_css_property('color') == "rgba(255, 79, 18, 1)"

def test_login_by_account_invalid():
    '''Проверяем поведение системы при вводе неправильного лицевого счёта'''
    driver = pytest.driver
    driver.implicitly_wait(10)

    driver.find_element(By.ID, 't-btn-tab-ls').click()
    driver.find_element(By.ID, 'username').send_keys(credentials.incorrect_account)
    driver.find_element(By.ID, 'password').send_keys(credentials.correct_password)
    driver.find_element(By.ID, 'kc-login').click()

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'
    assert driver.find_element(By.ID, 'forgot_password').value_of_css_property('color') == "rgba(255, 79, 18, 1)"

@pytest.mark.parametrize("password", ["1", "@", "рус"])
def test_login_by_phone_password_invalid(password):
    '''Проверяем поведение системы при некорректном пароле'''
    driver = pytest.driver
    driver.implicitly_wait(10)

    driver.find_element(By.ID, 't-btn-tab-phone').click()
    driver.find_element(By.ID, 'username').send_keys(credentials.correct_phone)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'kc-login').click()

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

def test_login_by_phone_long():
    '''Проверяем поведение системы при длинном пароле'''
    driver = pytest.driver
    driver.implicitly_wait(10)

    driver.find_element(By.ID, 't-btn-tab-phone').click()
    driver.find_element(By.ID, 'username').send_keys(credentials.correct_phone)
    driver.find_element(By.ID, 'password').send_keys(''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(256)))
    driver.find_element(By.ID, 'kc-login').click()

    assert driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

def test_login_by_email_valid():
    '''Проверяем поведение системы при вводе неправильного e-mail'''
    driver = pytest.driver
    driver.implicitly_wait(10)

    driver.find_element(By.ID, 't-btn-tab-mail').click()
    driver.find_element(By.ID, 'username').send_keys(credentials.correct_email)
    driver.find_element(By.ID, 'password').send_keys(credentials.correct_password)
    driver.find_element(By.ID, 'kc-login').click()
    try:
        assert driver.find_element(By.ID, 'user_contacts_edit')
    except Exception:
        assert False
    else:
        driver.find_element(By.ID, 'logout-btn').click()

def test_login_by_phone_valid():
    '''Проверяем поведение системы при вводе правильного телефона'''
    driver = pytest.driver
    driver.implicitly_wait(10)

    driver.find_element(By.ID, 't-btn-tab-phone').click()
    driver.find_element(By.ID, 'username').send_keys(credentials.correct_phone)
    driver.find_element(By.ID, 'password').send_keys(credentials.correct_phone)
    driver.find_element(By.ID, 'kc-login').click()

    try:
        assert driver.find_element(By.ID, 'user_contacts_edit')
    except Exception:
        assert False
    else:
        driver.find_element(By.ID, 'logout-btn').click()

def test_login_by_login_valid():
    '''Проверяем поведение системы при вводе правильного логина'''
    driver = pytest.driver
    driver.implicitly_wait(10)

    driver.find_element(By.ID, 't-btn-tab-login').click()
    driver.find_element(By.ID, 'username').send_keys(credentials.correct_login)
    driver.find_element(By.ID, 'password').send_keys(credentials.correct_password)
    driver.find_element(By.ID, 'kc-login').click()

    try:
        assert driver.find_element(By.ID, 'user_contacts_edit')
    except Exception:
        assert False
    else:
        driver.find_element(By.ID, 'logout-btn').click()

def test_login_by_account_valid():
    '''Проверяем поведение системы при вводе правильного счета'''
    driver = pytest.driver
    driver.implicitly_wait(10)

    driver.find_element(By.ID, 't-btn-tab-ls').click()
    driver.find_element(By.ID, 'username').send_keys(credentials.correct_account)
    driver.find_element(By.ID, 'password').send_keys(credentials.correct_password)
    driver.find_element(By.ID, 'kc-login').click()

    try:
        assert driver.find_element(By.ID, 'user_contacts_edit')
    except Exception:
        assert False
    else:
        driver.find_element(By.ID, 'logout-btn').click()