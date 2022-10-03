import os
import re
import yaml

path = "."
cnt = 0

for file in os.listdir(path):
    if file[-3:]==".md" : #判断是否为md文件
        cnt += 1
        print(cnt,file)

        with open(os.path.join(path,file),"r+",encoding="utf-8") as f:
            all_text = f.read()

        yaml_text = re.findall("---([\s\S]*?)---",all_text)[0]
        old_dic = yaml.load(yaml_text,Loader=yaml.FullLoader)
        new_dic = {
            "title": old_dic["title"],
            "author": "Hannibal0x",
            "date": old_dic["date"],
            "draft": False
        }

        yaml_res = yaml.dump(new_dic,allow_unicode=True)    #用yaml库将字典解析为yaml字符串
        # print("***",yaml_res,"***")

        res = all_text.replace(yaml_text,"\n"+yaml_res)
        with open(os.path.join(path,file),"w+",encoding="utf-8") as f:
            f.write(res)
