from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logInUrl = "https://www.totaljobs.com/account/signin?ReturnUrl=/profile"


class TotalJobsLogin:
    def __init__(self, driver, email, password):
        self.driver = driver
        self.email = email
        self.password = password

    def accept_cookie(self):
        try:
            accept_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[text()='Accept All']"))
            )

            if accept_button:
                accept_button.click()
                logging.info("Cookies Accepted")

        except Exception as e:
            logging.exception("No Cookie Popup")

    def go_to_url(self, url):
        self.driver.get(url)

    def input_email(self):
        try:
            _login_email = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="Form_Email"]'))
            )

            _login_email.click()
            _login_email.send_keys(self.email)
            logging.info("Email Entered")

        except Exception as e:
            logging.exception(f"Error while inputting email address => {e}")

    def input_pass(self):
        try:
            _login_pass = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//input[@id="Form_Password"]')
                )
            )

            _login_pass.click()
            _login_pass.send_keys(self.password)
            logging.info("Password Entered")

        except Exception as e:
            logging.exception(f"Error occurred while inputting password => {e}")

    def submit_login(self):
        try:
            _submit_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="btnLogin"]'))
            )

            _submit_button.click()
            logging.info("Login Successful")

        except Exception as e:
            logging.exception(f"Error while submitting login => {e}")

    def login(self):
        self.go_to_url(logInUrl)
        self.accept_cookie()

        self.input_email()
        self.input_pass()

        self.submit_login()


# Example usage:
# total_jobs_login = TotalJobsLogin(driver, 'your_email', 'your_password')
# total_jobs_login.login()
