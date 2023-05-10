# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 18:47:49 2021

@author: asus
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import imageio
from tqdm import trange
import random
plt.style.use("dark_background")

room = pd.read_csv("result//11_71_0.36_73room.csv",index_col = 0)
room_num = len(room.index.tolist())
person_status = pd.read_csv("result//11_71_0.36_73_person_status.csv",index_col = 0)

person_status = person_status.replace({999:room_num})
col = random.sample(person_status.columns.tolist(), 80)
slic = person_status.iloc[48*7:48*37,:]
slic = slic[col]


savepath = "people_move2/"

try:
    os.mkdir(savepath)
except:
    pass

filenames = []
num = 0
for i in trange(len(slic.index.tolist())//4):
    plt.figure(figsize=(40,8))
    num += 4
    # 绘制40张折线图
    slicc = slic.iloc[:num,:]
    if len(slicc.index.tolist()) > 48*5:
        slicc = slicc.iloc[-48*5:,:]
    plt.step(slicc.index.tolist(),slicc,alpha = 0.9,linewidth = 3)
    plt.ylim(-1, room_num+1)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)

    # 保存图片文件
    filename = f'{num}.png'
    filenames.append(savepath + filename)
    plt.savefig(savepath + filename,dpi = 100)
    plt.close()


# 生成gif

with imageio.get_writer('mygif3.gif', mode='I') as writer:
    for i in trange(len(filenames)):
        filename = filenames[i]
        image = imageio.imread(filename)
        writer.append_data(image)

# 删除折线图
#for filename in set(filenames):
#    os.remove(filename)

tot_room_count = room_num
df = pd.DataFrame(columns = list(range(tot_room_count)))
for eachtimestep in slic.index.tolist():
    status_slice = slic.loc[eachtimestep,:]
    rslice = pd.Series(dtype = np.float64)
    for each in range(tot_room_count):
        rslice.loc[each] = len(status_slice[status_slice == each])
    df.loc[eachtimestep] = rslice
    
savepath = "people_in_room2/"

try:
    os.mkdir(savepath)
except:
    pass

filenames = []
num = 0
for i in trange(len(df.index.tolist())//4):
    plt.figure(figsize=(40,8))
    num += 4
    # 绘制40张折线图
    slicc = df.iloc[:num,:]
    if len(slicc.index.tolist()) > 48*5:
        slicc = slicc.iloc[-48*5:,:]
    plt.step(slicc.index.tolist(),slicc,alpha = 0.9,linewidth = 3)
    plt.ylim(-1, df.max().max()+1)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)

    # 保存图片文件
    filename = f'{num}.png'
    filenames.append(savepath + filename)
    plt.savefig(savepath + filename,dpi = 100)
    plt.close()




# 生成gif

with imageio.get_writer('mygif4.gif', mode='I') as writer:
    for i in trange(len(filenames)):
        filename = filenames[i]
        image = imageio.imread(filename)
        writer.append_data(image)


### bar
savepath = "people_move_bar2/"

try:
    os.mkdir(savepath)
except:
    pass
     
filenames = []
num = 0
for i in trange(48*10):
    if (i % 48 <= 18) or (i % 48 >= 20*2):
        continue
    fig, ax = plt.subplots(figsize=(40, 8))
    num += 1
    # 绘制n张折线图
    plt.bar(df.columns.tolist(), df.iloc[num,:], width=0.4)
    plt.ylim(-1, df.max().max()+1)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # 设置虚线网格线
    ax.set_axisbelow(True)

    # 保存图片文件
    filename = f'{num}.png'
    filenames.append(savepath + filename)
    plt.savefig(savepath + filename,dpi = 100)
    
    # 最后一帧重复,画面停留一会
    if (i == 48*2-1):
        for j in range(5):
            filename = f'{num+j+1}.png'
            filenames.append(savepath + filename)
            plt.savefig(savepath + filename,dpi = 100)
    plt.close()


# 生成gif

with imageio.get_writer('mygif5.gif', mode='I') as writer:
    for i in trange(len(filenames)):
        filename = filenames[i]
        image = imageio.imread(filename)
        writer.append_data(image)
        
    
        
        
### lighting

savepath = "light_in_room2/"

try:
    os.mkdir(savepath)
except:
    pass

df2 = pd.read_csv("result//11_71_0.36_73_light_status.csv",index_col = 0).iloc[48*7:48*37,:]
df3 = pd.DataFrame(columns = df2.columns.tolist(),dtype = np.float64)
for each in df2.index.tolist():
     df3.loc[each] = df2.loc[each] * room["area"].values * 9 * 30 * 60 / 3600
     
df4 = pd.DataFrame(columns = df2.columns.tolist(),dtype = np.float64)
df4.loc[df2.index.tolist()[0]] = df3.iloc[0,:]
for i in range(len(df2.index.tolist())-1):
     each = df2.index.tolist()[i+1]
     df4.loc[each] = df3.iloc[:i,:].sum()
     
filenames = []
num = 0
for i in trange(48*30//4):
    
    fig, ax = plt.subplots(figsize=(40, 8))
    num += 4
    # 绘制n张折线图
    try:
        slic = df4.iloc[:num,:]
    except:
        slic = df4.iloc[:,:]
    
    if len(slic.index.tolist()) > 48*5:
        slic = slic.iloc[-48*5:,:]

    plt.plot(slic.index.tolist(), slic, linewidth=3)
    plt.ylim(-1, slic.max().max()+100)
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # 设置虚线网格线
    ax.set_axisbelow(True)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)

    # 保存图片文件
    filename = f'{num}.png'
    filenames.append(savepath + filename)
    plt.savefig(savepath + filename,dpi = 100)
    
    plt.close()

# 生成gif

with imageio.get_writer('mygif6.gif', mode='I') as writer:
    for i in trange(len(filenames)):
        filename = filenames[i]
        image = imageio.imread(filename)
        writer.append_data(image)
 