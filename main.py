"""
    file code
    chromeDriver để lưu driver chrome nhé
    data để lưu data lúc crawl dữ liệu về
    lưu ý nhớ cài selenium về để crawl dữ liệu được nhé
    Cú pháp: pip install selenium
"""
# import các thư viện cần thiết
from selenium import webdriver # import thư viện webdriver để thao tác trên website
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import datetime # lấy time để lưu file
import os, time # time.sleep() và os để nối đường dẫn
from selenium.webdriver.chrome.service import Service
import pandas as pd

"""
    để crawl data từ iframe:
       _ xác định được id của iframe.
       _ không có id thì sẽ xác định iframe thứ mấy trong trang web.

    xpath = '/html/body/div[2]/div[1]/div'
    class city
    class total
    class daynow
    class die
"""
try:
    if __name__ == '__main__':
        data_save_file_csv = [] # 1 biến này chứa data để lưu vào file csv
        url_file_driver = os.path.join('chromeDriver', 'chromedriver.exe') # use os.path.join() to use directory chromeDriver and use file chromeDriver.exe
        driver = webdriver.Chrome(service = Service(url_file_driver))
        driver.get('https://covid19.gov.vn/') # open the url on browser
        driver.maximize_window() # to maximize the window of browser

        # di chuyển vào iframe vừa tìm được, như lúc này sẽ là iframe số 2 có index là 1
        driver.switch_to.frame(1)

        """
            find_elements_by_xpath('path') == find_elements(By.XPATH, 'path')
            nếu element có s thì sẽ trả về một danh sách(mảng) còn ngược lại thì là str
        """

        # di chuyển đến xpath mình vừa tìm được lúc nảy

        target = driver.find_elements(By.XPATH, '/html/body/div[2]/div[1]/div')

        # di chuyển đến các class và tạo danh sách các class lấy các data tương ứng
        for data in target:
            cities = data.find_elements(By.CLASS_NAME, 'city')
            totals = data.find_elements(By.CLASS_NAME, 'total')
            todays = data.find_elements(By.CLASS_NAME, 'daynow')
            deads = data.find_elements(By.CLASS_NAME, 'die')

        # lấy các phần tử trong danh sách các class
        list_of_cities = [city.text for city in cities]
        list_of_totals = [total.text for total in totals]
        list_of_todays = [today.text for today in todays]
        list_of_deads = [die.text for die in deads]

        # lấy các phần tử rồi đưa vào một biến row để add vào file csv
        for el in range(len(list_of_cities)):
            row = "{},{},{},{}\n".format(list_of_cities[el], list_of_totals[el], list_of_todays[el], list_of_deads[el])
            data_save_file_csv.append(row)

        # tạo file csv với tên là ngày giờ để phân biệt nhé. VD như ngày hôm nay
        today_ = (datetime.datetime.now()).strftime('%Y%m%d') # format theo dạng YYYYmmdd, datetime.datetime.now() sẽ lấy ngày giờ hiện hành
        file_name = f'{today_}.csv' # một dạng format string, có chữ f đứng đầu, giống như '{}'.format()
        # 'w+' là chế độ ghi đè. Có nghĩa là file cũ nó chồng nội dung luôn chứ không có ghi tiếp
        with open(os.path.join('data', file_name), 'w+', encoding='utf-8') as f: # encoding='utf-8' mở với dạng utf-8
            f.writelines(data_save_file_csv)

        time.sleep(5) # stay 5 seconds before closing the browser
        driver.close() # close the browser
    print('url is valid!')
except:
    print('url is invalid!')