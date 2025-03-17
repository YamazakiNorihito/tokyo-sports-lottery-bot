import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait(driver, seconds=0.5):
    try:
        time.sleep(seconds)
        
        # 1. loadmsg が表示されるのを待つ（存在しない = 読み込み中）
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "loadmsg"))
        )
        
        # 2. loadmsg と usedate-loading が両方とも非表示になるのを待つ
        WebDriverWait(driver, 30).until(
            lambda d: all([
                _is_hidden(d, By.ID, "loadmsg"),
                _is_hidden_if_exists(d, By.ID, "usedate-loading")
            ])
        )
    except Exception as e:
        print(f"[WARN] wait skipped due to: {e}")

def _is_hidden(driver, by, identifier):
    try:
        element = driver.find_element(by, identifier)
        display = element.value_of_css_property("display")
        visibility = element.value_of_css_property("visibility")
        return display == "none" or visibility == "hidden"
    except Exception as e:
        print(f"[ERROR] {identifier} not found: {e}")
        return False  # 存在しないのは異常とみなして False

def _is_hidden_if_exists(driver, by, identifier):
    try:
        element = driver.find_element(by, identifier)
        display = element.value_of_css_property("display")
        visibility = element.value_of_css_property("visibility")
        return display == "none" or visibility == "hidden"
    except Exception:
        return True  # 存在しないなら非表示とみなす