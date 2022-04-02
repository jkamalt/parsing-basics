from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

from base.base_parser import BaseParser
from config.login_config import LOGIN, PASSWORD


class MailRuParser(BaseParser):
    """ Парсер почты mail.ru """

    def __init__(self):
        super().__init__()
        self._driver = webdriver.Chrome(executable_path='chromedriver.exe')
        self._wait = WebDriverWait(self._driver, 10)

    @property
    def url_to_parse(self):
        return 'https://account.mail.ru/login'

    @property
    def db_name(self):
        return 'letters_db'

    @property
    def collection_name(self):
        return 'letters'

    def _get_items(self):
        """
        Возвращает список адресов, соответствующих письмам.
        :return: список адресов
        """
        self._driver.get(self.url_to_parse)

        # Выключение чекбокса Запомнить
        checkbox = self._get_clickable_element(By.CLASS_NAME, 'save-auth-field-wrap')
        checkbox.click()

        login = self._driver.find_element(By.XPATH, '//input[@name="username"]')
        login.send_keys(LOGIN)

        # Кнопка Ввести пароль
        button = self._driver.find_element(By.XPATH, '//button[@data-test-id="next-button"]')
        button.click()

        password = self._get_visible_element(By.XPATH, '//input[@name="password"]')
        password.send_keys(PASSWORD)

        # Кнопка Войти
        button = self._driver.find_element(By.XPATH, '//button[@data-test-id="submit-button"]')
        button.click()

        # Ожидание загрузки списка писем
        first_letter = self._get_visible_element(By.XPATH, '//a[contains(@class, "js-letter-list-item")]')

        urls = set()
        last_url = ''
        while True:
            letters = self._driver.find_elements(By.XPATH, '//a[contains(@class, "js-letter-list-item")]')
            curr_last_url = letters[-1].get_attribute('href')

            # Если последний url-адрес на текущей странице совпадает с предыдущим, то выход из цикла
            if last_url == curr_last_url:
                break
            last_url = curr_last_url

            urls_subset = set([letter.get_attribute('href') for letter in letters])
            urls.update(urls_subset)

            actions = ActionChains(self._driver)
            actions.move_to_element(letters[-1])
            actions.perform()

            time.sleep(3)

        return list(urls)

    def _parse_items(self, urls):
        """
        Парсит письма по заданному списку адресов.
        :param urls: список адресов, соответствующие письмам
        """
        for url in urls:
            try:
                self._parse_item(url)
                time.sleep(2)
            except Exception as e:
                print(f'При парсинге письма по адресу {url} произошла ошибка: {e}')

    def _parse_item(self, item_url=None):
        """
        Парсит письмо по заданному адресу.
        :param item_url: адрес письма
        """
        self._driver.get(item_url)

        elem = self._get_visible_element(By.CLASS_NAME, 'letter-contact')
        from_name = elem.text
        from_mail = elem.get_attribute('title')

        elem = self._driver.find_element(By.CLASS_NAME, 'letter__date')
        date = elem.text

        elem = self._driver.find_element(By.CLASS_NAME, 'thread-subject')
        subject = elem.text

        elem = self._driver.find_element(By.CLASS_NAME, 'letter-body')
        p_tags = elem.find_elements(By.TAG_NAME, 'p')
        body = ' '.join([p.text for p in p_tags])

        letter = {
            'from_name': from_name,
            'from_mail': from_mail,
            'date': date,
            'subject': subject,
            'body': body,
        }
        self._result.append(letter)

    def parse(self):
        try:
            urls = self._get_items()
            self._parse_items(urls)
        except Exception as e:
            print(f'При парсинге писем произошла ошибка: {e}')
        finally:
            self._driver.quit()
            self.write_result_to_json('letters.json', ensure_ascii=False)

    def _get_clickable_element(self, by: By, value: str):
        """
        Возвращает элемент, когда он становится кликабельным.
        :param by: локатор
        :param value: значение для поиска
        :return: элемент страницы
        :rtype: WebElement
        """
        return self._wait.until(EC.element_to_be_clickable((by, value)))

    def _get_visible_element(self, by: By, value: str):
        """
        Возвращает элемент, когда он становится видимым.
        :param by: локатор
        :param value: значение для поиска
        :return: элемент страницы
        :rtype: WebElement
        """
        return self._wait.until(EC.visibility_of_element_located((by, value)))
