# main.py
from driver_setup import get_driver
from login import login
from logout import logout
from reservation import apply_for_lottery
from config import DRIVER_PATH, TARGET_DATE, TARGET_TIME, DEBUG_MODE
import argparse
import pandas as pd
from time import sleep
import random

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--driver_path", type=str, help="Driver path override", default=None)
    args = parser.parse_args()
    
    driver_path = args.driver_path if args.driver_path else DRIVER_PATH
    if args.driver_path:
        print(f"Overriding driver path to: {args.driver_path}")
    
    driver = get_driver(driver_path,DEBUG_MODE)

    data = pd.read_csv('./account.csv')
    for index, row in data.iterrows():
        try:
            account_id = row['id']
            account_password = row['password']
            account_name = row['name']
            print(f"account_name: {account_name}")

            max_retries = 3
            for attempt in range(max_retries):
                try:
                    login(driver, account_id, account_password)
                    apply_for_lottery(driver, TARGET_DATE, TARGET_TIME)
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"Attempt {attempt + 1} Retrying in {wait_time:.2f} seconds...")
                    sleep(wait_time)

            logout(driver)
        
        except Exception as e:
            print(f"Error processing row {index}: {e}")
    driver.quit()

if __name__ == "__main__":
    main()