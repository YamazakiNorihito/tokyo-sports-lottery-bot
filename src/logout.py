from selenium.webdriver.common.by import By
from wait import wait

def logout(driver):
    logout_button = driver.find_element(By.CSS_SELECTOR, "a.dropdown-item[href^='javascript:doAction']")
    driver.execute_script("arguments[0].click();", logout_button)

    wait(driver)

    print("Successfully logged out.")