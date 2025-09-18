from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    ChatJoinRequest
)
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

gif = ['https://telegra.ph/file/907671f537f2925e30755-041a2bd1a617b0ac68.gif']


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Main process ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_chat_join_request()
async def approve(client: Client, join_request: ChatJoinRequest):
    """
    Handle incoming chat join requests.
    Approves the request and attempts to DM the user a welcome message/video.
    Robustly handles cases where the bot cannot DM the user.
    """
    chat = join_request.chat
    user = join_request.from_user

    try:
        # store group in DB (if you want)
        add_group(chat.id)

        # approve the join request
        await client.approve_chat_join_request(chat.id, user.id)

        # record user in DB
        add_user(user.id)

        # prepare welcome media/text
        img = random.choice(gif)
        caption = (
            f"**Hello {user.mention}!**\n"
            f"Welcome To **{chat.title}**\n\n"
            "__Powerd By : @AcceptronBotUpdates__"
        )

        # try sending a video; fall back to text if sending media fails
        try:
            await client.send_video(chat_id=user.id, video=img, caption=caption)
            print(f"Sent welcome video to {user.id}")
        except errors.Flood as e:
            # rare: flood-type error
            print("Flood error while sending video:", e)
            # try send plain message after waiting a bit
            await asyncio.sleep(1)
            try:
                await client.send_message(chat_id=user.id, text=caption)
            except Exception as inner_e:
                print("Failed to send fallback message:", inner_e)
        except (errors.Forbidden, errors.PeerIdInvalid, errors.InputUserDeactivated) as send_err:
            # user probably didn't start bot or blocked bot; handle gracefully
            print(f"Can't DM user {user.id}: {send_err}")
            # don't remove user from DB here; just continue
        except FloodWait as fw:
            # obey Telegram's flood wait
            print(f"FloodWait: sleeping for {fw.value} seconds")
            await asyncio.sleep(fw.value)
            # optionally attempt again once
            try:
                await client.send_message(chat_id=user.id, text=caption)
            except Exception as e:
                print("Retry failed after FloodWait:", e)

    except errors.PeerIdInvalid as e:
        # this means the target peer (probably the user) is invalid for approve or something similar
        print("PeerIdInvalid (likely bot not started by group owner or invalid peer):", e)
    except Exception as err:
        # catch-all to prevent crash
        print("Unexpected error in approve handler:", err)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Start ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("start"))
async def op(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
        if m.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("📢 Updates", url="https://t.me/AcceptronBotUpdates"),
                        InlineKeyboardButton("📩 Support", url="https://t.me/AcceptronBotUpdates")
                    ],
                    [
                        InlineKeyboardButton("💬 Add to Group", url="https://t.me/AcceptronBot?startgroup=true&admin=invite_users+promote_members+delete_messages"),
                        InlineKeyboardButton("♂️ Add to Channel", url="https://t.me/AcceptronBot?startchannel=true&admin=post_messages+delete_messages+edit_messages+invite_users+promote_members")
                    ]
                ]
            )
            add_user(m.from_user.id)
            await m.reply_photo(
                "https://telegra.ph/file/3daa05d88c7c540d58a34-5fda1078570d6eb916.jpg",
                caption="**👋 Hey {}!\nApprove join requests instantly in your Groups & Channels. Just add & promote me!\n\n__Powerd By : @AcceptronBotUpdates__**".format(m.from_user.mention),
                reply_markup=keyboard
            )

        elif m.chat.type == enums.ChatType.GROUP or m.chat.type == enums.ChatType.SUPERGROUP:
            keyboar = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("💁‍♂️ Start me private 💁‍♂️", url="https://t.me/AcceptronBot?start=start")
                    ]
                ]
            )
            add_group(m.chat.id)
            await m.reply_text("**👋 Hey {}!\nwrite me private for more details**".format(m.from_user.first_name), reply_markup=keyboar)
        print(m.from_user.first_name + " Is started Your Bot!")

    except UserNotParticipant:
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🍀 Check Again 🍀", callback_data="chk")
                ]
            ]
        )
        await m.reply_text("**⚠️Access Denied!⚠️\n\nPlease Join @{} to use me.If you joined click check again button to confirm.**".format(cfg.FSUB), reply_markup=key)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ callback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_callback_query(filters.regex("chk"))
async def chk(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
        if cb.message.chat.type == enums.ChatType.PRIVATE:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("📢 Updates", url="https://t.me/AcceptronBotUpdates"),
                        InlineKeyboardButton("📩 Support", url="https://t.me/AcceptronBotUpdates")
                    ],
                    [
                        InlineKeyboardButton("💬 Add to Group", url="https://t.me/AcceptronBot?startgroup=true&admin=invite_users+promote_members+delete_messages"),
                        InlineKeyboardButton("♂️ Add to Channel", url="https://t.me/AcceptronBot?startchannel=true&admin=post_messages+delete_messages+edit_messages+invite_users+promote_members")
                    ]
                ]
            )
            add_user(cb.from_user.id)
            await cb.message.edit("**👋 Hey {}!\nApprove join requests instantly in your Groups & Channels. Just add & promote me!\n\n__Powerd By : @AcceptronBotUpdates__**".format(cb.from_user.mention), reply_markup=keyboard)
        print(cb.from_user.first_name + " Is started Your Bot!")
    except UserNotParticipant:
        await cb.answer("🙅‍♂️ You are not joined to channel join and try again. 🙅‍♂️")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ info ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    xx = all_users()
    x = all_groups()
    tot = int(xx + x)
    await m.reply_text(text=f"""
🍀 Chats Stats 🍀
🙋‍♂️ Users : `{xx}`
👥 Groups : `{x}`
🚧 Total users & groups : `{tot}` """)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "bcast":
                await m.reply_to_message.copy(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Broadcast Forward ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m: Message):
    allusers = users
    lel = await m.reply_text("`⚡️ Processing...`")
    success = 0
    failed = 0
    deactivated = 0
    blocked = 0
    for usrs in allusers.find():
        try:
            userid = usrs["user_id"]
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
            success += 1
        except FloodWait as ex:
            await asyncio.sleep(ex.value)
            if m.command[0] == "fcast":
                await m.reply_to_message.forward(int(userid))
        except errors.InputUserDeactivated:
            deactivated += 1
            remove_user(userid)
        except errors.UserIsBlocked:
            blocked += 1
        except Exception as e:
            print(e)
            failed += 1

    await lel.edit(f"✅Successfull to `{success}` users.\n❌ Faild to `{failed}` users.\n👾 Found `{blocked}` Blocked users \n👻 Found `{deactivated}` Deactivated users.")


print("I'm Alive Now!")
app.run()
