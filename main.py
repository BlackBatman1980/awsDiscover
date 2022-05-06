import requests
import statistics as stats
import sys
import os
from bs4 import BeautifulSoup

totalKeys = 0

openFiles = []
SC = []
ET = []
KEYS = []
LM = []
SIZE = []

help = '''
clear -- clear screen
help -- shows this help thing
get keys -- gets all file names
afs -- average file size
info <filename> -- get info on a file
af -- accessible files
mk -- max keys
'''

if os.name == "nt":
  clear = "cls"
else:
  clear = "clear"

def usrShell():
  while True:
    usr = input("awsd> ")
    usr = usr.split()

    if usr[0] == "help":
      print(help)

    if usr[0] == "af":
      print("Total Accessible Files:",len(openFiles))
      print("File Listing:", openFiles)

    if usr[0] == "exit":
      exit()

    if usr[0] == "mk":
      maxKeys()
      
    if usr[0] == "clear":
      os.system(clear)
      
    if usr == ["get","keys"]:
      getFileNames()

    elif usr[0] == "afs":
      averageFileSize()

    elif usr[0] == "info":
      try:
        file = usr[1]
        index = KEYS.index(file)
        print("File Name:",KEYS[index])
        print("File Size:",SIZE[index])
        print("ETag:",ET[index])
        print("Storage Class:",SC[index])
        print("Last Modified:",LM[index])
      except ValueError:
        print("[x] File not found")
      except IndexError:
        print("[x] Input a file name\nEg. info test.txt")
      except Exception as Error:
        print("[x] There was an error!\n{}".format(Error))
try:
  urlname = sys.argv[1]
  proto = sys.argv[2]
except:
  print(f"[!] Please add website name and/or protocol\nEg. python3 {__file__} somewebsite http")
  exit(1)

  
base = "-assets.s3.amazonaws.com"

statusCodes = {403: "403 -- Forbidden", 404: "[x] 404 -- Not Found", 500: "500 -- Internal Server Error", 301: "301 -- Moved Permanently", 200: "[+] 200 -- OK"}

def scan():
  url = proto + "://" + urlname + base
  print("[*] Scanning:", url)
  print()
  r = requests.get(url)
  code = r.status_code
    
  if code == 200:
    enumURL(url)

  else:
    print(f"[!] Could not access assests\n[!] URL returned status code {code}")
    exit()

def averageFileSize():
  averageFileSize = round(stats.mean(SIZE))
  print("[-] Average File Size:", averageFileSize)

def maxKeys():
  keys = soup.find_all("MaxKeys")
  MK = keys[0]
  MK = str(MK)[9:]
  MK = MK.replace("</MaxKeys>","")
  print("Max Keys:",MK)

def getFileNames():
  for name in KEYS:
    print(name)

def enumURL(url):
  global totalKeys
  global soup
  global totalStorageClass
  
  print("[*] Getting Data...", url)
  content = requests.get(url).content

  soup = BeautifulSoup(content, features='xml')
  storageClass = soup.find_all('StorageClass')
  totalStorageClass = len(storageClass)
  Keys = soup.find_all('Key')
  totalKeys = len(Keys)
  lastModified = soup.find_all('LastModified')
  size = soup.find_all("Size")
  ETag = soup.find_all("ETag")
  
  for i in range(0, len(storageClass)):
    SC.append(storageClass[i].get_text())
    ET.append(ETag[i].get_text())
    KEYS.append(Keys[i].get_text())
    LM.append(lastModified[i].get_text())
    SIZE.append(int(size[i].get_text()))

  complete = 0
  for file in KEYS:
    os.system(clear)
    percent = round((complete / len(KEYS))*100, 2)
    print("[*] Searching for accessible files...\n{}% Complete".format(percent))
    url = url + "/" + file
    r = requests.get(url)
    if r.status_code == 200:
      openFiles.append(file)
    complete += 1

  os.system(clear)
  if totalStorageClass == totalKeys:
    print("[-] Total Contents Gathered:", totalKeys)
  usrShell()  
scan()