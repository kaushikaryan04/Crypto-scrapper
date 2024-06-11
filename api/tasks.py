
from celery import shared_task
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .models import *
import time
@shared_task
def test_task(job_id, coins):
    # Configure WebDriver options
    options = Options()
    options.headless = True
    options.add_argument("--window-size=2560,1440")

    # Initialize WebDriver
    service = Service('/usr/local/bin/chromeDriver')  # Update with your chromedriver path
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Scraping logic
        data = {"tasks":[]}
        job = Job.objects.get(job_id = job_id)
        for coin in coins :
            d = scrape_data(driver , coin)
            data["tasks"].append(d)


        # Process and store data
        print(data)
        job = create_job_with_data(data , job)
        job.status = "COMPLETED"
        job.save()
        print("Job created with ID:", job.job_id)

    finally:
        # Quit WebDriver
        driver.quit()

def scrape_data(driver , coin):
    # Navigate to the page
    driver.get("https://coinmarketcap.com/")
    driver.maximize_window()

    # Wait for search bar to be clickable
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "sc-e20acb0c-2"))
    )

    # Perform search
    search_bar_div = driver.find_element(By.CLASS_NAME, "sc-e20acb0c-2")
    search_bar_div.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ctOzuc"))
    )
    search_input = driver.find_element(By.CLASS_NAME, "ctOzuc")
    search_input.send_keys(coin)
    time.sleep(2)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sc-230facf7-5"))
    )
    result_div = driver.find_element(By.CLASS_NAME, "sc-230facf7-5")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.TAG_NAME, "a"))
    )
    first_anchor = result_div.find_element(By.TAG_NAME, "a")
    first_anchor.click()

    time.sleep(4)

    # Extract data
    d = {}
    name = WebDriverWait(driver , 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "kcezP" ))
    )
    d["coin"] = name.text
    d["price"] = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "fsQm"))
    ).text
    price_change_element = driver.find_element(By.CLASS_NAME, "dTczEt")
    change_color = price_change_element.find_element(By.TAG_NAME, "p").value_of_css_property("color")
    sign = "-" if change_color == "red" else "+"
    d["price_change"] = sign + price_change_element.text
    d["market_cap"] = driver.find_element(By.CLASS_NAME, "hPHvUM").text.split('\n')[1]
    rank_elements = driver.find_elements(By.CLASS_NAME, "slider-value")
    d["market_cap_rank"] = rank_elements[0].text
    d["volume_rank"] = rank_elements[1].text
    volume_detail_elements = driver.find_elements(By.CLASS_NAME, "hPHvUM")
    change_color = volume_detail_elements[1].find_element(By.TAG_NAME, "p").value_of_css_property("color")
    sign = "-" if change_color == "red" else "+"
    volume_change, volume = volume_detail_elements[1].text.split('\n')
    d["volume"] = volume
    d["volume_change"] = sign + volume_change
    d["diluted_market_cap"] = volume_detail_elements[6].text
    supply_elements = driver.find_elements(By.CSS_SELECTOR, ".sc-d1ede7e3-0.hPHvUM.base-text")
    d["circulation_supply"] = supply_elements[3].text.split(" ")[0]
    d["total_supply"] = supply_elements[4].text.split(" ")[0]

    links = []
    for e in driver.find_elements(By.CLASS_NAME, "gRSwoF") :
        try :
            link = {}
            link[e.text] = e.find_element(By.TAG_NAME , "a").get_attribute("href")
            links.append(link)
        except NoSuchElementException :
            continue
    d["official_links"] = links

    print(d)
    return d

def create_job_with_data(data,job):

    for task in data['tasks']:
        coin = Coin.objects.create(job=job, name=task['coin'])
        output_data = task

        coin_output = CoinOutput.objects.create(
            coin=coin,
            price=output_data['price'],
            price_change=output_data['price_change'],
            market_cap=output_data['market_cap'],
            market_cap_rank=output_data['market_cap_rank'],
            volume=output_data['volume'],
            volume_rank=output_data['volume_rank'],
            volume_change=output_data['volume_change'],
            circulating_supply=output_data['circulation_supply'],
            total_supply=output_data['total_supply'],
            diluted_market_cap=output_data['diluted_market_cap']
        )
        coin_output.save()

        for link in output_data['official_links']:
            key , value = link.popitem()
            l = Link.objects.create(
                output=coin_output,
                name=key,
                link= value
            )
            l.save()


    return job
