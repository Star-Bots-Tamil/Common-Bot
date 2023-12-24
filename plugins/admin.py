from config import Config
from database.database import db
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import os, sys, time, asyncio, logging, datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
 
@Client.on_message(filters.command("stats") & filters.user(Config.ADMINS))
async def get_stats(bot, message):
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - bot.uptime))    
    start_t = time.time()
    st = await message.reply('**Accessing The Bot Details...**')    
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await st.edit(text=f"**--Bot Status--**\n\n👭 Total Users 📊 :-** `{total_users}`\n**⌚️ Bot Uptime :- `{uptime}`\n🐌 Current Ping :- `{time_taken_s:.3f} MS`")

@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMINS) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await bot.send_message(Config.LOG_CHANNEL, f"**{m.from_user.mention} or {m.from_user.id} is Started The Broadcast 💌...**")
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("**Broadcast 💌 Started...!**") 
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['_id'], broadcast_msg)
        if sts == 200:
           success += 1
        else:
           failed += 1
        if sts == 400:
           await db.delete_user(user['_id'])
        done += 1
        if not done % 20:
           await sts_msg.edit(f"**Broadcast 💌 in Progress :-\nTotal Users 📊 :- {total_users}\nCompleted :- {done} / {total_users}\nSuccess :- {success}\nFailed :- {failed}**")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"**Broadcast Completed...\nCompleted in :- `{completed_in}`.\n\nTotal Users 📊 :- {total_users}\nCompleted :- {done} / {total_users}\nSuccess :- {success}\nFailed :- {failed}**")
           
async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} :- Deactivated")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} :- Blocked The Bot")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} :- User ID Invalid")
        return 400
    except Exception as e:
        logger.error(f"{user_id} :- {e}")
        return 500
    
@Client.on_message(filters.private & filters.command("ban"))
async def ban(c, m):
    if m.from_user.id not in Config.ADMINS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"**Use This Command to Ban 🛑 any User From the Bot 🤖.\n\nUsage:-\n\n/ban user_id ban_duration ban_reason\n\n Example :- /ban 1234567 28 You Misused me.\n This Will Ban User with ID `1234567` for `28` Days for the Reason `You Misused me`.**",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = " ".join(m.command[3:])
        ban_log_text = f"**Banning user {user_id} for {ban_duration} Days for the Reason {ban_reason}.**"

        try:
            await c.send_message(
                user_id,
                f"**You are Banned 🚫 to Use This Bot for {ban_duration} day(s) for the reason __{ban_reason}__ \n\nMessage from the Admin 🤠**",
            )
            ban_log_text += "**\n\nUser Notified Successfully!!**"
        except BaseException:
            traceback.print_exc()
            ban_log_text += (
                f"**\n\n ⚠️ User Notification Failed! ⚠️ \n\n`{traceback.format_exc()}`**"
            )
        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(ban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"**Error Occurred ⚠️! Traceback Given below\n\n`{traceback.format_exc()}`**",
            quote=True
        )

@Client.on_message(filters.private & filters.command("unban"))
async def unban(c, m):
    if m.from_user.id not in Config.ADMINS:
        await m.delete()
        return
    if len(m.command) == 1:
        await m.reply_text(
            f"**Use this Command to Unban 😃 Any user.\n\nUsage:\n\n`/unban user_id`\n\nEg: `/unban 1234567`\n This will unban user with id `1234567`.**",
            quote=True,
        )
        return

    try:
        user_id = int(m.command[1])
        unban_log_text = f"**Unbanning User 🤪 {user_id}**"

        try:
            await c.send_message(user_id, f"Your ban was lifted!")
            unban_log_text += "**\n\n✅ User Notified Successfully!! ✅**"
        except BaseException:
            traceback.print_exc()
            unban_log_text += (
                f"**\n\n⚠️ User Notification Failed! ⚠️\n\n`{traceback.format_exc()}`**"
            )
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(unban_log_text, quote=True)
    except BaseException:
        traceback.print_exc()
        await m.reply_text(
            f"**⚠️ Error Occurred ⚠️! Traceback Given below\n\n`{traceback.format_exc()}`**",
            quote=True,
        )

@Client.on_message(filters.private & filters.command("banned"))
async def _banned_usrs(c, m):
    if m.from_user.id not in Config.ADMINS:
        await m.delete()
        return
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ""
    async for banned_user in all_banned_users:
        user_id = banned_user["id"]
        ban_duration = banned_user["ban_status"]["ban_duration"]
        banned_on = banned_user["ban_status"]["banned_on"]
        ban_reason = banned_user["ban_status"]["ban_reason"]
        banned_usr_count += 1
        text += f"💁🏻 **User ID :- `{user_id}`\nBan Duration :- `{ban_duration}`\nBanned on :- `{banned_on}`\nReason :- `{ban_reason}`\n\n**"
    reply_text = f"**Total Banned User(s) 🤭: `{banned_usr_count}`\n\n{text}**"
    if len(reply_text) > 4096:
        with open("banned-users.txt", "w") as f:
            f.write(reply_text)
        await m.reply_document("banned-users.txt", True)
        os.remove("banned-users.txt")
        return
    await m.reply_text(reply_text, True)
 
