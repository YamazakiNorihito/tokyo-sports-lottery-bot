from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def get_driver(driver_path, debugMode=False):
    edge_options = Options()
    edge_options.use_chromium = True
    edge_options.add_argument("--guest")
    edge_options.add_argument("--disable-default-apps")
    edge_options.add_argument("--disable-extensions")
    
    if not debugMode:
        edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)

    # Wait for the browser to be fully ready
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    return driver