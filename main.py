from dependencies import config
import time
from selenium import webdriver
from signup import SignupBot
from dependencies.config import email_api as ea, timeFormatter
from scrape import TotalJobsScraper
from apply import JobActions
from login import TotalJobsLogin
from uploadresume import ResumeUploader
import logging
import requests

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def run_chrome():
    """
    This function initializes a new instance of the Chrome WebDriver with the specified options.

    Args:
        options (ChromeOptions): A ChromeOptions object that specifies the desired options for the Chrome WebDriver.

    Returns:
        WebDriver: A new instance of the Chrome WebDriver.

    """
    options = webdriver.ChromeOptions()

    # Set the user agent to mimic a real browser
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")

    # Enable headless mode
    options.add_argument("--headless=new")

    # Set window size (optional, but can be useful for rendering)
    options.add_argument("--window-size=1920x1080")

    # Disable extensions
    options.add_argument("--disable-extensions")

    # Disable GPU acceleration (useful in headless mode)
    options.add_argument("--disable-gpu")

    # Disable sandboxing for Linux (may be required in some environments)
    options.add_argument("--no-sandbox")

    # Disable the /dev/shm usage (can be helpful for some environments)
    options.add_argument("--disable-dev-shm-usage")

    # Disable logging (optional)
    options.add_argument("--disable-logging")

    # Other optional options you may consider:
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=options)
    return driver


_resume = "CV.pdf"

start_time = time.time()

# Option to choose action
print("Choose an action:")
print("1. Signup")
print("2. Login")
print("3. Scrape Jobs")
print("4. Login and Scrape Jobs")
# Add more options as needed

user_choice = input("Enter the number of your choice: ")

driver = run_chrome()
driver.maximize_window()

# emailGen = MailsacEmailGenerator(api_key=ea)
# email, first_name, last_name = emailGen.generate_random_mail()

url = "https://ocean-app-b6gq7.ondigitalocean.app/api/create"
first_name = input("Enter First Name")
last_name = input("Enter Last Name")
client_email = input("Enter Email")

headers = {"X-API-KEY": "#$8sflkj@(ACMEU8m,"}

# Update the URL with path parameters
url = f"{url}/{first_name}/{last_name}/{client_email}"

response = requests.get(url, headers=headers)
if user_choice in ("1", "2", "4"):
    # Signup or login based on user choice
    if user_choice == "1":
        _email = response.json()['generated_email']
        print(f"Generated email => {_email}")
        signup_bot = SignupBot(
            driver, _resume, _email, config.password, first_name, last_name
        )
        email, password = signup_bot.make_totalBot_signup()
        print(email, password)
    elif user_choice == "2":
        email = input("enter email")
        password = input("enter password")
        total_jobs_login = TotalJobsLogin(driver, email, password)
        total_jobs_login.login()
        pass

if user_choice in ("3", "4"):
    total_jobs_scraper = TotalJobsScraper(driver)
    jobLinks = total_jobs_scraper.get_jobs("Python", "London")

    if jobLinks is not None:
        job_actions = JobActions(driver)
        for _job in jobLinks:
            logging.info(f"Current Job URL => {_job}")
            job_actions.apply_to_job(_job)

if user_choice == "5":
    resume_name = input("resume name")
    # Scrape jobs based on user choice
    uploadR = ResumeUploader(driver)
    uploadR.upload_resume(resume_name)

end_time = time.time()
total_time_taken = end_time - start_time
formatted_time = timeFormatter(total_time_taken)
logging.info(f"Total time taken: {formatted_time}")

# Close the browser window
driver.quit()
