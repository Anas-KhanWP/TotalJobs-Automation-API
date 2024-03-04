from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
from dependencies import config
from uploadresume import ResumeUploader
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
signUpUrl = "https://www.totaljobs.com/Account/Register?ReturnUrl=%2Fprofile"


class SignupBot:
    def __init__(self, driver, fname, lname, email, password, resumepath, job_title):
        self.resumepath = resumepath
        self.email = email
        self.password = password
        self.fname = fname
        self.lname = lname
        self.driver = driver
        self.job_title = job_title
        # self.salary = salary

    def accept_cookie(self):
        try:
            accept_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[text()='Accept All']"))
            )

            if accept_button:
                accept_button.click()
                logging.info("Cookies Accepted")

        except:
            logging.info("No Cookie popup")

    def submitSignUp(self):
        try:
            _submit_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[text()='Submit']"))
            )

            _submit_button.click()

        except:
            logging.info("No Submit button Found")

    def input_first_name(self):
        try:
            first_name = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="firstname"]'))
            )

            first_name.click()
            first_name.send_keys(self.fname)

        except Exception as e:
            logging.error(f"Error while inputting first name => {e}")

    def input_last_name(self):
        try:
            last_name = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="surname"]'))
            )

            last_name.click()
            last_name.send_keys(self.lname)

        except Exception as e:
            logging.exception(f"Error while inputting last name => {e}")

    def input_email(self):
        try:
            _email = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="email"]'))
            )

            _email.click()
            _email.send_keys(self.email)

        except Exception as e:
            logging.error(f"Error while inputting email address => {e}")

    def input_job_title(self):
        try:
            _job_title = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//input[@id="currentJobTitle"]')
                )
            )

            _job_title.click()
            _job_title.send_keys(self.job_title)
            _job_title.send_keys(Keys.ENTER)

        except Exception as e:
            logging.error(f"Error while inputting job title => {e}")

    def currentSalary(self):
        try:
            _salary_expectations = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//select[@id="ddlSalaryRange"]')
                )
            )

            # Creating a Select object
            dropdown = Select(_salary_expectations)

            # Selecting an option by value based on the input
            dropdown.select_by_value("5")

        except Exception as e:
            logging.error(
                f"Error occurred while inputting salary expectation => {e}"
            )

    def input_pass(self):
        try:
            _pass = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="password"]'))
            )

            _pass.click()
            _pass.send_keys(config.password)
        except Exception as e:
            logging.exception(f"Error occurred while inputting password => {e}")

    def input_pass_again(self):
        try:
            _pass_again = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//input[@id="confirmpassword"]')
                )
            )

            _pass_again.click()
            _pass_again.send_keys(config.password)
        except Exception as e:
            logging.exception(f"Error occurred while confirming password => {e}")

    def make_totalBot_signup(self):
        try:
            self.driver.get(signUpUrl)
            time.sleep(5)

            self.accept_cookie()

            self.input_first_name()
            logging.info(f"Entered first name: {self.fname}")
            self.input_last_name()
            logging.info(f"Entered last name: {self.lname}")
            self.input_email()
            logging.info(f"Entered email: {self.email}")
            # Initialize ResumeUploader with the driver
            resume_uploader = ResumeUploader(self.driver)
            resume_uploader.upload_resume(self.resumepath)
            logging.info(f"Resume Uploaded")
            self.input_job_title()
            logging.info(f"Entered Job Title")
            self.currentSalary()
            logging.info(f"Salary Expectations Selected")
            self.input_pass()
            logging.info("Entered password")
            self.input_pass_again()
            logging.info("Re-entered password")
            self.submitSignUp()
            time.sleep(5)
            return self.email, self.password
        except Exception as e:
            logging.exception(f"Received error: {e}")
