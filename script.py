import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

your_username = ""
your_password = ""
otp_secret_key = None
line_notify_token = None

max_wait_hours = 0
max_wait_minutes = 0
max_wait_seconds = 0

if line_notify_token is not None:
    import requests

if otp_secret_key is not None:
    import pyotp

def is_first_day_of_month():
    today = datetime.date.today()
    return today.day == 1

def login(username, password):
    try:
        driver.get("https://www.pythonanywhere.com/login/")
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_auth-username")))
        
        driver.find_element(By.ID, "id_auth-username").send_keys(username)
        driver.find_element(By.ID, "id_auth-password").send_keys(password)
        driver.find_element(By.ID, "id_next").click()
        
        if otp_secret_key:
            otp_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@name="token-otp_token"]')))
            totp = pyotp.TOTP(otp_secret_key)
            otp = totp.now()
            otp_input.send_keys(otp)
            
            submit_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.ID, "id_next"))
            )
            submit_button.click()
        until_3months()
        
    except Exception as e:
        print(f"登入時發生錯誤: {e}")
        raise

def until_3months():
    # Navigate to the specified URL
    web_url = f"https://www.pythonanywhere.com/user/{your_username}/webapps/#tab_id_{your_username}_pythonanywhere_com"
    driver.get(web_url)

    # Click "Run until 3 months from today"
    run_button_css_selector = 'input.btn.webapp_extend[value="Run until 3 months from today"]'
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, run_button_css_selector))).click()

def send_line_notify(message):
    try:
        if line_notify_token is not None:
            line_notify_api = 'https://notify-api.line.me/api/notify'
            headers = {'Authorization': f'Bearer {line_notify_token}'}
            payload = {'message': message}
    
            response = requests.post(line_notify_api, headers=headers, data=payload)
            response.raise_for_status()
            print("Line Notify 訊息已發送成功")
    except Exception as e:
        print(f"Line Notify 訊息發送失敗，錯誤為: {e}")

if __name__ == "__main__":

    today = datetime.date.today()

    if is_first_day_of_month():
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            wait_hours = random.randint(1, max_wait_hours) if max_wait_hours > 0 else 0
            wait_minutes = random.randint(1, max_wait_minutes) if max_wait_minutes > 0 else 0
            wait_seconds = random.randint(1, max_wait_seconds) if max_wait_seconds > 0 else 0
            wait_time = wait_hours * 3600 + wait_minutes * 60 + wait_seconds
            
            if wait_time > 0:
                print(f"等待時間：{wait_hours} 小時 {wait_minutes} 分鐘 {wait_seconds} 秒")
                time.sleep(wait_time)
            
            login(your_username, your_password)
            time.sleep(5)
            
            current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            message = f"使用者 {your_username} 的 pythonanywhere 腳本自動執行成功 本次等待時間: {wait_hours} 小時 {wait_minutes} 分鐘 {wait_seconds} 秒，執行時間: {current_time}"
            
            send_line_notify(message)
            
        except Exception as e:
            message = f"使用者 {your_username} 的 pythonanywhere 腳本自動執行失敗 錯誤為: {e}"
            send_line_notify(message)
            
        finally:
            driver.quit()
    else:
        print(f"今天不是每月的第一天，腳本未執行。當前日期: {today.strftime('%Y/%m/%d')}")
