import requests
import sys
from bs4 import BeautifulSoup


found = []

def generate(word):
  url = proto + "://"+ name + word
  return url
  
try:
  name = sys.argv[1]
  proto = sys.argv[2]
except:
  print(f"[!] Please add website name and/or protocol\nEg. python3 {__file__} somewebsite http")
  exit(1)

try:
  outFile = sys.argv[3]
  OUT = True
except:
  OUT = False
  
wordlist = ["-assets.s3.amazonaws.com","-www.s3.amazonaws.com","-public.s3.amazonaws.com","-private.s3.amazonaws.com"]

statusCodes = {403: "403 -- Forbidden", 404: "[x] 404 -- Not Found", 500: "500 -- Internal Server Error", 301: "301 -- Moved Permanently", 200: "[+] 200 -- OK"}

def scan():
  for i in wordlist:
    url = generate(i)
    print("[+] Scanning:", url)
    r = requests.get(url)
    code = r.status_code
    try:
      print(statusCodes[code])
    except:
      print(code)

    if code == 200:
      found.append(url)
      
    print("\n")


def writeOUT(data):
  print("[*] Writing Out To File")
  file = open(outFile, "a")
  file.write(data)
  file.close()
  
def enumURL():
  for url in found:
    print("[*] Enumerating", url)
    content = requests.get(url).content

    soup = BeautifulSoup(content, features='xml')
    storageClass = soup.find_all('StorageClass')
    Keys = soup.find_all('Key')
    lastModified = soup.find_all('LastModified')
    size = soup.find_all("Size")
    ETag = soup.find_all("ETag")
    
    for i in range(0, len(storageClass)):
      print("Storage Class: " + storageClass[i].get_text())
      print("ETag: " + ETag[i].get_text())
      print("Key: " + Keys[i].get_text())
      print("Last Modified: " + lastModified[i].get_text())
      print("Size: " + size[i].get_text())
      print("\n")

      if OUT:
        enumOut = {'Storage Class': storageClass[i].get_text(), 'ETag': ETag[i].get_text(), 'Key': Keys[i].get_text(), "lastModified": lastModified[i].get_text(), "Size": size[i].get_text()}
        writeOUT(str(enumOut))
        
    
scan()
enumURL()