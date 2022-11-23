import cloudscraper
from bs4 import BeautifulSoup
import re
import os
from os import system, name
from csv import DictWriter
import requests
import time
from time import sleep
from more_itertools import unique_everseen
from webserver import keep_alive
import nextcord.ext
from nextcord.ext import tasks
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import discord

# Fonction pour bypass CloudFlare

scraper = cloudscraper.create_scraper()

# Garder le script en marche (SEULEMENT POUR REPLIT)

keep_alive()

# une fonction clear
def clear():
 
    # pour windows
    if name == 'nt':
        _ = system('cls')
 
    # pour GNU/linux, mac etc...
    else:
        _ = system('clear')

# une fonction chargement        
def chargement(): 
    clear()
    print('\\')
    sleep(1)
    clear()
    print("|")
    sleep(1)
    clear()
    print("/")
    sleep(1)
    clear()
    print('-')
    sleep(1)
    clear()
    print('\\')
    sleep(1)
    clear()
    print("|")
    sleep(1)
    clear()
    print("/")
    sleep(1)
    clear()
    print(r'''
   ______           __        __          
  / ____/__  ____  / /___  __/ /_  _______
 / /   / _ \/ __ \/ __/ / / / / / / / ___/
/ /___/  __/ / / / /_/ /_/ / / /_/ (__  ) 
\____/\___/_/ /_/\__/\__,_/_/\__,_/____/  © ''')
print("\n")

chargement()    

# Les listes

produit = []
prix = []
links = []

# Grab le dernier gpu
def gpugraber():
  html_page = scraper.get("http://restockwatch.com/?page=stats").text
  soup = BeautifulSoup(html_page, "lxml")
  for link in soup.findAll('a',
                         attrs={'href':
                                re.compile("./?page=productfeed&id=")}):
                                  gpugraber.link_2 = link.get('href').replace(".", "http://restockwatch.com")
                                  linkz = gpugraber.link_2.replace(" ", "")
                                  pr_link = scraper.get(linkz).text
                                  grab_link = BeautifulSoup(pr_link, "lxml")
                                  alm_links = grab_link.find('a', attrs={'id': 'productlink'})
                                  b_links = str(alm_links).replace(' ', '')
                                  c_links = b_links.replace('\n', '')
                                  d_links = c_links.replace('<aclass="btnbtn-primary"href="', '')
                                  gpugraber.links = d_links.replace(
    '"id="productlink"style="margin-bottom:0px;color:#fff!important;border-color:#ffffff;width:100%;background-color:#3aa524;font-size:20px!important;"target="new"type="button">PRODUCTLINK</a>',
    "",
)

# Extraire les données
def extract_data():
  gpugraber()
  z = gpugraber.link_2
  v = gpugraber.links
  link_2 = z
  extract_data.links = v
  page = scraper.get(link_2).text
  soup = BeautifulSoup(page, "lxml")
  image_1 = soup.find('image', attrs={'id': 'previewimage'})
  img = str(image_1).replace('<image id="previewimage" src="', '')
  image_2 = img.replace('amp;', '')
  extract_data.image = image_2.replace('" style="width: 100%;"/>', '')
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
  extract_data.produit = produit_2.replace('\n', '')
  extract_data.prix = prix_2.replace('\n', '')

# Exporter dans un tableur

#field_names = ['Nom du Gpu', 'Prix', 'Lien']

#dict = {'Nom du Gpu': produit, 'Prix': prix, 'Lien': links}

#with open('result.csv', 'a') as f_object:
 # dictwriter_object = DictWriter(f_object, fieldnames=field_names)
  #dictwriter_object.writerow(dict)
 # f_object.close()

# Suprimmer les lignes en doubles

#with open('result.csv', 'r') as f, open('gpus.csv', 'w') as out_file:
 # out_file.writelines(unique_everseen(f))

# Requête vers un bot discord

extract_data()
pro = extract_data.produit
li = extract_data.links
prx = extract_data.prix
img = extract_data.image
produit = pro
links = li
prix = prx + "$"
image = img

embed=discord.Embed(title=produit, url=links, description=prix, color=0xFF5733)
embed.set_image(url=image)
x = 1

token = os.environ.get("DISCORD_BOT_SECRET")

intents = nextcord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix = "!", intents = intents)

@bot.slash_command()
async def gpu(interaction: nextcord.Interaction):
  """Grab le dernier gpu dispo"""
  if x == 1:
    ctx = await interaction.send("<a:loading:1045094164393627749>")
    chargement()
    gpugraber()
    extract_data()
    pro = extract_data.produit
    li = extract_data.links
    prx = extract_data.prix
    img = extract_data.image
    produit = pro
    links = li
    prix = prx + "$"
    image = img
    embed=discord.Embed(title=produit, url=links, description=prix, color=0xFF5733)
    embed.set_image(url=image)
    await ctx.edit ("_ _")
    await ctx.edit(embed=embed)
          
bot.run(token)
