# reservation.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wait import wait
import time
from selenium.webdriver.common.alert import Alert

def _accept_alert(driver, timeout=10):
    time.sleep(1)
    WebDriverWait(driver, timeout).until(EC.alert_is_present())
    alert = Alert(driver)
    alert.accept()
    time.sleep(1)


def _click_element(driver, by, selector):
    wait(driver)
    element = driver.find_element(by, selector)
    element.click()
    wait(driver)
    return element


def _select_dropdown_option(driver, select_id, target_text):
    wait(driver)
    select_element = driver.find_element(By.ID, select_id)
    for option in select_element.find_elements(By.TAG_NAME, "option"):
        if option.text.strip() == target_text:
            option.click()
            break
    wait(driver)


def start_lottery_application(driver):
    _click_element(driver, By.CSS_SELECTOR, 'a.nav-link.dropdown-toggle.m-auto.d-table-cell.align-middle[data-target="#modal-menus"]')
    _click_element(driver, By.XPATH, '//a[contains(@href, "gLotWOpeLotSearchAction")]')
    _click_element(driver, By.CSS_SELECTOR, 'button.btn.btn-primary.m-auto.btn-w-small[onclick="javascript:doLotEntry(\\"100\\")"]')


def apply_for_lottery(driver,target_date, target_time):
    # 抽選画面に遷移
    start_lottery_application(driver)

    # １回目の抽選申込
    success = click_date_and_time(driver, target_date, target_time, 1)
    
    if not success:
        print("１件目の申込みが失敗したため、２件目の処理をスキップします。")
        return
    
    # 引き続き抽選画面に遷移
    _click_element(driver, By.ID, "btn-light")
    
    time.sleep(1)

    # ２回目の抽選申込
    click_date_and_time(driver, target_date, target_time, 2)


def click_date_and_time(driver, target_date, target_time, application_index):
    _select_dropdown_option(driver, "bname", "東綾瀬公園")
    _select_dropdown_option(driver, "iname", "野球場")

    while True:
        headers = driver.find_elements(By.CSS_SELECTOR, '#usedate-table thead th.keep-all')
        if any(target_date in header.text.replace("\n", "").strip() for header in headers):
            break
        _click_element(driver, By.ID, "next-week")

    headers = driver.find_elements(By.CSS_SELECTOR, '#usedate-table thead th.keep-all')
    target_column_index = next(
        (idx for idx, header in enumerate(headers)
         if target_date in header.text.replace("\n", "").strip()),
        -1
    )

    if target_column_index == -1:
        raise Exception(f"指定された日付 {target_date} が見つかりませんでした。")
    
    rows = driver.find_elements(By.CSS_SELECTOR, '#usedate-table tbody tr')
    target_row = None
    for row in rows:
        time_text = row.find_element(By.CSS_SELECTOR, 'th').text
        if target_time in time_text:
            target_row = row
            break

    if not target_row:
        raise Exception(f"指定された時間帯 {target_time} が見つかりませんでした。")

    target_cell = target_row.find_elements(By.CSS_SELECTOR, 'td')[target_column_index]
    target_cell.click()

    _click_element(driver, By.ID, "btn-go")

    apply_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "apply"))
    )
    options = apply_dropdown.find_elements(By.TAG_NAME, "option")

    if len(options) == 1 and options[0].text.strip() == "選択してください。":
        print("申込み件数が上限なので、理を中断します。")
        return False

    if application_index == 1 and not any("申込み1件目" in option.text for option in options):
        print("１件目のオプションが無いため、２件目に切り替えます。")
        application_index = 2

    for option in options:
        if f"申込み{application_index}件目" in option.text:
            option.click()
            break

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btn-go"))
    ).click()

    _accept_alert(driver)
    print(f"申込み{application_index}件目 {target_date} の {target_time} を申請しました。")
    return True