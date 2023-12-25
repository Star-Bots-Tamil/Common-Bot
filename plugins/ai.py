from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters
from config import Config, temp
import openai
openai.api_key = Config.OPENAI_API

@Client.on_message(filters.private & filters.text)
async def ai_answer(client, message):
    if Config.AI == True: 
        user_id = message.from_user.id
        if user_id:
            try:
                users_message = message.text
                user_id = message.from_user.id
                response = openai.Completion.create(
                    model = "text-davinci-003",
                    prompt = users_message,
                    temperature = 0.5, 
                    max_tokens = 1000,
                    top_p=1,
                    frequency_penalty=0.1,
                    presence_penalty = 0.0,
                )
                btn=[
                        [InlineKeyboardButton(text=f"⇱🤷‍♀️ Take Action 🗃️⇲", url=f'https://t.me/{temp.U_NAME}')],
                        [InlineKeyboardButton(text=f"🗑 Delete log ❌", callback_data=f'close_data')],
                    ]
                reply_markup=InlineKeyboardMarkup(btn)
                footer_credit = "🦋<a href='https://telegram.me/LazyDeveloperSupport'>• ʀᴇᴘᴏʀᴛ ɪꜱꜱᴜᴇ •</a>══<a href='https://telegram.me/LazyDeveloperr'>• ᴄᴏɴᴛᴀᴄᴛ ᴍᴀꜱᴛᴇʀ •</a>🦋"
                response = response.choices[0].text 
                await client.send_message(Config.AI_LOGS, text=f"⚡️⚡️#Lazy_AI_Query \n\n• A user named **{message.from_user.mention}** with user id - `{user_id}`. Asked me this query...\n\n══❚█══Q   U   E   R   Y══█❚══\n\n\n[Q྿.]**{lazy_users_message}**\n\n👇Here is what i responded:\n:-`{lazy_response}`\n\n\n❚═USER ID═❚═• `{user_id}` \n❚═USER Name═❚═• `{message.from_user.mention}` \n\n🗃️" , reply_markup = reply_markup )
                await message.reply(f"{response}\n\n\n{footer_credit}")
            except Exception as error:
                print(error)
                await message.reply_text(f'Error aa gya Lazy Bhaiya 😀\n\n{error}')
    else:
        return
