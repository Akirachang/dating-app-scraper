import os
import re
import json
import time
import hashlib
import random
from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv


IMAGEDIR='images'
PROFILES='scam'


extractors = {'username': re.compile('username: ([^\n]+)'),
              'username': re.compile('Username ([^\n]+)'),
              'name': re.compile('\Wname: ([^\n]+)'),
              'name': re.compile('\WName ([^\n]+)'),
              'age': re.compile('\Wage: ([^\n]+)'),
              'age': re.compile('\WAge ([^\n]+)'),
              'location': re.compile('\Wlocation: ([^\n]+)'),
              'location': re.compile('\WCity ([^\n]+)'),
              'ethnicity': re.compile('\Wethnicity: ([^\n]+)'),
              'ethnicity': re.compile('\WEthnicity ([^\n]+)'),
              'occupation': re.compile('\Woccupation: ([^\n]+)'),
              'occupation': re.compile('\WOccupation ([^\n]+)'),
              'status': re.compile('\Wmarital status: ([^\n]+)'),
              'status': re.compile('\WMarital status: ([^\n]+)'),
              'phone': re.compile('\Wtel: ([^\n]+)'),
              'phone': re.compile('\WTel ([^\n]+)'),
              'inet': re.compile('\WIP address: ([^\n]+)'),
              'inet': re.compile('\WIP address ([^\n]+)'),
              'email': re.compile('\Wemail: ([^\n]+)'),
              'email': re.compile('\WEmail ([^\n]+)'),
              'description': re.compile('\Wdescription:([\n\w\W]+)\Wmessage:'),
              'description': re.compile('\WDescription ([^\n]+)'),
              'messages': re.compile('\Wmessage:([\n\w\W]+)\WWHY IS'),
              'messages': re.compile('\WMessage ([\n\w\W]+)\WWHY IS'),
              'justifications': re.compile('\WWHY IS IT A SCAM / FAKE:([\n\w\W]+)\W This post')}

def save_image(url):
    """ Take a URL, generate a unique filename, save 
        the image to said file and return the filename."""
    ext = url.split('.')[-1]
    filename = IMAGEDIR+os.sep+hashlib.md5(url.encode('utf-8')).hexdigest()+'.'+ext
    if os.path.exists(filename):
        return filename
    try:
        content = urlopen(url).read()
        f = open(filename,'wb') 
        f.write(content)
        f.close()
    except:
        return None
    return filename 


def scrape_profile(inhandle, outfile, year, month):
  """Scrape an input scamdiggers page for the profile content
  of the scammer. """
  #Read file
  html = inhandle.read()
  soup = BeautifulSoup(html, 'html.parser')

  #Find main page content
  content = soup.find('div', {'class':'entry-content'})

  profile = {}

  #Fill in known info from URL
  profile['year_reported'] = year
  profile['month_reported'] = month

  #Extract and download images.
  profile['images'] = [save_image(img['src']) for img in content.findAll('img')]

  #Get visible text
  text = content.get_text().strip()
  # print("here")
  # print(text)
  #Parse information from text
  for keys in extractors:
    profile[keys] = ""
    
  for key in extractors:
    match = extractors[key].search(text)
    if match:
      matchtext = match.group(1).strip()
      if key in ['justifications','messages']:
        vals = matchtext.split('\n')
      else:
        vals = matchtext
      profile[key] = vals 

  #Parse annotations
  content = soup.find('div', {'class':'entry-utility'})
  profile['tags']   = [node.get_text() for node in content.findAll('a', {'rel':'tag'})]
  profile['gender'] = 'female' if 'Female profiles' in profile['tags'] else 'male'

  #Save output
  # json.dump(profile, open(outfile,'w'))
  print(profile)
  myFile = open('data/data.csv', 'a')
  writer = csv.writer(myFile)
  str = profile['year_reported']+","+profile['month_reported']+","+","


  writer.writerow(profile.values())




def enumerate_profiles(inhandle, page):
  """ Extract all the profile page links from
  this index page. """
  html = inhandle.read()
  soup = BeautifulSoup(html, 'html.parser')
  # print(soup.findAll('h1',  {'class':'entry-title'}))
  urls = []
  for node in soup.findAll('h1',  {'class':'entry-title'}):
    # print(node.findAll("a"))
    for link in node.findAll("a"):
      urls.append(link.get("href"))
  return urls


def gather_all_profiles(year, month):
  """ Walk the index pages, harvesting the profile URLs,
  and then download and process all the profiles stored 
  under this year and month. """
  page = 1
  urls = []

  print("{}-{} : Begin indexing.".format(year, month))

  while (page > 0):

    urlstring = "http://scamdigger.com/{}/{}/page/{}".format(year,month,page)  
    if page == 1:
      urlstring = "http://scamdigger.com/{}/{}/".format(year,month) 
    print(urlstring)  

    jitter = random.choice([0,1])

    try:
      urlhandle = urlopen(urlstring)
    except:
      page = 0
      continue

    urls += enumerate_profiles(urlhandle, page)
    time.sleep(1+jitter)
    page += 1

  print("{}-{} : {} profiles".format(year,month,len(urls)))

  for url in urls:
    uid = url[30:-1]
    outfile=uid+'.json'
    jitter = random.choice([0,1])
    try:
      urlhandle = urlopen(url)
    except Exception as e:
      print("Exception when handling {}".format(url))
      print(e)
    scrape_profile(urlhandle, outfile, year, month)
    time.sleep(1+jitter)
  
  print("{}-{} : complete.".format(year,month))


def scrape(startyear, startmonth, endyear, endmonth):
  """ Walk the database through the defined ranges,
  downloading everything. """
  year = startyear
  month = startmonth
  while (not (year == endyear and month == endmonth)):
    ys = "{}".format(year)
    ms = "{:02d}".format(month)
    gather_all_profiles(ys,ms) 
    if month == 12:
      year += 1
      month = 0
    month += 1


scrape(2019,2,2022,9)
