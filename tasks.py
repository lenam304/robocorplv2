from robocorp.tasks import get_output_dir, task

import os
import time
from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive

browser = Selenium()
output_directory_name = "output"
output_directory_path = os.path.join(os.path.dirname(__file__), output_directory_name)

@task
def robot_spare_bin_python():
    dowload_file_csv()
    open_the_robot_order_website()
    log_in()
    fill_the_form_using_the_data_from_the_csv_file()
    
def dowload_file_csv():
    http = HTTP()
    http.download("https://robotsparebinindustries.com/orders.csv", overwrite=True)
    
def open_the_robot_order_website():
    browser.open_available_browser("https://robotsparebinindustries.com/")
    browser.maximize_browser_window()
    
def log_in():
    browser.input_text("id:username", "maria")
    browser.input_text("id:password", "thoushallnotpass")
    browser.submit_form
    browser.wait_until_page_contains_element("xpath://h1[text()='RobotSpareBin Industries Inc.']", timeout=20)
    browser.click_link("xpath://a[@href='#/robot-order']")
    browser.wait_until_page_contains_element("xpath://p[contains(text(),'RobotSpareBin Industries Inc.')]", timeout=20)
    browser.click_button("xpath://div[@class='modal-body']/div/button[contains(@class,'dark')]")
    
def fill_the_form_using_the_data_from_the_csv_file():
    tables = Tables()
    lib = Archive()
    
    sales_reps = tables.read_table_from_csv("orders.csv")
    for sales_rep in sales_reps:
        browser.wait_until_page_contains_element("xpath://label[@for='head']", timeout=50)
        browser.select_from_list_by_value("xpath://select[@id='head']", sales_rep["Head"])
        xpath_body = f"//input[@name='body' and @value='{sales_rep['Body']}']"
        browser.click_element(xpath_body)
        browser.input_text("xpath://input[@type='number']", sales_rep["Legs"])
        browser.input_text("xpath://input[@id='address']", sales_rep["Address"])
        browser.click_button("xpath://button[@id='preview']")
        browser.wait_until_page_contains_element("xpath://div[@id='robot-preview-image']/img[contains(@alt,'Head')]", timeout=20)
        browser.wait_until_page_contains_element("xpath://div[@id='robot-preview-image']/img[contains(@alt,'Body')]", timeout=20)
        browser.wait_until_page_contains_element("xpath://div[@id='robot-preview-image']/img[contains(@alt,'Legs')]", timeout=20)
        wait_until_keyword_succeeds(oders_robot, max_attempts=10, retry_interval_seconds=1)
        
        file_path_image = os.path.join(output_directory_path, f"{sales_rep['Order number']}.png")
        image_robot = browser.screenshot("xpath://div[@id='robot-preview-image']", file_path_image)
        orders_html = browser.get_element_attribute("xpath://div[@id='receipt']", "outerHTML")
        pdf = PDF()
        file_path_pdf = os.path.join(output_directory_path, "oders", f"{sales_rep['Order number']}.pdf")
        pdf.html_to_pdf(orders_html, file_path_pdf)
        pdf.open_pdf(file_path_pdf)
        pdf.add_watermark_image_to_pdf(image_robot, file_path_pdf)
        browser.click_button("xpath://button[@id='order-another']")
        browser.wait_until_page_contains_element("xpath://p[contains(text(),'RobotSpareBin Industries Inc.')]")
        browser.click_button("xpath://div[@class='modal-body']/div/button[contains(@class,'dark')]")
    
    lib.archive_folder_with_zip(output_directory_path, 'oders.Zip')

def oders_robot():
    browser.click_element("xpath://button[contains(text(),'Order')]")
    browser.wait_until_page_contains_element("xpath://div[@id='receipt']", timeout=20)
def wait_until_keyword_succeeds(keyword, max_attempts, retry_interval_seconds, *args, **kwargs):
    attempts = 0
    while attempts < max_attempts:
        try:
            keyword(*args, **kwargs)
            return
        except Exception as e:
            print(f"Attempt {attempts+1} failed: {e}")
            attempts += 1
            time.sleep(retry_interval_seconds)

    raise RuntimeError(f"Exceeded maximum number of attempts ({max_attempts})")