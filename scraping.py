import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import geopandas
from shapely.geometry import Point
from os import makedirs

# Fonction pour attendre le chargement d'un élément
def wait_for_element_loading(driver: webdriver, class_name: str, timeout: int =120):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
    )    

# Fonction pour créer un navigateur Firefox avec les options headless
def create_firefox_browser() -> webdriver.Firefox:
    options = Options()
    # Pour cacher la fenêtre du navigateur
    options.add_argument("--headless")
    options.add_argument('--disable-blink-features=AutomationControlled')
    return webdriver.Firefox(options=options)

# Fonction pour récupérer les liens des villes et les stocker dans une liste
def get_cities() -> list:
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

# Fonction pour récupérer les données des auto écoles et les stocker dans un fichier geojson
def get_driving_schools() -> None:
    cities = get_cities()

    auto_ecoles = geopandas.GeoDataFrame(columns=["name", "position", "grade", "geometry"])
    
    for city_link in cities:
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
                dict = {"name": name, "position": position, "grade": note, "geometry": geometry }
                auto_ecoles = auto_ecoles._append(dict, ignore_index=True)
        except TimeoutException:
            print(f"Couldn't load page {driver.current_url}")
            driver.quit()
        except Exception as e:
            print(e)
            driver.quit()

    auto_ecoles.to_file("data/driving_schools.geojson", driver="GeoJSON")

# Fonction pour récupérer les données des auto écoles
def get_scraping_data() -> None:
    print("Récupération des données des auto écoles...")
    global driver
    try:
        driver = create_firefox_browser()
    except Exception as e:
        driver = create_firefox_browser()

    makedirs("data", exist_ok=True)

    get_driving_schools()
    driver.quit()
    print("Scraping terminé !")


if __name__ == "__main__":
    get_scraping_data()
    