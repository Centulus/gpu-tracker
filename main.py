import cloudscraper
from bs4 import BeautifulSoup
import re
import os
from csv import DictWriter
import requests
import time
from more_itertools import unique_everseen

# Fonction pour bypass CloudFlare

scraper = cloudscraper.create_scraper()

# Cooldown

time.sleep(15)

# Les listes

produit = []
prix = []
links = []

# Grab le dernier gpu

html_page = scraper.get("http://restockwatch.com/?page=stats").text
soup = BeautifulSoup(html_page, "lxml")
for link in soup.findAll('a',
                         attrs={'href':
                                re.compile("./?page=productfeed&id=")}):
  link_2 = link.get('href').replace(".", "http://restockwatch.com")
  links = link_2.replace(" ", "")

# Extraire les données

page = scraper.get(links).text
soup = BeautifulSoup(page, "lxml")
image_1 = soup.find('image', attrs={'id': 'previewimage'})
img = str(image_1).replace('<image id="previewimage" src="', '')
image_2 = img.replace('amp;', '')
image = image_2.replace('" style="width: 100%;"/>', '')
prix_1 = soup.find('div', attrs={'id': 'productprice'})
produit_1 = soup.find('div', attrs={'id': 'productname'})
pr = str(produit_1).replace(
  '<div id="productname" style="font-weight: 600;font-size: 1.4em;padding: 5px;padding-top: 0px;margin-top: 0px;text-transform: uppercase;">',
  '')
produit_2 = pr.replace('</div>', '')
px = str(prix_1).replace(
  '<div id="productprice" style="font-weight: 600;font-size: 1.4em;padding: 5px;padding-top: 0px;margin-top: 0px;text-transform: uppercase;float:right;color: #109800;">',
  '')
prix_2 = px.replace('</div>', '')
produit = produit_2.replace('\n', '')
prix = prix_2.replace('\n', '')

# Exporter dans un tableur

field_names = ['Nom du Gpu', 'Prix', 'Lien']

dict = {'Nom du Gpu': produit, 'Prix': prix, 'Lien': links}

with open('result.csv', 'a') as f_object:
  dictwriter_object = DictWriter(f_object, fieldnames=field_names)
  dictwriter_object.writerow(dict)
  f_object.close()

# Suprimmer les lignes en doubles

with open('result.csv', 'r') as f, open('gpus.csv', 'w') as out_file:
  out_file.writelines(unique_everseen(f))

# Requête vers le webhook

webhook_url = os.environ.get("DISCORD_BOT_SECRET")

data = {}

data["embeds"] = [{
  "description": prix,
  "title": produit,
  "url": links,
  "image": {
    "url": image
  }
}]

result = requests.post(webhook_url, json=data)

try:
  result.raise_for_status()
except requests.exceptions.HTTPError as err:
  print(err)
else:
  print("Message envoyé avec succès, code {}.".format(result.status_code))

# Redémarrer le script

while 1:
  os.system("python3 main.py")
  print("Redémarrage en cours...")
