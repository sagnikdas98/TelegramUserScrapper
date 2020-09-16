
import sys
import csv
import traceback
import time
import random
import json

from telethon.sync import TelegramClient #Client Module to Login

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, InputPeerChat

from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest


credential_file = "credentials.json" #Relative Path of File which consists Telegram Credentials(api_id, api_hash, phone)
member_file ="members.csv" #File to save the scrapped members data

#Login & Verification Code
try:
    credentials = json.load(open(credential_file, 'r'))
except:
    print("credentials.json File not present in the directory")
    exit()

try:
    client = TelegramClient(credentials['phone'], credentials['api_id'], credentials['api_hash'])
    client.connect()
except:
    print("Could not create Telegram Client, Please check your Credentials in credentials.json file")
    exit()


if not client.is_user_authorized():
    client.send_code_request(credentials['phone'])
    client.sign_in(credentials['phone'], input('Enter  veryfication code: '))

#Chat parameters
chats = []
last_date = None
chunk_size = 200 # No of latest chats to load
groups = []

try:
    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)
except:
    print("Unable to gather chats from server. Please Check Chat parameters.")
    exit()



for chat in chats:
    try:
        groups.append(chat)
    except:
        continue

if len(groups) == 0:
    print("No Groups or Channels found.")
    exit()

print('Choose a group/channel to scrape members from:')
i=1
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

g_index = input("Enter a Number: ")
target_group=groups[int(g_index)-1]

print('Fetching Members...')
all_participants = []

try:
    all_participants = client.get_participants(target_group, aggressive=True)
except: 
    print("Unable to fetch participants of", target_group)
    exit()

if len(all_participants) == 0:
    print("No user found in", target_group+'.', "Please check the group.")
    exit()

# print(all_participants)

try:
    print('Saving In file...')
    with open(member_file,"w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
        for user in all_participants:
            if user.username:
                username= user.username
            else:
                username= ""
            if user.first_name:
                first_name= user.first_name
            else:
                first_name= ""
            if user.last_name:
                last_name= user.last_name
            else:
                last_name= ""
            name= (first_name + ' ' + last_name).strip()
            writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
    print(len(all_participants), 'Members scraped successfully.')

except:
    print("Could not write data to xsv file.")