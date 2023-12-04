import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import geopandas
from shapely.geometry import Point
from os import path

def wait_for_element_loading(driver, class_name, timeout=120):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
    )    

def create_chrome_browser():
    options = Options()
    # Pour cacher la fenêtre du navigateur
    options.add_argument("--headless")
    options.add_argument('--disable-blink-features=AutomationControlled')
    return webdriver.Chrome(options=options)

def get_cities():
    driver.get("https://www.vroomvroom.fr/auto-ecoles/hauts-de-seine/")
    department_class = "vv-department__link"
    cities = []
    try:
        wait_for_element_loading(driver, department_class)
        elements = driver.find_elements(By.CLASS_NAME, department_class)
        cities = [element.get_attribute("href")for element in elements]
    except TimeoutException:
        print(f"Couldn't load page {driver.current_url}")
        driver.quit()
    except Exception as e:
        print(e)
        driver.quit()
    return cities

def get_driving_schools(schools_number=38):
    cities = get_cities()

    auto_ecoles = geopandas.GeoDataFrame(columns=["nom", "position", "note", "geometry"])
    
    for i in range(schools_number):
        city_link = cities[i]
        print(city_link)
        driver.get(city_link)
        try:
            wait_for_element_loading(driver, "vv-search-item__content__title")
            list = driver.find_elements(By.CLASS_NAME, "vv-search-item")
            for element in list:
                name = element.get_attribute("data-name")
                position = element.get_attribute("data-position")
                note = element.get_attribute("data-note")
                coords = position.split(",")
                geometry = Point(coords[0], coords[1])
                dict = {"nom": name, "position": position, "note": note, "geometry": geometry }
                auto_ecoles = auto_ecoles._append(dict, ignore_index=True)
        except TimeoutException:
            print(f"Couldn't load page {driver.current_url}")
            driver.quit()
        except Exception as e:
            print(e)
            driver.quit()

    auto_ecoles.to_file("data/driving_schools.geojson", driver="GeoJSON")

def get_scraping_data():
    print("Récupération des données des auto écoles...")
    global driver
    driver = create_chrome_browser()
    get_driving_schools()
    driver.quit()
    print("Scrapping terminé !")


if __name__ == "__main__":
    asyncio.run(get_scraping_data(schools_number=30, regenerate=True))
    