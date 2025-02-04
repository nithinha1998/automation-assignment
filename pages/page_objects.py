from selenium import webdriver
from pages.web_elements import Elements as EL
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

#time sleeps are intentionally added for video recording purpose

class Pageobject:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service('/home/adcuratio/Downloads/chromedriver-linux64 (9)/chromedriver-linux64/chromedriver'))
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get('https://indeedemo-fyc.watch.indee.tv/')
        self.actions = ActionChains(self.driver)

    def read_credentials(self):
        with open('cred.csv', 'r') as pin:
            cred = pin.readlines()[1]
            return cred

    def switch_to_iframe(self):
        iframe = self.driver.find_element(By.ID, EL.IFRAME_ID)
        self.driver.switch_to.frame(iframe)

    def wait_for_element(self, by_type, locator):
        return self.wait.until(EC.visibility_of_element_located((by_type, locator)))

    def change_resolution(self, quality):
        self.driver.execute_script(f"""
            var player = jwplayer();
            var levels = player.getQualityLevels();
            for (var i = 0; i < levels.length; i++) {{
                if (levels[i].label === '{quality}') {{
                    player.setCurrentQuality(i);
                    break;
                }}
            }}
        """)
        current_quality = self.driver.execute_script("return jwplayer().getCurrentQuality();")
        levels = self.driver.execute_script("return jwplayer().getQualityLevels();")
        return levels[current_quality]['label']

    def sign_in(self):
        cred = self.read_credentials()
        self.driver.find_element(By.XPATH, EL.ACCESS_CODE_TEXT_BOX).send_keys(cred)
        self.driver.find_element(By.XPATH, EL.SIGN_IN).click()
        time.sleep(8)

    def title_page(self):
        self.wait_for_element(By.XPATH, EL.SELECT_TITLE).click()
        time.sleep(8)
        self.actions.send_keys(Keys.END).perform()
        time.sleep(3)
        self.driver.find_element(By.XPATH, EL.SELECT_DETAILS_SECTION).click()
        time.sleep(3)
        self.driver.find_element(By.XPATH, EL.SELECT_VIDEO_SECTION).click()
        self.driver.find_element(By.XPATH, EL.PLAY_BUTTON).click()
        time.sleep(18)

    def pause_video_and_continue(self):
        self.driver.execute_script("jwplayer().pause();")
        time.sleep(3)
        self.driver.switch_to.default_content()
        self.driver.find_element(By.XPATH, EL.CONTINUE_WATCHING).click()
        time.sleep(2)
        self.switch_to_iframe()

    def set_video_controls(self):
        video_player = self.driver.find_element(By.XPATH, EL.VIDEO_CONTAINER)
        self.actions.move_to_element(video_player).perform()
        volume_icon = self.driver.find_element(By.XPATH, EL.VOLUME_CONTROLLER)
        self.actions.move_to_element(volume_icon).perform()
        self.driver.execute_script("jwplayer().setVolume(50);")
        time.sleep(2)
        volume_level = self.driver.execute_script("return jwplayer().getVolume();")
        self.driver.find_element(By.XPATH, EL.SETTINGS).click()
        current_quality = self.change_resolution('480p')
        time.sleep(5)
        final_quality = self.change_resolution('720p')
        time.sleep(2)
        return volume_level, current_quality, final_quality

    def control_video(self):
        self.switch_to_iframe()
        self.pause_video_and_continue()
        volume_level, current_quality, final_quality = self.set_video_controls()
        self.driver.execute_script("jwplayer().pause();")
        self.driver.switch_to.default_content()
        return volume_level, final_quality, current_quality

    def exit(self):
        time.sleep(2)
        self.driver.find_element(By.XPATH, EL.BACK).click()
        time.sleep(3)
        self.driver.find_element(By.XPATH, EL.SIGN_OUT).click()
        time.sleep(3)
        self.driver.quit()






