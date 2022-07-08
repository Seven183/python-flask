from selenium import webdriver
from selenium.webdriver.common.by import By

if __name__ == '__main__':
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8') #改变标准输出的默认编码
    username = "18325649801"
    password = "qm03121212"
    driver = webdriver.Chrome()
    driver.get("https://pan.baidu.com/")
    driver.implicitly_wait(3)
    driver.maximize_window()

    driver.find_element(By.ID, "TANGRAM__PSP_4__userName").send_keys(username)
    driver.find_element(By.ID, "TANGRAM__PSP_4__password").send_keys(password)
    driver.find_element(By.ID, "TANGRAM__PSP_4__submit").click()

    # driver.save_screenshot('picture1.png')
    # print(driver.page_source.encode('utf-8').decode())
    print(driver.title)
    # driver.quit()
