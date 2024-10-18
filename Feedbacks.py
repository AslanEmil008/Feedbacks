from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the WebDriver for Firefox
driver = webdriver.Firefox()

# Open the Groover website
driver.get("https://groover.co/en/")

# Wait for the page to load
time.sleep(2)  

# Option 1: Click the login button using CSS Selector
login_button_css = driver.find_element(By.CSS_SELECTOR, "span[data-test-id='loginLink']")
login_button_css.click()

# Wait for the login page to load
time.sleep(2)

# Enter email and password
email_input = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='loginFormEmailInputField']")
email_input.send_keys("aspenjadeartist@gmail.com") #Replace with your email

password_input = driver.find_element(By.CSS_SELECTOR, "input[data-test-id='loginFormPasswordInputField']")
password_input.send_keys("Scrapy*11")  # Replace with your password

# Press Enter to log in
password_input.send_keys(Keys.RETURN)

#Cliking login button
login_submit_button = driver.find_element(By.CSS_SELECTOR, "button[data-test-id='loginFormSubmitCTA']")
login_submit_button.click()
time.sleep(5)

my_campaigns_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-test-id='bandTopNavigationCampaignsCTA']"))
)
my_campaigns_link.click()

time.sleep(5)
#Finding 'song' name and cliking it for feedbacks scraping
obsessed_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='BEFORE']"))
)
obsessed_element.click()

time.sleep(5)

# Open CSV file for writing and saving in csv format
with open('BEFORE_Feedback.csv', mode='w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write the header row
    csv_writer.writerow(['Feedback', 'Song'])  # Adjust the column names as needed

    def extract_feedbacks():
        # Find all span elements containing feedback without date
        feedback_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='tw-relative tw-overflow-hidden tw-overflow-ellipsis tw-whitespace-nowrap']/span"))
        )

        # Extract feedback from each span element
        feedbacks = [feedback.text for feedback in feedback_elements if feedback.text.strip() != '']
        
        # Get the campaign name (you can adjust this part based on how you want to identify it)
        campaign_name = "BEFORE"  # Adjust as needed to capture the current campaign
        
        # Write feedbacks to CSV
        for feedback in feedbacks:
            print(feedback)  # Print the extracted feedback
            csv_writer.writerow([feedback, campaign_name])  # Save feedback and campaign to CSV

    time.sleep(3)

    while True:
        # Extract feedbacks from the current page
        extract_feedbacks()

        # Locate the "Next Page" button
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@title='Next Page']"))
            )
            # Click the button
            button.click()
            time.sleep(4)  # Wait for the next page to load
        except Exception:
            # print("No more pages to click. Ending loop.")
            break 

    extract_feedbacks()

# Close the WebDriver
driver.quit()
