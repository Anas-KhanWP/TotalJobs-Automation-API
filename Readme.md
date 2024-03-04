# TotalJobs Automation API

This repository provides a FastAPI-based API for automating various actions on the TotalJobs platform, including signing up, logging in, replacing resumes, job scraping, and applying to jobs.

## Getting Started

### Prerequisites

- Python 3.6 or later
- Install dependencies using the following command:

  ```bash
  pip install -r requirements.txt
  ```

### Running the API

1. Clone this repository:

   ```bash
   git clone https://github.com/AffanAhmedUsmani/totaljobs-bot.git
   ```

2. Navigate to the project directory:

   ```bash
   cd totaljobs-bot
   ```

3. Run the API using:

   ```bash
   uvicorn fastAPI:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### 1. Sign Up (`/signup`)

- **Method:** `POST`
- **Parameters:**
  - `first_name` (form field, required): First name of the user.
  - `last_name` (form field, required): Last name of the user.
  - `client_email` (form field, required): Email address of the user.
  - `resume` (file upload, optional): Resume file to be uploaded.
  - `job_title` (form field, required): Job title of the user.
  - `annual_salary` (form field, required): Annual salary of the user.

#### Functionality:

- Initiates a headless Chrome browser.
- Uploads the provided resume or uses a default resume.
- Sends a request to an external API to generate an email.
- Logs the API request details and response.
- If successful, signs up the user using the generated email, job title, and annual salary, and returns the login credentials.

#### Example Usage:

```bash
curl -X POST "http://127.0.0.1:8000/signup" \
  -H "Content-Type: multipart/form-data" \
  -F "first_name=John" \
  -F "last_name=Doe" \
  -F "client_email=johndoe@example.com" \
  -F "resume=@path/to/resume.pdf" \
  -F "job_title=Software%20Engineer" \
  -F "annual_salary=50000"
```

### 2. Login (`/login`)

- **Method:** `POST`
- **Parameters:**
  - `email` (form field, required): User's email address.
  - `password` (form field, required): User's password.

#### Functionality:

- Initiates a headless Chrome browser.
- Logs in to TotalJobs using the provided email and password.

#### Example Usage:

```bash
curl -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=johndoe@example.com" \
  -d "password=your_password"
```

### 3. Replace Resume (`/replace_resume`)

- **Method:** `POST`
- **Parameters:**
  - `email` (form field, required): User's email address.
  - `password` (form field, required): User's password.
  - `resume` (file upload, required): New resume file to replace the existing one.

#### Functionality:

- Initiates a headless Chrome browser.
- Replaces the user's existing resume with a new one.
- Logs the action details.

#### Example Usage:

```bash
curl -X POST "http://127.0.0.1:8000/replace_resume" \
  -H "Content-Type: multipart/form-data" \
  -F "email=johndoe@example.com" \
  -F "password=your_password" \
  -F "resume=@path/to/new_resume.pdf"
```

### 4. Scrape Jobs (`/scrape_jobs`)

- **Method:** `GET`
- **Parameters:**
  - `job_title` (query parameter, required): Title of the job.
  - `location` (query parameter, required): Location of the job.

#### Functionality:

- Initiates a headless Chrome browser.
- Scrapes job links based on the provided job title and location.
- Logs the action details.

#### Example Usage:

```bash
curl -X GET "http://127.0.0.1:8000/scrape_jobs?job_title=Software%20Engineer&location=London"
```

### 5. Login, Scrape, and Apply (`/login_scrape_apply`)

- **Method:** `POST`
- **Parameters:**
  - `email` (form field, required): User's email address.
  - `password` (form field, required): User's password.
  - `job_title` (form field, required): Title of the job.
  - `location` (form field, required): Location of the job.

#### Functionality:

- Initiates a headless Chrome browser.
- Logs in to TotalJobs using the provided email and password.
- Scrapes job links based on the provided job title and location.
- Applies to each job using the obtained job links.
- Logs the action details.

#### Example Usage:

```bash
curl -X POST "http://127.0.0.1:8000/login_scrape_apply" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=johndoe@example.com" \
  -d "password=your_password" \
  -d "job_title=Software%20Engineer" \
  -d "location=London"
```

## Additional Information

- The API utilizes FastAPI for handling requests and responses.
- Logging information is stored in the `app.log` file.
- The API communicates with an external service at the specified `_url` for email generation.
- Ensure that the Chrome web browser is installed, as the API uses Selenium with Chrome for automation.

Feel free to explore and integrate these endpoints into your application or scripts for TotalJobs automation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.