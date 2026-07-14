# """
# Hands-On 4
# QA Concepts & Selenium Basics

# Task 1:
# 1. Describe Selenium Components.
# 2. Launch Chrome using webdriver-manager.
# 3. Open Selenium Playground.
# 4. Print page title.
# 5. Add implicit wait.
# 6. Run browser in headless mode.
# """

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager


# # ==========================================================
# # Selenium Components
# # ==========================================================
# #
# # WebDriver:
# # Selenium WebDriver is the main component used to automate
# # browser actions. It communicates with browser drivers
# # (ChromeDriver, GeckoDriver, etc.) and performs operations
# # such as opening websites, clicking buttons, entering text,
# # and validating results.
# #
# # Selenium Grid:
# # Selenium Grid allows tests to run on multiple browsers,
# # operating systems, and machines simultaneously. It helps
# # execute tests in parallel, reducing execution time.
# #
# # Selenium IDE:
# # Selenium IDE is a browser extension used to record and
# # replay browser actions. It is useful for beginners and
# # for generating automation scripts quickly.
# #
# # ==========================================================


# # Configure Chrome to run in headless mode
# options = Options()
# options.add_argument("--headless=new")
# options.add_argument("--disable-gpu")

# # Launch Chrome browser
# driver = webdriver.Chrome(
#     service=Service(ChromeDriverManager().install()),
#     options=options
# )

# # Implicit Wait
# driver.implicitly_wait(10)

# # Open Website
# driver.get("https://www.lambdatest.com/selenium-playground/")

# # Print Page Title
# print("=" * 60)
# print("Page Title : ", driver.title)
# print("Current URL:", driver.current_url)
# print("=" * 60)

# # Why Explicit Wait is Preferred?
# #
# # Implicit Wait applies globally to every element lookup,
# # which may unnecessarily slow down execution.
# #
# # Explicit Wait waits only for a specific element or condition,
# # making tests faster, more reliable, and easier to maintain.

# driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome Options
options = Options()

# Uncomment for headless execution
# options.add_argument("--headless=new")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.maximize_window()
driver.implicitly_wait(10)

# -------------------------------------------------
# Step 28
# Navigation
# -------------------------------------------------

driver.get("https://www.lambdatest.com/selenium-playground/")

print("Home Page:")
print(driver.title)

# Click Simple Form Demo
driver.find_element("link text", "Simple Form Demo").click()

time.sleep(2)

# Verify URL
if "simple-form-demo" in driver.current_url:
    print("Navigation Successful")
else:
    print("Navigation Failed")

# Go Back
driver.back()

time.sleep(2)

# -------------------------------------------------
# Step 29
# New Tab
# -------------------------------------------------

driver.switch_to.new_window("tab")

driver.get("https://www.google.com")

print("\nSecond Tab Title:")
print(driver.title)

# -------------------------------------------------
# Step 30
# Switch back and Screenshot
# -------------------------------------------------

tabs = driver.window_handles

driver.switch_to.window(tabs[0])

driver.save_screenshot("screenshots/homepage.png")

print("\nScreenshot Saved")

# -------------------------------------------------
# Step 31
# Window Size
# -------------------------------------------------

print("\nCurrent Window Size:")

size = driver.get_window_size()

print(size)

driver.set_window_size(1280, 800)

print("New Window Size:")

print(driver.get_window_size())

driver.quit()