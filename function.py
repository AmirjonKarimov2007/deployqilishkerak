from aiogram import Bot
from aiogram.types import Message    
import random
import string
import sqlite3

db = sqlite3.connect('my_database.db')
cursor = db.cursor()

group_id = -4506983186

def get_admin_ids():
    cursor.execute('SELECT admin_id FROM admins')
    return [row[0] for row in cursor.fetchall()]

def generate_unique_id():
    letters = string.ascii_letters
    digits = string.digits
    characters = letters + digits
    unique_id = ''.join(random.choice(characters) for _ in range(10))
    return unique_id

async def start(message: Message):
    if message.from_user.id == message.chat.id:
        await message.answer('-maktabning arizalar botiga hush kelibsiz. Bu yerda sizning anonymliginggiz 100% taminlangan. Habaringgizni yuborishinggiz mumkin.')
        admin_ids = get_admin_ids()
        if message.from_user.id not in admin_ids:
            cursor.execute('SELECT user_id FROM ids WHERE user_id = ?', (message.from_user.id,))
            if not cursor.fetchone():           
                while True:
                    unique_id = generate_unique_id()
                    cursor.execute('SELECT unique_id FROM ids WHERE unique_id = ?', (unique_id,))
                    if not cursor.fetchone():
                        break
                cursor.execute('INSERT INTO ids VALUES (?, ?)', (message.from_user.id, unique_id))
                db.commit()
                await message.answer(f'Sizning anonymlik kodingiz: #{unique_id}')
    
async def report(message: Message, bot: Bot):
    if message.from_user.id == message.chat.id:
        admin_ids = get_admin_ids()
        if message.from_user.id not in admin_ids:
            cursor.execute('SELECT unique_id FROM ids WHERE user_id = ?', (message.from_user.id,))
            unique_id = cursor.fetchone()[0]
            for admin_id in admin_ids:
                if message.content_type == 'text':
                    await bot.send_message(admin_id, f'#{unique_id} dan yangi habar\n\n{message.text}')
                    await bot.send_message(group_id, f'#{unique_id} dan yangi habar\n\n{message.text}')
                elif message.content_type == 'photo':
                    await bot.send_photo(admin_id, message.photo[-1].file_id, caption=f'#{unique_id} dan yangi rasm\n\n{message.caption if message.caption else ""}')
                    await bot.send_photo(group_id, message.photo[-1].file_id, caption=f'#{unique_id} dan yangi rasm\n\n{message.caption if message.caption else ""}')
                elif message.content_type == 'video':
                    await bot.send_video(admin_id, message.video.file_id, caption=f'#{unique_id} dan yangi video\n\n{message.caption if message.caption else ""}')
                    await bot.send_video(group_id, message.video.file_id, caption=f'#{unique_id} dan yangi video\n\n{message.caption if message.caption else ""}')
                elif message.content_type == 'document':
                    await bot.send_document(admin_id, message.document.file_id, caption=f'#{unique_id} dan yangi fayl\n\n{message.caption if message.caption else ""}')
                    await bot.send_document(group_id, message.document.file_id, caption=f'#{unique_id} dan yangi fayl\n\n{message.caption if message.caption else ""}')
                elif message.content_type == 'voice':
                    await bot.send_voice(admin_id, message.voice.file_id, caption=f'#{unique_id} dan yangi ovozli xabar')
                    await bot.send_voice(group_id, message.voice.file_id, caption=f'#{unique_id} dan yangi ovozli xabar')        
            await message.answer('Habaringgiz yuborildi javobni kuting')    
        else:
            if not message.reply_to_message:
                await message.answer('Iltimos unique id ga ega habarga javob bering')
            else:
                text = message.reply_to_message.text or message.reply_to_message.caption
                if not text or not text.startswith('#'):
                    await message.answer('Iltimos unique id ga ega habarga javob bering')
                else:
                    unique_id = text.split()[0][1:]
                    cursor.execute('SELECT user_id FROM ids WHERE unique_id = ?', (unique_id,))
                    result = cursor.fetchone()
                    if result:
                        user_id = result[0]
                        if message.content_type == 'text':
                            await bot.send_message(user_id, f"Direktordan yangi habar\n\n{message.text}")
                        elif message.content_type == 'photo':
                            await bot.send_photo(user_id, message.photo[-1].file_id, caption=f"Direktordan yangi habar\n\n{message.caption if message.caption else ''}")
                        elif message.content_type == 'video':
                            await bot.send_video(user_id, message.video.file_id, caption=f"Direktordan yangi habar\n\n{message.caption if message.caption else ''}")
                        elif message.content_type == 'document':
                            await bot.send_document(user_id, message.document.file_id, caption=f"Direktordan yangi habar\n\n{message.caption if message.caption else ''}")
                        elif message.content_type == 'voice':
                            await bot.send_voice(user_id, message.voice.file_id, caption="Direktordan yangi ovozli habar")
                        await message.answer('Habar yuborildi')

async def user_finder(message: Message):
    if message.from_user.id == message.chat.id:
        admin_ids = get_admin_ids()
        if message.from_user.id not in admin_ids:
            await message.answer('Sizga ruxsat yo\'q')
        else:
            text = message.text.split()
            if len(text) < 2 or not text[1].startswith('#'):
                await message.answer('Iltimos unique id kiriting')
                return
            
            unique_id = text[1][1:]
            cursor.execute('SELECT user_id FROM ids WHERE unique_id = ?', (unique_id,))
            result = cursor.fetchone()
            
            if not result:
                await message.answer('Foydalanuvchi topilmadi')
                return
                
            user_id = result[0]
            user = await message.bot.get_chat(user_id)
            
            response = f"ID: {user.id}\nTo'liq ismi: <a href='tg://user?id={user.id}'>{user.full_name}</a>"        
            if user.username:
                response += f"\nUsername: @{user.username}"
            if hasattr(user, 'phone_number') and user.phone_number:
                response += f"\nTelefon: {user.phone_number}"
            if user.bio:
                response += f"\nBio: {user.bio}"
                
            await message.answer(response, parse_mode='HTML')
    
async def add_admin(message: Message):
    if message.from_user.id == message.chat.id:
        cursor.execute('INSERT INTO admins (admin_id) VALUES (?)', (1567764330,))
        db.commit()
        admin_ids = get_admin_ids()
        if message.from_user.id not in admin_ids:
            await message.answer('Sizga ruxsat yo\'q')
        else:
            text = message.text.split()
            if len(text) < 2:
                await message.answer('Iltimos id kiriting')
                return
                
            user_id = text[1]
            if not user_id.isdigit():
                await message.answer('ID faqat sondan iborat bo\'lish kerak')
                return
                
            cursor.execute('SELECT admin_id FROM admins WHERE admin_id = ?', (user_id,))
            if cursor.fetchone():
                await message.answer('Bu ID avvaldan bor')
                return
                
            cursor.execute('INSERT INTO admins (admin_id) VALUES (?)', (user_id,))
            db.commit()
            await message.answer('Admin muvaffaqiyatli qo\'shildi')        

async def rm_admin(message: Message):
    if message.from_user.id == message.chat.id:
        admin_ids = get_admin_ids()
        if message.from_user.id not in admin_ids:
            await message.answer('Sizga ruxsat yo\'q')
        else:
            text = message.text.split()
            if len(text) < 2:
                await message.answer('Iltimos id kiriting')
                return
            user_id = text[1]
            if not user_id.isdigit():
                await message.answer('ID faqat sondan iborat bo\'lish kerak')
                return

            cursor.execute('SELECT admin_id FROM admins WHERE admin_id = ?', (user_id,))
            if not cursor.fetchone():
                await message.answer('Bu ID mavjud emas')
                return
            cursor.execute('DELETE FROM admins WHERE admin_id = ?', (user_id,))
            db.commit()
            await message.answer('Admin muvaffaqiyatli o\'chirildi')