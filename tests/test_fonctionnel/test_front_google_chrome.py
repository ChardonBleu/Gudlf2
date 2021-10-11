import time

from selenium.webdriver import Chrome


driver = Chrome(executable_path='tests/test_fonctionnel/chromedriver.exe')
driver.get('http://www.google.com/');
time.sleep(2) 
access_research = driver.find_element_by_id('L2AGLb')
access_research.click()
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(2)
driver.quit()

