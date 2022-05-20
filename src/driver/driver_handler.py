from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from typing import List

from src.utils.decorators import timer
from src.utils.logger_config import logger
from src.driver.consts import TIMEOUT_DELTA
from src.utils.song_files_handler import format_song_name, wait_till_download_is_finished
from src.params import CONVERTER_URL, DOWNLOADS_DIR_PATH


def config_driver(is_hidden_run: bool):
    """Configures the setting of the driver

    Args:
        is_hidden_run: runs the program without showing the driver if is_hidden_run=True. Otherwise the driver will be
                        visible

    Returns:
        driver - the initialized driver

    """
    options = ChromeOptions()
    if is_hidden_run:
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-dev-shm-usage")

        preferences = {"download.default_directory": DOWNLOADS_DIR_PATH}
        options.experimental_options["prefs"] = preferences

    driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
    load_page(driver=driver)

    return driver


def load_page(driver):
    """Loads the page of the converter on the driver

    Args:
        driver: the driver of this run

    """
    driver.get(CONVERTER_URL)


@timer
def download_songs(driver, songs: List[str]):
    """Iteratively downloads all the songs in the list of songs

    Args:
        driver: the driver of this run
        songs: a list of songs to downloads

    """
    downloaded_song_names = []
    num_songs = len(songs)
    for index, song in enumerate(songs):
        processed_song_name = format_song_name(song_name=song)
        logger.info(f'({index + 1}/{num_songs}) Beginning process for song: {processed_song_name}')

        song_frame, song_name = get_song_frame(driver=driver, song=song)
        download_button = get_download_button(driver=driver, song_frame=song_frame)
        download_button.click()

        logger.info(f'({index + 1}/{num_songs}) Downloading: {processed_song_name}')

        clear_popup_tabs(driver=driver)
        load_page(driver)

        downloaded_song_names.append(song_name)

    wait_till_download_is_finished(downloaded_song_names=downloaded_song_names)


def get_search(driver, search_id: str, target_song: str):
    """Searches for the requested song

    Args:
        driver: the driver of this run
        search_id: the id of the search bar
        target_song: the name of the song we're attempting to download

    Returns:
        search - the results frame of the search

    """
    search = driver.find_element(by=By.ID, value=search_id)
    search.clear()
    search.send_keys(target_song)
    search.send_keys(Keys.RETURN)

    logger.debug('Got search results')
    return search


def get_song_frame(driver, song: str):
    """Finds the first frame of retrieved by the search engine

    Args:
        driver: the driver of this run
        song: the name of the song

    Returns:
        song_frame - div containing all the html data relevant to the first option found by the search engine
        song_name - the name of the youtube clip as it appears in the retrieved frame

    """
    get_search(driver=driver, target_song=song, search_id='input')
    search_results = get_loaded_page(driver=driver, by=By.ID, by_value='search-result')
    song_frame = search_results.find_element(by=By.CLASS_NAME, value='search-item')
    song_name_div = song_frame.find_element(by=By.CLASS_NAME, value='name')
    song_name = song_name_div.text

    logger.debug('Got song frame')
    return song_frame, song_name


def get_download_button(driver, song_frame):
    """Retrieves the frame of the download button of the first option found

    Args:
        driver: the driver of this run
        song_frame: the frame of the first clip option found

    Returns:
        download_button - the download button of the first clip found

    """
    song_download_div = song_frame.find_element(by=By.CLASS_NAME, value='download')
    song_download_div.click()
    download_button = get_loaded_page(driver=driver, by=By.ID, by_value='download')

    logger.debug('Got download button')
    return download_button


def get_loaded_page(driver, by: str, by_value: str, timeout: int = TIMEOUT_DELTA):
    """Awaits for a div to appear on the page

    Args:
        driver: the driver of this run
        by: the type of identifier to search by
        by_value: the value of the identifier to search by
        timeout: the maximal time to wait for the div to appear

    Returns:
        item - the requested div, if found

    """
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
    """Closes ad tabs

    Args:
        driver: the driver of this run

    """
    open_tabs = driver.window_handles
    while len(open_tabs) > 1:
        driver.switch_to.window(open_tabs[-1])
        driver.close()
        open_tabs.pop(-1)

    driver.switch_to.window(open_tabs[0])
