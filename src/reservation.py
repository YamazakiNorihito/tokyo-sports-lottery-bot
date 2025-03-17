# reservation.py
from selenium.webdriver.common.by import By
import time

def apply_for_lottery(driver):
    # 抽選リンクをクリック
    lottery_link = driver.find_element(By.CSS_SELECTOR, 
        'a.nav-link.dropdown-toggle.m-auto.d-table-cell.align-middle[data-target="#modal-menus"]')
    lottery_link.click()

    time.sleep(1)

    # "抽選申込み" のリンクをクリック
    lottery_apply_link = driver.find_element(By.XPATH, '//a[contains(@href, "gLotWOpeLotSearchAction")]')
    lottery_apply_link.click()

    time.sleep(10)  # 画面遷移待機