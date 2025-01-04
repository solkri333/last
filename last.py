import random
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from webdriver_manager.chrome import ChromeDriverManager #type: ignore
import time
import logging
logging.basicConfig(level=logging.INFO)
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.common.action_chains import ActionChains #type: ignore
# import keyboard
# from pyvirtualdisplay import Display
# from signup import sign
import subprocess
import os
import platform
from playwright.sync_api import sync_playwright
import string

def install_dependencies_and_browser():
    """Install necessary dependencies and Chrome on Linux-based systems."""
    if platform.system() == "Linux":
        logging.info("Detected Linux environment. Installing dependencies and Chrome...")
        
        # Install dependencies using apt-get
        os.system("""
        apt-get update && apt-get install -y \
        ca-certificates \
        wget \
        curl \
        gnupg \
        unzip \
        libx11-xcb1 \
        libxcb-dri3-0 \
        libxcomposite1 \
        libxrandr2 \
        libxi6 \
        libxdamage1 \
        libgbm1 \
        libglib2.0-0 \
        libnss3 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libcups2 \
        libdbus-1-3 \
        libxss1 \
        libxtst6 \
        fonts-liberation \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libxkbcommon0 \
        libwayland-client0 \
        libwayland-server0 \
        libgdk-pixbuf2.0-0 \
        libgles2 \
        pulseaudio \
        libasound2 \
        pulseaudio-utils \
        && apt-get clean && rm -rf /var/lib/apt/lists/*
        """)

        
        # Download and install Chrome
        os.system("""wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable""")
        
        logging.critical("Dependencies and Chrome installed successfully.")
    elif platform.system() == "Windows":
        logging.warning("Detected Windows environment. No additional installation needed.")
    else:
        raise OSError("Unsupported OS. This script only supports Linux and Windows.")


def stream(address, password):
    # display = Display(visible=False, size=(1920, 1080))
    # display.start()
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Optional: Remove if you want the UI to appear
    # chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ["enable-automation", 'enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument("--window-size=1366,768")
    chrome_options.add_argument("--lang=en-US,en;q=0.9")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument(f"--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
    # chrome_options.add_argument(f"--lang={random_language}")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_experimental_option('prefs', {
        'profile.default_content_setting_values.notifications': 2
    })
    # chrome_options.add_argument("start-maximized")
    # chrome_options.add_argument('--disable-features=DialMediaRouteProvider')  # Disable media route handling

# Disable external protocol handlers in Chrome
    # chrome_options.add_experimental_option('prefs', {
    #     "protocol_handler.excluded_schemes": {
    #         "spotify": True, "https://": True, "open": True  # This prevents Chrome from asking to open Spotify application
    #     }
    # })
    # service = Service("/usr/local/bin/chromedriver/chromedriver")
    # Start Chrome browser with the configured options
    try:
        # If ChromeDriver is in the PATH, Selenium will automatically find it
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # Using Chrome WebDriver
        driver.get("https://accounts.spotify.com/en/login")
        # Log in
        driver.find_element(By.ID, "login-username").send_keys(address)
        driver.find_element(By.ID, "login-password").send_keys(password)
        logging.info("Username entered")
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(5)
        try:
            driver.find_element(By.ID, "login-button").click()
            time.sleep(10)
        except:
            pass
        # Play track
        driver.get("https://open.spotify.com/track/1fDFHXcykq4iw8Gg7s5hG9?si=463324e9cdc149c0")
        time.sleep(10)  # Increase sleep time for page to load
        # try:
        #     alert = Alert(driver)  # Switch to the alert
        #     alert.dismiss()  # Dismiss the alert to prevent the app from opening
        #     logging.info("Alert dismissed (Spotify app prompt).")
        # except:
        #     logging.info("No alert found.")
        logging.info("Spotify song")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        driver.execute_script("window.scrollTo(0, 500)")
        try:
            # Calculate the middle of the page (viewport)
            width = driver.execute_script("return window.innerWidth")
            height = driver.execute_script("return window.innerHeight")

            # Move to the center of the page
            actions = ActionChains(driver)
            actions.move_by_offset(width // 2, height // 2).click().perform()
            logging.info("actionchain")
        except Exception as error:
            logging.info(str(error))
        try:
            # Calculate the middle of the page (viewport)
            width = driver.execute_script("return window.innerWidth")
            height = driver.execute_script("return window.innerHeight")

            # Move to the center of the page
            actions = ActionChains(driver)
            actions.move_by_offset(width // 2, height // 2).click().perform()
            time.sleep(5)
            logging.info("actionchain")
        except Exception as error:
            logging.info(str(error))
        # try:
        #     button = driver.find_element(By.XPATH, '//*[@data-testid="user-widget-link"]')
        #     actions = ActionChains(driver)
        #     actions.move_to_element(button).click().perform()
        #     time.sleep(2)
        #     logging.info("button clicked")
        # except Exception as error:
        #     logging.info("User Widget "+str(error))
        
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        driver.maximize_window()

        # keyboard.press_and_release('esc')
        driver.refresh()
        time.sleep(5)
#         try:
#             button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, '//*[@data-testid="home-button"]'))
# )

#             actions = ActionChains(driver)
#             actions.move_to_element(button).click().perform()
#             time.sleep(2)
#             logging.info("button clicked")
#         except Exception as error:
#             logging.info("Home-Button"+str(error))
        # time.sleep(2)
        # driver.back()
        # time.sleep(4)
        try:
            button = driver.find_element(By.XPATH, '//*[@data-testid="user-widget-link"]')
            actions = ActionChains(driver)
            actions.move_to_element(button).click().perform()
            time.sleep(2)
            logging.info("button clicked")
        except Exception as error:
            logging.info(str(error))
        # driver.get("https://open.spotify.com/track/1fDFHXcykq4iw8Gg7s5hG9?si=463324e9cdc149c0")
        er=1
        a=1
        b=1
        for _ in range(40):
            time.sleep(6)
            # Debugging: Print the page source to check if the play button is there
            a+=1
            if(a==2):
            #     try:
            #         play_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="play-button"]'))
            # )
            #         play_button.click()
            #         logging.info("play button")
            #     except Exception as e:
            #         logging.info(f"Error: {str(e)}")
                time.sleep(6)
                try:
                    play_buttons = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//button[@data-testid="play-button"]'))
)

                    # Create an ActionChains instance
                    actions = ActionChains(driver)

                    # Use ActionChains to click the second play button
                    actions.move_to_element(play_buttons[1]).click().perform()
                    logging.info("[1] play button")
                    time.sleep(5)
                    playback_position = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@data-testid="playback-position"]'))
)

# Get and print the current playback time
                    current_time = playback_position.text
                    logging.info("Current time"+current_time)
                    # keyboard.press_and_release("alt+r")
                except Exception as e:
                    er+=1
                    if(er==3):
                        er=1
                        driver.get("https://open.spotify.com/track/1fDFHXcykq4iw8Gg7s5hG9?si=463324e9cdc149c0")
                    driver.refresh()
                    a=1
                    logging.info(f"Error aria-label: {str(e)}")
                    continue
            else:
            #     try:
            #         play_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="control-button-skip-back"]'))
            # )
            #         play_button.click()
            #         play_button = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="play-button"]'))
            # )
            #         play_button.click()
            #     except Exception as e:
            #         logging.info(f"Error: {str(e)}")
                time.sleep(4)
                playback_position = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@data-testid="playback-position"]'))
)

# Get and print the current playback time
                current_time = playback_position.text
                logging.info(current_time)
                try:
                    play_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//button[@data-testid="control-button-skip-back"]'))
        )
                    play_buttons[0].click()
                    time.sleep(2)
                    logging.info("button skip back")
                    playback_position = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@data-testid="playback-position"]'))
)
                    current_time = playback_position.text
                    logging.info(current_time)
                    return
       #             play_buttons = WebDriverWait(driver, 10).until(
        #     EC.presence_of_all_elements_located((By.XPATH, '//button[@data-testid="play-button"]'))
        # )
        #             play_buttons[1].click()
                except Exception as e:
                    logging.info(f"Error skip back: {str(e)}")
                    a=1
                    try:
                        button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-close-btn-container"]//button'))
            )
                        button.click()
                        driver.refresh()
                    except Exception as error:
                        logging.info(str(error))
                    driver.refresh()
                    continue
            if(b==1):
                try:
                    button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-close-btn-container"]//button'))
        )
                    button.click()
                    b=2
                    # logs = driver.get_log('browser')
                    # for log in logs:
                    #     logging.warning(log)
                    logging.info("Closed")
                except Exception as error:
                    b=1
                    logging.info("Close"+str(error))
                    
            time.sleep(random.randint(90, 120))  # Wait for song to play

        driver.quit()
    except Exception as error:
        logging.info(f"Error: {str(error)}")
        # display.stop()
        driver.quit()
        
email_domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com", "mail.com", "gg.cc", "uc.cl", "aol.com", "gf.cc", "xc.at", "google.com", "au.com", "qq.com", "me.com"]
def generate_random_string(length=10):
    """Generate a random string of a given length"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_random_text(length=9):
    return '@a'+''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_names():
    return ''.join(random.choices(string.ascii_letters, k=8))

def generate_email():
    """Generate a random email address"""
    user_name = generate_random_string()
    domain = random.choice(email_domains)
    email = f"{user_name}@{domain}"
    return email

def signup(email, password):
    try:
        logging.info("Ensuring Firefox is installed...")
        subprocess.run(["playwright", "install", "firefox"], check=True)
        logging.info("Firefox is ready to use.")
        with sync_playwright() as p:
            # Launch a Chromium browser (Playwright handles browser installation for you)
            browser = p.firefox.launch(headless=True)  # Set headless=True to run without UI
            context = browser.new_context()

            # Create a new page within the context
            page = context.new_page()

            # Go to the first page
            page.goto("https://www.spotify.com/signup", timeout=60000)  # Replace with your actual URL

            # Wait for the email input field and fill it
            page.fill('input[name="username"]', email)
            time.sleep(2)

            # Wait for the "Next" button and click it (on the email page)
            next_button = page.locator('button[data-testid="submit"]')
            next_button.wait_for(state="visible")  # Wait until the "Next" button is visible
            next_button.click()
                
            # Wait for the password page to load and fill the password
            page.fill('input[name="new-password"]', password)  # Replace with the actual password

            time.sleep(2)
            # Click the "Next" button (on the password page)
            next_button=page.locator('button[data-testid="submit"]')
            if next_button.is_visible() and next_button.is_enabled():
                # Click the "Next" button on the email page and wait for the next page to load
                next_button.click()

                # Wait for the page to load completely after clicking the "Next" button
                # You can adjust this to "load" if you need more time
                logging.info("Page has loaded after clicking 'Next'")
            else:
                logging.info("Next button not visible or not clickable!")

            # Wait for the name, birthdate, and gender fields
            # Fill in the name
            page.fill('input[name="displayName"]', generate_names())
            # time.sleep(2)
            # Fill in the birth year
            page.fill('input[name="year"]', "1990")
            # time.sleep(2)
            # Select the birth month
            page.select_option('select[name="month"]', str(random.randrange(1, 12)))  # May
            # time.sleep(2)
            # Fill in the birth day
            page.fill('input[name="day"]', str(random.randrange(1, 31)))
            # time.sleep(2)
            # Click the gender option (Man)
            page.click('label:has-text("Man")')
            time.sleep(1)
            # Click the "Next" button on the name/birthdate page
            next_button=page.locator('button[data-testid="submit"]')
            if next_button.is_visible() and next_button.is_enabled():
                # Click the "Next" button on the email page and wait for the next page to load
                next_button.click()

                # Wait for the page to load completely after clicking the "Next" button
                # You can adjust this to "load" if you need more time
                logging.info("Page has loaded after clicking 'Next'")
            else:
                logging.info("Next button not visible or not clickable!")

            time.sleep(1)
            # Wait for the "Sign up" button and click it (final step)
            next_button=page.locator('button[data-testid="submit"]')
            if next_button.is_visible() and next_button.is_enabled():
                # Click the "Next" button on the email page and wait for the next page to load
                next_button.click()

                # Wait for the page to load completely after clicking the "Next" button
                # You can adjust this to "load" if you need more time
                logging.info("Page has loaded after clicking 'Next'")
            else:
                logging.info("Next button not visible or not clickable!")
            time.sleep(10)
            if next_button.is_visible() and next_button.is_enabled():
                # Click the "Next" button on the email page and wait for the next page to load
                next_button.click()
                time.sleep(10)
            context.clear_cookies()
            browser.close()
            return 0
    except Exception as error:
        logging.info("Error: "+str(error))
        return 1


def create_mails(n):
    mail_addresses=[]
    for _ in range(n):
        mail_addresses.append(generate_email())
        return mail_addresses

def main():
    install_dependencies_and_browser()
    mail_addresses=create_mails(1)
    password=generate_random_text()
    for mail_address in mail_addresses:
        try:
            if(signup(mail_address, password)): raise Exception
        except Exception as error:
            logging.info("Error during signing up: "+ str(error))
            mail_addresses.remove(mail_address)
    for mail_address in mail_addresses:
            stream(mail_address, password)
            
if __name__=="__main__":
    main()