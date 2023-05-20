import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

df = pd.read_excel('output.xlsx', nrows=4000)
df = df.rename(columns={df.columns[0]: 'URL'})
browser = webdriver.Chrome()

for i, row in df.iterrows():
    url = row['URL']
    browser.get(url)
    browser.maximize_window()

    try:
        brand_element = browser.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/main/div[2]/div[2]/div[1]/h1[1]")
        brand = brand_element.text
    except:
        brand = ""

    try:
        title_element = browser.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/main/div[2]/div[2]/div[1]/h1[2]")
        title = title_element.text
    except:
        title = ""

    try:
        description_element = browser.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/main/div[2]/div[2]/div[3]")
        description = description_element.text.replace("\n", " ")
    except:
        description = ""

    try:
        price_element = browser.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/main/div[2]/div[2]/div[1]/div/p[1]/span[1]/strong")
        price = price_element.text.replace("₹", "")
    except:
        price = ""

    # Update the DataFrame for the current entry
    df.at[i, 'BRANDS'] = brand
    df.at[i, 'PRODUCTS'] = title
    df.at[i, 'DESCRIPTION'] = description
    df.at[i, 'PRICE'] = price

    # Save the DataFrame to the Excel file after each iteration
    df.to_excel("dataset.xlsx", index=False, header=False)

    print(f"Scraped data for row {i + 1}")

browser.quit()
