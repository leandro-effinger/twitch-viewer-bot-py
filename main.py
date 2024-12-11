import requests
import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import Fore
from pystyle import Center, Colors, Colorate
import os
import time

warnings.filterwarnings("ignore", category=DeprecationWarning)

def main():
    proxy_servers = {
        1: "https://www.blockaway.net",
        2: "https://www.croxyproxy.com",
        3: "https://www.croxyproxy.rocks",
        4: "https://www.croxy.network",
        5: "https://www.croxy.org",
        6: "https://www.youtubeunblocked.live",
        7: "https://www.croxyproxy.net",
    }

    # Selecting proxy server
    print(Colors.green, "Proxy Server 1 Is Recommended")
    print(Colorate.Vertical(Colors.green_to_blue, "Please select a proxy server(1,2,3..):"))
    for i in proxy_servers.items():
        print(Colorate.Vertical(Colors.red_to_blue, f"Proxy Server {i}"))
    proxy_choice = int(input("> "))
    proxy_url = proxy_servers.get(proxy_choice)

    twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Enter your channel name (e.g lero): "))
    proxy_count = int(input(Colorate.Vertical(Colors.cyan_to_blue, "How many proxy sites do you want to open? (Viewer to send)")))

    print("Viewers Send! Please Wait")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_extension('adblock.crx')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(proxy_url)

    for _ in range(proxy_count):
        driver.execute_script(f"window.open('{proxy_url}')")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(proxy_url)

        text_box = driver.find_element(By.ID, 'url')
        text_box.send_keys(f'www.twitch.tv/{twitch_username}')
        text_box.send_keys(Keys.RETURN)

    try:
        while True:
            active_connections = len(driver.window_handles)
            print(f"Active connections: {active_connections}")

            for handle in driver.window_handles:
                driver.switch_to.window(handle)
                try:
                    if "blocked" in driver.page_source:  # Replace with actual condition to detect blocked connection
                        print(f"Connection blocked, closing tab: {handle}")
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])  # Switch back to the first tab
                        driver.execute_script(f"window.open('{proxy_url}')")
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.get(proxy_url)
                        text_box = driver.find_element(By.ID, 'url')
                        text_box.send_keys(f'www.twitch.tv/{twitch_username}')
                        text_box.send_keys(Keys.RETURN)
                except Exception as e:
                    print(f"Error checking connection: {e}")

            time.sleep(3)  # Update every 3 seconds
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        print("All headless browsers have been closed.")

if __name__ == '__main__':
    main()