from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from typing import List

from src.utils.logger_config import logger
from src.utils.song_files_handler import format_song_name


def config_driver(converter_url: str):
    options = ChromeOptions()
    # options.add_argument('headless')
    driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(converter_url)

    return driver


def download_songs(driver, songs: List[str]):
    downloaded_song_names = []
    for song in songs:
        processed_song_name = format_song_name(song=song)
        logger.info(f'Beginning process for song: {processed_song_name}')

        song_frame, song_name = get_song_frame(driver=driver, song=song)
        download_button, next_button = get_download_button(driver=driver, song_frame=song_frame)
        download_button.click()

        logger.info(f'Downloaded: {processed_song_name}')

        next_button.click()
        clear_popup_tabs(driver=driver)

        downloaded_song_names.append(song_name)

    return downloaded_song_names


def get_song_frame(driver, song: str):
    get_search(driver=driver, target=song, search_id='input')
    search_results = get_loaded_page(driver=driver, by=By.ID, by_value='search-result')
    song_frame = search_results.find_element(by=By.CLASS_NAME, value='search-item')
    song_name_div = song_frame.find_element(by=By.CLASS_NAME, value='name')
    song_name = song_name_div.text

    logger.info('Got song frame')
    return song_frame, song_name


def get_search(driver, search_id: str, target: str):
    search = driver.find_element(by=By.ID, value=search_id)
    search.clear()
    search.send_keys(target)
    search.send_keys(Keys.RETURN)

    logger.info('Got search results')
    return search


def get_download_button(driver, song_frame):
    song_download_div = song_frame.find_element(by=By.CLASS_NAME, value='download')
    song_download_div.click()
    download_button = get_loaded_page(driver=driver, by=By.ID, by_value='download')
    next_button = driver.find_element(by=By.LINK_TEXT, value='Convert next')

    logger.info('Got download button')
    return download_button, next_button


def get_loaded_page(driver, by, by_value, timeout=10):
    try:
        driver.implicitly_wait(time_to_wait=timeout)
        item = WebDriverWait(driver=driver, timeout=timeout) \
            .until(EC.presence_of_element_located((by, by_value)))
        return item
    except TimeoutException as error:
        logger.debug(f'get_loaded_page failed for div {by_value} - {str(error)}')
        driver.quit()
        exit()


def clear_popup_tabs(driver):
    open_tabs = driver.window_handles
    while len(open_tabs) > 1:
        driver.switch_to.window(open_tabs[-1])
        driver.close()
        open_tabs.pop(-1)
