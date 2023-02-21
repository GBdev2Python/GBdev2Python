import re
from time import sleep
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from authapp.models import CustomUser
from applicantapp.models import Applicants
from employerapp.models import Employer


class TestCaseIndexPage(StaticLiveServerTestCase):
    fixtures = (
        'newsapp/fixtures/001_news.json',
        'employerapp/fixtures/001_customuser.json',
        'employerapp/fixtures/002_skill.json',
        'employerapp/fixtures/003_towns.json',
        'employerapp/fixtures/004_type_employment.json',
        'employerapp/fixtures/005_employer.json',
        'employerapp/fixtures/006_vacancy_header.json',
    )

    def setUp(self) -> None:
        super().setUp()
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.selectors = {
            'partners_cards': '#partners-block .card-body',
            'news_cards': '#news-block .card',
            'news_link': "a[href='/news/']",
            'register_body': '.row .boxed-btn3',
            'register_button_text': 'Создать Резюме',
            'dropdown': '.dropdown',
        }
        self.applicant_data = {
            'username': 'turbo_test_user',
            'email': 'turbo_tester@mail.ru',
            'password': 'hello_world_1',
        }

    def tearDown(self) -> None:
        self.driver.close()
        super().tearDown()

    def test_index_page_correct_fullfilment(self):

        self.driver.get(self.live_server_url)
        re_index_pattern = re.compile(r'(http://localhost:[\d]*/hhapp/)|(http://127.0.0.1:[\d]*/hhapp/)')
        self.assertTrue(re_index_pattern.search(self.driver.current_url))

        partners = self.driver.find_elements(by=By.CSS_SELECTOR, value=self.selectors['partners_cards'])
        self.assertEqual(len(partners), 3, msg=f'expected 3 partners items, got {len(partners)} instead')

        news = self.driver.find_elements(by=By.CSS_SELECTOR, value=self.selectors['news_cards'])
        self.assertEqual(len(news), 5, msg=f'expected 5 news items, got {len(news)} instead')

        news_page_link = self.driver.find_elements(by=By.CSS_SELECTOR, value=self.selectors['news_link'])
        self.assertEqual(len(news_page_link), 1, f'news link not found')

    def test_register_and_login_applicant(self):
        self.driver.get(self.live_server_url)

        custom_users_amount = CustomUser.objects.count()
        self.assertEqual(custom_users_amount, 5)

        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, self.selectors['register_body']))
        )
        register_button = self.driver.find_element(by=By.CSS_SELECTOR, value=self.selectors['register_body'])
        self.assertEqual(register_button.text, self.selectors['register_button_text'])
        register_button.click()

        username_field = self.driver.find_element(by=By.CSS_SELECTOR, value="input[name='username']")
        email_field = self.driver.find_element(by=By.CSS_SELECTOR, value="input[name='email']")
        password1_field = self.driver.find_element(by=By.CSS_SELECTOR, value="input[name='password1']")
        password2_field = self.driver.find_element(by=By.CSS_SELECTOR, value="input[name='password2']")

        username_field.send_keys(self.applicant_data['username'])
        email_field.send_keys(self.applicant_data['email'])
        password1_field.send_keys(self.applicant_data['password'])
        password2_field.send_keys(self.applicant_data['password'])

        register_button = self.driver.find_element(by=By.CSS_SELECTOR, value='.container-md .row .btn')
        register_button.click()

        self.assertEqual(CustomUser.objects.count(), 6)
        applicant_as_user = CustomUser.objects.last()
        self.assertEqual(applicant_as_user.username, self.applicant_data['username'])
        self.assertEqual(applicant_as_user.email, self.applicant_data['email'])

        print(self.driver.current_url)
        self.driver.find_element(by=By.CSS_SELECTOR, value='.dropdown').click()
        self.driver.find_element(by=By.CSS_SELECTOR, value='.dropdown .dropdown-item.text-danger').click()

        login_button = self.driver.find_element(by=By.CSS_SELECTOR, value='.navbar .boxed-btn3')
        self.assertEqual(login_button.text, 'Login')
        login_button.click()

        print(self.driver.current_url)
        username = self.driver.find_element(by=By.CSS_SELECTOR, value='form input[name="username"]')
        password = self.driver.find_element(by=By.CSS_SELECTOR, value='form input[name="password"]')
        entry_button = self.driver.find_element(by=By.CSS_SELECTOR, value='form .btn-primary')

        username.send_keys(self.applicant_data['username'])
        password.send_keys(self.applicant_data['password'])
        entry_button.click()

        print(self.driver.current_url)

    def test_register_employer(self):
        self.driver.get(self.live_server_url)

        custom_users_amount = CustomUser.objects.count()
        print(custom_users_amount)
