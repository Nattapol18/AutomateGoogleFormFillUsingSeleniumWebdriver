from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time

def automate_form():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 30)
    
    try:
        print("Starting form automation...")
        
        # Open the form
        driver.get("https://docs.google.com/forms/d/e/1FAIpQLScyajy4oHpasMrCGjW1qM9wAMak_wpofCTcm7ferae9mKfpNQ/viewform")
        
        # Handle dropdown
        print("Handling dropdown selection...")
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="listbox"]')))
        dropdown.click()
        
        # Find target option
        target_text = "39. ศูนย์สื่อสารและสารสนเทศ"
        found = False
        scroll_attempts = 0
        max_scroll_attempts = 10
        
        while not found and scroll_attempts < max_scroll_attempts:
            driver.execute_script(
                "arguments[0].scrollTop += 100;", 
                wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="listbox"]')))
            )
            
            options = driver.find_elements(By.XPATH, '//div[@role="option"]')
            for option in options:
                if target_text in option.text:
                    ActionChains(driver).move_to_element(option).click().perform()
                    found = True
                    break
                    
            scroll_attempts += 1
            time.sleep(0.5)
        
        # Click Next button
        print("Moving to next page...")
        next_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//span[contains(text(), "ถัดไป")]')
        ))
        next_button.click()
        
        # Wait for page 2 to load
        print("Waiting for page 2 to load...")
        time.sleep(3)

        # Select radio buttons (option 5 for each question)
        for question_num in range(1, 6):
            try:
                # Calculate index for option 5 (last option) of each question
                radio_xpath = f"(//div[@role='radio'])[{question_num * 5}]"  # Changed to multiply by 5
                print(f"Selecting radio button 5 for question {question_num}...")
                
                radio = wait.until(EC.presence_of_element_located((By.XPATH, radio_xpath)))
                driver.execute_script("arguments[0].scrollIntoView(true);", radio)
                time.sleep(1)
                
                ActionChains(driver).move_to_element(radio).click().perform()
                time.sleep(1)
                
            except TimeoutException:
                print(f"Timeout waiting for radio button {question_num}")
                continue
        
        # Submit form by clicking the "Submit" button
        print("Clicking submit button...")
        submit_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//span[text()="ส่ง"]')
        ))
        submit_button.click()
        
        print("Form submitted successfully!")
        time.sleep(2)
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Taking screenshot...")
        driver.save_screenshot("error_screenshot.png")
        raise e
        
    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    automate_form()
