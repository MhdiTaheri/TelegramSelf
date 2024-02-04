#coded by @DevSeyed in Telegram
from lib import *

settings_folder = 'settings'
file_defaults = {
    'time.txt': 'False',
    'nameinfo.txt': 'time',
    'bioinfo.txt': 'False',
    'heart.txt': 'False',
    'rnamest.txt': 'False',
    'bio.txt': 'time',
    'mode.txt': 'Default',
    'creator.txt': '@DevSeyed',
    'rname.txt': ''
}

if not os.path.exists(settings_folder):
    os.makedirs(settings_folder)

for file_name, default_content in file_defaults.items():
    file_path = os.path.join(settings_folder, file_name)
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write(default_content)

#check command
@client.on(events.NewMessage(pattern='/check'))
async def handle_start_command(event):
    await start_command(event)
#end of command check


@client.on(events.NewMessage(pattern='/help'))
async def handle_inline(event):
    if event.sender_id == admin_user_id:
        try:
            if event.raw_text == '/help 1':
                await help_1(event)
            elif event.raw_text == '/help 2':
                await help_2(event)
            elif event.raw_text == '/help 3':
                await help_3(event)
            elif event.raw_text == '/help 4':
                await help_4(event)
        except Exception as e:
            await event.reply(f"Error sending panel: {e}")


@client.on(events.NewMessage(pattern='/ping'))
async def handle_ping(event):
    await ping(event)


@client.on(events.NewMessage(pattern='/mem'))
async def handle_mem(event):
    await mem(event)


if not os.path.exists(MSAVE_DIRECTORY):
    os.makedirs(MSAVE_DIRECTORY)

@client.on(events.NewMessage(pattern='/gmusic'))
async def handle_sc(event):
    await sc(event)

@client.on(events.NewMessage(pattern='/tarikh'))
async def handle_tarikh(event):
    await tarikh(event)

@client.on(events.NewMessage(pattern='/gmsg'))
async def handle_gmsg(event):
    await gmsg(event)

@client.on(events.NewMessage(pattern='/weather'))
async def handle_weather(event):
    await weather(event)

@client.on(events.NewMessage(pattern='/rsong'))
async def handle_rsong(event):
    await rsong(event)

@client.on(events.NewMessage(pattern='/info'))
async def handle_info(event):
    await info(event)

@client.on(events.NewMessage(pattern='/setprof'))
async def handle_set_profile_pic(event):
    await set_profile_pic(event)

@client.on(events.NewMessage(pattern='/delprof'))
async def handle_delete_profile_pic(event):
    await delete_profile_pic(event)

@client.on(events.NewMessage(pattern='/rinfo'))
async def handle_rinfo(event):
    await rinfo(event)

@client.on(events.NewMessage(pattern='/rem'))
async def handle_delete_recent_messages(event):
    await delete_recent_messages(event)

@client.on(events.NewMessage(pattern='/sgoogle'))
async def handle_sgoogle(event):
    await sgoogle(event)

@client.on(events.NewMessage(pattern='/wiki'))
async def handle_wiki(event):
    await wiki(event)

@client.on(events.NewMessage(pattern='/save'))
async def handle_save_message(event):
    await save_message(event)


#Auto Save
@client.on(events.NewMessage)
async def save_self_destructing_media(event):
    try:
        if (
            event.sender_id != admin_user_id
            and event.is_private
            and event.message.media
            and hasattr(event.message.media, 'ttl_seconds')
            and event.message.media.ttl_seconds is not None
            and event.message.media.ttl_seconds > 0
        ):
            file = await event.download_media()
            user_id = event.sender_id
            username = event.sender.username
            caption = f"**❈ Self-Saved Photo From User: `{user_id}`, @{username}**"
            await client.send_file(admin_user_id, file, caption=caption)
            os.remove(file)

    except Exception as e:
        await event.respond(f"❈ Error while saving self-destructing media: {str(e)}")
# End Auto Save


@client.on(events.NewMessage(pattern='/addbio'))
async def handle_add_bio(event):
    await add_bio(event)

@client.on(events.NewMessage(pattern='/addlname'))
async def handle_add_lname(event):
    await add_lname(event)

@client.on(events.NewMessage(pattern='/addrname'))
async def handle_add_rname(event):
    await add_rname(event)

@client.on(events.NewMessage(pattern='/delrname'))
async def handle_delete_rname(event):
    await delete_rname(event)

@client.on(events.NewMessage(pattern='/reload'))
async def handle_reload_bot(event):
    await reload_bot(event)

@client.on(events.NewMessage(pattern='/backupchat'))
async def handle_backup_chat(event):
    await backup_chat(event)

@client.on(events.NewMessage(pattern='/calc'))
async def handle_calculator(event):
    await calculator(event)

@client.on(events.NewMessage(pattern='/create_channel (.*)'))
async def handle_create_channel(event):
    await create_channel(event)

@client.on(events.NewMessage(pattern='/silent'))
async def handle_enemy_mode(event):
    await enemy_mode(event)

@client.on(events.NewMessage(pattern='/unsilent'))
async def handle_unenemy_mode(event):
    await unenemy_mode(event)

@client.on(events.NewMessage)
async def delete_enemy_messages(event):
    sender_id = event.sender_id
    if sender_id in enemy_list:
        user_msgs = user_messages.get(sender_id, [])
        user_msgs.append(event.message)
        user_messages[sender_id] = user_msgs[-10:]

        if len(user_msgs) >= 10:
            await client(functions.contacts.BlockRequest(sender_id))
            await client.send_message(admin_user_id, f"**❈System Notification ⚠\nBlocked User {sender_id} for sending too many messages while in silent mode**")

        await event.delete()

@client.on(events.NewMessage(pattern='/tag'))
async def handle_tag_all_members(event):
    await tag_all_members(event)

@client.on(events.NewMessage(pattern='/Del'))
async def handle_delete_reply(event):
    await delete_reply(event)

@client.on(events.NewMessage(pattern='/GSilent'))
async def handle_save_user_id(event):
    await save_user_id(event)

@client.on(events.NewMessage(pattern='/GUnSilent(\s+\d+)?'))
async def handle_remove_user_from_silenced(event):
    await remove_user_from_silenced(event)

@client.on(events.NewMessage(pattern='/promote'))
async def handle_promote_user_to_admin(event):
    await promote_user_to_admin(event)

@client.on(events.NewMessage(pattern='/demote'))
async def handle_demote_admin(event):
    await demote_admin(event)

@client.on(events.NewMessage)
async def delete_silent_user_messages(event):
    if event.is_group and event.sender_id in silenced_users:
        await client.delete_messages(event.chat_id, [event.id])

@client.on(events.NewMessage(pattern='/pass'))
async def handle_generate_password(event):
    await generate_password(event)

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

@client.on(events.NewMessage(pattern='/Gmedia'))
async def handle_save_video(event):
    await save_video(event)

@client.on(events.NewMessage(pattern='/Smedia'))
async def handle_send_video(event):
    await send_video(event)

@client.on(events.NewMessage(pattern='/Lmedia'))
async def handle_list_saved_media(event):
    await list_saved_media(event)

@client.on(events.NewMessage(pattern='/Freplay'))
async def handle_fast_replies(event):
    await ffast_replies(event)

@client.on(events.NewMessage(pattern='/Lreplay'))
async def handle_show_fast_replies(event):
    await show_fast_replies(event)

@client.on(events.NewMessage)
async def handle_user_message(event):
    if event.sender_id != admin_user_id:
        message = event.raw_text
        reply = fast_replies.get(message.lower())
        if reply:
            await event.reply(reply)

@client.on(events.NewMessage(pattern='/whois'))
async def handle_whois_domain(event):
    await whois_domain(event)

@client.on(events.NewMessage(pattern='/Scrypto'))
async def handle_show_crypto_prices(event):
    await show_crypto_prices(event)

@client.on(events.NewMessage(pattern='/sreplace'))
async def handle_replace_words(event):
    await replace_words(event)

@client.on(events.NewMessage(pattern='/Convertdate'))
async def convert_date(event):
    await convert_date(event)

@client.on(events.NewMessage(pattern='/setname'))
async def handle_set_user_first_name(event):
    await set_user_first_name(event)

@client.on(events.NewMessage(pattern='/sfootball'))
async def handle_get_football_stats(event):
    await get_football_stats(event)

@client.on(events.NewMessage(pattern='/setcolor'))
async def apply_color_filter(event):
    await apply_color_filter(event)

@client.on(events.NewMessage(pattern='/flood (\d+) - ([\w,]+)'))
async def handle_flood_message(event):
    await flood_message(event)

@client.on(events.NewMessage(pattern='/orcen (.+)'))
async def handle_replay_as_voice(event):
    await replay_as_voice(event)

@client.on(events.NewMessage(pattern='/setfname (.+)'))
async def handle_set_music_name(event):
    await set_music_name(event)

@client.on(events.NewMessage(pattern='/screen (.+)'))
async def handle_take_screenshot(event):
    await take_screenshot(event)

if not os.path.exists(SAVE_DIRECTORY_YT):
    os.makedirs(SAVE_DIRECTORY_YT)

@client.on(events.NewMessage(pattern='/yt (.+)'))
async def handle_download_youtube_video(event):
    await download_youtube_video(event)

@client.on(events.NewMessage(pattern='/Sproxy'))
async def handle_proxy_command(event):
    await proxy_command(event)

@client.on(events.NewMessage(pattern='/Sv2ray'))
async def handle_v2ray_command(event):
    await v2ray_command(event)


@client.on(events.NewMessage(pattern='/time (.+)'))
async def handle_get_world_time(event):
    await get_world_time(event)

load_timers()

@client.on(events.NewMessage(pattern='newtimer (.+)'))
async def handle_create_timer(event):
    await create_timer(event)

@client.on(events.NewMessage(pattern='deltimer (.+)'))
async def handle_delete_timer(event):
    await delete_timer(event)

@client.on(events.NewMessage(pattern='timers'))
async def handle_list_timers(event):
    await list_timers(event)

@client.on(events.NewMessage(pattern='clean timers'))
async def handle_clean_timers(event):
    await clean_timers(event)

@client.on(events.NewMessage(pattern='gfile (.+)'))
async def handle_download_file(event):
    await download_file(event)

@client.on(events.NewMessage(pattern='getip (.+)'))
async def handle_get_ip_info(event):
    await get_ip_info(event)

@client.on(events.NewMessage(pattern='/sunextract|/استخراج فایل'))
async def handle_extract_files(event):
    await extract_files(event)


@client.on(events.NewMessage(pattern='Stv'))
async def handle_send_tv_channels(event):
    await send_tv_channels(event)

@client.on(events.NewMessage(pattern='(به qr|sqr)'))
async def handle_create_qr_code(event):
    await create_qr_code(event)

@client.on(events.NewMessage(pattern='(?i)(خواندن qr|readqr)'))
async def handle_read_qr_code(event):
    await read_qr_code(event)

@client.on(events.NewMessage(pattern='(پاکسازی همه|cleanall)'))
async def handle_clean_messages_containing_text(event):
    await clean_messages_containing_text(event)

@client.on(events.NewMessage(pattern='^(joinall|پیوستن به همه)$'))
async def handle_join_all_channels(event):
    await join_all_channels(event)

@client.on(events.NewMessage(pattern='^(setusername|تنظیم نام کاربری) (.+)'))
async def handle_set_bot_username(event):
    await set_bot_username(event)

@client.on(events.NewMessage(pattern='^(اخراج|kick) (.+)'))
async def handle_kick_users(event):
    await kick_users(event)

@client.on(events.NewMessage(pattern='(پاکسازی بین|cleanb)'))
async def handle_clean_between_messages(event):
    await clean_between_messages(event)

@client.on(events.NewMessage(pattern='(?i)/Ggit'))
async def handler_Git(event):
    await Git(event)

@client.on(events.NewMessage(pattern='/copycontent'))
async def handler_copycontent(event):
    await copycontent(event)

@client.on(events.NewMessage(pattern='^(timename on|timename off|mini on|bio on|bio off|bold on|default on|mono on|heart on|heart off|rname on|rname off|see rname|see bio|see lname)$'))
async def handle_settings(event):
    await settings(event)

client.start()
client.loop.create_task(update_first_name())
client.loop.create_task(update_last_name())
client.loop.create_task(update_about())
client.loop.run_until_complete(send_welcome_message())
client.run_until_disconnected()
