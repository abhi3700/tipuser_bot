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

# ===================================================command: /deposit===========================================================================
@bot.command("deposit")
def deposit_command(chat, message, args):
    """Deposit your EOSIO token to this bot by telegram ID as memo"""
    chat.send(f"Send token to \'{tip_eosio_ac}\' with your unique telegram ID - {chat.id} as the memo to deposit!")

# ===================================================command: /withdraw===========================================================================
@bot.command("withdraw")
def withdraw_command(chat, message, args):
    """
        Withdraw your EOSIO token from this bot to your EOSIO account
        Demo:
        =====
        User: 
            /withdraw tipuser11111 1.0000 EOS
        Bot:
            DONE!
    """
    if len(args) == 3:
        chat.send(f"arg0: {args[0]}\narg1: {args[1]}\narg2: {args[2]}")        # for testing
    else:
        chat.send("Please enter withdrawal request in this format: /withdrawmemo ACCOUNT AMOUNT SYMBOL \n(e.g. /withdraw tipuser11111 1.0000 EOS)")

# ===================================================command: /withdrawmemo===========================================================================
@bot.command("withdrawmemo")
def withdrawmemo_command(chat, message, args):
    """
        Withdraw your EOSIO token from this bot to your EOSIO account with a memo
        NOTE: Please don't use 'space' in between words in `memo`. Instead, use 'hyphen', etc.
        
        Demo:
        =====
        User: 
            /withdrawmemo tipuser11111 1.0000 EOS pay-bill
        Bot:
            DONE!
    """
    if len(args) == 4:
        chat.send(f"arg0: {args[0]}\narg1: {args[1]}\narg2: {args[2]}\narg3: {args[3]}")        # for testing
    else:
        chat.send("Please enter withdrawal request (with memo) in this format: /withdrawmemo ACCOUNT AMOUNT SYMBOL MEMO \n(e.g. /withdrawmemo tipuser11111 1.0000 EOS pay_bill)")

# ===================================================command: /tip===========================================================================
@bot.command("tip")
def tip_command(chat, message, args):
    """
        Tip your EOSIO token from this bot to a user (with telegram id) along with a memo
        NOTE: Please don't use 'space' in between words in `memo`. Instead, use 'hyphen', etc.
        
        Demo:
        =====
        User: 
            /tip tipuser11112 0.1000 EOS restaurant-tip-for-excellent-service
        Bot:
            DONE!
    """
    if len(args) == 4:
        chat.send(f"arg0: {args[0]}\narg1: {args[1]}\narg2: {args[2]}\narg3: {args[3]}")        # for testing
    else:
        chat.send("Please enter tip request (with memo) in this format: /tip RECEIVER-ACCOUNT AMOUNT SYMBOL MEMO \n(e.g. /tip tipuser11112 0.1000 EOS restaurant-tip-for-excellent-service)")


# ================================================MAIN===========================================================================
if __name__ == "__main__":
    bot.run()