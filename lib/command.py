from library import *
from Information import *
from updater import *

async def send_welcome_message():
    admin_user = await client.get_entity(admin_user_id)
    admin_first_name = admin_user.first_name if admin_user.first_name else "there"
    helptxt = f"use `/help 1` command"
    
    try:
        await client(JoinChannelRequest("@TRself"))
    except Exception as e:
        print(f"Failed to join @TRself channel: {e}")

    await client.send_message(admin_user_id, f'Hi {admin_first_name}!\nWelcome to the TRself bot.\n**DEV: @TRself **\n{helptxt}')



def set_user_bio(bio):
    with open('settings/bio.txt', 'w') as f:
        f.write(bio)

def set_user_lname(lname):
    with open('settings/nameinfo.txt', 'w') as f:
        f.write(lname)

def get_user_bio():
    with open('settings/bio.txt', 'r') as f:
        return f.read().strip()

async def download_and_send(audio_url, event, title, artist, views, release_date, url):
    response = urllib.request.urlopen(audio_url)
    audio_file = io.BytesIO(response.read())
    audio_file.name = f"{title}.mp3"
    caption = f"{title} - {artist}\nViews: {views} k\nRelease date: {release_date}\nLink: {url}\n\n**Note: Due to the copyright law, we can only show you 30 seconds of music here, I hope you understand us**"
    await client.send_file(event.chat_id, audio_file, caption=caption)

def load_admins():
    try:
        with open('settings/admin.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_admins(admins):
    with open('settings/admin.json', 'w') as file:
        json.dump(admins, file)

def generate_random_filename():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(10))

def find_matching_filename(message):
    for file in os.listdir(SAVE_FOLDER):
        if message.lower() == os.path.splitext(file)[0].lower():
            return os.path.join(SAVE_FOLDER, file)
    return None

fast_replies_file = 'settings/fast_replies.json'

def load_fast_replies():
    try:
        with open(fast_replies_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_fast_replies(fast_replies):
    with open(fast_replies_file, 'w') as f:
        json.dump(fast_replies, f, indent=4)




def get_uptime(start_time):
    now = datetime.datetime.now()
    uptime = now - start_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} days {hours} hours {minutes} minutes {seconds} seconds"

start_time = datetime.datetime.now()
async def start_command(event):
    if event.sender_id == admin_user_id:
        uptime = get_uptime(start_time)
        message = f"**Bot is online:)\nUptime is: {uptime}**"
        await event.edit(message)

async def ping(event):
    if event.sender_id == admin_user_id:
        start_time = datetime.datetime.now()
        await event.delete()
        message = await event.respond('Pong!')
        end_time = datetime.datetime.now()
        response_time = (end_time - start_time).total_seconds() * 1000
        user_link = f'❈[I Never Lose](tg://user?id={admin_user_id})'
        await message.edit(f'**{user_link} ! Response time: {response_time:.2f} ms**')

async def mem(event):
    if event.sender_id == admin_user_id:
        memory = psutil.virtual_memory().percent
        await event.edit(f'**❈MEMORY USAGE: {memory} MEG**')

MSAVE_DIRECTORY = 'music'

async def sc(event):
    if event.sender_id == admin_user_id:
        query = event.raw_text[7:]  # Adjust the index to match '/gmusic '
        results = sp.search(q=query, type='track')
        tracks = results.get('tracks', {}).get('items', [])
        
        if tracks:
            track = tracks[0]
            title = track.get('name', '')
            artist = track.get('artists', [{}])[0].get('name', '')
            url = track.get('external_urls', {}).get('spotify', '')
            views = track.get('popularity', '')
            release_date = track.get('album', {}).get('release_date', '')
            
            await event.delete()
            await download_and_send(track, event, title, artist, views, release_date, url)
        else:
            await event.edit(f'**❈Sorry, no results found.**')

async def download_and_send(track, event, title, artist, views, release_date, url):
    try:
        audio_url = track.get('preview_url')
        
        if audio_url:
            audio_file_path = os.path.join(MSAVE_DIRECTORY, f'{title}.mp3')
            async with aiohttp.ClientSession() as session:
                async with session.get(audio_url) as resp:
                    if resp.status == 200:
                        with open(audio_file_path, 'wb') as file:
                            while True:
                                chunk = await resp.content.read(1024)
                                if not chunk:
                                    break
                                file.write(chunk)
                        
                        await event.reply(
                            file=audio_file_path,
                            message=f"**❈Title: {title}\nArtist: {artist}\nViews: {views} K\nRelease Date: {release_date}\n[Listen on Spotify]({url})**",
                        )
                        
                        os.remove(audio_file_path)
                    else:
                        await event.reply(f"Failed to download: Status {resp.status}")
        else:
            await event.reply(f"No audio preview available.")
    
    except Exception as e:
        await event.reply(f"Failed: {str(e)}")


async def tarikh(event):
    if event.sender_id == admin_user_id:
        try:
            jalali_date = JalaliDate.today().strftime('%A %d %B %Y')
            await event.edit(f'**❈ Today is: {jalali_date}**')
        except Exception as e:
            await event.reply(f"Failed to retrieve date: {str(e)}")

async def gmsg(event):
    if event.sender_id == admin_user_id:
        try:
            await event.delete()
            processing_message = await event.respond("Processing your message...")

            msg = event.raw_text[6:]
            for i in range(len(msg)):
                await processing_message.edit(f"{msg[:i+1]}")
                await asyncio.sleep(0.3)

            await processing_message.edit(f"{msg} 💚")
        except Exception as e:
            await event.reply(f"Failed to process message: {str(e)}")

async def weather(event):
    if event.sender_id == admin_user_id:
        try:
            location = event.raw_text[9:]
            url = f'https://wttr.in/{location}?format=%C\n%t\n%h\n'
            response = requests.get(url)

            if response.status_code == 200:
                weather_data = response.text.split('\n')
                condition = weather_data[0]
                temperature = weather_data[1]
                humidity = weather_data[2]

                message = f'**❈ Current weather in {location}:**\n\nCondition: {condition}\nTemperature: {temperature}\nHumidity: {humidity}'
                await event.edit(message)
            else:
                await event.reply('**❈ Sorry, there was an error retrieving the weather information.**')
        except Exception as e:
            await event.reply(f'Failed to fetch weather: {str(e)}')

async def rsong(event):
    if event.sender_id == admin_user_id:
        try:
            channel = '@LiMuTa'
            limit = 100
            messages = await client.get_messages(channel, limit=limit)
            
            audio_messages = [
                m for m in messages 
                if hasattr(m, 'media') 
                and hasattr(m.media, 'document') 
                and m.media.document.mime_type == 'audio/mpeg'
            ]
            
            if audio_messages:
                random_audio_message = random.choice(audio_messages)
                await client.forward_messages(event.chat_id, random_audio_message)
                await event.edit('**❈ Your random song has been sent!**')
                await asyncio.sleep(0.5)
                await client.delete_messages(event.chat_id, event.id)
            else:
                await event.respond('**❈ No audio messages found.**')
        except Exception as e:
            await event.respond(f'Failed to retrieve and send random song: {str(e)}')

async def info(event):
    if event.sender_id == admin_user_id:
        try:
            username = event.text[6:].strip()

            if username:
                user = await client.get_entity(username)

                if isinstance(user, User):
                    photo = await client.download_profile_photo(user)

                    if os.path.exists(photo):
                        caption = f"Id: {user.id}\nFirst: {user.first_name}\nUsername: @{user.username}"
                        await event.reply(file=photo, message=caption)

                        os.remove(photo)
                    else:
                        await event.edit("**❈ Failed to download the profile picture.**")
                else:
                    await event.edit('**❈ Username belongs to a channel or group.**')
            else:
                await event.edit('❈ Please provide a username.')

        except ValueError:
            await event.edit('**❈ Invalid username provided.**')
        except Exception as e:
            await event.edit(f'Failed to retrieve user info: {str(e)}')

async def set_profile_pic(event):
    if event.sender_id == admin_user_id:    
        if event.is_reply:
            try:
                reply = await event.get_reply_message()

                if reply.photo:
                    photo = await client.download_media(reply.photo)

                    with open(photo, 'rb') as f:
                        uploaded_file = await client.upload_file(photo)
                        await client(functions.photos.UploadProfilePhotoRequest(file=uploaded_file))

                    os.remove(photo)  # Remove the photo after it's been uploaded
                    await event.edit(f'**❈ [Profile](tg://user?id={admin_user_id}) picture updated successfully!**')
                else:
                    await event.edit('**❈ Please reply to a photo to set as your profile picture.**')

            except ValueError:
                await event.edit('**❈ Error: Invalid media format.**')
            except Exception as e:
                await event.respond(f'**❈ Error updating profile picture: {str(e)}**')
        else:
            await event.edit('**❈ Please reply to a photo to set as your profile picture.**')

async def delete_profile_pic(event):
    if event.sender_id == admin_user_id:
        try:
            photos = await client.get_profile_photos('me')
            
            if photos:
                await client(functions.photos.DeletePhotosRequest(id=[InputPhoto(id=photos[0].id, access_hash=photos[0].access_hash, file_reference=photos[0].file_reference)]))
                await event.edit(f'**❈ [Profile](tg://user?id={admin_user_id}) picture deleted successfully!**')
            else:
                await event.edit('**❈ No profile photos found to delete.**')
        
        except ValueError:
            await event.edit('**❈ Error: Invalid profile photo data.**')
        except Exception as e:
            await event.edit(f'**❈ Error deleting profile picture: {str(e)}**')

async def rinfo(event):
    if event.sender_id == admin_user_id:
        try:
            await event.delete()
            if event.is_reply:
                reply = await event.get_reply_message()

                if reply.sender_id:
                    user = await client.get_entity(reply.sender_id)

                    if isinstance(user, types.User):
                        user_full = await client(functions.users.GetFullUserRequest(user.id))
                        user_info = await client(functions.users.GetUsersRequest([user.id]))
                        user_status = user_info[0].status

                        if isinstance(user_status, types.UserStatusOnline):
                            last_seen = "آنلاین"
                        elif isinstance(user_status, types.UserStatusOffline):
                            last_seen = user_status.was_online.strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            last_seen = "اخیرا"

                        common_chats = await client(functions.messages.GetCommonChatsRequest(user_id=user.id, max_id=0, limit=10))
                        groups_count = len(common_chats.chats)

                        bio = user_info[0].about if hasattr(user_info[0], 'about') else "ندارد"

                        photos = await client(functions.photos.GetUserPhotosRequest(user_id=user.id, offset=0, max_id=0, limit=0))
                        profile_count = len(photos.photos) if photos and photos.photos else 0

                        info_text = (
                            f"نام: ({user.first_name})\nشناسه: (`{user.id}`)\nنام کاربری: (@{user.username})\nشماره: (***********)\nتعداد پروفایل: ({profile_count})\nوضعیت: ({last_seen})\nگروه‌ها: ({groups_count})\n\nبیوگرافی: ({bio})"
                        )

                        if photos and len(photos.photos) > 0:
                            await client.send_file(event.chat_id, file=photos.photos[0], caption=info_text)
                        else:
                            await client.send_message(event.chat_id, info_text)

                    elif isinstance(user, types.Channel):
                        info_text = f"Id: {user.id}\nTitle: {user.title}\nUsername: {user.username}\nDescription: {user.description}"
                        await client.send_message(event.chat_id, info_text)

                else:
                    await client.send_message(event.chat_id, '**❈ The replied message does not have a sender.**')
            else:
                await client.send_message(event.chat_id, '**❈ Please reply to a message to get its sender information.**')
        except ValueError:
            await client.send_message(event.chat_id, '**❈ Error: Invalid message sender data.**')
        except Exception as e:
            await client.send_message(event.chat_id, f'❈ Error getting information: {str(e)}')

async def delete_recent_messages(event):
    if event.sender_id == admin_user_id:
        try:
            num = int(event.text.split()[1])

            if num > 50:
                await event.respond('**❈ Sorry, you can only delete up to 50 messages at a time.**')
                return

            messages = await client.get_messages(event.chat_id, limit=num)

            if not messages:
                await event.respond('**❈ No messages found to delete.**')
                return

            deleted_messages = await client.delete_messages(entity=event.chat_id, message_ids=[msg.id for msg in messages], revoke=True)
            await event.respond(f'**❈ {num} messages deleted successfully!**')

        except ValueError:
            await event.respond('**❈ Please specify a valid number of messages to delete.**')
        except Exception as e:
            await event.respond(f'**❈ Error deleting messages: {str(e)}**')

async def sgoogle(event):
    if event.sender_id == admin_user_id:
        query = event.raw_text[9:].strip()
        if not query:
            await event.edit('Please enter a query to search.')
            return

        try:
            await event.edit(f'Searching for "{query}"...')
            search_results = list(search(query, num_results=5))

            if not search_results:
                await event.edit('No results found.')
                return

            response_text = f'Top 5 results for "{query}":\n\n'
            for i, result in enumerate(search_results):
                response_text += f'{i + 1}. {result}\n'

            await event.edit(response_text)

        except Exception as e:
            print(f'Error searching Google: {str(e)}')
            await event.edit('Sorry, there was an error searching Google.')

async def wiki(event):
    if event.sender_id == admin_user_id:
        query = event.raw_text[6:].strip()
        if not query:
            await event.edit('Please enter a query to search.')
            return

        try:
            await event.edit(f'Searching for "{query}" on Persian Wikipedia...')
            wikipedia.set_lang('fa')
            page = wikipedia.page(query)
            summary = wikipedia.summary(query)
            response_text = f'Page title: {page.title}\n\nSummary: {summary}'
            await event.edit(response_text)

        except wikipedia.exceptions.PageError:
            await event.edit(f'No Wikipedia page found for "{query}".')

        except wikipedia.exceptions.DisambiguationError as e:
            options = "\n- ".join(e.options[:5])
            await event.edit(f'Multiple options found for "{query}". Please try again with a more specific query.\n\nOptions:\n- {options}')

        except Exception as e:
            print(f'Error searching Wikipedia: {str(e)}')
            await event.respond('Sorry, there was an error searching Wikipedia.')

async def save_message(event):
    if event.sender_id == admin_user_id:
        try:
            await event.delete()
            reply = await event.get_reply_message()
            
            if reply and reply.media:
                if isinstance(reply.media, types.MessageMediaDocument) or isinstance(reply.media, types.MessageMediaPhoto):
                    file = await client.download_media(reply)
                    caption = f"Saved from @{reply.sender.username}" if reply.sender.username else f"Saved from user ID {reply.sender.id}"
                    await client.send_file('me', file, caption=caption)
                    os.remove(file)
                else:
                    return
            else:
                return

        except Exception as e:
            await event.respond(f"❈ Error while saving: {str(e)}")

async def add_bio(event):
    if event.sender_id == admin_user_id:
        try:
            bio = event.message.text.replace('/addbio', '').strip()
            set_user_bio(bio)
            await event.edit(f"**❈ Your bio has been updated to: `{bio}` **")

        except Exception as e:
            await event.respond(f"❈ Error updating bio: {str(e)}")

async def add_lname(event):
    if event.sender_id == admin_user_id:
        try:
            lname = event.message.text.replace('/addlname', '').strip()
            set_user_lname(lname)
            await event.edit(f"**❈ Your lname has been updated to: `{lname}` **")

        except Exception as e:
            await event.respond(f"❈ Error updating lname: {str(e)}")

async def add_rname(event):
    if event.sender_id == admin_user_id:
        try:
            rname_list = event.message.text.replace('/addrname', '').strip()
            rname_items = rname_list.split(',')
            if len(rname_items) >= 3:
                with open('settings/rname.txt', 'w') as f:
                    f.write(rname_list)
                await event.respond(f"**❈ Your rname list has been updated to: `{rname_list}` **")
            else:
                await event.respond(f"❈ Please provide at least 3 items separated by commas for the rname list.")
        
        except Exception as e:
            await event.respond(f"❈ Error updating rname list: {str(e)}")

async def delete_rname(event):
    if event.sender_id == admin_user_id:
        try:
            with open('settings/rname.txt', 'w') as f:
                f.write('')
            await event.respond("**❈ The list of names has been cleared.**")

        except Exception as e:
            await event.respond(f"❈ Error clearing the list of names: {str(e)}")

async def reload_bot(event):
    if event.sender_id == admin_user_id:
        await event.edit('❈𝑹𝒆𝒍𝒐𝒂𝒅𝒊𝒏𝒈 𝒃𝒐𝒕...')
        await asyncio.sleep(0.5)
        await event.edit('❈𝑹𝒆𝒍𝒐𝒂𝒅 𝑪𝒐𝒎𝒑𝒍𝒊𝒕𝒆𝒅!')
        os.execl(sys.executable, sys.executable, *sys.argv)

async def backup_chat(event):
    if event.sender_id == admin_user_id:
        chat = await event.get_chat()
        if isinstance(chat, types.Channel):
            filename = f'{chat.id}_backup.txt'
            messages = await client.get_messages(event.chat_id, limit=1500)
            with open(filename, 'w') as f:
                for message in messages:
                    f.write(f'{message.date} - {message.sender_id} - {message.text}\n')
            caption = f'Backup of the {chat.title if chat.title else "Unnamed chat"} channel'
            await client.send_file(admin_user_id, filename, caption=caption)
            os.remove(filename)
        elif isinstance(chat, types.User):
            filename = f'{chat.id}_backup.txt'
            messages = await client.get_messages(event.chat_id, limit=1500)
            with open(filename, 'w') as f:
                for message in messages:
                    f.write(f'{message.date} - {message.sender_id} - {message.text}\n')
            if chat.last_name:
                caption = f'Backup of the chat with {chat.first_name} {chat.last_name}'
            else:
                caption = f'Backup of the chat with {chat.first_name}'
            await client.send_file(admin_user_id, filename, caption=caption)
            os.remove(filename)
        await event.delete()

async def calculator(event):
    if event.sender_id == admin_user_id:
        expression = event.message.text.replace('/calc', '').strip()
        try:
            result = eval(expression)
            await event.edit(f"{expression} = {result}")
        except:
            await event.edit(f"❈Sorry, I couldn't evaluate the expression.")

async def create_channel(event):
    if event.sender_id == admin_user_id:
        channel_name = event.pattern_match.group(1)
        result = await client(CreateChannelRequest(channel_name, 'Private Channel', megagroup=False))
        if result:
            channel_link = f'https://t.me/{channel_name}'
            await event.edit(f"Channel [{channel_name}]({channel_link}) created", link_preview=False)
        else:
            await event.edit("Failed to create the channel")


enemy_list = []
user_messages = {}

async def enemy_mode(event):
    if event.sender_id == admin_user_id:
        replied_to = await event.get_reply_message()
        if replied_to:
            sender_id = replied_to.sender_id
            if sender_id not in enemy_list:
                enemy_list.append(sender_id)
                await event.edit(f"**❈[User](tg://user?id={sender_id}) has been put in silent mode. All their messages will be deleted.**")
            else:
                await event.edit(f"**❈[User](tg://user?id={sender_id}) is already in silent mode.**")
        else:
            await event.edit(f"**❈Please reply to a message to put the user in silent mode.**")


async def unenemy_mode(event):
    if event.sender_id == admin_user_id:
        replied_to = await event.get_reply_message()
        if replied_to:
            sender_id = replied_to.sender_id
            if sender_id in enemy_list:
                enemy_list.remove(sender_id)
                await event.edit(f"**❈[User](tg://user?id={sender_id}) has been removed from silent mode.**")
            else:
                await event.edit(f"**❈[User](tg://user?id={sender_id}) is not in silent mode.**")
        else:
            await event.edit(f"**❈Please reply to a message to remove the user from silent mode.**")

async def tag_all_members(event):
    if event.is_group and event.sender_id == admin_user_id:
        try:
            chat = await event.get_chat()
            if chat.admin_rights and chat.admin_rights.delete_messages:
                members = await client.get_participants(chat)
                tag_string = '**❈ All Members Tagged:**\n\n'
                for member in members:
                    tag_string += f'[{member.first_name}](tg://user?id={member.id})\n'
                await event.edit(tag_string, parse_mode='Markdown')
            else:
                await event.respond('**❈ You need to be a chat admin with delete messages rights to use this command.**')
        
        except Exception as e:
            await event.respond(f'❈ Error tagging members: {str(e)}')

    else:
        await event.edit('**❈ This command can only be used in groups by an admin.**')

async def delete_reply(event):
    if event.sender_id == admin_user_id:
        try:
            replied_msg = await event.get_reply_message()
            if replied_msg:
                await replied_msg.delete()
                await event.delete()
            else:
                await event.respond('**❈ Please reply to a message to delete it.**')

        except Exception as e:
            await event.respond(f'❈ Error deleting message: {str(e)}')

    else:
        await event.respond('**❈ Only the admin can use this command.**')


GAdmins = load_admins()
SAVE_FOLDER = 'save'
silenced_users = []
async def save_user_id(event):
    if event.is_group and event.sender_id == admin_user_id or event.sender_id in GAdmins:
        replied_msg = await event.get_reply_message()
        if replied_msg:
            user_id = replied_msg.sender_id
            if user_id == admin_user_id or user_id in GAdmins:
                await event.delete()
                await event.respond(f"**❈You can't silence an admin.**")
                return

            if user_id not in silenced_users:
                silenced_users.append(user_id)
                await event.delete()
                await event.respond(f'**❈User with ID [{user_id}](tg://user?id={user_id}) has been added to the silent list.**')
            else:
                await event.delete()
                await event.respond(f'**❈User with ID [{user_id}](tg://user?id={user_id}) is already in the silent list.**')
        else:
            await event.delete()
            await event.respond('Please reply to a message to save the user ID.')
    else:
        await event.delete()
        await event.respond('This command can only be used in groups by the admin.')

async def remove_user_from_silenced(event):
    if event.is_group and event.sender_id == admin_user_id or event.sender_id in GAdmins:
        replied_msg = await event.get_reply_message()
        user_id = None
        if replied_msg:
            user_id = replied_msg.sender_id
        elif event.pattern_match.group(1):
            user_id = int(event.pattern_match.group(1).strip())
        
        if user_id and user_id in silenced_users:
            silenced_users.remove(user_id)
            await event.delete()
            await event.respond(f'**❈User [{user_id}](tg://user?id={user_id}) has been unsilenced.**')
        else:
            await event.delete()
            await event.respond(f'**❈Invalid user or user is not in the silenced list.**')
    else:
        await event.delete()
        await event.respond(f'**❈This command can only be used in groups.**')

async def promote_user_to_admin(event):
    if event.is_group and event.sender_id == admin_user_id:
        replied_msg = await event.get_reply_message()
        if replied_msg:
            user_id = replied_msg.sender_id
            if user_id not in GAdmins:
                GAdmins.append(user_id)
                save_admins(GAdmins)
                await event.edit(f'**❈ User {user_id} has been promoted to admin.**')
            else:
                await event.edit('**❈ User is already an admin.**')
        else:
            await event.edit('**❈ Please reply to a user\'s message to promote them.**')
    else:
        await event.edit('**❈ This command can only be used by group admins.**')

async def demote_admin(event):
    if event.is_group and event.sender_id == admin_user_id:
        replied_msg = await event.get_reply_message()
        if replied_msg:
            user_id = replied_msg.sender_id
            if user_id in GAdmins:
                GAdmins.remove(user_id)
                save_admins(GAdmins)
                await event.edit(f'**❈ User {user_id} has been demoted from admin.**')
            else:
                await event.edit('**❈ User is not an admin.**')
        else:
            await event.edit('**❈ Please reply to a user\'s message to demote them.**')
    else:
        await event.edit('**❈ This command can only be used by group admins.**')

async def generate_password(event):
    if event.sender_id == admin_user_id:
        try:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            await event.edit(f"**❈ Random Password: `{password}` **")

        except Exception as e:
            await event.edit(f'❈ Error generating password: {str(e)}')

async def save_video(event):
    if event.reply_to_msg_id and event.sender_id == admin_user_id:
        replied_msg = await event.get_reply_message()
        if isinstance(replied_msg.media, (types.MessageMediaPhoto, types.MessageMediaDocument)):
            media = replied_msg.media
            filename = generate_random_filename()
            save_path = os.path.join(SAVE_FOLDER, filename)
            await client.download_media(media, file=save_path)
            await event.edit(f"**❈Media saved as `{filename}`**")
        else:
            await event.edit(f"**❈Reply to a photo or video to save it.**")
    else:
        await event.edit(f"**❈Please reply to a photo or video to save it.**")

async def send_video(event):
    if event.sender_id == admin_user_id:
        message = event.raw_text.replace('/Smedia', '').strip()
        filename = find_matching_filename(message)
        if filename:
            await event.delete()
            await client.send_file(event.chat_id, filename)
            os.remove(filename)
        else:
            await event.edit(f"**❈No video file found with the name {message}.**")

async def list_saved_media(event):
    if event.sender_id == admin_user_id:
        files = os.listdir(SAVE_FOLDER)
        if files:
            file_names = [os.path.splitext(file)[0] for file in files]
            file_list = '\n'.join(file_names)
            await event.edit(f"**❈List of saved media:**\n`{file_list}`")
        else:
            await event.edit("**❈No media files saved.**")


fast_replies = load_fast_replies()

async def ffast_replies(event):
    global fast_replies, admin_user_id

    if event.sender_id == admin_user_id:
        text = event.raw_text.replace('/Freplay', '').strip()
        if text.startswith('add'):
            parts = text.split(',', 1)
            if len(parts) == 2:
                keyword = parts[0].strip().replace('add', '').strip()
                reply = parts[1].strip()
                fast_replies[keyword.lower()] = reply
                save_fast_replies(fast_replies)
                await event.edit(f"**❈Fast reply added: {keyword} -> {reply}**")
            else:
                await event.edit(f"**❈Invalid command format. Please use '`/Freplay add [keyword],[reply]`'**")
        elif text.startswith('remove'):
            keyword = text.replace('remove', '').strip()
            if keyword.lower() in fast_replies:
                del fast_replies[keyword.lower()]
                save_fast_replies(fast_replies)
                await event.edit(f"**❈Fast reply removed: {keyword}**")
            else:
                await event.edit(f"**❈No fast reply found with the keyword: {keyword}**")
        else:
            await event.edit("**❈Invalid command format. Please use '`/Freplay add [keyword],[reply]`' or '`/Freplay remove [keyword]`'**")

async def show_fast_replies(event):
    global fast_replies, admin_user_id

    if event.sender_id == admin_user_id:
        if fast_replies:
            reply_text = "**❈ Fast Replies:**\n"
            for keyword, reply in fast_replies.items():
                reply_text += f"- {keyword}: {reply}\n"
        else:
            reply_text = "**❈ No fast replies available.**"

        await event.edit(reply_text)

async def whois_domain(event):
    if event.sender_id == admin_user_id:
        try:
            text = event.raw_text.strip()
            domain = text.replace('/whois', '').strip()

            if domain:
                domain_info = whois.whois(domain)
                message = f"**Domain: {domain}\n\n**"
                message += f"**Registrar: {domain_info.registrar}\n**"
                message += f"**Registered Name: {domain_info.name}\n**"
                message += f"**Creation Date: {domain_info.creation_date}\n**"
                message += f"**Expiration Date: {domain_info.expiration_date}\n**"

                message += "**Name Servers:\n**"
                name_servers = domain_info.name_servers
                if isinstance(name_servers, list):
                    for nameserver in name_servers:
                        message += f"**- {nameserver}\n**"
                else:
                    message += f"**- {name_servers}\n**"

                message += f"**Status: {domain_info.status}\n**"
            else:
                message = "**Please provide a domain name to perform a whois lookup.**"

        except Exception as e:
            message = f"**An error occurred while performing a whois lookup for the domain: {domain}\nError: {str(e)}**"

        await event.edit(message)

async def show_crypto_prices(event):
    if event.sender_id == admin_user_id:
        cryptos = {
            'Bitcoin (BTC)': 'bitcoin',
            'Tether (USDT)': 'tether',
            'TRON (TRX)': 'tron',
            'Litecoin (LTC)': 'litecoin',
            'Dogecoin (DOGE)': 'dogecoin'
        }
        prices = {}

        for crypto, symbol in cryptos.items():
            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd')
            if response.status_code == 200:
                data = response.json()
                prices[crypto] = data[symbol]['usd']
            else:
                await event.edit(f"**❈Unable to fetch {crypto} price.**")
                return

        message = "Cryptocurrency Prices:\n"
        for crypto, price in prices.items():
            message += f"{crypto}: ${price}\n"

        await event.edit(f"**{message}**")

async def replace_words(event):
    if event.sender_id == admin_user_id:
        if not event.is_reply:
            await event.edit('**❈Please reply to a message to perform the replacement.**')
            return

        replied_msg = await event.get_reply_message()
        if not replied_msg.text:
            await event.edit('**❈The replied message does not contain any text.**')
            return

        text = replied_msg.text

        args = event.raw_text.split(' ', 1)
        if len(args) == 2:
            replace_words = args[1].split(',')
            if len(replace_words) == 2:
                word1, word2 = map(str.strip, replace_words)
                replaced_text = text.replace(word1, word2)
                await event.edit(replaced_text)
                return

    await event.edit('**❈Please provide two words separated by a comma to perform the replacement.**')

async def convert_date(event):
    if event.sender_id == admin_user_id:
        args = event.raw_text.split(' ', 1)
        if len(args) != 2:
            await event.edit(f'**❈Please provide a valid date in the format: `/Convertdate yyyy/mm/dd`**')
            return

        try:
            date_str = args[1]
            date = datetime.datetime.strptime(date_str, '%Y/%m/%d').date()

            jalali_date = JalaliDate(date)
            shamsi_date_str = jalali_date.strftime('%Y/%m/%d')

            await event.edit(f'**❈Converted date: `{shamsi_date_str}`**')
        except ValueError:
            await event.edit(f'**❈Invalid date format. Please use the format: yyyy/mm/dd**')

async def set_user_first_name(event):
    if event.sender_id == admin_user_id:
        text = event.message.text
        _, new_first_name = text.split(' ', 1)
        try:
            await client(functions.account.UpdateProfileRequest(
                first_name=new_first_name
            ))
            await event.edit(f'**❈ [Your](tg://user?id={admin_user_id}) First name updated successfully.**')
        except Exception as e:
            await event.edit(f'**❈An error occurred while updating the first name: {str(e)}**')

async def get_football_stats(event):
    if event.sender_id == admin_user_id:
        api_key = '23396b8847eb488c9545aafd07374788'
        url = 'https://api.football-data.org/v4/competitions/BL1/standings'
        headers = {'X-Auth-Token': api_key}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()

                league_name = data['competition']['name']
                start_date = data['season']['startDate'].split('-')[0]
                end_date = data['season']['endDate'].split('-')[0]
                season = f"{start_date} - {end_date}"
                standings = data['standings'][0]['table']

                message = f"Football League: {league_name}\nSeason: {season}\n\n"

                for position, team in enumerate(standings, start=1):
                    team_name = team['team']['name']
                    points = team['points']
                    wins = team['won']
                    draws = team['draw']
                    losses = team['lost']

                    message += f"{position}. {team_name}\n"
                    message += f"Points: {points}, Wins: {wins}, Draws: {draws}, Losses: {losses}\n\n"

                await event.edit(f"**{message}**")
            else:
                await event.edit("**Failed to fetch football stats. Please try again later.**")
        except Exception as e:
            await event.edit(f'**An error occurred while fetching the Bundesliga stats: {str(e)}**')

async def apply_color_filter(event):
    if event.sender_id == admin_user_id:
        if not event.is_reply:
            await event.edit('**❈Please reply to a photo message to apply the color filter.**')
            return

        replied_msg = await event.get_reply_message()
        if not replied_msg.photo:
            await event.edit('**❈The replied message should be a photo.**')
            return

        command_args = event.message.text.split(' ', 1)
        if len(command_args) != 2:
            await event.edit('**❈Please provide a valid color name.**')
            return

        color_name = command_args[1].lower()

        colors = {
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'purple': (128, 0, 128),
            'orange': (255, 165, 0),
            'pink': (255, 192, 203),
        }

        if color_name not in colors:
            await event.edit('**❈Invalid color name.**')
            return

        color_rgb = colors[color_name]

        photo = await replied_msg.download_media()

        img = Image.open(photo)

        img = img.convert('RGB')
        img = Image.blend(img, Image.new('RGB', img.size, color_rgb), alpha=0.5)

        edited_photo_io = BytesIO()
        img.save(edited_photo_io, 'PNG')
        edited_photo_io.seek(0)

        file_name = f"{color_name.capitalize()}.png"

        caption_text = f"**❈Color filtered to : {color_name.capitalize()}**"
        
        await client.send_file(
            event.chat_id,
            edited_photo_io,
            caption=caption_text,
            force_document=False,
            attributes=[types.DocumentAttributeFilename(file_name)]
        )

        os.remove(photo)
        await event.delete()

async def flood_message(event):
    if event.sender_id == admin_user_id:
        count = int(event.pattern_match.group(1))
        texts = event.pattern_match.group(2).split(',')
        for _ in range(count):
            text = random.choice(texts)
            await event.delete()
            await event.respond(text)
            time.sleep(0.2)

async def replay_as_voice(event):
    if event.sender_id == admin_user_id:
        text = event.pattern_match.group(1)
        language = 'en'
        tts = gTTS(text=text, lang=language)
        voice_file_path = 'voice.mp3'
        tts.save(voice_file_path)
        await event.delete()
        await client.send_file(event.chat_id, voice_file_path, voice_note=True)
        os.remove(voice_file_path)

async def set_music_name(event):
    if event.sender_id == admin_user_id:
        name = event.pattern_match.group(1)
        reply_message = await event.get_reply_message()
        if reply_message and reply_message.media:
            try:
                if reply_message.media and hasattr(reply_message.media, 'document'):
                    await event.edit(f"**❈Downloading . . . **")
                    music = await client.download_media(reply_message)
                    await event.edit(f"**❈Sending . **")
                    await asyncio.sleep(0.5)
                    await event.edit(f"**❈Sending . . **")
                    await asyncio.sleep(0.5)
                    await event.edit(f"**❈Sending . . . **")
                    file_ext = os.path.splitext(music)[1]
                    new_name = f'{name}{file_ext}'
                    new_music = os.path.join(os.path.dirname(music), new_name)
                    os.rename(music, new_music)

                    duration = 0
                    performer = ''
                    for attr in reply_message.document.attributes:
                        if isinstance(attr, DocumentAttributeAudio):
                            duration = attr.duration
                            performer = attr.performer
                            break

                    await event.reply(
                        file=new_music,
                        attributes=[
                            DocumentAttributeAudio(
                                duration=duration,
                                title=name,
                                performer=performer
                            )
                        ]
                    )
                    os.remove(new_music)
                    await asyncio.sleep(0.5)
                    await event.edit(f"**❈Sent Successfully!**")
                else:
                    await event.edit(f"**❈Please reply to a music message.**")
            except FileNotFoundError:
                await event.edit(f"**❈Failed to rename the music file.**")

async def take_screenshot(event):
    if event.sender_id == admin_user_id:
        url = event.pattern_match.group(1)
        file_name = f"screenshot_{event.id}.png"
        try:
            api_key = '863fe7'
            screenshot_api_url = f"https://api.screenshotmachine.com/?key={api_key}&url={url}&dimension=1024x768&format=png"
            response = requests.get(screenshot_api_url)
            response.raise_for_status()
            with open(file_name, "wb") as file:
                file.write(response.content)
            await event.edit(f"**❈Sending . **")
            await asyncio.sleep(0.5)
            await event.edit(f"**❈Sending . . **")
            await asyncio.sleep(0.5)
            await event.edit(f"**❈Sending . . . **")
            await event.reply(file=file_name)
            os.remove(file_name)
            await event.edit(f"**❈Sent Successfully!**")
        except Exception as e:
            await event.reply(f"**❈Failed to capture screenshot: {str(e)}**")


SAVE_DIRECTORY_YT = 'videos'
async def download_youtube_video(event):
    if event.sender_id == admin_user_id:
        video_url = event.pattern_match.group(1)
        await event.edit("**❈Downloading...**")
        try:
            ydl_opts = {
                'outtmpl': os.path.join(SAVE_DIRECTORY_YT, '%(title)s.%(ext)s'),
                'writethumbnail': True,
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'quiet': True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                file_path = ydl.prepare_filename(info)
                thumbnail_path = info['thumbnails'][0]['url']

            thumbnail_filename = os.path.join(SAVE_DIRECTORY_YT, f'{info["title"]}.webp')
            thumbnail_response = requests.get(thumbnail_path)
            with open(thumbnail_filename, 'wb') as thumbnail_file:
                thumbnail_file.write(thumbnail_response.content)

            await event.reply(
                file=file_path,
                message=f"**❈Downloaded [Video]({video_url}) in Highest Resolution For [You](tg://user?id={admin_user_id})\nName: {info.get('title')}**",
                supports_streaming=True,
                thumb=thumbnail_filename
            )

            os.remove(file_path)
            os.remove(thumbnail_filename)

            await event.edit("**❈Successfully Done**")
            await asyncio.sleep(3)
            await event.delete()

        except Exception as e:
            await event.reply(f"Failed to download YouTube video: {str(e)}")

        thumbnail_filename = os.path.join(SAVE_DIRECTORY_YT, f'{info["title"]}.webp')
        if os.path.exists(thumbnail_filename):
            os.remove(thumbnail_filename)

async def proxy_command(event):
    if event.sender_id == admin_user_id:
        try:
            await event.edit("Fetching random proxies...")
            
            url = "https://yebekhe.github.io/MTProtoCollector/proxy/mtproto.json"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                random_proxies = random.sample(data, min(5, len(data)))
                messages = []
                
                for i, proxy in enumerate(random_proxies):
                    proxy_link = proxy.get('link', '')
                    if proxy_link:
                        messages.append(f"**❈ Random Proxy {i + 1}:\n**{proxy_link}")
                
                if messages:
                    await event.edit("\n\n".join(messages))
                else:
                    await event.edit("**❈ No proxy links found in the JSON response. Please try again later.**")
            else:
                await event.edit("**❈ The JSON response is empty or in an unexpected format. Please try again later.**")
        except Exception as e:
            await event.edit(f"An error occurred: {str(e)}")

async def v2ray_command(event):
    if event.sender_id == admin_user_id:
        try:
            await event.edit("Fetching random VLESS configurations...")
            
            url = "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/reality"
            response = requests.get(url)
            response.raise_for_status()
            data = response.text.split('\n')
            
            vless_configs = [config.strip() for config in data if config.startswith('vless://')]
            random_configs = random.sample(vless_configs, min(5, len(vless_configs)))
            
            if random_configs:
                messages = [f"**❈ Random VLESS Configuration {i + 1}:\n `{config}`**" for i, config in enumerate(random_configs)]
                
                await event.edit("\n\n".join(messages))
            else:
                await event.edit("**❈ No VLESS configurations found at the moment. Please try again later.**")
        except Exception as e:
            await event.edit(f"An error occurred: {str(e)}")


timezone_cache = {}
async def get_world_time(event):
    if event.sender_id == admin_user_id:
        city_name = event.pattern_match.group(1).capitalize()

        timezone = timezone_cache.get(city_name)
        if not timezone:
            geolocator = Nominatim(user_agent="world_time_bot")
            location = geolocator.geocode(city_name, exactly_one=True, featuretype="P")

            if location:
                tf = TimezoneFinder()
                timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)

                if timezone_str:
                    timezone = pytz.timezone(timezone_str)
                    timezone_cache[city_name] = timezone
                else:
                    reply_message = f"Sorry, I couldn't find the timezone for {city_name}"
                    await event.edit(f"**❈{reply_message}**")
                    return
            else:
                reply_message = f"Sorry, I couldn't find the location for {city_name}"
                await event.edit(f"**❈{reply_message}**")
                return

        current_time = datetime.datetime.now(timezone)
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        reply_message = f"The current time in {city_name} is: {formatted_time}"

        await event.edit(f"**❈{reply_message}**")


timers = {}
def load_timers():
    if os.path.exists("settings/timers.json"):
        with open("settings/timers.json", "r") as file:
            timers.update(json.load(file))

def save_timers():
    with open("settings/timers.json", "w") as file:
        json.dump(timers, file)

async def create_timer(event):
    if event.sender_id == admin_user_id:
        timer_name = event.pattern_match.group(1)
        timers[timer_name] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_timers()
        await event.edit(f"**❈Timer `{timer_name}` created.**")

async def delete_timer(event):
    if event.sender_id == admin_user_id:
        timer_name = event.pattern_match.group(1)
        if timer_name in timers:
            del timers[timer_name]
            save_timers()
            await event.edit(f"**❈Timer `{timer_name}` deleted.**")
        else:
            await event.edit(f"**❈Timer `{timer_name}` not found.**")

async def list_timers(event):
    if event.sender_id == admin_user_id:
        if timers:
            reply_message = "**List of your saved Timers:**\n"
            for i, (timer_name, start_time) in enumerate(timers.items(), start=1):
                time_elapsed = datetime.datetime.now() - datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
                days = time_elapsed.days
                hours, remainder = divmod(time_elapsed.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                reply_message += f"**{i} - {timer_name}:**\n `{days} days, {hours} hours, {minutes} minutes, {seconds} seconds`\n"
            await event.edit(reply_message)
        else:
            await event.edit("**❈No timers found.**")

async def clean_timers(event):
    if event.sender_id == admin_user_id:
        timers.clear()
        save_timers()
        await event.edit(f"**❈Timers cleaned.**")

async def download_file(event):
    if event.sender_id == admin_user_id:
        file_url = event.pattern_match.group(1)
        try:
            response = requests.head(file_url)
            if response.status_code == 200 and 'content-length' in response.headers:
                file_size = int(response.headers['content-length'])

                if file_size <= 200 * 1024 * 1024:
                    download_msg = await event.edit("**❈Downloading file...**")
                    file_name = file_url.split("/")[-1]
                    response = requests.get(file_url, stream=True)
                    with open(file_name, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                file.write(chunk)

                    await client.send_file(event.chat_id, file=file_name, caption=f"**❈Downloaded File Url : `{file_url}`**")
                    await download_msg.delete()
                    os.remove(file_name)
                else:
                    await event.edit("**❈File size exceeds the limit (`200 MB`).**")
            else:
                await event.edit("**❈Invalid or inaccessible URL.**")
        except Exception as e:
            await event.edit(f"**❈An error occurred while downloading the file: {str(e)}**")

async def get_ip_info(event):
    if event.sender_id == admin_user_id:
        ip = event.pattern_match.group(1)
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            data = response.json()
            
            if "ip" in data:
                ip_address = data["ip"]
                city = data.get("city", "")
                region = data.get("region", "")
                country = data.get("country", "")
                org = data.get("org", "")
                
                reply_message = f"**IP Address:** `{ip_address}`\n"
                reply_message += f"**City:** `{city}`\n" if city else ""
                reply_message += f"**Region:** `{region}`\n" if region else ""
                reply_message += f"**Country:** `{country}`\n" if country else ""
                reply_message += f"**Organization:** `{org}`\n" if org else ""
                
                await event.edit(reply_message)
            else:
                await event.edit(f"**❈Failed to retrieve IP information for `{ip}`.**")
                
        except requests.exceptions.RequestException as e:
            await event.edit(f"**❈An error occurred while retrieving IP information: `{str(e)}`**")

EXSAVE_DIRECTORY = 'extracted_files'
async def extract_files(event):
    if event.is_reply and event.sender_id == admin_user_id:
        reply_message = await event.get_reply_message()
        if reply_message.media and reply_message.media.document.mime_type == 'application/zip':
            try:
                await event.edit("**❈Extracting files...**")
                zip_file = await event.client.download_media(reply_message)
                extracted_files = await extract_zip_files(zip_file)
                await delete_files(zip_file)
                await send_extracted_files(event, extracted_files)
                await event.edit("**❈Successfully Sent Extracted Files**")
                await delete_extracted_files(extracted_files)
            except Exception as e:
                await event.edit(f"**❈Failed to extract and send files: {str(e)}**")
        else:
            await event.respond("**❈Please reply to a zip file to extract the files.**")

async def extract_zip_files(zip_file_path):
    extracted_files = []
    if not os.path.exists(EXSAVE_DIRECTORY):
        os.makedirs(EXSAVE_DIRECTORY)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(EXSAVE_DIRECTORY)
        extracted_files = zip_ref.namelist()
    return extracted_files

async def delete_files(zip_file):
    if os.path.isfile(zip_file):
        os.remove(zip_file)

async def send_extracted_files(event, extracted_files):
    for file_name in extracted_files:
        file_path = os.path.join(EXSAVE_DIRECTORY, file_name)
        if os.path.isfile(file_path):
            await event.respond(file=file_path)
            await asyncio.sleep(1)

async def delete_extracted_files(extracted_files):
    for file_name in extracted_files:
        file_path = os.path.join(EXSAVE_DIRECTORY, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    shutil.rmtree(EXSAVE_DIRECTORY)

TV_CHANNELS = {
    'IRIB 1': 'https://telewebion.com/live/tv1',
    'IRIB 2': 'https://telewebion.com/live/tv2',
    'IRIB 3': 'https://telewebion.com/live/tv3',
    'IRIB 4': 'https://telewebion.com/live/tv4/',
    'IRIB 5': 'https://telewebion.com/live/tv5/',
    'Radio Javan': 'https://mrtv.me/playonline/?id=58&media=cjlKejM3ZlljWXBoS1l4QU80dllzR0RLaTJhT1VLaGNLbUM1S2RpUGUwZFMxU3dRWU42YStSQnJaV2gzMUZzRG5FOXh4SUphS0FtdktaWEJvZlYyUWc9PQ==&subtitle=RTBrZUxqQUJESEEvZy83alpXQ1pDUT09&quality1=&quality2=&quality3=',
    'IRIB Nasim': 'https://telewebion.com/live/nasim/',
    'IRIB Varzesh': 'https://telewebion.com/live/varzesh/',
    'IRIB Pooya': 'https://telewebion.com/live/pooya/',
    'IRIB Salamat': 'https://telewebion.com/live/salamat/',
}

async def send_tv_channels(event):
    if event.sender_id == admin_user_id :
        channel_list = '\n'.join([f'• {channel}: [Watch Now]({link})' for channel, link in TV_CHANNELS.items()])
        message = f"Here are the live TV channels in Iran:\n\n{channel_list}"
        await event.edit(message, link_preview=False)

async def create_qr_code(event):
    if event.sender_id == admin_user_id:
        command = event.raw_text.lower()
        if "به qr" in command or "sqr" in command:
            qr_data = command.replace("به qr", "").replace("sqr", "").strip()
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img.save("qr_code.png")
            await event.edit("**❈QR code created successfully!**")
            await client.send_file(event.chat_id, "qr_code.png")
            os.remove("qr_code.png")

async def read_qr_code(event):
    if event.is_reply and event.sender_id == admin_user_id:
        replied_msg = await event.get_reply_message()
        if replied_msg.photo:
            try:
                photo = await replied_msg.download_media()

                files = {'file': open(photo, 'rb')}
                url = 'https://zxing.org/w/decode'
                response = requests.post(url, files=files)

                os.remove(photo)

                if response.ok:
                    content = re.search(r'<pre>(.*?)</pre>', response.text)
                    if content:
                        qr_data = content.group(1)
                        await event.edit(f"**❈QR Code says: {qr_data}**")
                    else:
                        await event.edit("**❈No content found in QR code response.**")
                else:
                    await event.edit("**❈Error decoding QR code.**")
            except Exception as e:
                await event.edit(f"Error: {str(e)}")
        else:
            await event.edit("**❈Please reply to a message containing a photo with a QR code.**")
    else:
        await event.edit("**❈Please reply to a message with 'خواندن qr' or 'readqr' to detect a QR code.**")

async def clean_messages_containing_text(event):
    if event.sender_id == admin_user_id:
        command = event.raw_text.lower()
        if "پاکسازی همه" in command or "cleanall" in command:
            text_to_clean = command.split(maxsplit=1)[1].strip()
            if text_to_clean:
                async for message in client.iter_messages(event.chat_id):
                    if message.text and text_to_clean in message.text:
                        await message.delete()
                await event.respond(f"**❈All messages containing '{text_to_clean}' have been deleted.**")
            else:
                await event.edit("**❈Please provide the text you want to search for and clean.**")

async def join_all_channels(event):
    if event.sender_id == admin_user_id:
        try:
            replied_to_msg = await event.get_reply_message()
            if replied_to_msg and replied_to_msg.reply_markup:
                joined_channels = 0
                for row in replied_to_msg.reply_markup.rows:
                    for button in row.buttons:
                        if button.url:
                            try:
                                entity = await client.get_entity(button.url)
                                if isinstance(entity, types.Channel):
                                    try:
                                        await client(functions.channels.JoinChannelRequest(channel=entity))
                                        await event.edit(f"Joined {entity.title}")
                                        joined_channels += 1
                                        await asyncio.sleep(5)  # Delay to prevent rate limits and avoid flooding
                                    except Exception as join_error:
                                        await event.edit(f"Couldn't join {entity.title}: {str(join_error)}. Please manually join: {button.url}")
                                        await asyncio.sleep(10)  # Adding delay to prevent flooding
                                        continue
                                else:
                                    await event.edit(f"{entity.title} is not a channel.")
                            except Exception as entity_error:
                                await event.edit(f"Error: {str(entity_error)}")
                        else:
                            await event.edit("No URLs found in the inline keyboard.")
                
                if joined_channels > 0:
                    await event.edit(f"Joined {joined_channels} channels successfully!")
                else:
                    await event.edit("No channels joined.")
            
            else:
                await event.edit("Please reply to a message with an inline keyboard containing channel join buttons.")
        except Exception as e:
            await event.edit(f"An error occurred: {str(e)}")

async def set_bot_username(event):
    if event.sender_id == admin_user_id:
        try:
            command_parts = event.raw_text.split(maxsplit=2)
            new_username = command_parts[1]
            
            if not new_username:
                await event.edit(f"**❈Please provide a valid new username.**")
                return
            
            try:
                await event.client.get_entity(f'@{new_username}')
                await event.edit(f"**❈The username is already taken. Please choose a different one.**")
            except Exception:
                await event.client(functions.account.UpdateUsernameRequest(new_username))
                await event.edit(f"**❈Your username has been updated to: @{new_username}**")
        except Exception as e:
            await event.edit(f"An error occurred: {str(e)}")

async def kick_users(event):
    if event.sender_id == admin_user_id:
        try:
            command_parts = event.raw_text.split()
            users_to_kick = command_parts[1:]
            
            if users_to_kick:
                chat = await event.get_chat()
                chat_id = chat.id
                
                user_ids_to_kick = []
                
                for user_to_kick in users_to_kick:
                    async for user in event.client.iter_participants(chat_id):
                        if isinstance(user, types.User) and (
                            user.username == user_to_kick.lstrip('@') or
                            str(user.id) == user_to_kick
                        ):
                            user_ids_to_kick.append(user.id)
                
                # Kick the users
                if user_ids_to_kick:
                    await event.edit("**❈Kicking users...**")
                    for user_id in user_ids_to_kick:
                        await event.client(functions.channels.EditBannedRequest(
                            chat_id,
                            user_id,
                            banned_rights=types.ChatBannedRights(
                                until_date=None,
                                view_messages=True,
                                send_messages=True,
                                send_media=True,
                                send_stickers=True,
                                send_gifs=True,
                                send_games=True,
                                send_inline=True,
                                embed_links=True,
                            ),
                        ))
                    await event.edit("**❈Users kicked successfully!**")
                else:
                    await event.edit("**❈No valid users found to kick.**")
            else:
                await event.edit("**❈Please provide usernames or numerical user IDs to kick.**")
        except Exception as e:
            await event.edit(f"An error occurred: {str(e)}")

async def clean_between_messages(event):
    if event.sender_id == admin_user_id:
        command = event.raw_text.lower()
        if "پاکسازی بین" in command or "cleanb" in command:
            command_parts = command.split()
            if len(command_parts) == 3:
                link1 = command_parts[1]
                link2 = command_parts[2]

                try:
                    message_id1 = int(link1.split('/')[-1])
                    message_id2 = int(link2.split('/')[-1])

                    async for message in client.iter_messages(event.chat_id, min_id=message_id1, max_id=message_id2):
                        await message.delete()

                    await event.edit("**❈Messages between the provided links have been deleted.**")
                except Exception as e:
                    await event.respond(f"An error occurred: {str(e)}")
            else:
                await event.reply("**❈Please provide two message links to clean between.**")


##########################################################################################
patterns_actions = {
    'timename on': ('settings/time.txt', 'True', '**❈Time Name Activated!**'),
    'timename off': ('settings/time.txt', 'False', '**❈Time Name DeActivated!**'),
    'bio on': ('settings/bioinfo.txt', 'True', '**❈Bio Activated!**'),
    'bio off': ('settings/bioinfo.txt', 'False', '**❈Bio DeActivated!**'),
    'bold on': ('settings/mode.txt', 'Bold', '**❈Bold Mode Activated!**'),
    'mini on': ('settings/mode.txt', 'Mini', '**❈Mini Mode Activated!**'),
    'default on': ('settings/mode.txt', 'Default', '**❈Default Mode Activated!**'),
    'mono on': ('settings/mode.txt', 'Mono', '**❈Mono Mode Activated!**'),
    'heart on': ('settings/heart.txt', 'True', '**❈heart Activated!**'),
    'heart off': ('settings/heart.txt', 'False', '**❈heart DeActivated!**'),
    'rname on': ('settings/rnamest.txt', 'True', '**❈Rname Activated!**'),
    'rname off': ('settings/rnamest.txt', 'False', '**❈Rname DeActivated!**'),
    'see rname': ('settings/rname.txt', None, '**❈Rnames : \n**'),
    'see bio': ('settings/bio.txt', None, '**❈Your Bio : \n**'),
    'see lname': ('settings/nameinfo.txt', None, '**❈Your lname : \n**')
}
async def settings(event):
    if event.sender_id == admin_user_id:
        pattern = event.pattern_match.string
        file_path, content, response = patterns_actions[pattern]

        if content is not None:
            with open(file_path, 'w') as f:
                f.write(content)

        if pattern == 'timename off':
            await client(UpdateProfileRequest(last_name=''))

        if pattern == 'timename on':
            await client(UpdateProfileRequest(last_name=f'{current_time_str}'))

        if pattern == 'bio off':
            await client(UpdateProfileRequest(about=''))


        if file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                file_content = f.read()
            if file_content not in ["True", "False", "Bold", "Mono", "Default", "Mini"]:
                response += f"`{file_content}`"

        await event.edit(response)