from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg
import random, asyncio

app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

gif = ['https://telegra.ph/file/e49a2ea353601f51c2079-2a4cbf3cfb9ab01201.jpg']


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request(filters.group | filters.channel & ~filters.private)
async def approve(_, m : Message):
    op = m.chat
    kk = m.from_user
    try:
        add_group(m.chat.id)
        await app.approve_chat_join_request(op.id, kk.id)
        img = random.choice(gif)
        await app.send_video(kk.id,img, "**Hello {}!\nWelcome To {}\n\n__Powerd By : @AcceptronBotUpdates__**".format(m.from_user.mention, m.chat.title))
        add_user(kk.id)
    except errors.PeerIdInvalid as e:
        print("user isn't start bot(means group)")
    except Exception as err:
        print(str(err))    
 
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("start"))
async def op(_, m :Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id) 
        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("📢 Updates", url="https://t.me/AcceptronBotUpdates"),
                        InlineKeyboardButton("📩 Support", url="https://t.me/AcceptronBotUpdates")
                    ],[
                        InlineKeyboardButton("💬 Add to Group", url="https://t.me/AcceptronBot?startgroup=true&admin=invite_users+promote_members+delete_messages"),
                        InlineKeyboardButton("♂️ Add to Channel", url="https://t.me/AcceptronBot?startchannel=true&admin=post_messages+delete_messages+edit_messages+invite_users+promote_members")
                    ]
                ]
            )
            add_user(m.from_user.id)
            await m.reply_photo("https://telegra.ph/file/e49a2ea353601f51c2079-2a4cbf3cfb9ab01201.jpg", caption="**👋 Hey {}!\nApprove join requests instantly in your Groups & Channels. Just add & promote me!\n\n__Powerd By : @AcceptronBotUpdates__**".format(m.from_user.mention), reply_markup=keyboard)
    
        elif m.chat.type == enums.ChatType.GROUP or enums.ChatType.SUPERGROUP:
            keyboar = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💁‍♂️ Start me private 💁‍♂️", url="https://t.me/AcceptronBott?start=start")
                    ]
                ]
            )
            add_group(m.chat.id)
            await m.reply_text("**👋 Hey {}!\nwrite me private for more details**".format(m.from_user.first_name), reply_markup=keyboard)
        print(m.from_user.first_name +" Is started Your Bot!")

  from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

# Your channel username
FSUB = "@AcceptronBotUpdates"  # replace with your actual channel

# Initialize the bot
app = Client(
    "my_bot",                 # session name
    bot_token="YOUR_BOT_TOKEN"  # replace with your bot token
)

# Start command
@app.on_message(filters.private & filters.command("start"))
async def start(client, m):
    try:
        # Check if user is a member
        member = await client.get_chat_member(FSUB, m.from_user.id)
        await m.reply_text("✅ You have access!")
    except UserNotParticipant:
        # User not a member, show button
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🍀 Check Again 🍀", callback_data="chk")
                ]
            ]
        )
        await m.reply_text(
            f"⚠️ Access Denied! ⚠️\n\nPlease join @{FSUB} to use me.\nIf you joined, click 'Check Again' to confirm.",
            reply_markup=key
        )

# Callback for "Check Again"
@app.on_callback_query()
async def check_again(client, callback_query):
    if callback_query.data == "chk":
        try:
            member = await client.get_chat_member(FSUB, callback_query.from_user.id)
            await callback_query.message.edit_text("✅ Access Granted! Welcome!")
        except UserNotParticipant:
            await callback_query.answer("❌ You are still not joined!", show_alert=True)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb : CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("📢 Updates", url="https://t.me/AcceptronBotUpdates"),
                        InlineKeyboardButton("📩 Support", url="https://t.me/AcceptronBotUpdates")
                    ],[
                         InlineKeyboardButton("💬 Add to Group", url="https://t.me/AcceptronBot?startgroup=true&admin=invite_users+promote_members+delete_messages"),
                         InlineKeyboardButton("♂️ Add to Channel", url="https://t.me/AcceptronBot?startchannel=true&admin=post_messages+delete_messages+edit_messages+invite_users+promote_members") 
                    ]
                ]
            )
            add_user(cb.from_user.id)
            await cb.message.edit("**👋 Hey {}!\nApprove join requests instantly in your Groups & Channels. Just add & promote me!\n\n__Powerd By : @AcceptronBotUpdates__**".format(m.from_user.mention), reply_markup=keyboard)
        print(cb.from_user.first_name +" Is started Your Bot!")
    except UserNotParticipant:
        await cb.answer("🙅‍♂️ You are not joined to channel join and try again. 🙅‍♂️")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m : Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m : Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            #print(int(userid))
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success +=1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated +=1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked +=1
        except Exception as e:
            print(e)
            failed +=1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")

print("I'm Alive Now!")
app.run()
