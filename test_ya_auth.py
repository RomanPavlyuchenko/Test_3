from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from pytest import fixture
import json


class TestYaAuth:

    @fixture()
    def login_data(self):
        '''
        В файле login_data.json находятся корректные данные для входа в аккаунт
        '''
        with open('login_data.json') as login_data:
            data = json.load(login_data)
        return data

    @fixture
    def driver(self):
        driver = webdriver.Chrome()
        driver.get("https://passport.yandex.ru/auth/")
        yield driver
        driver.close()

    @fixture()
    def wait(self, driver):
        return WebDriverWait(driver, 5)

    def test_auth_is_opening(self, driver):
        title = driver.find_element_by_class_name('passp-title').text
        assert 'Войдите с Яндекс ID' in title

    def test_auth_positive(self, driver, login_data, wait):
        form_field = driver.find_element_by_name('login')
        form_field.send_keys(login_data['email'])
        form_field.send_keys(Keys.ENTER)

        text = 'Войдите, чтобы продолжить'
        try:
            elem = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'h1'), text))
        finally:
            assert elem

        form_field = driver.find_element_by_name('passwd')
        form_field.send_keys(login_data['password'])
        form_field.send_keys(Keys.ENTER)

        text = 'Яндекс ID'
        try:
            elem = wait.until(EC.title_is(text))
        finally:
            assert elem

    def test_auth_empty_email(self, driver, wait):
        form_field = driver.find_element_by_name('login')
        form_field.send_keys(Keys.ENTER)

        text = 'Логин не указан'
        try:
            elem = wait.until(EC.text_to_be_present_in_element((By.ID, 'field:input-login:hint'), text))
        finally:
            assert elem

    def test_auth_empty_password(self, driver, login_data, wait):
        form_field = driver.find_element_by_name('login')
        form_field.send_keys(login_data['email'])
        form_field.send_keys(Keys.ENTER)

        text = 'Войдите, чтобы продолжить'
        try:
            elem = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'h1'), text))
        except TimeoutException:
            assert False

        form_field = driver.find_element_by_name('passwd')
        form_field.send_keys(Keys.ENTER)
        text = 'Пароль не указан'
        try:
            elem = wait.until(EC.text_to_be_present_in_element((By.ID, 'field:input-passwd:hint'), text))
        finally:
            assert elem

    def test_auth_incorrect_password(self, driver, login_data, wait):
        form_field = driver.find_element_by_name('login')
        form_field.send_keys(login_data['email'])
        form_field.send_keys(Keys.ENTER)

        text = 'Войдите, чтобы продолжить'
        try:
            elem = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'h1'), text))
        except TimeoutException:
            assert False

        form_field = driver.find_element_by_name('passwd')
        form_field.send_keys(login_data['password'][:-2])
        form_field.send_keys(Keys.ENTER)

        text = 'Неверный пароль'
        try:
            elem = wait.until(EC.text_to_be_present_in_element((By.ID, 'field:input-passwd:hint'), text))
        finally:
            assert elem
