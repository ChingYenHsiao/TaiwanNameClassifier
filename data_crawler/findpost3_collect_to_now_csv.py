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
    print(type(message))
    print(message)
    print(message.replace(",","，".decode("utf-8")))
    # if(isinstance(message, unicode)):
    #     message = message.encode('utf-8')
    #     print 'encode!',type(message)

    # result = message
    # print result,type(result)
    # result = result.replace(',','£¬'.decode('utf-8'))
    # print result


    # result = result.replace("\r"," ")
    # result = result.replace("\n","<NL>")
    
    # #result = result.strip()

    # #result = del_url(result)
    # original_len = len(result)
    # for  i in range(100):
    #     result = change_Username_metion(result)
    #     if original_len == len(result):
    #         break
    #     else:
    #         original_len = len(result)

    # return result


def main():
    #set  intialize path.date.id_list

    until = 'until=2017-06-01'
    since = 'since=2017-06-01'

    Path = "./data/"
    dir_layer1 = ""
    dir_layer2 = ""
    graph = facebook.GraphAPI(access_token = 'EAAXfzQZBz8EMBAMFVsf1Kgu9zWaYRE2a6NBa1IBYZApckFtcPIbOyWjMZBkYtZCBkoJOmuo7Vhv19b5rZCl4wsYGxC9m4fUoKArZAvwwhLhUuHPNjopgjStizdjuZCcqWlW0c3k20JZAgKnQbLusMGy73itFQrSed7QZD', version = '2.7')
    graph2 = facebook.GraphAPI(access_token = 'EAAXfzQZBz8EMBAMFVsf1Kgu9zWaYRE2a6NBa1IBYZApckFtcPIbOyWjMZBkYtZCBkoJOmuo7Vhv19b5rZCl4wsYGxC9m4fUoKArZAvwwhLhUuHPNjopgjStizdjuZCcqWlW0c3k20JZAgKnQbLusMGy73itFQrSed7QZD', version = '2.8')
    start = False
    total_page_count = 0
    reaction_page_count = 0
    page_count = 0
    page_id ='330133697344117_433555783668574'
    fileName = 'LOOKER'
    print ("No.",page_count,fileName.decode('utf-8') )
    Post_dict = {}
    get_post_comment(Path,Post_dict,graph)
    #     Post_csv.write("PostId,week,hour,shares,comments,SAD,ANGRY,HAHA,WOW,LOVE,Thankful,Likes,characters,message,type,updated_time,created_time,link,picture,story\n")
    #     #Post •þ×¥µ½µÄ™ÚÎ» ¿ÉÒÔµ½FBé_°lÕß¾Wí“ ßx“ñ×Ô¼ºÏëÒªµÄ™ÚÎ»
    #     #https://developers.facebook.com/docs/graph-api/reference/v2.8/post
    #     page_path = "/" + page_id + "/posts?fields=id,admin_creator,application,call_to_action,caption,created_time,description,feed_targeting,from,icon,is_hidden,is_published,link,message,name,object_id,parent_id,picture,place,privacy,properties,shares,source,story,story_tags,targeting,to,updated_time,type,with_tags,likes,comments,message_tags,status_type"#&"+until+"&"+since

    #     resp = get_resp(page_path,graph,30)
    #     print resp
    #     if(resp!='null'  and len(resp)>1):
    #         Post_dict = {}
    #         for Post in resp['data']:
    #             add_Post_to_Postdic(Post,Post_dict)
    #             #print (Post_dict)
    #         if((len(resp) > 1)):
    #             if(len(resp['paging']) > 1):
    #                 next_page = resp['paging']['next']
    #                 print (next_page)
    #                 get_next_post(next_page,Post_dict) #ÕÒÏÂÒ»30¹Ppost
    #         get_post_comment(Path,Post_dict,graph)     #ÕÒ Post µÄ comments
            

            # reaction_list = ["LIKE","LOVE","WOW","HAHA","SAD","ANGRY","THANKFUL"]    #ÕÒÃ¿‚€reactionÓÐ¶àÉÙÈË°´
            # for l in range(0,len(reaction_list),1):
            #     reaction_path = "/" + page_id + "/posts?fields=created_time,reactions.limit(0).type(" + reaction_list[l]  + ").summary(1)&"+until+"&"+since
            #     error_flag_1 = False
            #     try:
            #         resp2 = graph2.get_object(reaction_path,limit=30)
            #     except facebook.GraphAPIError as g:
            #         error_flag_1 = True
            #         print ("error_flag_1 \t"+ g.message)
            #         loop = True
            #         skip =0
            #         while loop :
            #             time.sleep(2)
            #             try:
            #                 resp2 = graph2.get_object(reaction_path,limit=30)
            #                 error_flag_1 = False
            #                 break
            #             except facebook.GraphAPIError as g2:
            #                 print (g2.message+" again")
            #                 skip = skip +1
            #                 if  skip == 5 :
            #                     print ("Fail too much time! skip this !")
            #                     break      

            #     if (error_flag_1) == False:
            #         reaction_length = len(resp2['data'])
            #         for m in range(0,reaction_length,1):
            #             reaction = resp2['data'][m]
            #             if reaction['id'] in Post_dict:
            #                 Post_dict[ reaction['id'] ][reaction_list[l]] =   reaction['reactions']['summary']['total_count']
            #             #print reaction_list[l],ob2['reactions']['summary']['total_count'],ob2['id']
                                                                


            #         if len(resp2) > 1:
            #             if(len(resp2['paging']) > 1):
            #                 next_page_reaction = resp2['paging']['next']
            #                 get_next_reaction(next_page_reaction,reaction_list[l],Post_dict)   #À^ÀmÕÒreaction

            # print ("Finish" + reaction_list[l])
            # time.sleep(0.1)

            # for PostID in  Post_dict: 
            #     print (Post_dict[PostID])
            #     #PostId,week,hour,shares,comments,SAD,ANGRY,HAHA,WOW,LOVE,THANKFUL,Likes,characters,message,type,updated_time,created_time,link,picture,story
            #     Post_csv.write( str(Post_dict[PostID]["PostId"])+','+str(Post_dict[PostID]['week'])+','+str(Post_dict[PostID]["hour"])+','+str(Post_dict[PostID]["shares"]))
            #     #Post_csv.write( ',0,'+str(Post_dict[PostID]["SAD"])+','+str(Post_dict[PostID]["ANGRY"])+','+str(Post_dict[PostID]["HAHA"])+','+str(Post_dict[PostID]["WOW"]))

            #     Post_csv.write( ","+str(Post_dict[PostID]["comments"])+','+str(Post_dict[PostID]["SAD"])+','+str(Post_dict[PostID]["ANGRY"])+','+str(Post_dict[PostID]["HAHA"])+','+str(Post_dict[PostID]["WOW"]))
            #     Post_csv.write( ','+str(Post_dict[PostID]["LOVE"])+','+str(Post_dict[PostID]["THANKFUL"])+','+str(Post_dict[PostID]["LIKE"]))
            #     Post_csv.write( ","+str(Post_dict[PostID]["characters"])+','+str(Post_dict[PostID]["message"])+","+str(Post_dict[PostID]['type'])+","+str(Post_dict[PostID]["updated_time"])+","+str(Post_dict[PostID]["created_time"]))
            #     #print(type(Post_dict[PostID]["message"]))

            # # print(type(Post_dict[PostID]["message"].encode('utf-8')))
            # # print (type(Post_dict[PostID]["link"]))
            # # print(type(Post_dict[PostID]["picture"]))
            # # print(type(Post_dict[PostID]["story"]))
            # Post_csv.write(','+str(Post_dict[PostID]["link"])+","+str(Post_dict[PostID]["picture"])+','+Post_dict[PostID]["story"]+"\n")
                


def get_next_post(next_page,Post_dict):
    while len(next_page) > 0:
        error_flag2 = False
        try:
            req = urllib2.Request(next_page)
            content = urllib2.urlopen(req).read()
        except Exception as e:

        #except urllib3.HTTPError as e:
            error_flag2 = True
            #print "error_flag2:HTTP ERROR\n"
            loop = True
            while loop:
                try:
                    req = urllib2.Request(next_page)
                    content = urllib2.urlopen(req).read()
                    error_flag2 = False
                    break
                except Exception as e2:    
                #except urllib3.HTTPError as e2:
                    time.sleep(2)
                    print (str(e2)+"\terror\n")
        if (error_flag2) != True:
            next_resu = json.loads(content, strict=False)
            ob_length = len(next_resu['data'])
            for i in range(0,ob_length,1):
                ob = next_resu['data'][i]
                add_Post_to_Postdic(ob,Post_dict)
                #print "Post number :" + str(outfile.tell())

            if((len(next_resu) > 1)):
                #print "in"
                if(len(next_resu['paging']) > 1):
                    next_page = next_resu['paging']['next']
                    print ("\n" + next_page)
                    get_next_post(next_page,Post_dict)
                else:
                    next_page = ''
            else:
                next_page = ''
        time.sleep(0.1)

def get_resp(path,graph,limit_number):
    resp = 'null'
    try:
        resp = graph.get_object(path,limit=limit_number)   #Ã¿´Î300‚€ ¿ÉÄÜ•þ‰Äµô
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
                    resp_2 = graph.get_object(path,limit=100)    #×Ô„ÓœpÁ¿ ¿É×ÔÓ†
                    error_flag3 = 0
                    k = k + 1
                    return resp
                except facebook.GraphAPIError as g2:
                    if "User request limit reached" in g.message:
                        time.sleep(60)      
def get_reaction_dict(post_id,graph,limit):  
    reaction_list = ["LIKE","LOVE","WOW","HAHA","SAD","ANGRY","THANKFUL"]    #ÕÒÃ¿‚€reactionÓÐ¶àÉÙÈË°´
    reaction_dict = {}
    for reaction in reaction_list:
        reaction_path  = post_id+"?fields=created_time,reactions.limit(0).type("+reaction+").summary(1)"
        reaction_resp = get_resp(reaction_path,graph,limit)
        reaction_dict[reaction ] = reaction_resp['reactions']['summary']['total_count']
        time.sleep(0.2)
    return reaction_dict

def write_comment_csv(post_id,comment,comment_reaction_dict,outfile):
    output = str(post_id)+","+str(comment['from']['name'].encode('utf-8'))+','+str(comment['from']['id'])+','
    print comment['message']
    #output+= str(comment['message'])+","
    output+=(message_clear(comment['message']))+',' 
    output+=str(comment['like_count'])+','+str(comment['comment_count'])+','+str(comment['created_time'])+','+str(comment['id'])
    # if in:

    # else:
    #     output+=',null,'
    # output+=str(comment_reaction_dict["LOVE"])+","+str(comment_reaction_dict["WOW"])+","+str(comment_reaction_dict["HAHA"])+","
    # output+=str(comment_reaction_dict['SAD'])+","+str(comment_reaction_dict['ANGRY'])+","+ str(comment_reaction_dict['THANKFUL'])+"\n"
    output+="\n"
    outfile.write(output)

def get_post_comment(result_path,Post_dict,graph):
    #page_id = ""
    # for post_id in Post_dict:
    #     page_id = post_id.split("_")[0]
    #     break
    result_comment =  'SB.csv'#result_path + page_id + "_comment_reaction.csv"
    with open(result_comment, 'a') as outfile:
        outfile.write("PostID,name,userID,message,like_count,comment_count,created_time,comment_id,parentID,LOVE,WOW,HAHA,SAD,ANGRY,THANKFUL\n")
        post_id = '330133697344117_433555783668574'
        #for post_id in Post_dict:
        post_comments_count = 0

        time.sleep(0.1)
        error_flag3 = 0
        #print (post_id)
        #comment •þ×¥µ½µÄ–|Î÷ ¿ÉÒÔµ½FBé_°lÕß¾Wí“ ÕÒ×Ô¼ºÒªµÄ™ÚÎ»Ãû·Q
        comment_path = "/" + post_id + "/comments" + "?fields=from,message,message_tags,created_time,id,comments.limit(50){from,id,message,message_tags,created_time,like_count,parent,can_remove,user_likes},comment_count,user_likes,can_remove,parent,like_count"

        resp_2 = get_resp(comment_path,graph,300)  #Ã¿´Î300‚€ ¿ÉÄÜ•þ‰Äµô


        if int(error_flag3) == 0:
            #PostID,name,userID,message,like_count,comment_count,created_time,comment_id,parentID,LOVE,WOW,HAHA,SAD,ANGRY,THANKFUL
            ob_len = 0

            ob = resp_2['data']
            ob_len += len(ob)
            for comment in ob:
                #print comment['message'],len(comment['message'])
                if (len(comment['message'])==0):
                        continue
                resu_id = comment['id']

                comment_reaction_dict = ''#get_reaction_dict(comment['id'],graph,100)
                #print type(comment['message'])
                write_comment_csv(post_id,comment,comment_reaction_dict,outfile)
                # output = str(post_id)+","+str(comment['from']['name'].encode('utf-8'))+','+str(comment['from']['id'])+','
                # # print comment['message']
                # # print message_clear(comment['message'])
                # output+=(message_clear(comment['message']))+',' 
                # output+=str(comment['like_count'])+','+str(comment['comment_count'])+','+str(comment['created_time'])+','+str(comment['id'])+',null,'
                # output+=str(comment_reaction_dict["LOVE"])+","+str(comment_reaction_dict["WOW"])+","+str(comment_reaction_dict["HAHA"])+","
                # output+=str(comment_reaction_dict['SAD'])+","+str(comment_reaction_dict['ANGRY'])+","+ str(comment_reaction_dict['THANKFUL'])+"\n"
                # outfile.write(output)
                #outfile.write(str(post_id)+","+str(comment['from']['name'].encode('utf-8'))+','+str(comment['from']['id'])+',')       
                # outfile.write((message_clear(comment['message']))+',' )
                # outfile.write(str(comment['like_count'])+','+str(comment['comment_count'])+','+str(comment['created_time'])+','+str(comment['id'])+',null,')
                # outfile.write(str(comment_reaction_dict["LOVE"])+","+str(comment_reaction_dict["WOW"])+","+str(comment_reaction_dict["HAHA"])+",")
                # outfile.write(str(comment_reaction_dict['SAD'])+","+str(comment_reaction_dict['ANGRY'])+","+ str(comment_reaction_dict['THANKFUL'])+"\n")

                resu_comcom = comment['comment_count']
                # if int(resu_comcom) > 50:
                #     next_ob_page = comment ['comments']
                #     if len(next_ob_page['paging']) > 1:
                #         next_comcom_page = next_ob_page['paging']['next']
                #         get_com_com(next_comcom_page,outfile,post_id)    #ÕÒsubcomment

            print ("Get F and Comment_1 Ok\n")
            if(len(resp_2) > 1):
                if(len(resp_2['paging']) > 1):
                    n = 1
                    next_page = resp_2['paging']['next']
                    ob_len+= get_next_comment(next_page,post_id,n,graph,outfile)  #ÕÒÏÂN¹Pcomment
            Post_dict[ post_id]['comments'] = str(ob_len)
        #return 0

def get_next_comment(next_page,post_id,n,graph,outfile):
    while len(next_page) > 0:
        error_flag4 = 0
        try:
            req = urllib2.Request(next_page)
            content = urllib2.urlopen(req).read()
        except urllib2.HTTPError as e:
            error_flag4 = 1
            print (e.message)
            #i = 0
            #while i == 0:
            try:
                req = urllib2.Request(next_page)
                content = urllib2.urlopen(req).read()
                error_flag4 = 0
                #i = i + 1
            except urllib2.HTTPError as e2:
                print (e2)
                print (post_id + " error\n")

        if int(error_flag4) == 0:
            next_resu_j_2 = json.loads(content, strict=False)
            next_ob = next_resu_j_2['data']
            #result_comment = date_dir + result_dir + "/" + post_id + "_raw_" + str(n)   #ÈÕÆÚÒª¸úÖø¸Ä
            #with open(result_comment,'w') as outfile:
            #   outfile.write(json.dumps(next_resu_j_2,ensure_ascii=False).encode('utf8'))

            for comment in next_ob:
                resu_id =comment['id']
                print comment['message'],len(comment['message'])
                if (len(comment['message'])==0):
                        continue     
                comment_reaction_dict = ''#get_reaction_dict(comment['id'],graph,100)
                write_comment_csv(post_id,comment,comment_reaction_dict,outfile)

                # output = str(post_id)+","+str(comment['from']['name'].encode('utf-8'))+','+str(comment['from']['id'])+','
                # output+=(message_clear(comment['message']))+',' 

                # outfile.write(output)

                #outfile.write(str(post_id)+","+str(comment['from']['name'].encode('utf-8'))+','+str(comment['from']['id'])+',')       
                # outfile.write((message_clear(comment['message']))+',' )
                # outfile.write(str(comment['like_count'])+','+str(comment['comment_count'])+','+str(comment['created_time'])+','+str(comment['id'])+',null,')
                # outfile.write(str(comment_reaction_dict["LOVE"])+","+str(comment_reaction_dict["WOW"])+","+str(comment_reaction_dict["HAHA"])+",")
                # outfile.write(str(comment_reaction_dict['SAD'])+","+str(comment_reaction_dict['ANGRY'])+","+ str(comment_reaction_dict['THANKFUL'])+"\n")


                # resu_comcom = comment['comment_count']
                # if int(resu_comcom) > 50:
                #     next_ob_page = next_comment['comments']
                #     if len(next_ob_page['paging']) > 1:
                #         next_comcom_page = next_ob_page['paging']['next']
                #         get_com_com(next_comcom_page,outfile,post_id)    #ÕÒsubcomment
            n = n + 1
            print ("Get Comment_next Ok\n")
            ob_len = 0
            if(len(next_resu_j_2) > 1):
                if(len(next_resu_j_2['paging']) > 2):
                    next_page = next_resu_j_2['paging']['next']
                    ob_len+= get_next_comment(next_page,post_id,n,graph,outfile) 
                else:
                    next_page = ''
            else:
                next_page = ''
            return ob_len

def get_com_com(next_page,outfile,post_id):
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
            resu_id = comment['id']
            graph = facebook.GraphAPI(access_token = 'EAAXfzQZBz8EMBAEZCdBTSpMciqzw7xDAP5Ugkqvy85XvCaY62QOfU6vMR11ERlWv8zS9Utvd4cfqX7ypmHDD5ZCYp3YQaZAYqYhRUrxO8A5rJF0HMae3PObZB0LhQ26Nudz2EhNLgzpVXgVoSj5UWgSEBGnrJgAAZD', version = '2.8')
            comment_reaction_dict = get_reaction_dict(comment['id'],graph,300)

            write_comment_csv(post_id,comment,comment_reaction_dict,outfile)
            
            # output = str(post_id)+","+str(comment['from']['name'].encode('utf-8'))+','+str(comment['from']['id'])+','
            # output+=(message_clear(comment['message']))+',' 
            # output+=str(comment['like_count'])+','+str(comment['comment_count'])+','+str(comment['created_time'])+','+str(comment['id'])+',null,'
            # output+=str(comment_reaction_dict["LOVE"])+","+str(comment_reaction_dict["WOW"])+","+str(comment_reaction_dict["HAHA"])+","
            # output+=str(comment_reaction_dict['SAD'])+","+str(comment_reaction_dict['ANGRY'])+","+ str(comment_reaction_dict['THANKFUL'])+"\n"
            # outfile.write(output)

            # outfile.write(str(post_id)+","+str(comment['from']['name'].encode('utf-8'))+','+str(comment['from']['id'])+',')
            # outfile.write(message_clear(comment['message'])+','+str(comment['like_count'])+',' )
            # if 'comment_count' in comment:
            #     outfile.write(str(comment['comment_count'])+',')
            # else :
            #     outfile.write('0,')
            # outfile.write(str(comment['created_time'])+','+str(comment['id'])+','+comment['parent']['id']+',')
            # outfile.write(str(comment_reaction_dict["LOVE"])+","+str(comment_reaction_dict["WOW"])+","+str(comment_reaction_dict["HAHA"])+",")
            # outfile.write(str(comment_reaction_dict['SAD'])+","+str(comment_reaction_dict['ANGRY'])+","+ str(comment_reaction_dict['THANKFUL'])+"\n")

        if(len(next_comcom) > 1):
            if(len(next_comcom['paging']) > 2):
                n = 1
                next_page = next_comcom['paging']['next']
                get_next_comcom(next_page,post_id,n,outfile)  #ÕÒÏÂN¹Psubcomment

def get_next_comcom(next_page,post_id,n,outfile):
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
            resu_id = comment['id']
            graph = facebook.GraphAPI(access_token = 'EAAXfzQZBz8EMBAEZCdBTSpMciqzw7xDAP5Ugkqvy85XvCaY62QOfU6vMR11ERlWv8zS9Utvd4cfqX7ypmHDD5ZCYp3YQaZAYqYhRUrxO8A5rJF0HMae3PObZB0LhQ26Nudz2EhNLgzpVXgVoSj5UWgSEBGnrJgAAZD', version = '2.8')
            comment_reaction_dict = get_reaction_dict(comment['id'],graph,100)

            outfile.write(str(post_id)+","+str(comment['from']['name'].encode('utf-8'))+','+str(comment['from']['id'])+',')
            outfile.write(message_clear(comment['message'])+','+str(comment['like_count'])+',' )
            if 'comment_count' in comment:
                outfile.write(str(comment['comment_count'])+',')
            else :
                outfile.write('0,')
            outfile.write(str(comment['created_time'])+','+str(comment['id'])+','+comment['parent']['id']+',')
            outfile.write(str(comment_reaction_dict["LOVE"])+","+str(comment_reaction_dict["WOW"])+","+str(comment_reaction_dict["HAHA"])+",")
            outfile.write(str(comment_reaction_dict['SAD'])+","+str(comment_reaction_dict['ANGRY'])+","+ str(comment_reaction_dict['THANKFUL'])+"\n")

        if(len(next_comcom) > 1):
            if(len(next_comcom['paging']) > 2):
                n =  n + 1
                next_page = next_comcom['paging']['next']
                get_next_comcom(next_page,post_id,n,outfile)  #recursive

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

                # # After 20160226, the post will have emotion reaction
                # # time[0] = year \  time[1] = month \ time[2][0:2] = day
                # #print "emotion_reaction_flag:\t"+emotion_reaction_flag
                # ctime = (ob['created_time'].split("-"))
                # #if(int(time[0])>=2016 and (  ( int(time[1])>=3 ) or  ( int(time[1])>=2) and int(time[2][0:2])>=26) ):
                # if(int(ctime[0])>=2016 and (  ( int(ctime[1])>=2)) ):
                #     emotion_reaction_flag = True
                # #
                # result_reaction_0226 = date_dir + result_dir + "/after20160226/" + ob['id'] + "_" + reaction_type + "_raw"

                # result_reaction = date_dir + result_dir + "/" + ob['id'] + "_" + reaction_type + "_raw"

                # #


                # if(reaction_type == "NONE" or reaction_type == "LIKE"  ):
                #     with open(result_reaction,'w') as outfile:
                #         outfile.write(json.dumps(ob,ensure_ascii=False).encode('utf8'))
                # if(emotion_reaction_flag) :
                #     with open(result_reaction_0226,'w') as outfile:
                #         outfile.write(json.dumps(ob,ensure_ascii=False).encode('utf8'))
                #         #print json.dumps(ob,ensure_ascii=False).encode('utf8')

            if(len(next_resu_j_2) > 1):
                if(len(next_resu_j_2['paging']) > 1):
                    next_page = next_resu_j_2['paging']['next']
                    print ("\n" + next_page)
                else:
                    next_page = ''
            else:
                next_page = ''
        time.sleep(0.2)

if __name__ == "__main__":
    main()
