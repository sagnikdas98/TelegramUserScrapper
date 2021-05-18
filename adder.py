import sys
import csv
import traceback
import time
import random
import json

from telethon.sync import TelegramClient #Client Module to Login

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, InputPeerChat

from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserAlreadyParticipantError

from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest


credential_file = "credentials2.json" #Relative Path of File which consists Telegram Credentials(api_id, api_hash, phone)
try:
    input_file = sys.argv[1]# list of users #File to save the scrapped members data
except:
    input_file = "members1.csv"
    print("Pass members.csv as command-line argument.")

start_index = 1
continue_script = False

if len(sys.argv) == 5:
    g_index = int(sys.argv[2])
    mode = int(sys.argv[3])
    start_index = int(sys.argv[4])
    continue_script = True


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

users = []
try:
    with open(input_file, encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
            users.append(user)
except:
    print("Could not read from csv file. Please check the csv file.")
    exit()

if len(users) == 0:
    print("No Users found.")
    exit()

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
    print("No groups or Channels found.")
    exit()  

if not continue_script:
    print('Choose a group to add members:')
    i = 1
    for group in groups:
        print(str(i) + '- ' + group.title)
        i += 1

    g_index = input("Enter a Number: ")

target_group = groups[int(g_index) - 1]

isChannel = None

try:
    target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)
    isChannel = True
except:
    target_group_entity = InputPeerChat(target_group.id)
    isChannel = False

if not continue_script:
    mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

if(mode not in [1,2]):
    sys.exit("Invalid Mode Selected. Please Try Again.")
    

n = 0
user_added_count = 0

for i in range(start_index,len(users)):
    user = users[i]
    n += 1
    if n % 50 == 0:
        time.sleep(900)
    try:
        print("Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")
        
        if isChannel:
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        else:
            client(AddChatUserRequest(target_group.id, user_to_add,fwd_limit=50))

        user_added_count += 1
        wait_time = random.randrange(50, 80)
        print("Waiting for",wait_time, "Seconds...")
       # time.sleep(wait_time)
    except PeerFloodError:
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        print("Run the following command after few hours to contiune where you left off:")
        print("python3 adder.py members.csv",g_index, mode, i)
        sys.exit()
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
    except UserAlreadyParticipantError:
        continue
    except KeyboardInterrupt:
        print("python3 adder.py members.csv", g_index, mode, i)
        sys.exit("Stopping Process")

    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue
    
print("Added:", user_added_count, "users to the group")
