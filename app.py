from discord.ext import commands, tasks
import discord
import asyncio
import random
from datetime import datetime, timedelta

TOKEN = "MTIxMjc2OTQ4NjU0NjAxODM4Nw.G8s5jE.YpE9LFVWcdtDV9zdhTSsJRjMTuiIn2pQC9KP_M"
VOICE_CHANNEL_ID = 1216277642551234616
SPAM_CHANNEL_ID = 1400385587353223198

client = commands.Bot(command_prefix="!", self_bot=True)

message_counter = 0
last_daily_sent = None  # thời điểm gửi owo daily gần nhất

@client.event
async def on_ready():
    print(f"✅ Đã đăng nhập: {client.user}")
    await join_voice_channel()
    check_voice_loop.start()
    spam_owo_loop.start()

async def join_voice_channel():
    channel = client.get_channel(VOICE_CHANNEL_ID)
    if isinstance(channel, discord.VoiceChannel):
        try:
            if client.voice_clients:
                print("🔁 Đã kết nối voice, không cần join lại.")
                return
            await channel.connect()
            print(f"🎧 Đã kết nối vào kênh voice: {channel.name}")
        except Exception as e:
            print(f"❌ Lỗi khi kết nối voice: {e}")
    else:
        print("⚠️ ID không phải là kênh voice hợp lệ.")

@tasks.loop(seconds=10)
async def check_voice_loop():
    if not client.voice_clients:
        print("🚨 Bị disconnect khỏi voice! Đang reconnect...")
        await join_voice_channel()

@tasks.loop(seconds=20)
async def spam_owo_loop():
    global message_counter, last_daily_sent

    channel = client.get_channel(SPAM_CHANNEL_ID)
    if not channel:
        print("⚠️ Không tìm thấy kênh spam.")
        return

    # Gửi owo daily nếu đã qua 1 ngày
    now = datetime.now()
    if last_daily_sent is None or (now - last_daily_sent) >= timedelta(days=1):
        await channel.send("owo daily")
        print("🗓️ Đã gửi: owo daily")
        last_daily_sent = now
        return

    if message_counter < 10:
        # Random tin nhắn
        msg = generate_random_msg()
        await channel.send(msg)
        print(f"💬 Đã gửi: {msg}")
        message_counter += 1
    else:
        # Gửi lệnh phụ sau mỗi 10 tin
        msg = random.choice(["owo cash", "owo help", "ocash","owo inv","owo zoo"])
        await channel.send(msg)
        print(f"✨ Đã gửi (sau 10 tin): {msg}")
        message_counter = 0

def generate_random_msg():
    msg_type = random.choice(["action_with_number", "direct_command"])
    
    if msg_type == "action_with_number":
        action = random.choice(["owo cf", "owo slots"])
        amount = random.randint(20, 30)
        return f"{action} {amount}"
    else:
        return random.choice(["owo lb", "owo wc", "owo hunt", "owo blush", "owo cry"])

client.run(TOKEN)
