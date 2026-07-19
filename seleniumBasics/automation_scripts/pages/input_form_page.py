from selenium.webdriver.common.by import By
from .base_page import BasePage


class InputFormPage(BasePage):

    NAME = (By.ID, "name")
    EMAIL = (By.ID, "inputEmail4")
    PASSWORD = (By.ID, "inputPassword4")
    COMPANY = (By.ID, "company")
    WEBSITE = (By.ID, "websitename")
    COUNTRY = (By.NAME, "country")
    CITY = (By.ID, "inputCity")
    ADDRESS1 = (By.ID, "inputAddress1")
    ADDRESS2 = (By.ID, "inputAddress2")
    STATE = (By.ID, "inputState")
    ZIP = (By.ID, "inputZip")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")

    def fill_form(
        self,
        name,
        email,
        password,
        company,
        website,
        city,
        address1,
        address2,
        state,
        zipcode,
    ):

        self.wait_for_element(self.NAME).send_keys(name)
        self.wait_for_element(self.EMAIL).send_keys(email)
        self.wait_for_element(self.PASSWORD).send_keys(password)
        self.wait_for_element(self.COMPANY).send_keys(company)
        self.wait_for_element(self.WEBSITE).send_keys(website)
        self.wait_for_element(self.CITY).send_keys(city)
        self.wait_for_element(self.ADDRESS1).send_keys(address1)
        self.wait_for_element(self.ADDRESS2).send_keys(address2)
        self.wait_for_element(self.STATE).send_keys(state)
        self.wait_for_element(self.ZIP).send_keys(zipcode)

    def submit_form(self):
        self.wait_for_element(self.SUBMIT).click()