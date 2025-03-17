from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

def get_driver(driver_path):
    edge_options = Options()
    edge_options.use_chromium = True
    edge_options.add_argument("--guest")
    edge_options.add_argument("--disable-default-apps")
    edge_options.add_argument("--disable-extensions")

    edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)
    return driver