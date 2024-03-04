import os, time
from pynput.keyboard import Key, Controller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import TotalJobsLogin
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class ResumeUploader:
    """
    This class is used to upload a resume to the TotalJobs website.

    Args:
        driver (webdriver): The WebDriver instance used to interact with the website.

    Attributes:
        driver (webdriver): The WebDriver instance used to interact with the website.

    """

    def __init__(self, driver):
        self.driver = driver

    def uploadToServer(self, resume):
        """
        This function is used to store the uploaded file in the "resumes" directory.

        Args:
            resume (werkzeug.datastructures.FileStorage): The uploaded resume file.

        Returns:
            str: The path of the stored resume file.

        """
        # Store the uploaded file in the "/resumes" directory
        resume_directory = "resumes"
        os.makedirs(resume_directory, exist_ok=True)
        resume_filename = os.path.join(resume_directory, resume.filename.lower())

        with open(resume_filename, "wb") as resume_file:
            resume_file.write(resume.file.read())
            return resume_filename

    def upload_resume(self, resume_name):
        """
        This function is used to upload the resume to the TotalJobs website.

        Args:
            resume_name (str): The name of the resume file.

        Raises:
            Exception: If an error occurs while uploading the resume.

        """
        try:
            # Find and click the button to open the container
            btn_cv_upload = self.driver.find_element(By.ID, "btnCVUpload")
            btn_cv_upload.click()

            # Wait for the container to appear (adjust the timeout as needed)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "cvUploadOptions"))
            )

            current_file_directory = os.path.dirname(__file__)
            _resume_path = os.path.join(current_file_directory, resume_name)

            # Find and click the label inside the li element
            self.driver.find_element(
                By.ID,
                "localCv",
            ).send_keys(_resume_path)

            time.sleep(1.5)

            logging.info("Resume uploaded")

        except Exception as e:
            logging.exception(f"Error while uploading resume => {e}")

    def replaceResume(self, driver, email, password, resume):
        """
        This function is used to replace the resume on the TotalJobs website.

        Args:
            driver (webdriver): The WebDriver instance used to interact with the website.
            email (str): The email address used to login to TotalJobs.
            password (str): The password used to login to TotalJobs.
            resume (werkzeug.datastructures.FileStorage): The uploaded resume file.

        Raises:
            Exception: If an error occurs while replacing the resume.

        """
        try:
            self.driver.get("https://www.totaljobs.com/profile")

            resume_name = self.uploadToServer(resume)
            resume_name_absolute = os.path.abspath(resume_name)  # Convert to absolute path

            total_jobs_login = TotalJobsLogin(driver, email, password)
            total_jobs_login.login()
            logging.info("Logged in to TotalJobs")

            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//span[normalize-space(text())='CV']"))
            ).click()

            time.sleep(3)

            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            ).send_keys(resume_name_absolute)

            time.sleep(5)
            logging.info(f"Resume Updated Successfully, Resume path: {resume_name_absolute}")
        except Exception as e:
            logging.exception(f"Error while uploading resume => {e}")

# aasdf31083@cvws.msdc.co
# testpass@123