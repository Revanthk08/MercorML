#importing modules
from selenium import webdriver
import pandas as pd
from time import sleep
from selenium.webdriver.common.by import By
browser = webdriver.Chrome()
products=[]
for i in range(1000):
    browser.get('https://www.myntra.com/clothing?p='+ str(i+1))
    browser.maximize_window()
    for index in range(1,51):
        xpath="//*[@id='desktopSearchResults']/div[2]/section/ul/li["+ str(index)+"]/a"
        product_data = browser.find_element(By.XPATH, xpath).get_attribute('href')
        products.append(product_data)
    

df=pd.DataFrame(products)
df.to_excel("output.xlsx", index=False, header=False)
