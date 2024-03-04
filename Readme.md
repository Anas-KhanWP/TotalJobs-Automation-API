# Welcome to TotalJobs Automation API

Welcome to the TotalJobs Automation API! 🚀 This repository houses a powerful API built with FastAPI, aimed at simplifying various tasks on the TotalJobs platform. From user registration and login to resume management, job scraping, and even automatic job applications, this API is your gateway to effortless interaction with TotalJobs.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Endpoints](#endpoints)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)
- [License](#license)

## Overview

Tired of mundane hours spent navigating through TotalJobs? Say goodbye to manual labor! The TotalJobs Automation API empowers you to automate repetitive tasks, liberating your time for more meaningful pursuits—like perfecting your resume or acing that interview!

## Getting Started

### Prerequisites

Before diving into the wonders of the TotalJobs Automation API, ensure you have the following prerequisites:

- Python 3.6 or later
- Chrome web browser

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Anas-KhanWP/TotalJobs-Automation-API.git
   cd TotalJobs-Automation-API
   ```

2. Install dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Endpoints

The API boasts a variety of endpoints, each catering to a specific TotalJobs task:

1. **Sign Up (`/signup`):** Register for a TotalJobs account.
2. **Login (`/login`):** Log in to your TotalJobs account.
3. **Replace Resume (`/replace_resume`):** Update your resume on TotalJobs.
4. **Scrape Jobs (`/scrape_jobs`):** Retrieve job listings based on job title and location.
5. **Login, Scrape, and Apply (`/login_scrape_apply`):** Automate login, job scraping, and job applications.

For comprehensive usage guidelines and examples, consult the [API Endpoints](#api-endpoints) section in the README.

## Tech Stack

The TotalJobs Automation API leverages the following cutting-edge technologies:

- [FastAPI](https://fastapi.tiangolo.com/) 🛠️: A lightning-fast web framework for building APIs with Python 3.6+.
- [Selenium](https://www.selenium.dev/) ⚙️: A versatile tool for automating web browsers, pivotal for web scraping and automation.
- [Requests](https://docs.python-requests.org/en/latest/) 📡: An elegant HTTP library for Python, facilitating seamless interaction with external services.
- [pynput](https://pypi.org/project/pynput/) ⌨️: A Python library enabling monitoring and control of input devices—ideal for automating keyboard inputs.
- [Logging](https://docs.python.org/3/library/logging.html) 📝: Python's in-built logging module, indispensable for recording detailed API activities.

## Contributing

Contributions are warmly welcomed! Whether you have suggestions, bug fixes, or new features to propose, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. Refer to the [LICENSE](LICENSE) file for further details. Happy automating! 🤖✨
