#!/usr/bin/env python
# coding=UTF-8
import sys

import json
import re
import facebook
import urllib2
#import urllib3
import time
import requests
import os

import datetime
import pytz
import csv
import time

#python 3
#To continue to collect more data that I  finished at past
#This time all data is located at 2017-04-06
global name_count
name_count = 0
def add_Post_to_Postdic(Post,Post_dict):

    us = pytz.timezone('US/Pacific')
    Post_dt = datetime.datetime.strptime(Post['created_time'][0:18] , '%Y-%m-%dT%H:%M:%S').replace(tzinfo=us)
    Post_dt = Post_dt.astimezone(pytz.utc)
    week = datetime.date(Post_dt.year, Post_dt.month, Post_dt.day).weekday()
    hour = Post_dt.hour
    post_len = 0
    shares_number = '0'
    if( 'shares' in Post):
        shares_number = Post['shares']['count']
    if('message' in Post):
        post_message = message_clear(Post['message'])
        post_len =  len(post_message)
    else:
        post_message = 'null'

    if('type' in Post):
        post_type = Post['type']
    else:
        post_type = 'null'   
     
    link,picture,story = "null","null","null"
    if'link' in Post:
        link = Post['link']
    if 'picture' in Post:
        picture = Post['picture']
    if 'story' in Post:
        story = Post['story'].encode('utf-8').replace(",","£¬")

    Post_dict[ Post['id'] ] = {"PostId":Post['id'],"week":week,"hour":hour,"shares":shares_number,"created_time":Post['created_time'],"updated_time":Post['updated_time'] \
    ,"characters":post_len,"message":post_message,"link":link,"picture":picture,"story":story,"type":post_type}

def change_Username_metion(line):
    result = line
    emoji_list = ['@@','@_@']
    #print (line)
    if '@' in line :
        start = line.index("@")
        #print (start)
        emoji = False

        if line[start:start+2] =='@@' or line[start:start+3] =='@_@':
            emoji = True
        finish = -1
        if emoji==False:
            if(" " in line[start:]):
                finish = line[start:].index(" ") + start

            if(start == 0 ):
                if(finish == -1):
                    result = line.replace(line[start:len(line)],"<Usermention>")
                else:
                    result = line.replace(line[start:finish],"<Usermention>")
            elif(line[start-1] ==" "):
                if(finish == -1):
                    result = line.replace(line[start:len(line)],"<Usermention>")
                else:
                    result = line.replace(line[start:finish],"<Usermention>")

        return result
    return result

# to remove url
def del_url(line): #return re.sub(r'https?:\/\/.*', "", line).lower()
    result = ''
    # p_list = ["s'","'s"]
    #print (re.sub(r'https?:\/\/\S*', "", line).lower().split(' '))
    for i in re.sub(r'https?:\/\/\S*', "", line).lower().split(' '):
        # if "s'" in i:
        #     print (i)
        #     result += i.replace("s'"," ")
        # elif "'s" in i:
        #     #print (i)
        #     result += i.replace("'s"," ")
        # elif i.startswith("'"):
        #     #print (i)
        #     result += i.replace("'"," ") + " "
        # elif i.endswith("'"):
        #     #print (i)
        #     result += i.replace("'"," ")
        # else:
            result += i + " "
                

    return result
def message_clear(message):

    result = message.replace(",","£¬".decode("utf-8")).replace("\r"," ").replace('\n','<NL>')
    #print result
    if(isinstance(result, unicode)):
        result = result.encode('utf-8')
        #print 'encode!',type(message)

    # result = message
    # print result,type(result)
    # result = result.replace(',','£¬'.decode('utf-8'))
    # print result


    # result = result.replace("\r"," ")
    # result = result.replace("\n","<NL>")
    
    #result = result.strip()

    #result = del_url(result)
    original_len = len(result)
    for  i in range(100):
        result = change_Username_metion(result)
        if original_len == len(result):
            break
        else:
            original_len = len(result)

    return result


def main():
    #set  intialize path.date.id_list
    name_count = 0

    until = 'until=2017-05-26'
    since = 'since=2017-04-07'

    Path = "../../data/"
    dir_layer1 = ""
    dir_layer2 = ""
    graph = facebook.GraphAPI(access_token = 'EAAEpCePdcvgBAKKBxMoNfKSTUZA359xgk0ZAWuU6BYP5ZBl11Cbri74fZAg7A4ZBQfufaiwH60aZAwuiRImcWTnFsZAFVR6OTG5nZAdC7wqsir9xdXFEF6HGr7lZB2haZBtnU53bCZCVXZC6gBmxncKVRnZCzi9J3bKpuZCtsZD', version = '2.7')
    graph2 = facebook.GraphAPI(access_token = 'EAAEpCePdcvgBAKKBxMoNfKSTUZA359xgk0ZAWuU6BYP5ZBl11Cbri74fZAg7A4ZBQfufaiwH60aZAwuiRImcWTnFsZAFVR6OTG5nZAdC7wqsir9xdXFEF6HGr7lZB2haZBtnU53bCZCVXZC6gBmxncKVRnZCzi9J3bKpuZCtsZD', version = '2.8')
    start = False
    total_page_count = 0
    reaction_page_count = 0
    page_count = 0


    #FanpageList = open("./post_dir_traverse_list",'r')
    page_id ='330133697344117_433555783668574'
    fileName = 'LOOKER'
    #print ("No.",page_count,fileName.decode('utf-8') )
    print "Start crawling"
    Post_dict = {}
    get_post_comment(Path,Post_dict,graph)

def get_next_post(next_page,Post_dict):
    while len(next_page) > 0:
        error_flag2 = False
        try:
            req = urllib2.Request(next_page)
            content = urllib2.urlopen(req).read()
        except Exception as e:
            error_flag2 = True
            print "error_flag2:HTTP ERROR\n"
            loop = True
            while loop:
                try:
                    req = urllib2.Request(next_page)
                    content = urllib2.urlopen(req).read()
                    error_flag2 = False
                    break
                except Exception as e2:    
                    time.sleep(2)
                    print (str(e2)+"\terror\n")
        if (error_flag2) != True:
            next_resu = json.loads(content, strict=False)
            ob_length = len(next_resu['data'])
            for i in range(0,ob_length,1):
                ob = next_resu['data'][i]
                add_Post_to_Postdic(ob,Post_dict)

            if((len(next_resu) > 1)):
                if(len(next_resu['paging']) > 1):
                    next_page = next_resu['paging']['next']
                    print ("\n" + next_page)
                    get_next_post(next_page,Post_dict)
                else:
                    next_page = ''
            else:
                next_page = ''
        time.sleep(0.5)

def get_resp(path,graph,limit_number):
    resp = 'null'
    try:
        resp = graph.get_object(path)   #Ã¿´Î300‚€ ¿ÉÄÜ•þ‰Äµô
        #resp = graph.get_object(path, offset=2000)
        #resp = graph.get_object(path,limit=1000)  
        return resp
    except  facebook.GraphAPIError as g:
        gstr = "Object with ID" 
        gstr2 = "does not exist"
        if (gstr in g.message) & (gstr2 in g.message):
            print (g.message)
        else:
            print (g.message)
            if "User request limit reached" in g.message:
                time.sleep(60)
            k = 0
            while k == 0:
                time.sleep(5)
                try:
                    resp_2 = graph.get_object(path,limit=200)    #×Ô„ÓœpÁ¿ ¿É×ÔÓ†
                    error_flag3 = 0
                    k = k + 1
                    return resp
                except facebook.GraphAPIError as g2:
                    if "User request limit reached" in g.message:
                        time.sleep(60)      
def get_reaction_dict(post_id,graph,limit):  

    reaction_list = ["LOVE","WOW","HAHA","SAD","ANGRY","THANKFUL"]    #ÕÒÃ¿‚€reactionÓÐ¶àÉÙÈË°´
    reaction_dict = {}
    for reaction in reaction_list:
        reaction_path  = post_id+"?fields=created_time,reactions.limit(0).type("+reaction+").summary(1)"
        reaction_resp = get_resp(reaction_path,graph,limit)
        reaction_dict[reaction ] = reaction_resp['reactions']['summary']['total_count']
        time.sleep(0.5)
    return reaction_dict

def get_reaction_dict2(post_id,graph,limit,comment_reaction_name_file):  
    reaction_path  = post_id+"?fields=created_time,reactions.limit("+str(limit)+")"
    reaction_resp = get_resp(reaction_path,graph,limit)
    reaction_dict = {"LOVE":0,"WOW":0,"HAHA":0,"SAD":0,"ANGRY":0,"THANKFUL":0,"LIKE":0}
    #print reaction_resp
    if 'reactions' in reaction_resp:
        for reaction in reaction_resp['reactions']['data']:
            reaction_dict[ reaction['type'] ] +=1
            #print type(post_id),type(reaction['id']),type(reaction['name']),type(reaction['type'])
            comment_reaction_name_file.write(str(post_id.encode('utf-8'))+','+str(reaction['id'].encode('utf-8'))+','+str(reaction['name'].encode('utf-8'))+','+str(reaction['type'].encode('utf-8'))+'\n')
    time.sleep(0.2)
    return reaction_dict



def write_comment_csv(post_id,comment,comment_reaction_dict,outfile):
    #PostID,name,userID,message,like_count,comment_count,created_time,comment_id,parentID,LOVE,WOW,HAHA,SAD,ANGRY,THANKFUL
    try:
        global name_count 
        name_count +=1
        print name_count,comment['message'],comment['from']['name']
        output = str(post_id)+","+str(comment['from']['name'].encode('utf-8'))+','+str(comment['from']['id'])+','
        # print str(comment['message'].encode('utf-8'))

        output+= str(comment['message'].encode('utf-8'))
        #output+=(message_clear(comment['message']))+',' 
        output+=str(comment['like_count'])+','
        if 'comment_count' in comment:
            output +=(str(comment['comment_count'])+',')
        else :
            output +='0,'
        output+=str(comment['created_time'])+','+str(comment['id'])
        if 'parent'in comment:
            output+=','+str(comment['parent']['id'])+','
        else:
            output+=',null,'
        # output+=str(comment_reaction_dict["LOVE"])+","+str(comment_reaction_dict["WOW"])+","+str(comment_reaction_dict["HAHA"])+","
        # output+=str(comment_reaction_dict['SAD'])+","+str(comment_reaction_dict['ANGRY'])+","+ str(comment_reaction_dict['THANKFUL'])+"\n"
        output += "\n"
        outfile.write(output)
    except Exception as e:
        print e  
        print comment

def get_post_comment(result_path,Post_dict,graph):
    # page_id = ""
    # for post_id in Post_dict:
    #     page_id = post_id.split("_")[0]
    #     break
    # result_comment =  result_path + page_id + "_comment_reaction.csv"
    PageID = '349314125104211'
    PostID = PageID+'_'+'1501930349842577'

    #PostID = '422000531331494_584377425093803'
    since="2017-06-01"
    until="2017-07-04"
    #result_comment =  './name/name_'+PostID+"_"+since+"_"+until+'.csv'#result_path + page_id + "_comment_reaction.csv"
    result_comment =  './name/name_'+PostID+'.csv'#result_path + page_id + "_comment_reaction.csv"

    with open(result_comment, 'w') as outfile:
        outfile.write("PostID,name,userID,message,like_count,comment_count,created_time,comment_id,parentID,LOVE,WOW,HAHA,SAD,ANGRY,THANKFUL\n")
        with open("123", 'a') as comment_reaction_name_file:
            comment_reaction_name_file.write("CommentID,id,name,type\n")
            Post_dict = [PostID]

            for post_id in Post_dict:
                post_comments_count = 0

                time.sleep(0.5)
                error_flag3 = 0
                #comment •þ×¥µ½µÄ–|Î÷ ¿ÉÒÔµ½FBé_°lÕß¾Wí“ ÕÒ×Ô¼ºÒªµÄ™ÚÎ»Ãû·Q
                comment_path = "/" + post_id + "/comments?fields=from,message,message_tags,created_time,id,comments.limit(50){from,id,message,message_tags,created_time,like_count,parent,can_remove,user_likes},comment_count,user_likes,can_remove,parent,like_count&filter=stream"
                #comment_path = "/" + post_id + "?fields=comments.filter(stream).limit(100){id,created_time,from,message}"
                #comment_path = "/" + post_id + "/comments?fields=from,message,message_tags,created_time,id,comments.limit(50){from,id,message,message_tags,created_time,like_count,parent,can_remove,user_likes},comment_count,user_likes,can_remove,parent,like_count"+"&"+since+"&"+until
                #comment_path = "/" + post_id + "/comments?fields=from,message,created_time,id,comments.limit(50){from,id,message,message_tags,created_time,like_count,parent,can_remove,user_likes},comment_count"+"&"+since+"&"+until

                resp_2 = get_resp(comment_path,graph,1000)  #Ã¿´Î300‚€ ¿ÉÄÜ•þ‰Äµô
                print resp_2
                if int(error_flag3) == 0:
                    #PostID,name,userID,message,like_count,comment_count,created_time,comment_id,parentID,LOVE,WOW,HAHA,SAD,ANGRY,THANKFUL
                    ob_len = 0

                    ob = resp_2['data']
                    ob_len += len(ob)
                    print (len(resp_2['data']))
                    for index,comment in enumerate(ob):
                        print("comment No.",index)
                        if (len(comment['message'])!=8 ):
                            continue

                        #comment_reaction_dict = get_reaction_dict(comment['id'],graph,100)
                        #comment_reaction_dict = get_reaction_dict2(comment['id'],graph,1000,comment_reaction_name_file)
                        comment_reaction_dict = {}
                        write_comment_csv(post_id,comment,comment_reaction_dict,outfile)

                        resu_comcom = comment['comment_count']
                        if('comments' in comment):
                            for index,comcom in enumerate(comment ['comments']['data']):
                                if (len(comcom['message'])==8 ):
                                    print  ("comcom No.",index)
                                    write_comment_csv(post_id,comcom,comment_reaction_dict,outfile)

                        if int(resu_comcom) > 50:
                            next_ob_page = comment ['comments']
                            if len(next_ob_page['paging']) > 1:
                                next_comcom_page = next_ob_page['paging']['next']
                                get_com_com(next_comcom_page,outfile,post_id,comment_reaction_name_file)    #ÕÒsubcomment

                    print ("Get F and Comment_1 Ok\n")
                    print len(resp_2)
                    if(len(resp_2) > 1):
                        print len(resp_2['paging']),resp_2['paging']
                        if(len(resp_2['paging']) > 1):
                            print "next!!"
                            n = 1
                            next_page = resp_2['paging']['next']
                            next_page = next_page.replace("limit=25","limit=1000")

                            ob_len+= get_next_comment(next_page,post_id,n,graph,outfile,comment_reaction_name_file)  #ÕÒÏÂN¹Pcomment
                    #Post_dict[ post_id]['comments'] = (ob_len)
        
        print PostID    #return 0

def get_next_comment(next_page,post_id,n,graph,outfile,comment_reaction_name_file):
    while len(next_page) > 0:
        error_flag4 = 0
        try:
            req = urllib2.Request(next_page)
            content = urllib2.urlopen(req).read()
        except urllib2.HTTPError as e:
            error_flag4 = 1
            print 'get_next_comment request error'
            print (e.message)
            print(next_page) 
            #return 0 
            i = 0
            time.sleep(5)
            while i == 0:
                try:
                    req = urllib2.Request(next_page)
                    content = urllib2.urlopen(req).read()
                    error_flag4 = 0
                    i = i + 1
                except urllib2.HTTPError as e2:
                    print (e2)
                    print (post_id + " error\n")

        if int(error_flag4) == 0:
            time.sleep(2)
            next_resu_j_2 = json.loads(content, strict=False)
            next_ob = next_resu_j_2['data']

            for comment in next_ob:
                resu_id =comment['id']
                #print comment['message'],len(comment['message'])
                if (len(comment['message'])!=8):
                    continue     
                comment_reaction_dict = ""#get_reaction_dict2(comment['id'],graph,1000,comment_reaction_name_file)
                write_comment_csv(post_id,comment,comment_reaction_dict,outfile)


                if 'comments' in comment:
                    for index,comment_coment in enumerate(comment['comments']['data']):
                        if(len(comment_coment['message'])!=8):
                            continue
                        comment_reaction_dict = ""#get_reaction_dict2(comment_coment['id'],graph,1000,comment_reaction_name_file)
                        write_comment_csv(post_id,comment_coment,comment_reaction_dict,outfile)

                resu_comcom = comment['comment_count']
                if int(resu_comcom) > 50:
                    next_ob_page = comment['comments']
                    if len(next_ob_page['paging']) > 1:
                        next_comcom_page = next_ob_page['paging']['next']
                        next_comcom_page = next_comcom_page.replace("limit=25","limit=1000")

                        get_com_com(next_comcom_page,outfile,post_id,comment_reaction_name_file)    #ÕÒsubcomment
            n = n + 1
            print ("Get Comment_next Ok\n")
            ob_len = 0

            if(len(next_resu_j_2) > 1):
                print len(next_resu_j_2['paging']),next_resu_j_2['paging']
                if(len(next_resu_j_2['paging']) > 2):
                    next_page = next_resu_j_2['paging']['next']
                    next_page = next_page.replace("limit=25","limit=1000")
                    ob_len+= get_next_comment(next_page,post_id,n,graph,outfile,comment_reaction_name_file) 
                else:
                    next_page = ''
            else:
                next_page = ''
            return ob_len

def get_com_com(next_page,outfile,post_id,comment_reaction_name_file):
    error_flag5 = 0
    try:
        req = urllib2.Request(next_page)
        content = urllib2.urlopen(req).read()
    except urllib2.HTTPError as e:
        error_flag5 = 1
        print (e.message)
        k = 0
        while k == 0:
            time.sleep(5)
            try:
                req = urllib2.Request(next_page)
                content = urllib2.urlopen(req).read()
                error_flag5 = 0
                k = k + 1
            except urllib2.HTTPError as e2:
                print (e2.message)
    except requests.exceptions.ConnectionError as r:
        error_flag5 = 1
        print (r.message)
        k2 = 0
        while k2 == 0:
            time.sleep(5)
            try:
                req = urllib2.Request(next_page)
                content = urllib2.urlopen(req).read()
                error_flag5 = 0
                k2 = k2 + 1
            except requests.exceptions.ConnectionError as r2:
                print (r2.message)
                time.sleep(60)

    if int(error_flag5) == 0:
        next_comcom = json.loads(content, strict=False)
        ob = next_comcom['data']
        ob_len = len(ob)
        for comment in ob:
            if (len(comment['message'])!=8):
                continue  

            resu_id = comment['id']
            graph = facebook.GraphAPI(access_token = 'EAAEpCePdcvgBAKKBxMoNfKSTUZA359xgk0ZAWuU6BYP5ZBl11Cbri74fZAg7A4ZBQfufaiwH60aZAwuiRImcWTnFsZAFVR6OTG5nZAdC7wqsir9xdXFEF6HGr7lZB2haZBtnU53bCZCVXZC6gBmxncKVRnZCzi9J3bKpuZCtsZD', version = '2.8')
            comment_reaction_dict ={}# get_reaction_dict2(comment['id'],graph,1000,comment_reaction_name_file)
            write_comment_csv(post_id,comment,comment_reaction_dict,outfile)


            # output = str(post_id)+","+str(comment['from']['name'].encode('utf-8'))+','+str(comment['from']['id'])+','
            # output += message_clear(comment['message'])+','+str(comment['like_count'])+',' 
            # if 'comment_count' in comment:
            #     output +=(str(comment['comment_count'])+',')
            # else :
            #     output +='0,'
            # output +=str(comment['created_time'])+','+str(comment['id'])+','+comment['parent']['id']+','
            # output +=str(str(comment_reaction_dict["LOVE"])+","+str(comment_reaction_dict["WOW"])+","+str(comment_reaction_dict["HAHA"])+",")
            # output +=str(comment_reaction_dict['SAD'])+","+str(comment_reaction_dict['ANGRY'])+","+ str(comment_reaction_dict['THANKFUL'])+"\n"
            # outfile.write(output)

            if 'comments' in comment:
                for comment_coment in comment['comments']['data']:
                    if(len(comment_coment['message'])!=8):
                        continue
                    comment_reaction_dict = {}#get_reaction_dict2(comment_coment['id'],graph,1000,comment_reaction_name_file)
                    write_comment_csv(post_id,comment_coment,comment_reaction_dict,outfile)
                    # output = str(post_id)+","+str(comment_coment['from']['name'].encode('utf-8'))+','+str(comment_coment['from']['id'])+','
                    # output+=(message_clear(comment_coment['message']))+',' 
                    # output+=str(comment_coment['like_count'])+',0,'+str(comment_coment['created_time'])+','+str(comment_coment['id'])+','+str(comment_coment['parent']['id'])+','
                    # output+=str(comment_reaction_dict["LOVE"])+","+str(comment_reaction_dict["WOW"])+","+str(comment_reaction_dict["HAHA"])+","
                    # output+=str(comment_reaction_dict['SAD'])+","+str(comment_reaction_dict['ANGRY'])+","+ str(comment_reaction_dict['THANKFUL'])+"\n"
                    # outfile.write(output)

        if(len(next_comcom) > 1):
            if(len(next_comcom['paging']) > 2):
                n = 1
                next_page = next_comcom['paging']['next']
                next_page = next_page.replace("limit=25","limit=1000")
                get_next_comcom(next_page,post_id,n,outfile,comment_reaction_name_file)  #ÕÒÏÂN¹Psubcomment

def get_next_comcom(next_page,post_id,n,outfile,comment_reaction_name_file):
    error_flag6 = 0
    try:
        req = urllib2.Request(next_page)
        content = urllib2.urlopen(req).read()
    except urllib2.HTTPError as e:
        error_flag6 = 1
        print (e.message)
        i = 0
        while i == 0:
            time.sleep(5)
            try:
                req = urllib2.Request(next_page)
                content = urllib2.urlopen(req).read()
                error_flag6 = 0
                i = i + 1
            except urllib2.HTTPError as e2:
                print (post_id + " error\n")
    except requests.exceptions.ConnectionError as r:
        error_flag6 = 1
        print (r.message)
        k2 = 0
        while k2 == 0:
            time.sleep(2)
            try:
                req = urllib2.Request(next_page)
                content = urllib2.urlopen(req).read()
                error_flag6 = 0
                k2 = k2 + 1
            except requests.exceptions.ConnectionError as r2:
                time.sleep(60)
    if int(error_flag6) == 0:
        next_comcom = json.loads(content, strict=False)

        ob = req['data']
        ob_len = len(ob)
        for comment in ob:
            if (len(comment['message'])!=8):
                continue  

            graph = facebook.GraphAPI(access_token = 'EAAEpCePdcvgBAKKBxMoNfKSTUZA359xgk0ZAWuU6BYP5ZBl11Cbri74fZAg7A4ZBQfufaiwH60aZAwuiRImcWTnFsZAFVR6OTG5nZAdC7wqsir9xdXFEF6HGr7lZB2haZBtnU53bCZCVXZC6gBmxncKVRnZCzi9J3bKpuZCtsZD', version = '2.8')
            comment_reaction_dict = {}#get_reaction_dict2(comment['id'],graph,1000,comment_reaction_name_file)
            write_comment_csv(post_id,comment,comment_reaction_dict,outfile)

            if 'comments' in comment:
                for comment_coment in comment['comments']['data']:
                    if(len(comment_coment['message'])!=8):
                        continue

                    comment_reaction_dict ={}# get_reaction_dict2(comment_coment['id'],graph,1000),comment_reaction_name_file
                    write_comment_csv(post_id,comment_coment,comment_reaction_dict,outfile)

        if(len(next_comcom) > 1):
            if(len(next_comcom['paging']) > 2):
                n =  n + 1
                next_page = next_comcom['paging']['next']

                get_next_comcom(next_page,post_id,n,outfile,comment_reaction_name_file)  #recursive

def get_next_reaction(next_page,reaction_type,Post_dict):
    while len(next_page) > 0:
        error_flag7 = False
        try:
            req = urllib2.Request(next_page)
            content = urllib2.urlopen(req).read()
        except urllib2.HTTPError as e:
            error_flag7 = True
            print ("error_flag7  "+e.message)
            loop = True
            while loop:
                try:
                    req = urllib2.Request(next_page)
                    content = urllib2.urlopen(req).read()
                    error_flag7 = False
                    break
                except urllib2.HTTPError as e2:
                    print ("error e2:"+e2+"\n")
                    time.sleep(2)

        if (error_flag7) == False:
            next_resu_j_2 = json.loads(content, strict=False)
            ob_length = len(next_resu_j_2['data'])
            emotion_reaction_flag = False
            for j in range(0,ob_length,1):
                #
                if(emotion_reaction_flag and not(reaction_type == "NONE" or reaction_type == "LIKE"  )):
                    pass

                reaction = next_resu_j_2['data'][j]

                reaction_list = ["LIKE","LOVE","WOW","HAHA","SAD","ANGRY","THANKFUL"]    #ÕÒÃ¿‚€reactionÓÐ¶àÉÙÈË°´
                for r in reaction_list:
                    if reaction['id'] in Post_dict:
                        Post_dict[ reaction['id'] ][r] =   reaction['reactions']['summary']['total_count']

            if(len(next_resu_j_2) > 1):
                if(len(next_resu_j_2['paging']) > 1):
                    next_page = next_resu_j_2['paging']['next']
                    print ("\n" + next_page)
                else:
                    next_page = ''
            else:
                next_page = ''
        time.sleep(0.5)

if __name__ == "__main__":
    main()
