import requests
import time
import math
import random
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class TotalJobsScraper:
    """
    A class for scraping job postings from the website TotalJobs.com.

    Args:
        driver (webdriver): A Selenium WebDriver instance for interacting with the website.

    Attributes:
        driver (webdriver): A Selenium WebDriver instance for interacting with the website.

    """

    def __init__(self, driver):
        self.driver = driver

    def accept_cookie(self):
        """
        Accepts any cookies that may be displayed by the website.

        """
        try:
            accept_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[text()='Accept All']"))
            )

            if accept_button:
                accept_button.click()
                logging.info("Cookies Accepted")

        except:
            logging.info("No Cookie popup")

    def getRandomSleep(self):
        """
        Returns a random number of seconds to sleep for, between 1 and 10.

        Returns:
            float: A random number of seconds to sleep for.

        """
        random_sleep_duration = random.uniform(1, 10)
        return random_sleep_duration

    def get_job_link(self, job):
        """
        Extracts the job link from the given job element.

        Args:
            job (WebElement): A job element from the website.

        Returns:
            str: The job link, or None if the job link could not be found.

        """
        try:
            job_a = job.find_element(By.XPATH, ".//a[@class='res-1taea5l']")
            job_link = job_a.get_attribute("href")
            logging.info(f"Job Link: {job_link}")
            return job_link
        except NoSuchElementException:
            logging.error("Element not found: Unable to locate job link")
            logging.exception("Element not found")

    def getTotalJobs(self):
        """
        Extracts the total number of jobs from the website.

        Returns:
            int: The total number of jobs, or None if the total number of jobs could not be found.

        """
        try:
            # Find the <span> element with data-at attribute set to "search-jobs-count" using XPath
            xpath_expression = "//span[@data-at='search-jobs-count']"
            results_span = self.driver.find_element(By.XPATH, xpath_expression)
            # Get the text content of the <span> element
            results_text = results_span.text
            result = int(results_text)
            # Print the text content
            logging.info(f"Total Jobs: {result}")

            return result
        except NoSuchElementException:
            logging.info("Element not found")

    def getJobsList(self):
        """
        Returns a list of job elements from the website.

        Returns:
            list: A list of job elements, or None if no job elements could be found.

        """
        try:
            job_divs = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
            )

            time.sleep(5)

            # job_divs = base.find_elements(By.CLASS_NAME, "res-vxbpca")
            logging.info(f"Total Jobs on this page => {len(job_divs)}")

            return job_divs
        except:
            return None

    def get_jobs(self, title, location):
        """
        Scrapes job postings from the website TotalJobs.com.

        Args:
            title (str): The job title to search for.
            location (str): The location to search for jobs in.

        Returns:
            list: A list of job links, or an empty list if no jobs were found.

        """
        job_links = []

        start_url = f"https://www.totaljobs.com/jobs/{title}/in-{location}?radius=10&page=1"
        self.driver.get(start_url)

        self.accept_cookie()

        total_job = self.getTotalJobs()
        job_divs = self.getJobsList()

        if total_job is None or len(job_divs) == 0:
            logging.info("No jobs found")
            return []

        # Calculate the rounded-up division
        total_pages = math.ceil(int(total_job) / len(job_divs))
        # Print the rounded-up division
        logging.info(f"Rounded-up division: {total_pages}")

        for page in range(1, total_pages):

            job_divs = self.getJobsList()

            total_jobs = len(job_links)

            if total_jobs >= 50:
                logging.info(f"{len(job_links)} Jobs Found")
                break

            if job_divs is None:
                logging.info("No jobs")
                continue

            for job in job_divs:
                job_link = self.get_job_link(job)
                if job_link:  # Check if job_link is not None
                    job_links.append(job_link)

            meta = self.getRandomSleep()
            time.sleep(meta)

            if page <= total_pages - 1:
                next_button_xpath = '//a[@class="res-1xvjmp2" and @data-genesis-element="BUTTON" and @aria-label="Next"]'
                next_button = self.driver.find_element(By.XPATH, next_button_xpath)
                logging.info(f"Going to page Number {page + 1}")
                next_button.click()

            logging.info(f"Total Jobs Found So far => {total_jobs}")

        logging.info(f"Total Job Links => {len(job_links)}")
        if job_links is None:
            raise Exception("No jobs found")
        return job_links

# adef29424@cvws.msdc.co
# testpass@123