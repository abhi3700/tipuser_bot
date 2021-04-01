import botogram
# import redis
import json

from input import *

# -------------------------------------------------------About Bot--------------------------------------------------------------------
bot = botogram.create(API_key)
bot.about = "This is a Tip Bot."
bot.owner = "@abhi3700"

# -------------------------------------------------------Redis DB------------------------------------------------------------------------
# define Redis database
# r = redis.from_url(REDIS_URL)

# ===================================================Share telegram_id===========================================================================
@bot.command("deposit")
def deposit_command(chat, message, args):
    """Please share your telegram id. Also Get it from @userinfobot"""
    chat.send("Send token to tippedtipped with your unique telegram ID {chat_id} as the memo to deposit!".format(chat_id=chat.id))

# ===================================================remove keyboard(s)=================================================================
# @bot.command("removekeyboard")
# def removekeyboard_command(chat, message):
#     """removes the keyboard appearing below"""
#     bot.api.call('sendMessage', {
#         'chat_id': chat.id,
#         'reply_to_message': message.id,
#         'text': 'keyboards removed.',
#         'reply_markup': json.dumps({
#             'remove_keyboard': True,
#             # This 1 parameter below is optional
#             # See https://core.telegram.org/bots/api#replykeyboardremove
#             'selective': True,
#         })
#     })

# ================================================MAIN===========================================================================
if __name__ == "__main__":
    bot.run()