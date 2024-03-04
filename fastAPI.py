import json
from typing import List
from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    Form,
    File,
    Depends,
    Query,
    status,
)
import requests
from selenium import webdriver
from apply import JobActions
from login import TotalJobsLogin
from uploadresume import ResumeUploader
from signup import SignupBot
from scrape import TotalJobsScraper
import logging
from dependencies import config
from dependencies.config import API_KEY
from fastapi.security import APIKeyHeader

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI()

# Define common variables
_resume = "resumes/CV.pdf"
_url = "https://ocean-app-b6gq7.ondigitalocean.app/api/create"
api_key_scheme = APIKeyHeader(name="X-API-KEY", auto_error=False)


# Custom function to validate the API key
def get_api_key(api_key: str = Depends(api_key_scheme)):
    """
    Validate the API key.

    Args:
        api_key (str): The API key sent by the client.

    Returns:
        str: The validated API key.

    Raises:
        HTTPException: If the API key is invalid.
    """
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )


def run_chrome() -> WebDriver:
    """
    This function creates a new instance of Chrome WebDriver with the desired options.

    Returns:
        WebDriver: A new instance of Chrome WebDriver with the desired options.
    """
    options = webdriver.ChromeOptions()
    # Set the user agent to mimic a real browser
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    # Enable headless mode
    # options.add_argument("--headless=new")

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


@app.get("/", dependencies=[Depends(get_api_key)])
async def check_Auth():
    return {"message": "Authorized"}


@app.post("/signup", dependencies=[Depends(get_api_key)])
async def signup(
    api_key: str = Depends(get_api_key),
    first_name: str = Form(...),
    last_name: str = Form(...),
    client_email: str = Form(...),
    resume: UploadFile = File(default=None),
    job_title: str = Form(...),
):
    """
    Signup endpoint.

    Args:
        api_key (str): The API key used to authenticate the request.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        client_email (str): The email address of the user.
        resume (UploadFile): The resume of the user.
        job_title (str): The job title of the user.

    Returns:
        A JSON object containing the email and password of the newly created user.

    Raises:
        HTTPException: If the API key is invalid, or if the email is not generated from the API.
    """
    try:
        driver = run_chrome()
        # Create an instance of ResumeUploader
        resume_uploader = ResumeUploader(driver)
        # Call the upload_resume method to handle resume upload
        if resume is None:
            resume_filename = _resume
        else:
            resume_filename = resume_uploader.uploadToServer(resume)

        c_url = f"{_url}/{first_name}/{last_name}/{client_email}"
        response = requests.get(c_url, headers={"X-API-KEY": api_key})

        # Log API request details
        logging.info(f"API Request: {c_url}")
        logging.info(f"API Response Status Code: {response.status_code}")
        logging.info(f"API Response Content: {response.text}")

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Extract and store the generated email in a variable
            generated_email = data.get("generated_email")
            logging.info(f"Generated email => {generated_email}")
            signup_bot = SignupBot(
                driver,
                first_name,
                last_name,
                generated_email,
                config.password,
                resume_filename,
                job_title,
            )
            email, password = signup_bot.make_totalBot_signup()
            driver.quit()
            logging.info(
                f"Signup successful. Credentials => Email: {email}, Password: {password}"
            )
            return {"email": email, "password": password}
        else:
            logging.error(f"API request failed. Status code: {response.status_code}")
            logging.error(f"API response content: {response.text}")
            raise HTTPException(
                status_code=500, detail="Email not generated from the API"
            )
    except FileNotFoundError as e:
        logging.error(f"File not found while handling signup: {e}")
        raise HTTPException(status_code=500, detail=f"File not found: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to API failed during signup: {str(e)}")
        raise HTTPException(status_code=500, detail="Error communicating with API")
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response during signup: {str(e)}")
        raise HTTPException(status_code=500, detail="Error parsing API response")


@app.post("/login", dependencies=[Depends(get_api_key)])
async def login(
    email: str,  # The email address of the user
    password: str,  # The password of the user
):
    """
    Login endpoint.

    Args:
        email (str): The email address of the user.
        password (str): The password of the user.

    Returns:
        A JSON object containing a message indicating whether the login was successful.

    Raises:
        HTTPException: If the login is unsuccessful.
    """
    try:
        driver = run_chrome()
        total_jobs_login = TotalJobsLogin(driver, email, password)
        total_jobs_login.login()
        driver.quit()
        return {"message": "Login successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/replace_resume", dependencies=[Depends(get_api_key)])
async def replace_resume(
    email: str,  # The email address of the user
    password: str,  # The password of the user
    resume: UploadFile,  # The resume file to be uploaded
):
    """
    Replace the resume of a user.

    Args:
        email (str): The email address of the user.
        password (str): The password of the user.
        resume (UploadFile): The resume file to be uploaded.

    Returns:
        A JSON object containing a message indicating whether the resume was uploaded successfully.

    Raises:
        HTTPException: If the resume upload fails.
    """
    try:
        driver = run_chrome()
        resume_uploader = ResumeUploader(driver)
        resume_uploader.replaceResume(driver, email, password, resume)
        driver.quit()
        return {"message": "Resume uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scrape_jobs", dependencies=[Depends(get_api_key)])
async def scrape_jobs(
    user_id: str = Query(..., description="TotalJobs User ID"),
    job_title: str = Query(..., description="Title of the job"),
    location: str = Query(..., description="Location of the job"),
):
    """
    This function uses the TotalJobsScraper class to scrape job postings from the TotalJobs website.

    Args:
        user_id (str): The TotalJobs user ID.
        job_title (str): The job title.
        location (str): The location.

    Returns:
        A JSON object containing a list of job links.

    Raises:
        HTTPException: If an error occurs.
    """
    try:
        driver = run_chrome()
        total_jobs_scraper = TotalJobsScraper(driver)
        job_links = total_jobs_scraper.get_jobs(job_title, location)
        driver.quit()
        return {"job_links": job_links}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login_apply", dependencies=[Depends(get_api_key)])
async def login_scrape_apply(
    email: str,  # The email address of the user
    password: str,  # The password of the user
    job_links: List[str],  # A list of job links
):
    """
    This function logs in to TotalJobs, scrapes job postings, and applies to the jobs.

    Args:
        email (str): The email address of the user.
        password (str): The password of the user.
        job_links (List[str]): A list of job links.

    Returns:
        A JSON object containing a message indicating the status of the login, scrape, and apply process.

    Raises:
        HTTPException: If an error occurs.
    """
    try:
        driver = run_chrome()
        total_jobs_login = TotalJobsLogin(driver, email, password)
        total_jobs_login.login()

        job_actions = JobActions(driver)
        for job_link in job_links:
            logging.info(f"Current Job URL => {job_link}")
            response_msg = job_actions.apply_to_job(job_link)

        driver.quit()
        if response_msg == 200:
            return {"message": "Login and apply successful"}
        elif response_msg == 201:
            return {"message": "External Job Skipping"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login_scrape_apply", dependencies=[Depends(get_api_key)])
async def login_scrape_apply(
    email: str = Form(...),
    password: str = Form(...),
    job_title: str = Form(...),  # job title
    location: str = Form(...),  # location
):
    """
    This function logs in to TotalJobs, scrapes job postings, and applies to the jobs.

    Args:
        email (str): The email address of the user.
        password (str): The password of the user.
        job_title (str): The job title to search for.
        location (str): The location to search for jobs.

    Returns:
        A JSON object containing a message indicating the status of the login, scrape, and apply process.

    Raises:
        HTTPException: If an error occurs.
    """
    try:
        driver = run_chrome()
        total_jobs_login = TotalJobsLogin(driver, email, password)
        total_jobs_login.login()

        total_jobs_scraper = TotalJobsScraper(driver)
        job_links = total_jobs_scraper.get_jobs(job_title, location)

        job_actions = JobActions(driver)
        for job_link in job_links:
            logging.info(f"Current Job URL => {job_link}")
            response_msg = job_actions.apply_to_job(job_link)

        driver.quit()
        if response_msg == 200:
            return {"message": "Login and apply successful"}
        elif response_msg == 201:
            return {"message": "External Job Skipping"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
