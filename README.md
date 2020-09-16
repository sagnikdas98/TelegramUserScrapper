# TelegramUserScrapper
A Telegram Client to scrape users from a group or channel and add them to another group or channel.

Files Included:
credentials.json
adder.py
scrapper_together.py
scrapper_channel.py
scrapper_group.py
scrapper_and_adder.py



File Descriptions:

credentials.json
{
"app_title": "Title_of_the_app",
"api_id": 123456,
"api_hash":"YOUR_API_HASH",
"phone": "+111111111111"
}


	
scrapper_together.py

Command to run: python3 scrapper_together.py 
Scraps participants from Telegram Groups and Channels and stores them in a members.csv file. This script logs the user in according to the credentials.json file and gets the previous 200 chats of the user and extracts the groups and channel chats out of them. The user is then prompted to enter the index of the group from which participants should be extracted and stored in the members.csv file.


scrapper_channel.py

Command to run: python3 scrapper_channel.py 
Scraps participants from Telegram Channels and stores them in a members.csv file.

scrapper_group.py

Command to run: python3 scrapper_group.py 
Scraps participants from Telegram Channels and stores them in a members.csv file.

adder.py

Command to run: python3 adder.py members.csv  
Adds participants from members.csv file to  Telegram Channels and groups. A .csv file has to be passed as a command line argument containing user data created by the scraper scripts. The script waits 60-180 seconds after adding every participant or else the server throws PeerFloodError. It additionally waits 15 minutes after adding 50 participants. Incase of PeerFloodError the script prints a command, which must be run after a few hours that continues adding participants from where it left off previous time. This feature is added so that time is not wasted on participants who have already been added the previous time.

scrapper_and_adder.py
Command to run: python3 scrapper_and_adder.py 
Scraps participants from Telegram Groups and Channels and Adds those participants to other Groups and Channels. It is a combination of scrapper and adder scripts for quicker use.
