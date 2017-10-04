#
auth='ENTER YOUR AUTH HERE! GET IT FROM developer.ciscospark.com'

import os
from cli import cli
import time
import difflib
import requests,json,time,datetime

def save_config():

  output = cli('show run')

  timestr = time.strftime("%Y%m%d-%H%M%S")
  filename = "/bootflash/" + timestr + "_shrun"

  f = open(filename,"w")
  f.write(output)
  f.close

  f = open('/bootflash/current_config_name','w')
  f.write(filename)
  f.close

  return filename

def compare_configs(cfg1,cfg2):

  d = difflib.unified_diff(cfg1, cfg2)

  diffstr = ""

  for line in d:
    if line.find('Current configuration') == -1:
      if line.find('Last configuration change') == -1:
        if (line.find("+++")==-1) and (line.find("---")==-1):
          if (line.find("-!")==-1) and (line.find('+!')==-1):
            if line.startswith('+'):
              diffstr = diffstr + "\n" + line
            elif line.startswith('-'):
              diffstr = diffstr + "\n" + line

  return diffstr

if __name__ == '__main__':

  old_cfg_fn = "/bootflash/baseline-config"
  new_cfg_fn = save_config()

  f = open(old_cfg_fn)
  old_cfg = f.readlines()
  f.close

  f = open(new_cfg_fn)
  new_cfg = f.readlines()
  f.close

  diff =  compare_configs(old_cfg,new_cfg)

  f = open("/bootflash/diff","w")
  f.write(diff)
  f.close

  headers = {'Authorization': 'Bearer '+auth, 'Content-Type': 'application/json'}
  createroom = json.dumps({'title': 'Catalyst 9k Output Room - '+time.asctime()})
  rcreate=requests.post('https://api.ciscospark.com/v1/rooms',data=createroom,headers=headers)
  data2 = json.dumps({'markdown': '# There has been a configuration change as of ' + time.asctime() + ' :\nHere are the changes:\n'
                      +str(diff)+"###*Powered by fewer than 100 lines of Python code on a Catalyst 9K!* "
                     ,'roomId': rcreate.json()['id']})
  data3=unicode(data2, "utf-8")
  req = requests.post('https://api.ciscospark.com/v1/messages',data=data3,headers=headers)
