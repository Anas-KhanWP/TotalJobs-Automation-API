import http.client
from dependencies import config
import random
import ast
import logging

logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
api_key = config.email_api


class MailsacEmailGenerator:
    """
    This class provides methods to interact with the Mailsac API.
    """

    def __init__(self, api_key):
        """
        Initialize the MailsacEmailGenerator class with the API key.

        Args:
            api_key (str): The API key for Mailsac.
        """
        self.api_key = api_key
        self.base_url = "mailsac.com"

    def random_string_generator(self, str_size, allowed_chars):
        """
        Generate a random string of a given size and using a given set of allowed characters.

        Args:
            str_size (int): The size of the random string to generate.
            allowed_chars (str): The set of allowed characters for the random string.

        Returns:
            str: The random string.
        """
        return "".join(random.choice(allowed_chars) for x in range(str_size))

    def get_all_mail_created(self):
        """
        Get a list of all the email addresses created using the API key.

        Returns:
            str: The response from the API.
        """
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {"Mailsac-Key": self.api_key}
        conn.request("GET", "/api/addresses", headers=headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

    def create_email(self, mail):
        """
        Create a new email address with the given email address.

        Args:
            mail (str): The email address to create.

        Returns:
            str: The response from the API.
        """
        conn = http.client.HTTPSConnection(self.base_url)
        payload = '{"info":"string","forward":"","enablews":false,"webhook":"","webhookSlack":"","webhookSlackToFrom":true}'
        headers = {"content-type": "application/json", "Mailsac-Key": self.api_key}
        conn.request("POST", "/api/addresses/{}".format(mail), payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

    def get_mail_content(self, mail):
        """
        Get the content of the email addressed with the given email address.

        Args:
            mail (str): The email address of the email to get the content of.

        Returns:
            str: The response from the API.
        """
        conn = http.client.HTTPSConnection(self.base_url)
        headers = {"Mailsac-Key": self.api_key}
        conn.request("GET", "/api/addresses/{}/messages".format(mail), headers=headers)
        res = conn.getresponse()
        data = res.read()
        logging.info(data.decode("utf-8"))
        return data.decode("utf-8")

    def generate_random_mail(self):
        """
        Generate a random email address and return it along with the first and last names of a fictitious person.

        Returns:
            tuple: A tuple containing the random email address, the first name, and the last name.
        """
        random_mail = (
            self.random_string_generator(10, "abcdefghijklmnopqrstuvwxyz")
            + "@mailsac.com"
        )
        f_name = self.random_string_generator(10, "abcdefghijklmnopqrstuvwxyz")
        l_name = self.random_string_generator(10, "abcdefghijklmnopqrstuvwxyz")
        self.create_email(random_mail)
        logging.info(
            f"Email => {random_mail}\n"
            f"First Name => {f_name}\n"
            f"Last Name => {l_name}"
        )

        return random_mail, f_name, l_name

    def get_verification_links(self, mail):
        """
        Get the verification links from the email addressed with the given email address.

        Args:
            mail (str): The email address of the email to get the verification links from.

        Returns:
            list: A list of verification links.
        """
        mail_content = self.get_mail_content(mail)
        confirm_link = mail_content.split('links":[')[1].split("]")[0]
        links = confirm_link.replace('"', "").split(",")
        return links

    def get_verification_codes(self, mail):
        """
        Get the verification codes from the email addressed with the given email address.

        Args:
            mail (str): The email address of the email to get the verification codes from.

        Returns:
            list: A list of verification codes.
        """
        mail_content = self.get_mail_content(mail)
        confirm_code = mail_content.split('subject":')[1].split(" ")[0]
        verify_code = confirm_code.replace('"', "").split(",")
        return verify_code
