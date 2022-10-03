#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import re
path = "."
cnt = 0
for file in os.listdir(path):
    if file[-3:]==".md" :
        cnt += 1
        print(cnt,file)
        with open(os.path.join(path,file),"r+",encoding="utf-8") as f:
            all_text = f.read()
        res = re.sub("http://.*/uploads/","https://cdn.jsdelivr.net/gh/Hannibal0x/img/",all_text)
        with open(os.path.join(path,file),"w+",encoding="utf-8") as f:
            f.write(res)

