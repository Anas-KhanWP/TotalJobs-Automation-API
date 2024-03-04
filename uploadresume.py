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
    def __init__(self, driver):
        self.driver = driver

    def uploadToServer(self, resume):
        # Store the uploaded file in the "/resumes" directory
        resume_directory = "resumes"
        os.makedirs(resume_directory, exist_ok=True)
        resume_filename = os.path.join(resume_directory, resume.filename.lower())

        with open(resume_filename, "wb") as resume_file:
            resume_file.write(resume.file.read())
            return resume_filename

    def upload_resume(self, resume_name):
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
            logging.info(f"Resume Updated Successfully, Resume path: %s" % resume_name_absolute)
        except Exception as e:
            logging.exception(f"Error while uploading resume => {e}")

# aasdf31083@cvws.msdc.co
# testpass@123