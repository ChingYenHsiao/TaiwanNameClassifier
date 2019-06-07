# coding=UTF-8
# python 3
#I want to correct enough fanpage information to distinguish garbage / writer fanpage
import json
import re
import facebook
#import urllib2
import time
import requests
import os
import csv



def main():

    graph = facebook.GraphAPI(access_token = 'EAAXfzQZBz8EMBAAyvxNoWjYVdplxEE7KvgYZC8aOVMEQwEicWEuLwwUi2MhSKrnnf1KCqVDmcVSveZCZCv08OSbbJLXgZAWX9qDWIeeCNGWcaVBWn6U78ZBTh20gmWpgwjUslgmLDFPYoXpYZCXeeUB6lMwS46dj1EZD', version = '2.6')
    w = open("analysis/Fanpage_full.csv",'w')
    w.write("FanPage,ID,postNum,date,category,fan_count,talking_about_count,about,bio,description,personal_info,personal_interests,verification_status\n")
    error_flag = 0

    #read fanpage.csv
    with open("analysis/Fanpage.csv",'r') as f:
        reader = csv.reader(f)
        mylist = list(reader)

        #Get all id
        for item in mylist[1:]:
            print(item [0])
            FanPage = item [0]
            ID = item [1]
            postNum = item[2]
            date = item [3]

            #page_path = "/69744736647?fields=name,fan_count,category,category_list,about,can_checkin,app_id,app_links,artists_we_like,attire,awards,best_page,bio,birthday,booking_agent,business,checkins,emails,featured_video,hours,influences,is_community_page"
            query = "category,fan_count,talking_about_count,about,bio,description,personal_info,personal_interests,verification_status"
            page_path = '/' + ID + '?fields=' +query

            try:
                #print (page_path)
                resp = graph.get_object(page_path)

                #print ((resp))
                s = FanPage.replace(",", "，")+","+ID+","+postNum+","+date+","
                #w.write (FanPage+","+ID+","+postNum+","+date)
                if('category' in resp):
                    s+=str(resp['category']).replace(",", "，")
                else:
                    s +=",null"
                if('fan_count' in resp):
                    s+= ","+str(resp['fan_count'])
                else:
                    s +=",null"
                if('talking_about_count' in resp):
                    s+= ","+str(resp['talking_about_count']).replace(",", "，")
                else:
                    s +=",null"
                if('about' in resp):
                    s +=","+str(resp['about']).replace(",", "，")
                else:
                   s +=",null"
                if('bio' in resp):
                    s+= ","+str(resp['bio']).replace(",", "，")
                else:
                    s +=",null"
                if('description' in resp):
                    s+= ","+str(resp['description']).replace(",", "，")
                else:
                    s +=",null"
                if('personal_info' in resp):
                    s+= ","+str(resp['personal_info']).replace(",", "，")
                else:
                    s +=",null"
                if('personal_interests' in resp):
                    s+= ","+str(resp['personal_interests']).replace(",", "，")
                else:
                    s +=",null"
                if('verification_status' in resp):
                    s+= ","+str(resp['verification_status']).replace(",", "，")
                else:
                    s +=",null"
                s = s.replace("\r\n", " ").replace("\n"," ")
                s+="\n"
                print(s)
                w.write(s)
                    #str(resp['fan_count'])+","+str(resp['personal_info'])+","+str(resp['personal_interests'])+","+str(resp['talking_about_count'])+","+str(resp['verification_status'])+"\n")

            except facebook.GraphAPIError as g:
                error_flag = 1
                estr = "Object with ID"
                estr2 = "does not exist"
                print (g)
    w.close
if __name__ == "__main__":
    main()
    print ("Finished fanpage profile collect.")
