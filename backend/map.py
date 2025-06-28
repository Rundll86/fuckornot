import os,json
promptDict=json.load(open(os.path.join(os.path.dirname(__file__),'prompt.json'),"r",encoding='utf-8'))
for i in promptDict:
    open(os.path.join(os.path.dirname(__file__),"prompts",f'{i}.txt'),'w',encoding='utf-8').write(promptDict[i])