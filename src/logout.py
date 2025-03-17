from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def logout(driver):
    try:
        logout_button = driver.find_element(By.CSS_SELECTOR, "a.dropdown-item[href^='javascript:doAction']")
        driver.execute_script("arguments[0].click();", logout_button)
        print("Successfully logged out.")
        time.sleep(2)
    except Exception as e:
        print(f"Logout failed: {e}")