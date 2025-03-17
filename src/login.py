from selenium.webdriver.common.by import By
from wait import wait

def login(driver, account_id, account_password):
    driver.get("https://kouen.sports.metro.tokyo.lg.jp/web/")
    
    # ログインボタンをクリック
    login_button = driver.find_element(By.ID, 'btn-login')
    login_button.click()

    wait(driver)

    # IDとパスワードを入力
    user_id = driver.find_element(By.ID, 'userId')
    user_id.send_keys(account_id)
    password = driver.find_element(By.ID, 'password')
    password.send_keys(account_password)

    # ログインをクリック
    submit_button = driver.find_element(By.ID, 'btn-go')
    submit_button.click()

    wait(driver)