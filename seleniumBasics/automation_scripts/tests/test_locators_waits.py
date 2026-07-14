from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import NoSuchElementException
import time

# ---------------------------------------------------------
# Selenium WebDriver Setup
# ---------------------------------------------------------

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()
driver.implicitly_wait(10)

driver.get("https://www.lambdatest.com/selenium-playground/")

print("=" * 50)
print("TASK 1 - LOCATOR STRATEGIES")
print("=" * 50)

# ---------------------------------------------------------
# Open Simple Form Demo
# ---------------------------------------------------------

driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

# ---------------------------------------------------------
# By.ID
# ---------------------------------------------------------

id_element = driver.find_element(By.ID, "user-message")
print("By.ID -> PASS")

# ---------------------------------------------------------
# By.NAME
# ---------------------------------------------------------

name_element = driver.find_element(By.NAME, "message")
print("By.NAME -> PASS")

# ---------------------------------------------------------
# By.CLASS_NAME
# ---------------------------------------------------------

class_element = driver.find_element(By.CLASS_NAME, "form-control")
print("By.CLASS_NAME -> PASS")

# ---------------------------------------------------------
# By.TAG_NAME
# ---------------------------------------------------------

tag_element = driver.find_element(By.TAG_NAME, "input")
print("By.TAG_NAME -> PASS")

# ---------------------------------------------------------
# Absolute XPath
# ---------------------------------------------------------

absolute_xpath = driver.find_element(
    By.XPATH,
    "/html/body/div[1]/section[2]/div/div/div[1]/div/div[2]/div/input"
)

print("Absolute XPath -> PASS")

# ---------------------------------------------------------
# Relative XPath
# ---------------------------------------------------------

relative_xpath = driver.find_element(
    By.XPATH,
    "//input[@id='user-message']"
)

print("Relative XPath -> PASS")

# ---------------------------------------------------------
# CSS Selector by ID
# ---------------------------------------------------------

driver.find_element(
    By.CSS_SELECTOR,
    "#user-message"
)

print("CSS Selector (#id) -> PASS")

# ---------------------------------------------------------
# CSS Selector by Attribute
# ---------------------------------------------------------

driver.find_element(
    By.CSS_SELECTOR,
    "input[name='message']"
)

print("CSS Selector (attribute) -> PASS")

# ---------------------------------------------------------
# CSS Parent > Child
# ---------------------------------------------------------

driver.find_element(
    By.CSS_SELECTOR,
    "div > input#user-message"
)

print("CSS Selector (parent > child) -> PASS")

# ---------------------------------------------------------
# Return Home
# ---------------------------------------------------------

driver.back()

# ---------------------------------------------------------
# Checkbox Demo
# ---------------------------------------------------------

driver.find_element(By.LINK_TEXT, "Checkbox Demo").click()

# XPath using text()

label = driver.find_element(
    By.XPATH,
    "//label[text()='Option 1']"
)

print("XPath text() ->", label.text)

# XPath contains()

labels = driver.find_elements(
    By.XPATH,
    "//label[contains(text(),'Option')]"
)

print("\nCheckbox Labels")

for item in labels:
    print(item.text)

# ---------------------------------------------------------
# Ranking of Locators
# ---------------------------------------------------------

"""
Locator Preference Ranking

1. By.ID
   Unique, fastest and easiest to maintain.

2. By.NAME
   Good when unique.

3. CSS_SELECTOR
   Fast and flexible.

4. CLASS_NAME
   Useful but classes are often reused.

5. Relative XPath
   Powerful when CSS cannot locate an element.

6. Absolute XPath
   Least preferred because any HTML change breaks it.
"""

print("\nTask 1 Completed Successfully")

print("=" * 50)
print("TASK 2 - WAITS")
print("=" * 50)

# ---------------------------------------------------------
# Return Home
# ---------------------------------------------------------

driver.get("https://www.lambdatest.com/selenium-playground/")

# ---------------------------------------------------------
# Open Bootstrap Alerts
# ---------------------------------------------------------

driver.find_element(
    By.LINK_TEXT,
    "Bootstrap Alerts"
).click()

# ---------------------------------------------------------
# STEP 36 - Explicit Wait
# ---------------------------------------------------------

print("\nSTEP 36 - Explicit Wait")

success_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.ID, "autoclosable-btn-success")
    )
)

success_button.click()

alert = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".alert-autocloseable-success")
    )
)

print("Alert Text:", alert.text)

assert "successfully" in alert.text.lower()

print("Explicit Wait Test Passed")


# ---------------------------------------------------------
# STEP 37 - time.sleep() vs Explicit Wait
# ---------------------------------------------------------

print("\nSTEP 37 - Comparing sleep() and Explicit Wait")

driver.refresh()

sleep_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.ID, "autoclosable-btn-success")
    )
)

start = time.time()

sleep_button.click()

time.sleep(3)

sleep_time = time.time() - start

print("Time using sleep():", round(sleep_time, 2), "seconds")


driver.refresh()

wait_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.ID, "autoclosable-btn-success")
    )
)

start = time.time()

wait_button.click()

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".alert-autocloseable-success")
    )
)

wait_time = time.time() - start

print("Time using Explicit Wait:", round(wait_time, 2), "seconds")

print("""
Explanation:
sleep() always waits the complete time.
Explicit Wait stops immediately after the element appears.
Hence Explicit Wait is faster and more reliable.
""")


# ---------------------------------------------------------
# STEP 38 - element_to_be_clickable
# ---------------------------------------------------------

print("\nSTEP 38 - element_to_be_clickable()")

driver.refresh()

clickable = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.ID, "autoclosable-btn-success")
    )
)

clickable.click()

print("""
visibility_of_element_located():
Element is present and visible.

element_to_be_clickable():
Element is visible AND enabled, so Selenium can click it.
""")


# ---------------------------------------------------------
# STEP 39 - Fluent Wait
# ---------------------------------------------------------

print("\nSTEP 39 - Fluent Wait")

driver.get("https://www.lambdatest.com/selenium-playground/table-sort-search-demo")

try:

    row = WebDriverWait(
        driver,
        timeout=10,
        poll_frequency=0.5,
        ignored_exceptions=[NoSuchElementException]
    ).until(

        EC.presence_of_element_located(
            (By.XPATH, "//table/tbody/tr[1]")
        )

    )

    print("Fluent Wait Successful")
    print("First Row:")
    print(row.text)

except Exception as e:

    print("Fluent Wait Failed")
    print(e)


print("""
Fluent Wait:
• Maximum timeout : 10 seconds
• Polling interval : 500 milliseconds
• Ignores NoSuchElementException while polling.
""")


# ---------------------------------------------------------
# End of Hands-On 5
# ---------------------------------------------------------

print("\nHands-On 5 Completed Successfully!")

driver.quit()