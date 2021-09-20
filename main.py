from seleniumwire import webdriver
from time import sleep
from selenium.webdriver.firefox.options import Options
import os,requests,datetime

class scraping():
    """
    Cette classe regroupe les differentes fonctions de scraping utilisées pour récuperer les données
    """
    def __init__(self):
        #On initialise le headless webbrowser
        options = Options()
        options.headless = True
        profile = webdriver.FirefoxProfile()
        #On met la langue en français pour pouvoir reconnaitre les élements
        profile.set_preference('intl.accept_languages', 'fr-FR, fr')
        
        self.driver = webdriver.Firefox(options=options,firefox_profile=profile)
        
    def track_price(self,url):
        self.driver.get(url)
        init_value = 0
        while(True):
            if datetime.datetime().now().hour == 10:
                try:
                    selector = self.driver.find_elements_by_xpath('.//p[@class = "fix-price"]')
                    for elem in selector:
                        value = elem.text
                        
                    if value !=init_value:
                        self.envoie_notification(init_value,value)
                        init_value=value
                        print(f"le nouveau prix est de {init_value}")
                    
                    sleep(600)
                    
                    self.driver.refresh()
                except KeyboardInterrupt or Exception:
                    self.driver.quit()
            
            
    def envoie_notification(self,prix_precedent,prix_actuel):
        try:
            token = "1813447727:AAHDPI54DetjXDDNFCMqtN-7phGvwNy9rqY"
            chat_id = "-431364858"
            message = f"Le prix vient de passer de {prix_precedent}€ à {prix_actuel}€ "
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
            requests.post(url)
        except Exception as error:
            print(error)


if __name__ == "__main__": 
    scraping().track_price("https://www.boulanger.com/ref/8008595")
    
        