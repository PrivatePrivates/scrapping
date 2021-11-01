#!/usr/bin/python3
import json
import os
import argparse
import instaloader
from time import sleep
try:
    import lzma
except ImportError:
    from backports import lzma

ig_username = os.environ["IG_USER"]
ig_pass = os.environ["IG_PASS"]
command = ""

#usage : ./python
# Input : Username
# Output: All media of username (Optional) including meta data (locaation tags and all)
#         All the people he is following
# Under Work 


#instaloader and login
L = instaloader.Instaloader()
L.login(ig_username, ig_pass)    

def get_user_command(user, m):
    #mdt is file to write filename-location info.
    mdt= open(user+"/metadata.txt",'w')
    print("started")
    num=0
    filename=''
    loc=''
    profile = instaloader.Profile.from_username(L.context, user)
    #(fix1)
    # #This if isnt working downloads all files 
    if (m!=0):
        for post in profile.get_posts():
            L.download_post(post, target=profile.username)   #download post
            filename =L.format_filename(post, target=profile.username) #getfilename
            print(filename)
            mdt.write(filename+'.jpg\n')
            file=lzma.open('./'+profile.username+'/'+filename+'.json.xz').read()  #unzip metdata
            data=json.loads(file)
            loc=data['node']['location']
            mdt.write(str(loc)+"\n") 
            num+=1
            if(num==m):
                break
    else:
        for post in profile.get_posts():
            L.download_post(post, target=profile.username)   #download post
            filename =L.format_filename(post, target=profile.username) #getfilename
            print(filename)
            mdt.write(filename+'.jpg\n')
            file=lzma.open('./'+profile.username+'/'+filename+'.json.xz').read()  #unzip metdata
            data=json.loads(file)
            loc=data['node']['location']
            mdt.write(str(loc)+"\n")                    #write into a file   
    sleep(2)
    with open(user + "/followee.txt", "w") as f:       #write followers into file
        for followee in profile.get_followees():
            f.write(followee.username + "\n")
            



#all parsing stuff 

parser = argparse.ArgumentParser()
parser.add_argument("users", type=str, nargs="+", help="Users to retreive data from")
parser.add_argument(
    "--all", "-a", help="Get all followers and their posts", action="store_true"
)
parser.add_argument(
    "-m",
    type=int,
    const=20,
    required=False,
    help="Number of media to retrieve",
    nargs="?",
)
args = parser.parse_args()
print(args)

if len(args.users) != 1 and args.all:
    parser.error("--all cannot be used with multiple users")

##starts from here 
if len(args.users) == 1 :
    get_user_command(args.users[0],args.m)
    print("Retrieved photos")

if (len(args.users)>2):
    for x in args.users:
        get_user_command(x,0)

else:
    print("Usage : python3 scrape.py <username>")


