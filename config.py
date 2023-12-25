import re, os, time

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # star bots client config
    API_ID    = os.environ.get("API_ID", "11973721")
    API_HASH  = os.environ.get("API_HASH", "5264bf4663e9159565603522f58d3c18")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") 
   
    # database config
    DATABASE_NAME = os.environ.get("DATABASE_NAME","") # Bot Username  
    DATABASE_URL  = os.environ.get("DATABASE_URL","mongodb+srv://KarthikMovies:KarthikUK007@cluster0.4l5byki.mongodb.net/?retryWrites=true&w=majority")
 
    # other configs
    BOT_UPTIME  = time.time()
    PIC         = os.environ.get("PIC", "") # https://graph.org/file/1412d9f93d77c350d8268.jpg
    ADMINS      = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '1391556668 5162208212 5239847373').split()]
    FORCE_SUB   = os.environ.get("FORCE_SUB", "Star_Bots_Tamil") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001821439025"))

    # AI
    OPENAI_API = environ.get("OPENAI_API","")
    AI = is_enabled((environ.get("AI","True")), False)
    AI_LOGS = int(environ.get("AI_LOGS", LOG_CHANNEL)) #GIVE YOUR NEW LOG CHANNEL ID TO STORE MESSAGES THAT THEY SEARCH IN BOT PM.... [ i have added this to keep an eye on the users message, to avoid misuse of AI Star Bots]
 
    # wes response configuration     
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))

class temp(object):
    U_NAME = None

class Text(object):
    # part of text configuration
    START_TEXT = """<b>Hello 👋🏻 {} ❤️,\nI'm An Star Bots Tamil's Official () Bot. This is An Advanced () Bot.\n➠ For More Details Check /help\n\nMaintenance By :- [Star Bots Tamil](https://t.me/Star_Bots_Tamil)</b>"""

    ABOUT_TEXT = """<b>🤖 My Name :- {}\n
🧑🏻‍💻 Developer :- <a href=https://t.me/TG_Karthik><b>Karthik</b></a>\n
💁🏻 My Best Friend :- {}\n
📝 Language :- Python3\n
📚 Framework :- Pyrogram\n
📡 Hosted on :- VPS\n
💾 Database :- <a href=https://cloud.mongodb.com/>Mongo DB</a>\n
🎥 Movie Updates :- <a href=https://t.me/Star_Moviess_Tamil><b></b>Star Movies Tamil</a>\n
🤖 Bot Channel :- <a href=https://t.me/Star_Bots_Tamil><b></b>Star Bots Tamil</a></b>"""

    HELP_TEXT = """
<b><u>Available Commands</u>

➠ /start :- Check if 😊 I'm Alive
➠ /help :- How to Use❓
➠ /about :- to Know About Me 😌
➠ /stats :- Total Users 📊
➠ /ban :- Ban a User 🚫
➠ /unban :- Unban a User 😁
➠ /banned :- Total Banned Users 🤕
➠ /broadcast :- to Broadcast 💌 a Message to All Users

⚠️ Contact For Any Problem :- [👥 Support Group](https://t.me/Star_Bots_Tamil_Support)</b>"""

    DEV_TEXT = """<b><u>Special Thanks & Developer</b></u>
**You Can pay Any Our Bot's Repo. If you're able to Donate or Buy Our Bot's Repo, please Consider using these Methods:

UPI ID :- `starbotstamil@upi`

GPay :- `starbotstamil@oksbi`

Phonepe :- `starbotstamil@ybl`

Paytm :- `starbotstamil@paytm`

After pay Must Send Screenshot Admin**

<b>🧑🏻‍💻 Developer :- </b><a href=https://t.me/TG_Karthik><b>Karthik</b></a>
**Contact me for more info**"""
