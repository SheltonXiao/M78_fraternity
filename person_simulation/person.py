# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 20:42:18 2021

@author: Tong
"""

import numpy as np
import pandas as pd

### schedule type
SCHDULE_TIMEGAP = 2
SCHDULE = {
    0: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2],
    1: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0,
        5, 5, 0, 4, 4, 1, 0, 0, 0, 0, 0, 0, 5, 5, 1, 0, 0, 0, 2, 2, 2, 2,
        2, 2, 2, 2],
    2: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0,
        5, 5, 0, 4, 4, 1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2],
    3: [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0,
        5, 5, 0, 4, 4, 1, 0, 3, 3, 3, 3, 3, 5, 5, 1, 0, 0, 0, 2, 2, 2, 2,
        2, 2, 2, 2]}
### schdule choice
#holiday = pd.read_csv("holiday.csv",header = None)
#a = holiday.values.T.tolist()[0]
HOLIDAY = [  1,   2,   3,  42,  43,  44,  45,  46,  47,  48, 120, 121, 122,
           123, 124, 125, 164, 165, 166, 292, 293, 294, 322, 323, 324, 334,
           335, 336, 337, 338, 339, 340]
#weekend = pd.read_csv("weekend.csv",header = None)
#a = weekend.values.T.tolist()
#a[0].extend(a[1])
#a = a[0]
WEEKEND = [  6,  13,  20,  27,  34,  41,  48,  55,  62,  69,  76,  83,  90,
            97, 104, 111, 118, 125, 132, 139, 146, 153, 160, 167, 174, 181,
           188, 195, 202, 209, 216, 223, 230, 237, 244, 251, 258, 265, 272,
           279, 286, 293, 300, 307, 314, 321, 328, 335, 342, 349, 356, 363,
           370,   7,  14,  21,  28,  35,  42,  49,  56,  63,  70,  77,  84,
            91,  98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175,
           182, 189, 196, 203, 210, 217, 224, 231, 238, 245, 252, 259, 266,
           273, 280, 287, 294, 301, 308, 315, 322, 329, 336, 343, 350, 357,
           364, 371]


# -------daytype and schedule-------
def daytype(timerange,timegap):
    df = pd.DataFrame(index = timerange)
    df["hourOfYear"] = df.index // timegap
    df["day"] = df["hourOfYear"] // 24
    df["hourOfDay"] = (df.index) % (24*timegap)
    
    restday = list(set(HOLIDAY) | set(WEEKEND))
    restday = [each - 1 for each in restday]
    #restday2 = []
    #for each in restday:
    #    restday2.extend(list(range(restday*24*timegap,(restday+1)*24*timegap)))
    
    ran_meeting = np.random.randint(7)
    meetingday = list(range(ran_meeting,timerange[-1],(ran_meeting+1)))
    
    ran_party = np.random.randint(30)
    partyday = list(range(ran_party,timerange[-1],(ran_party+1)))
    
    # default basic weekday
    df["dayType"] = 1
    # set party day
    partyday_index = [each for each in df.index if df.loc[each,"day"] in partyday]
    df["dayType"].loc[partyday_index] = 2
    # set meeting day
    meetingday_index = [each for each in df.index if df.loc[each,"day"] in meetingday]
    df["dayType"].loc[meetingday_index] = 3
    # set rest day
    restday_index = [each for each in df.index if df.loc[each,"day"] in restday]
    df["dayType"].loc[restday_index] = 0
    
    return df

def schedule(df):
    df["schedule"] = df[["dayType","hourOfDay"]].T.apply(lambda x: 
                                                       SCHDULE[x["dayType"]][x["hourOfDay"]])
    return df


# -------create moving property matrix---------
def p_communicate(person_inroom,person_status,currenttimestep):
    # communication property
    p_indoor_com = 0.3
    p_not_move = 0.6
    p_ourdoor_com = 0.1
    move = person_status[currenttimestep-1,:] == person_inroom
    p = np.ones(person_inroom.shape)
    p[move] = p_indoor_com + p_not_move
    return p

def p_arrive():
    pass

def p_relax(conworktime,timegap):
    # linear
    p = conworktime/timegap * 0.1
    return p

def p_meeting():
    pass

def p_leave():
    pass

# ------judge status-------
"""
def worktime(person_status,currenttimestep,timegap,relax_zone):
    conworktime = np.zeros(person_status.shape[1])
    for timeperiod in range(1,timegap*5):
        to_relax = person_status[currenttimestep - timeperiod,:] == relax_zone
        work = np.zeros(person_status.shape[1])
        work[~to_relax] = 1
        conworktime += work
    return conworktime
"""
def worktime(conworktime,person_status,currenttimestep,person_inroom,meeting_room,relax_zone):
    relax = ((person_status[currenttimestep,:] == relax_zone) |
            (person_status[currenttimestep,:] == 999))
    work = ~relax
    conworktime[relax] = 0
    conworktime[work] += 1
    return conworktime

def communication_destination(communicate_status,person_inroom,person_status,room_count):
    com_person_count = len(person_status[communicate_status])
    randroom = np.random.randint(0,room_count,size = com_person_count)
    #basicroom = person_inroom[communicate_status]
    person_status[communicate_status] = randroom
    return person_status
    

# ------generate data-------
def generate_personInRoom(person_status,currenttimestep,tot_room_count):
    status_slice = person_status[currenttimestep,:]
    room_count_status_slice = []
    for each in range(tot_room_count):
        room_count_status_slice.append(len(status_slice[status_slice == each]))
    return room_count_status_slice


timerange = range(8760*2)
timegap = 2
df = daytype(timerange,timegap)
df = schedule(df)
person_count = 260 ##
tot_room_count = 7
room_count = 16
person_inroom = np.random.randint(0,room_count,size = person_count)
meeting_room_count = 4
meeting_room = np.random.randint(0,meeting_room_count,size = person_count) + room_count #存一个离得最近的会议室
relax_zone_count = 4
relax_zone = np.random.randint(0,relax_zone_count,size = person_count) + room_count + meeting_room_count#存一个离得最近的休息区

person_status = np.zeros((timerange[-1]+1,person_count))
light_status = np.zeros((timerange[-1]+1,tot_room_count))
conworktime = np.zeros(person_count)
room_count_status = np.zeros((timerange[-1]+1,tot_room_count))

for eachtimestep in timerange:
    
    
    if df.loc[eachtimestep,"schedule"] == 1: 
        #arrive
        person_status[eachtimestep,:] = person_inroom
        light_status[eachtimestep,:] = 1
    elif df.loc[eachtimestep,"schedule"] == 2: 
        #leaving
        person_status[eachtimestep,:] = 999
        light_status[eachtimestep,:] = 0
    elif df.loc[eachtimestep,"schedule"] == 3: 
        #meeting
        person_status[eachtimestep,:] = meeting_room
        light_status[eachtimestep,:] = 0
    elif df.loc[eachtimestep,"schedule"] == 4:
        #relax
        person_status[eachtimestep,:] = person_inroom
        light_status[eachtimestep,:] = 0
    elif df.loc[eachtimestep,"schedule"] == 5:
        #meals
        random_meals = np.random.randint(0,2,size = person_count)
        to_relax = random_meals == 0
        person_status[eachtimestep,to_relax] = relax_zone[to_relax]
        person_status[eachtimestep,~to_relax] = 999
        light_status[eachtimestep,:] = 1
    else:
        #default in room
        person_status[eachtimestep,:] = person_inroom 
        #communication or work
        is_relax = conworktime == 0
        person_status[eachtimestep,is_relax] = person_inroom[is_relax]
        
        p = p_relax(conworktime,timegap)
        random_relax = np.random.random(person_count)
        to_relax = random_relax < p
        to_relax = to_relax & ~is_relax
        person_status[eachtimestep,to_relax] = relax_zone[to_relax]
        
        p = p_communicate(person_inroom,person_status,eachtimestep)
        random_communicate = np.random.random(person_count)
        to_communicate = random_communicate > p
        to_communicate = to_communicate & ~is_relax & ~to_relax
        person_status[eachtimestep,:] = communication_destination(to_communicate,
                                                                  person_inroom,
                                                                  person_status[eachtimestep,:],
                                                                  room_count)
        light_status[eachtimestep,:] = 1
        
        
    #calculate work time
    conworktime = worktime(conworktime,person_status,eachtimestep,
                           person_inroom,meeting_room,relax_zone)
    #calculate person in rooms
    room_count_status[eachtimestep,:] = generate_personInRoom(person_status,
                                                              eachtimestep,
                                                              tot_room_count)
    #light status
    room_zero = room_count_status[eachtimestep,:] == 0
    light_status[eachtimestep,:][room_zero] = 0
    #if eachtimestep == 48*8+19:
#    break
