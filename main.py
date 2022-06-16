import os
from random import random

def alnum(str):
  return ''.join(ch for ch in str if ch.isalnum())

def abbreviate(val, c):
  alist = val.split(' ')
  abbrev = ''
  i = 0
  for elt in alist:
    elt = alnum(elt)
    if (len(elt) > 0): 
      if (len(alist) <= 3):
        if (i == 0):
          abbrev += elt.casefold()
        else:
          abbrev += elt[0].upper() +  elt[1:].casefold()
      else: 
        try:
          if (i == 0):
            abbrev += elt[:4].casefold()
          else:
            abbrev += elt[0].upper() + elt[1:4].casefold()
        except:
          abbrev
    else:
      continue
    i += 1
  if len(abbrev) == 0:
    abbrev = 'constant' + str(c)
  abbrev = abbrev.replace("\n", "")
  return abbrev

def create_map(lines): 
  map = {}
  c = 0
  for elt in lines:
    if (elt != '\n' and elt.find('=') != -1): 
      temp = elt.split('=')
      var = temp[0]
      val = temp[1].split(';')[0]
      if (len(val.split(' ')) > 5):
        abbrev = 'sentence' + str(c)
        c = c + 1
      else:
        abbrev = abbreviate(val, c)
      pre = var[:var.rindex('.')]
      key = pre + '.'+ abbrev
      map[var] = key
  return map

def remove_dup_keys(map1):
  temp = []
  res = dict()
  for key, val in map1.items():
      if val not in temp:
          temp.append(val)
          res[key] = val
  return res

def remove_dynamic(lines):
  unique = []
  for line in lines:
    if (line.find('dynamic') != -1):
      continue
    else:
      unique.append(line)
  return unique

def final_templates(html, map1):
  i = 0
  for line in html:
    for key in map1:
      if (key in line):
        if (line[line.index(key) + len(key)].isdigit() == False):
          html[i] = line.replace(key, map1[key])
    i = i + 1
  return html

def read(path):
  print(path)
  with open(path, 'r') as r:
    text = r.readlines()
    return text

def write(path, lines):
  with open(path, 'w') as w:
    w.writelines(lines)

def driver_comm(i18n_path, map1):
  for root, dirs, files in os.walk(i18n_path, topdown=False):
    for name in files:
      path = os.path.join(root, name)
      if name.find(".properties") != -1:
        raw_lines = read(path)
        i = 0
        for line in raw_lines:
          for key in map1:
            if key in line:
              if (line[line.index(key) + len(key)].isdigit() == False):
                raw_lines[i] = line.replace(key, map1[key])
          i = i + 1
        write(path, remove_dynamic(raw_lines))

def driver_temp(folder_path, map1): 
  for root, dirs, files in os.walk(folder_path, topdown=False):
    for name in files:
      path = os.path.join(root, name)
      if name.find("html") != -1:
        write(path, final_templates(read(path), map1))

def main():
  src_path = input("Enter path to commons_en: ")
  i18n_path = input("Enter path to i18n: ")
  templates_path = input("Enter path to templates: ")
  map2 = create_map(read(src_path))
  map1 = remove_dup_keys(map2)
  driver_comm(i18n_path, map1)
  driver_temp(templates_path, map2)

if __name__ == "__main__":
  main()