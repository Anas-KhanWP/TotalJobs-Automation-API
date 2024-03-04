from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class JobActions:
    def __init__(self, driver):
        self.driver = driver

    def to_job_url(self, url):
        self.driver.get(url)

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

    def apply_to_job(self, job):
        try:
            self.to_job_url(job)

            # Find the <a> element with text content "Send application" using XPath
            xpath_expression = "//a[normalize-space(text())='Send application']"
            send_application = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath_expression))
            )

            if send_application:
                # Click on the <a> element
                send_application.click()
                print("Application Sent Successfully")
                msg = 200
                return msg
            else:
                pass
        except Exception as e:
            msg = 201
            logging.exception(f"External Job Skipping")
            return msg
