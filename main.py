
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
        

    def get_price(self,url):
        while(True):
            try:
                self.driver.get(url)
                for elem in self.driver.find_elements_by_xpath('.//span[@class = "exponent"]'):
                    try:
                        if float(elem.text):
                            unit_price = float(elem.text)
                    except:
                        pass
            except Exception as error:
                print(f"Il y a une erreur : {error}")
            
            try:
                unit_price
                self.driver.close()
                return unit_price
            except:
                print("Impossible de recupérer le prix, nouvel essai dans 5 minutes")
                sleep(300)
                
        

        
        
def envoie_notification(prix_precedent,prix_actuel):
    try:
        token = "1813447727:AAHDPI54DetjXDDNFCMqtN-7phGvwNy9rqY"
        chat_id = "-431364858"
        message = f"Le prix vient de passer de {prix_precedent}€ à {prix_actuel}€ soit une difference de {round((prix_actuel/prix_precedent-1)*100,2)}%"
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        requests.post(url)
    except Exception as error:
        print(error)
    
def cls():
    """
    This function clear the terminal in order to get the clear view of the prints.c
    """
    os.system('cls' if os.name=='nt' else 'clear')
    
if __name__ == "__main__":
    prix_precedent = scraping().get_price("https://www.boulanger.com/ref/8008595")
    print(f"Le prix du produit est actuellement de : {prix_precedent} €")
    while(True):
        if datetime.datetime.now().minute == 0:
            cls()
            prix_actuel = scraping().get_price("https://www.boulanger.com/ref/8008595")
            if prix_precedent != prix_actuel:
                envoie_notification(prix_precedent,prix_actuel)
                prix_precedent=prix_actuel
            print(f"Le prix du produit est actuellement de : {prix_actuel} €")
            sleep(60)
        
        