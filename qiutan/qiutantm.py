from selenium import webdriver
import time

driver=webdriver.Chrome(executable_path='C:/Users\Yukli\AppData\Local\Google\Chrome\Application\chromedriver.exe')

driver.get('http://zq.win007.com/cn/League/2018-2019/36.html')
time.sleep(2)

name_list=driver.find_element_by_xpath('//table[@id="Table3"]/td[3]/a/text()')

print(name_list)

# for tr in name_list:
#     name=tr.xpath('./td[3]/a/text()')
#     print(name)



