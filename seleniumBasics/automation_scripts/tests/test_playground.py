# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


# def test_simple_form_submission(driver):

#     driver.get("https://www.lambdatest.com/selenium-playground/")

#     driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

#     message = "Hello Selenium"

#     driver.find_element(By.ID, "user-message").send_keys(message)

#     driver.find_element(By.ID, "showInput").click()

#     output = WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located(
#             (By.ID, "message")
#         )
#     )

#     assert output.text == message


# def test_checkbox_demo(driver):

#     driver.get("https://www.lambdatest.com/selenium-playground/")

#     driver.find_element(By.LINK_TEXT, "Checkbox Demo").click()

#     checkbox = driver.find_element(By.ID, "isAgeSelected")

#     checkbox.click()

#     assert checkbox.is_selected()

#     checkbox.click()

#     assert not checkbox.is_selected()

from selenium.webdriver.common.by import By

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage


def test_simple_form_submission(driver, base_url):

    page = SimpleFormPage(driver)

    page.navigate_to(base_url + "simple-form-demo")

    page.enter_message("Hello Selenium")

    page.click_submit()

    assert page.get_displayed_message() == "Hello Selenium"


def test_checkbox_demo(driver, base_url):

    page = CheckboxPage(driver)

    page.navigate_to(base_url + "checkbox-demo")

    page.check_option()

    assert page.is_option_checked()

    page.uncheck_option()

    assert not page.is_option_checked()


def test_dropdown_selection(driver, base_url):

    page = DropdownPage(driver)

    page.navigate_to(base_url + "select-dropdown-demo")

    page.select_day("Wednesday")

    assert page.get_selected_day() == "Wednesday"


def test_input_form_submit(driver, base_url):

    page = InputFormPage(driver)

    page.navigate_to(base_url + "input-form-demo")

    page.fill_form(
        "John",
        "john@gmail.com",
        "123456",
        "ABC",
        "abc.com",
        "Chennai",
        "Street 1",
        "Street 2",
        "Tamil Nadu",
        "600001"
    )

    page.submit_form()

    assert "input-form-demo" in driver.current_url