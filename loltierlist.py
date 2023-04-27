from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

url = "https://u.gg/lol/tier-list"

options = Options()
options.add_argument("--headless") # Run Chrome in headless mode
service = Service("chromedriver.exe") # Path to your Chromedriver executable
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)

file = open("Tierlist.csv", 'w')
writer = csv.writer(file)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.rt-tr-group")))

champions = []
win_rates = []
ban_rates = []
test_1 = []
champion_grades = []
matches_played = []
test_2 = []
test_7 = []
test_8 = []
test_9 = []
test_10 = []
test_11 = []
test_12 = []
test_13 = []
test_14 = []
test_15 = []
writer.writerow(['Champion Name', 'Win Rate', 'Ban Rate', 'Champion Grade', 'Matches Played This Patch'])

while True:
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    
    # Scroll back to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    
    # Check if all rows have been loaded
    rows = driver.find_elements(By.CSS_SELECTOR, "div.rt-tr-group")
    if len(rows) == len(champions):
        break
    
    # Otherwise, continue to extract the data
    for i in range(len(champions), len(rows)):
        row = rows[i]
        champion = row.find_element(By.CSS_SELECTOR, "div.rt-td:nth-of-type(3)").get_attribute("textContent")
        win_rate = row.find_element(By.CSS_SELECTOR, "div.rt-td:nth-of-type(5)").text.strip()
        ban_rate = row.find_element(By.CSS_SELECTOR, "div.rt-td:nth-of-type(6)").text.strip()
        test1 = row.find_element(By.CSS_SELECTOR, "div.rt-td:nth-of-type(1)").get_attribute("textContent")
        test2 = row.find_element(By.CSS_SELECTOR, "div.rt-td:nth-of-type(2)").text.strip() #fix this shit to show role position
        champion_grade = row.find_element(By.CSS_SELECTOR, "div.rt-td:nth-of-type(4)").text.strip()
        test7 = row.find_element(By.CSS_SELECTOR, "div.rt-td:nth-of-type(7)").text.strip() #this should be pick rate
        match_played = row.find_element(By.CSS_SELECTOR, "div.rt-td:nth-of-type(8)").get_attribute("textContent")

            
        champions.append(champion)
        win_rates.append(win_rate)
        ban_rates.append(ban_rate)
        test_1.append(test1)
        #test_2.append(test2)
        champion_grades.append(champion_grade)
        test_7.append(test7)
        matches_played.append(match_played)


        writer.writerow([champion, win_rate, ban_rate, champion_grade, match_played])

#print(champions)
#print(win_rates)
#print(ban_rates)
print(test1)
print(test2)
print(test7)
print("test 1")
print(test_1)
print("test 2")
print(test_2)
print("test 7")
print(test_7)
print("test 8")
print(matches_played)


driver.quit()

#I did not make this
