import capsolver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize capsolver with your API key
capsolver.api_key = "CAP-2BF9057E866C0095F43CF74F502103DA"

# Solve the hCaptcha using capsolver
solution = capsolver.solve({
    "type": "HCaptchaTaskProxyless",  # Required.
    "websiteKey": "a5f74b19-9e45-40e0-b45d-47ff91b7a6c2",  # Required. This is the domain's public key, often called the 'site key.'
    "websiteURL": "https://accounts.hcaptcha.com/demo",  # Required. The URL of the page where the hCaptcha is located.
})

print("CAPSolver Solution:", solution)

# Extract the CAPTCHA token from the solution
token = solution.get('gRecaptchaResponse')

if not token:
    print("Failed to get CAPTCHA token from capsolver.")
    exit()

# Set up Selenium WebDriver (you may need to specify the path to your chromedriver)
driver = webdriver.Chrome()

try:
    # Navigate to the target website
    driver.get("https://accounts.hcaptcha.com/demo")

    # Wait for the hCaptcha to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title*='hCaptcha security challenge']"))
    )

    # Inject the CAPTCHA token into the page
    driver.execute_script("""
    document.getElementsByName('h-captcha-response')[0].style.display = 'block';
    document.getElementsByName('h-captcha-response')[0].value = arguments[0];
    """, token)

    # Submit the form
    submit_button = driver.find_element(By.ID, 'hcaptcha-demo-submit')
    submit_button.click()

    # Wait for the result page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'hcaptcha-success'))
    )

    # Print the result
    result = driver.find_element(By.CLASS_NAME, "hcaptcha-success").text
    print("Result:", result)

finally:
    # Close the browser
    driver.quit()
