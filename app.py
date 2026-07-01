import re
import json
import os
import threading
import random
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ============ FLASK FOR RENDER ============
flask_app = Flask(__name__)

@flask_app.route('/')
@flask_app.route('/health')
def health():
    return "Premium Emoji Bot is running!", 200

def run_flask():
    port = int(os.environ.get('PORT', 5000))
    flask_app.run(host='0.0.0.0', port=port)

# ============ CONFIG ============
BOT_TOKEN = "8903487173:AAE3huf5T77b7U4OVonum23sUKNFPfWPrLs"
OWNER_ID = 7977493987
ADMIN_IDS = [OWNER_ID]

USERS_FILE = "users.json"
BANNED_FILE = "banned.json"

# ============ ALL PREMIUM EMOJIS ============
PREMIUM_EMOJIS = {
    "verified": {"id": "6246537187614005254", "fallback": "✅"},
    "verify": {"id": "6246782404476803545", "fallback": "✅"},
    "verify_blue": {"id": "6010060634803148161", "fallback": "✅"},
    "verify_purple": {"id": "6010498532488778300", "fallback": "✅"},
    "eye": {"id": "6035338338406242050", "fallback": "👁️"},
    "eyeball": {"id": "6035051267087143217", "fallback": "👁️"},
    "eyes": {"id": "6035225389356290238", "fallback": "👀"},
    "eyes_blue": {"id": "6035081585261287115", "fallback": "👀"},
    "fire": {"id": "4956222745814762495", "fallback": "🔥"},
    "fire_red": {"id": "4956606007221421405", "fallback": "🔥"},
    "fire_orange": {"id": "4956429969396859866", "fallback": "🔥"},
    "explosion": {"id": "6032673796530377389", "fallback": "💥"},
    "heart": {"id": "5783157259152397008", "fallback": "❤️"},
    "heart_red": {"id": "5801084710343938087", "fallback": "❤️"},
    "heart_pink": {"id": "6010280773351904888", "fallback": "❤️"},
    "heart_blue": {"id": "5780496071645991525", "fallback": "💙"},
    "heart_green": {"id": "5888789252493283486", "fallback": "💚"},
    "heart_yellow": {"id": "5840261097719148872", "fallback": "💛"},
    "heart_orange": {"id": "5840263144212529797", "fallback": "🧡"},
    "heart_purple": {"id": "5840265018655703965", "fallback": "💜"},
    "heart_black": {"id": "5840266939932994956", "fallback": "🖤"},
    "star": {"id": "6244496562752331516", "fallback": "⭐"},
    "star_gold": {"id": "5904618938578243567", "fallback": "⭐"},
    "star_blue": {"id": "6010193314932855525", "fallback": "⭐"},
    "star_glow": {"id": "6010156854955480259", "fallback": "🌟"},
    "sparkle": {"id": "6010338729640596556", "fallback": "✨"},
    "sparkle_blue": {"id": "6010086134023985536", "fallback": "✨"},
    "vampire": {"id": "6034871295072539452", "fallback": "🧛"},
    "monster": {"id": "6034962795055812935", "fallback": "👹"},
    "ghost": {"id": "6035070298087231243", "fallback": "👻"},
    "devil": {"id": "6035242444671421879", "fallback": "👿"},
    "demon": {"id": "6035136809950778133", "fallback": "😈"},
    "crown": {"id": "5794422335599546668", "fallback": "👑"},
    "crown_gold": {"id": "6089003761496232797", "fallback": "👑"},
    "crown_blue": {"id": "6247039939305808563", "fallback": "👑"},
    "money": {"id": "6089104607328342288", "fallback": "💰"},
    "money_bag": {"id": "6086730718774300509", "fallback": "💰"},
    "dollar": {"id": "6089140105233044310", "fallback": "💵"},
    "diamond": {"id": "6086778246882399112", "fallback": "💎"},
    "like": {"id": "6089313931149448495", "fallback": "👍"},
    "unlike": {"id": "6088789257285988672", "fallback": "👎"},
    "clap": {"id": "6093744967304352336", "fallback": "👏"},
    "smile": {"id": "6093864814071780526", "fallback": "😀"},
    "big_smile": {"id": "6093922327978840798", "fallback": "😀"},
    "laugh": {"id": "5782741660936966676", "fallback": "😂"},
    "teeth": {"id": "6035060329468137931", "fallback": "😁"},
    "wink": {"id": "6089024570612781324", "fallback": "😉"},
    "heart_eyes": {"id": "6010179687001625256", "fallback": "😍"},
    "kiss": {"id": "6044373012566774137", "fallback": "😘"},
    "cool": {"id": "6032853480782172520", "fallback": "😎"},
    "sad": {"id": "5780793884678296697", "fallback": "😢"},
    "cry": {"id": "5783024321324651865", "fallback": "😭"},
    "angry": {"id": "6035355642829475999", "fallback": "😡"},
    "think": {"id": "5782756916660802905", "fallback": "🤔"},
    "flag_us": {"id": "5433865586356531140", "fallback": "🇺🇸"},
    "flag_gb": {"id": "5433827537241258614", "fallback": "🇬🇧"},
    "flag_fr": {"id": "5433636707549331311", "fallback": "🇫🇷"},
    "flag_de": {"id": "5433845881046578644", "fallback": "🇩🇪"},
    "flag_in": {"id": "5433601609076586221", "fallback": "🇮🇳"},
    "flag_jp": {"id": "5434147542369579483", "fallback": "🇯🇵"},
    "flag_cn": {"id": "5435996255207567113", "fallback": "🇨🇳"},
    "flag_ru": {"id": "5433674924168328689", "fallback": "🇷🇺"},
    "flag_br": {"id": "5433825269498525925", "fallback": "🇧🇷"},
    "flag_it": {"id": "5433627189901801019", "fallback": "🇮🇹"},
    "flag_ca": {"id": "5433979415874779870", "fallback": "🇨🇦"},
    "flag_au": {"id": "5434067655977874913", "fallback": "🇦🇺"},
    "flag_kr": {"id": "5434142701941437163", "fallback": "🇰🇷"},
    "flag_es": {"id": "5434026158003862063", "fallback": "🇪🇸"},
    "flag_mx": {"id": "5434131139889478358", "fallback": "🇲🇽"},
    "flag_tr": {"id": "5433792911214917126", "fallback": "🇹🇷"},
    "flag_pk": {"id": "5434064563601421981", "fallback": "🇵🇰"},
    "flag_bd": {"id": "5433854239052935880", "fallback": "🇧🇩"},
    "flag_ng": {"id": "5433982207603520017", "fallback": "🇳🇬"},
    "flex": {"id": "6147464060305676048", "fallback": "😎"},
    "blue_verification": {"id": "6147524086768604985", "fallback": "💎"},
    "frozen": {"id": "5449449325434266744", "fallback": "❄️"},
    "crying_face": {"id": "6273840152980755328", "fallback": "😭"},
    "smiley": {"id": "6276057176444246654", "fallback": "🙂"},
    "seeing_up": {"id": "6273997026661241933", "fallback": "😋"},
    "teeth_smile": {"id": "6273726078649372769", "fallback": "😁"},
    "done_emoji": {"id": "6274007313107915274", "fallback": "👍"},
    "blue_badge": {"id": "5978776771623914876", "fallback": "🟫"},
    "black_badge": {"id": "5978686323907628843", "fallback": "🔸"},
    "busy_tag": {"id": "5852873584912896283", "fallback": "🟧"},
    "instagram_emoji": {"id": "5895297528106061174", "fallback": "🌐"},
    "telegram_emoji": {"id": "5895735846698487922", "fallback": "🌐"},
    "whatsapp_emoji": {"id": "5895343514320899727", "fallback": "🌐"},
    "india_emoji": {"id": "5913754823643107921", "fallback": "🇮🇳"},
    "dollar_emoji": {"id": "5197434882321567830", "fallback": "💵"},
    "top_emoji": {"id": "5463071033256848094", "fallback": "🔝"},
    "bro_emoji": {"id": "5463256910851546817", "fallback": "🤝"},
    "yes_emoji": {"id": "5463423955014529788", "fallback": "👌"},
    "lock_emoji": {"id": "5465443379917629504", "fallback": "🔓"},
    "good_emoji": {"id": "5465465194056525619", "fallback": "👍"},
    "sigma_emoji": {"id": "6235620067942341623", "fallback": "🥃"},
    "don_emoji": {"id": "6235717714023814969", "fallback": "🍂"},
    "skills_emoji": {"id": "6235593671073339928", "fallback": "💀"},
    "heart_fire": {"id": "6147617184479711380", "fallback": "❤️‍🔥"},
    "stars_emoji": {"id": "6235403472741603087", "fallback": "⭐"},
    "github_emoji": {"id": "5346181118884331907", "fallback": "📱"},
    "motion_emoji": {"id": "5971944878815317190", "fallback": "💠"},
    "bolt": {"id": "5791970059597386804", "fallback": "⚡"},
    "zap": {"id": "6087079590377820415", "fallback": "⚡"},
    "kiss_heart": {"id": "6044369013952222465", "fallback": "🥰"},
    "cute": {"id": "6044359320211034681", "fallback": "🥰"},
    "mad": {"id": "6034865170449175739", "fallback": "😤"},
    "angry_face": {"id": "6034855438053282213", "fallback": "😤"},
    "thinking": {"id": "5783034045130610245", "fallback": "🤔"},
    "grin": {"id": "5782942227319756256", "fallback": "😄"},
    "sweat_smile": {"id": "5782670102486848559", "fallback": "😅"},
    "blush": {"id": "5780690182692935276", "fallback": "😊"},
    "flag_ae": {"id": "5434013938821902926", "fallback": "🇦🇪"},
    "flag_sa": {"id": "5433991338703991663", "fallback": "🇸🇦"},
    "flag_za": {"id": "5431489619038320862", "fallback": "🇿🇦"},
    "flag_sg": {"id": "5433884376838454074", "fallback": "🇸🇬"},
    "flag_ph": {"id": "5434119663736862995", "fallback": "🇵🇭"},
    "flag_vn": {"id": "5431676201007592926", "fallback": "🇻🇳"},
    "flag_th": {"id": "5433814347396692144", "fallback": "🇹🇭"},
    "flag_eg": {"id": "5433643519367461444", "fallback": "🇪🇬"},
    "flag_ke": {"id": "5433845881046578644", "fallback": "🇰🇪"},
    "flag_ar": {"id": "5433845881046578644", "fallback": "🇦🇷"},
}

def get_emoji_html(name):
    try:
        if name in PREMIUM_EMOJIS:
            data = PREMIUM_EMOJIS[name]
            return f'<tg-emoji emoji-id="{data["id"]}">{data["fallback"]}</tg-emoji>'
        return ""
    except:
        return ""

def get_random_emoji():
    try:
        names = list(PREMIUM_EMOJIS.keys())
        if not names:
            return ""
        random_name = random.choice(names)
        return get_emoji_html(random_name)
    except:
        return "✅"

def get_emoji_by_name(name):
    try:
        if name in PREMIUM_EMOJIS:
            return get_emoji_html(name)
        return None
    except:
        return None

# ============ SIMPLE TEXT FORMATTING ============
def to_fancy(text):
    try:
        fancy_map = {
            'A': '𝐀', 'B': '𝐁', 'C': '𝐂', 'D': '𝐃', 'E': '𝐄', 'F': '𝐅', 'G': '𝐆', 'H': '𝐇', 'I': '𝐈',
            'J': '𝐉', 'K': '𝐊', 'L': '𝐋', 'M': '𝐌', 'N': '𝐍', 'O': '𝐎', 'P': '𝐏', 'Q': '𝐐', 'R': '𝐑',
            'S': '𝐒', 'T': '𝐓', 'U': '𝐔', 'V': '𝐕', 'W': '𝐖', 'X': '𝐗', 'Y': '𝐘', 'Z': '𝐙',
            'a': '𝐚', 'b': '𝐛', 'c': '𝐜', 'd': '𝐝', 'e': '𝐞', 'f': '𝐟', 'g': '𝐠', 'h': '𝐡', 'i': '𝐢',
            'j': '𝐣', 'k': '𝐤', 'l': '𝐥', 'm': '𝐦', 'n': '𝐧', 'o': '𝐨', 'p': '𝐩', 'q': '𝐪', 'r': '𝐫',
            's': '𝐬', 't': '𝐭', 'u': '𝐮', 'v': '𝐯', 'w': '𝐰', 'x': '𝐱', 'y': '𝐲', 'z': '𝐳',
            '0': '𝟎', '1': '𝟏', '2': '𝟐', '3': '𝟑', '4': '𝟒', '5': '𝟓', '6': '𝟔', '7': '𝟕', '8': '𝟖', '9': '𝟗'
        }
        return ''.join(fancy_map.get(c, c) for c in text)
    except:
        return text

def format_with_double_emojis(text):
    try:
        lines = text.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip():
                left_emoji = get_random_emoji()
                right_emoji = get_random_emoji()
                formatted_lines.append(f"{left_emoji} {line} {right_emoji}")
            else:
                formatted_lines.append(line)
        return '\n'.join(formatted_lines)
    except:
        return text

# ============ FILE FUNCTIONS ============
def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except:
        return {}

def save_users(users):
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
    except:
        pass

def load_banned():
    try:
        if os.path.exists(BANNED_FILE):
            with open(BANNED_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except:
        return []

def save_banned(banned):
    try:
        with open(BANNED_FILE, 'w', encoding='utf-8') as f:
            json.dump(banned, f, indent=2, ensure_ascii=False)
    except:
        pass

users = load_users()
banned = load_banned()

def register_user(user_id, username, first_name):
    try:
        user_id_str = str(user_id)
        if user_id_str not in users:
            users[user_id_str] = {
                "id": user_id,
                "username": username or "NoUsername",
                "name": first_name or "User",
                "joined": str(datetime.now())
            }
            save_users(users)
            return True
        return False
    except:
        return False

def is_owner(user_id):
    return user_id == OWNER_ID

def is_banned(user_id):
    return str(user_id) in banned

# ============ COMMAND HANDLERS ============
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        user_id = user.id
        first_name = user.first_name or "User"
        username = user.username or "NoUsername"
        
        if is_banned(user_id):
            await update.message.reply_text("❌ You are banned!")
            return
        
        register_user(user_id, username, first_name)
        
        content = f"""
✨ WELCOME TO PREMIUM EMOJI BOT ✨
━━━━━━━━━━━━━━━━━━
👋 Hey {first_name}! Welcome aboard!
🔹 Convert any emoji to premium
🔹 Supports all formatting
🔹 100+ premium emojis
━━━━━━━━━━━━━━━━━━
📌 COMMANDS
📋 /all - Show all emojis
✨ /emojify (name) text - Convert to premium
❓ /help - Help menu
━━━━━━━━━━━━━━━━━━
💡 EXAMPLE
/emojify (verified) hello world
━━━━━━━━━━━━━━━━━━
👑 @iflexbluddy
"""
        await update.message.reply_text(content, parse_mode=None)
    except Exception as e:
        print(f"Error in start: {e}")
        await update.message.reply_text("❌ Error! Please try /start again.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        if is_banned(user_id):
            await update.message.reply_text("❌ You are banned!")
            return
        
        content = """
❓ HELP GUIDE ❓
━━━━━━━━━━━━━━━━━━
📌 HOW TO USE
1️⃣ Type /all to see all emojis
2️⃣ Use /emojify (name) your text
3️⃣ Emoji will be applied!
━━━━━━━━━━━━━━━━━━
📝 EXAMPLES
/emojify (verified) hello
/emojify (fire) (heart) I'm the best
━━━━━━━━━━━━━━━━━━
📋 COMMANDS
/all - All emojis
/emojify - Convert text
/help - This menu
━━━━━━━━━━━━━━━━━━
👑 @iflexbluddy
"""
        await update.message.reply_text(content)
    except Exception as e:
        print(f"Error in help: {e}")

async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        if is_banned(user_id):
            await update.message.reply_text("❌ You are banned!")
            return
        
        register_user(user_id, update.effective_user.username or "NoUsername", update.effective_user.first_name or "User")
        
        # Simple emoji list without HTML to avoid errors
        emoji_list = []
        for name in PREMIUM_EMOJIS.keys():
            emoji_list.append(f"✅ {name}")
        
        # Split into chunks
        chunks = [emoji_list[i:i+30] for i in range(0, len(emoji_list), 30)]
        
        for idx, chunk in enumerate(chunks):
            content = f"""📋 PREMIUM EMOJIS 📋
━━━━━━━━━━━━━━━━━━
📦 Total: {len(PREMIUM_EMOJIS)} emojis
📄 Page {idx+1}/{len(chunks)}
━━━━━━━━━━━━━━━━━━

{chr(10).join(chunk)}

━━━━━━━━━━━━━━━━━━
💡 /emojify (name) text
"""
            await update.message.reply_text(content)
    except Exception as e:
        print(f"Error in all: {e}")
        await update.message.reply_text("❌ Error loading emojis. Use /help for commands.")

async def emojify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        if is_banned(user_id):
            await update.message.reply_text("❌ You are banned!")
            return
        
        register_user(user_id, update.effective_user.username or "NoUsername", update.effective_user.first_name or "User")
        
        if not context.args:
            await update.message.reply_text(
                "📝 Usage: /emojify (emoji_name) your text\n\n"
                "Example: /emojify (verified) hello\n\n"
                "Use /all to see all emojis"
            )
            return
        
        # Get full text
        full_text = " ".join(context.args)
        
        # Replace (emoji_name) with premium emoji
        def replace_emoji(match):
            emoji_name = match.group(1).lower().strip()
            if emoji_name in PREMIUM_EMOJIS:
                return f"✅{emoji_name}✅"  # Simple replacement
            return match.group(0)
        
        # Apply replacement
        result = re.sub(r'\(([^)]+)\)', replace_emoji, full_text)
        
        # Check if any emoji was applied
        if "✅" not in result:
            await update.message.reply_text(
                "❌ No valid emoji found!\n\n"
                "Use /all to see available emojis"
            )
            return
        
        # Make text fancy
        fancy_result = to_fancy(result)
        
        # Add random emojis at start and end
        final_text = f"✨ {fancy_result} ✨"
        
        await update.message.reply_text(final_text)
    except Exception as e:
        print(f"Error in emojify: {e}")
        await update.message.reply_text("❌ Error! Please try again.")

async def owner_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        if not is_owner(user_id):
            await update.message.reply_text("❌ Owner only!")
            return
        
        total_users = len(users)
        banned_count = len(banned)
        
        content = f"""
👑 OWNER PANEL 👑
━━━━━━━━━━━━━━━━━━
📊 STATISTICS
👥 Total Users: {total_users}
🚫 Banned: {banned_count}
✅ Active: {total_users - banned_count}
📦 Total Emojis: {len(PREMIUM_EMOJIS)}
━━━━━━━━━━━━━━━━━━
👑 COMMANDS
📋 /users - List all users
🚫 /ban USER_ID - Ban user
✅ /unban USER_ID - Unban user
📊 /stats - Bot stats
━━━━━━━━━━━━━━━━━━
👑 @iflexbluddy
"""
        await update.message.reply_text(content)
    except Exception as e:
        print(f"Error in owner: {e}")

async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        if not is_owner(user_id):
            await update.message.reply_text("❌ Owner only!")
            return
        
        if not users:
            await update.message.reply_text("📭 No users found.")
            return
        
        # Create user list
        user_list = []
        for uid, u in users.items():
            status = "🚫" if uid in banned else "✅"
            username = u.get('username', 'NoUsername')
            name = u.get('name', 'User')
            user_list.append(f"{status} {uid} - @{username} ({name})")
        
        # Split into chunks
        chunks = [user_list[i:i+20] for i in range(0, len(user_list), 20)]
        
        for idx, chunk in enumerate(chunks):
            content = f"""👥 USERS LIST 👥
━━━━━━━━━━━━━━━━━━
📊 Total: {len(users)} users
📄 Page {idx+1}/{len(chunks)}
━━━━━━━━━━━━━━━━━━

{chr(10).join(chunk)}

━━━━━━━━━━━━━━━━━━
✅ = Active | 🚫 = Banned
"""
            await update.message.reply_text(content)
    except Exception as e:
        print(f"Error in users: {e}")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        if not is_owner(user_id):
            await update.message.reply_text("❌ Owner only!")
            return
        
        if len(context.args) < 1:
            await update.message.reply_text(
                "📝 Usage: /ban USER_ID\n\n"
                "Example: /ban 123456789"
            )
            return
        
        user_id_to_ban = context.args[0]
        
        if user_id_to_ban not in users:
            await update.message.reply_text(f"❌ User {user_id_to_ban} not found!")
            return
        
        if user_id_to_ban == str(OWNER_ID):
            await update.message.reply_text("❌ Cannot ban the owner!")
            return
        
        if user_id_to_ban not in banned:
            banned.append(user_id_to_ban)
            save_banned(banned)
            await update.message.reply_text(f"✅ User {user_id_to_ban} banned!")
        else:
            await update.message.reply_text(f"⚠️ User {user_id_to_ban} is already banned!")
    except Exception as e:
        print(f"Error in ban: {e}")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        if not is_owner(user_id):
            await update.message.reply_text("❌ Owner only!")
            return
        
        if len(context.args) < 1:
            await update.message.reply_text(
                "📝 Usage: /unban USER_ID\n\n"
                "Example: /unban 123456789"
            )
            return
        
        user_id_to_unban = context.args[0]
        
        if user_id_to_unban in banned:
            banned.remove(user_id_to_unban)
            save_banned(banned)
            await update.message.reply_text(f"✅ User {user_id_to_unban} unbanned!")
        else:
            await update.message.reply_text(f"⚠️ User {user_id_to_unban} is not banned!")
    except Exception as e:
        print(f"Error in unban: {e}")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        if not is_owner(user_id):
            await update.message.reply_text("❌ Owner only!")
            return
        
        total_users = len(users)
        banned_count = len(banned)
        
        content = f"""
📊 BOT STATISTICS 📊
━━━━━━━━━━━━━━━━━━
👥 Total Users: {total_users}
🚫 Banned: {banned_count}
✅ Active: {total_users - banned_count}
📦 Premium Emojis: {len(PREMIUM_EMOJIS)}
━━━━━━━━━━━━━━━━━━
👑 @iflexbluddy
"""
        await update.message.reply_text(content)
    except Exception as e:
        print(f"Error in stats: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        if is_banned(user_id):
            await update.message.reply_text("❌ You are banned!")
            return
        
        if update.message.text and update.message.text.startswith('/'):
            return
        
        register_user(user_id, update.effective_user.username or "NoUsername", update.effective_user.first_name or "User")
        
        content = """
💡 Did you mean to use a command?
━━━━━━━━━━━━━━━━━━
📌 Try these:
/all - Show all emojis
/emojify (name) text - Convert
━━━━━━━━━━━━━━━━━━
💡 /emojify (verified) hello
━━━━━━━━━━━━━━━━━━
👑 @iflexbluddy
"""
        await update.message.reply_text(content)
    except Exception as e:
        print(f"Error in message: {e}")

# ============ MAIN ============
def main():
    try:
        # Start Flask server for Render
        threading.Thread(target=run_flask, daemon=True).start()
        
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("all", all_command))
        application.add_handler(CommandHandler("emojify", emojify_command))
        application.add_handler(CommandHandler("owner", owner_panel))
        application.add_handler(CommandHandler("users", list_users))
        application.add_handler(CommandHandler("ban", ban_user))
        application.add_handler(CommandHandler("unban", unban_user))
        application.add_handler(CommandHandler("stats", stats_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("=" * 50)
        print("✨ PREMIUM EMOJI BOT STARTED ✨")
        print(f"👑 Owner ID: {OWNER_ID}")
        print(f"📦 Total Emojis: {len(PREMIUM_EMOJIS)}")
        print("✅ Bot is ready!")
        print("👑 Developer: @iflexbluddy")
        print("=" * 50)
        
        # Start polling
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
