from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()
driver.implicitly_wait(10)

driver.get("https://www.lambdatest.com/selenium-playground/")

# Open Simple Form Demo
driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

# Enter message
message = "Hello Selenium"

input_box = driver.find_element(By.ID, "user-message")
input_box.send_keys(message)

# Click "Get Checked Value"
driver.find_element(By.ID, "showInput").click()

# Verify output
output = driver.find_element(By.ID, "message").text

print("Displayed Message:", output)

assert output == message

print("Test Passed")

driver.quit()