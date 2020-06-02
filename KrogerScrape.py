from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3

from DataProcessing import process_data
from Database import add_purchased_items, get_uncategorized_items, create_new_category, update_item_category, \
    initialize_databases


def scrap_list_items(driver):
    #TODO: get both name and price in one iteration?
    items = []
    driver.implicitly_wait(30)
    articles = driver.find_elements_by_css_selector("article a")
    for a in articles:
        if a.get_attribute('text') != '':
            items.append([a.get_attribute('text'), 0])
    prices = driver.find_elements_by_class_name("PH-ProductCard-Total")
    for index, p in enumerate(prices):
        items[index][1] = p.get_attribute("innerHTML")
    return items

if __name__ == "__main__":

    initialize_databases()

    driver = webdriver.Chrome('/Users/abisht/Downloads/chromedriver')
    driver.get('https://www.kroger.com/')
    wait = WebDriverWait(driver, 500)
    desired_url = "https://www.kroger.com/mypurchases"
    wait.until(
        lambda driver: driver.current_url == desired_url)
    purchases = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH,"//*[contains(text(), 'See Order Details')]")))
    count = 0
    purchased_items = []
    while count < len(purchases):
        purchases = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(), 'See Order Details')]")))
        dates = driver.find_elements_by_xpath("//span[contains(@class, 'kds-Text--m mb-12')]")
        date = (dates[count].get_attribute("innerHTML"))
        purchases[count].click()
        items = scrap_list_items(driver)
        items = [[date, i[0].replace("'", ""), i[1].replace("$", "")] for i in items]
        print(items)
        purchased_items.extend(items)
        count += 1
        driver.back()

    process_data(purchased_items)


