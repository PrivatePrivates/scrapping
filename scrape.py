#!/usr/bin/python3
import json
import os
import argparse
import instaloader
import csv
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
# Output: All media of username (Optional) including meta data (location tags and all)
#         All the people he is following
# Under Work 


#instaloader and login
L = instaloader.Instaloader()
try:
    L.load_session_from_file(ig_username)
except:
    if os.path.exists('~/.config/instaloader/session-test_private_privates'):
        os.remove('~/.config/instaloader/session-test_private_privates')
    pass
finally:
    command = 'instaloader -l {} -p {}'.format(ig_username, ig_pass)
    os.system(command)
    L.load_session_from_file(ig_username)

def get_user_command(user, m):
    # Create Dir if not exists
    if not os.path.exists(user):
        os.makedirs(user)
    #mdt is file to write filename-location info.
    mdt= open(user+"/metadata.csv",'w')
    csvwriter=csv.writer(mdt)
    nodata=open(user+"/nolocation.txt",'w')
    print("started")
    num=0
    filename=''
   
    profile = instaloader.Profile.from_username(L.context, user)
    #(fix1)
    # #This if isnt working downloads all files 
    if (m!=0):
        for post in profile.get_posts():
            meta_data={}
            L.download_post(post, target=profile.username)   #download post
            filename =L.format_filename(post, target=profile.username) #getfilename
            print(filename)
            file=lzma.open('./'+profile.username+'/'+filename+'.json.xz').read()  #unzip metdata
            data=json.loads(file)
            meta_data=data['node']['location']
            if meta_data is not None:
                meta_data['imagename']=filename
                for key, value in meta_data.items():
                    csvwriter.writerow([key, value])
            else:
                nodata.write(filename+'.jpg\n')
            num+=1
            if(num==m):
                break
    else:
        for post in profile.get_posts():
            meta_data={}
            L.download_post(post, target=profile.username)   #download post
            filename =L.format_filename(post, target=profile.username) #getfilename
            print(filename)
            file=lzma.open('./'+profile.username+'/'+filename+'.json.xz').read()  #unzip metdata
            data=json.loads(file)
            meta_data['imagename']=filename
            meta_data=data['node']['location']
            for key, value in meta_data.items():
                csvwriter.writerow([key, value])                #write into a file   
    #sleep(1)
    with open(user + "/followee.txt", "w") as f:       #write followers into file
        for followee in profile.get_followees():
            f.write(followee.username + "\n")
            

def get_multiple_users(user, users):
    if len(users) <= 0:
        print("No Followers found")
        return
    users = " ".join(i for i in users)
    command="mkdir -p {}/followers && cd {}/followers && instagram-scraper {} --media-metadata --include-location -u {} -p {}".format(user, user, users, ig_username, ig_pass)   
    os.system(command)

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
elif args.all:
    followers = []
    with open(args.users[0] + '/followee.txt', 'r') as f:
        followers = f.read()
    followers = followers.split('\n')
    followers.remove('')
    get_multiple_users(args.users[0], followers)
elif len(args.users) == 1 :
    get_user_command(args.users[0],args.m)
    print("Retrieved photos")
elif (len(args.users)>2):
    for x in args.users:
        get_user_command(x,0)



