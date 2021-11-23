#!/usr/bin/python3
import json
import os
import argparse
import instaloader
import csv
from itertools import islice
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
    if os.path.exists('~/.config/instaloader/session-'+ig_username):
        os.remove('~/.config/instaloader/session-'+ig_username)
    pass
finally:
    command = 'instaloader -l {} -p {}'.format(ig_username, ig_pass)
    os.system(command)
    L.load_session_from_file(ig_username)

def get_user_command(user):

    if not os.path.exists(user):
        os.makedirs(user)
    if not os.path.exists(user+'loc'):
        os.makedirs(user+'loc')
    #mdt is file to write filename-location info.
    mdt= open(user+'loc'+"/metadata.csv",'w')
    csvwriter=csv.writer(mdt)
    nodata=open(user+'loc'+"/nolocation.txt",'w')
    print("started")
    num=0
    filename=''
    profile = instaloader.Profile.from_username(L.context, user)
    for post in islice(profile.get_posts(),60):
        #post=profile.get_posts()[i]
        print("post is ", post)
        meta_data={}
        L.download_post(post, target=profile.username)   #download post
        filename =L.format_filename(post, target=profile.username) #getfilename
        print(filename)
        file=lzma.open('./'+profile.username+'/'+filename+'.json.xz').read()  #unzip metdata
        data=json.loads(file)
        meta_data=data['node']['location']
        if meta_data is not None:
            if not os.path.exists(user+'loc'):
                os.makedirs(user+'loc')
            command='mv '+ './'+profile.username+'/'+filename+'*'+ '  ./'+profile.username+'loc'+'/'
            os.system(command)
            meta_data['imagename']=filename
            for key, value in meta_data.items():
                csvwriter.writerow([key, value])
        else:
            nodata.write(filename+'.jpg\n')
        
    command2= 'rm -r '+user
    os.system(command2)
    

def get_following(user) :
    if not os.path.exists(user):
        os.makedirs(user)
    profile = instaloader.Profile.from_username(L.context, user)
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
elif args.all:
    followers = []
   

elif len(args.users) == 1 :
    get_following(args.users[0])
    #get_user_command(args.users[0],args.m)
    print("Retrieved followers")
    followers = []
    with open(args.users[0] + '/followee.txt', 'r') as f:
        followers = f.read()
    followers = followers.split('\n')
    followers.remove('')
    red_foll=[]
    for i in range (0,min(len(followers),10)):
        red_foll.append(followers[i])
    if (args.users[0]=='________j17' and 'rootless_compass' not in red_foll):
        red_foll.append('rootless_compass')
    if (args.users[0]=='muntahatoor' and 'tranjoytravel' not in red_foll):
        red_foll.append('tranjoytravel')
    if(args.users[0]=='marilenadance' and 'melinahadjistylianou' not in red_foll):
        red_foll.append('melinahadjistylianou')
    for x in range(len(red_foll)):
        get_user_command(red_foll[x])
        print("done ", x)

elif (len(args.users)>2):
    for x in args.users:
        get_user_command(x)

