import botogram
# import redis
import json
import asyncio

from aioeos import EosAccount, EosJsonRpc, EosTransaction
from aioeos import types

from aioeos.exceptions import EosRpcException
from aioeos.exceptions import EosAccountDoesntExistException
from aioeos.exceptions import EosAssertMessageException
from aioeos.exceptions import EosDeadlineException
from aioeos.exceptions import EosRamUsageExceededException
from aioeos.exceptions import EosTxCpuUsageExceededException
from aioeos.exceptions import EosTxNetUsageExceededException

from input import *

# -------------------------------------------------------About Bot--------------------------------------------------------------------
bot = botogram.create(API_key)
bot.about = "This is a Tip Bot."
bot.owner = "@abhi3700"

# -------------------------------------------------------Redis DB------------------------------------------------------------------------
# define Redis database
# r = redis.from_url(REDIS_URL)

# ===================================================UTILITY func========================================================
# '''
# 	Validate JSON response
# '''
# def validate(j, chat):
#     try:
#         return json.load(j) # put JSON-data to a variable
#     except json.decoder.JSONDecodeError:
#         # print("Invalid JSON") # in case json is invalid
#         chat.send(f"Invalid JSON. Please contact the Bot owner {bot.owner} with the error message.") # in case json is invalid
#     # else:
#     #     print("Valid JSON") # in case json is valid

# ===================================================UTILITY func========================================================

# ===================================================func for show balance========================================================
async def balance(
		from_id,
		chat
	):
	rpc = EosJsonRpc(url=Chain_URL)
	table_response = await rpc.get_table_rows(
							code=tip_eosio_ac,
							scope= tip_eosio_ac, 
							table=tip_table, 
							lower_bound= from_id, 
							upper_bound= from_id
						)
	
	table_response = str(table_response).replace("\'", "\"")
	table_response = table_response.replace("False", "false")       # As False is invalid in JSON, so replace with false
	# print(table_response)
	
	for r in json.loads(table_response)['rows'][0]["balances"]:
		prec, sym_name = r["key"]["sym"].split(",")
		# print(f'token precision: {prec}')                 		# precision
		# print(f'token sym_name: {sym_name}')              		# symbol name
		# print(f'val: {r["value"]/10**int(prec)}\n\n')     		# exact value
		chat.send(f'{r["value"]/10**int(prec)} {sym_name}\n')     	# result e.g. 2.0 EOS

# ===================================================func for withdraw & withdrawmemo ACTION========================================================
async def withdraw(
		from_id,
		from_username,
		to_ac,
		quantity,
		memo,
		chat
	):
	contract_account = EosAccount(
	  name=tip_eosio_ac,
	  private_key=tip_ac_private_key
	)

	action = types.EosAction(
		account=tip_eosio_ac,
		name=withdraw_action,
		authorization=[contract_account.authorization(tip_ac_key_perm)],
		data={
			'from_id': from_id,
			'from_username': from_username,
			'to_ac': to_ac,
			'quantity': quantity,
			'memo': memo
		}
	)

	rpc = EosJsonRpc(url=Chain_URL)
	block = await rpc.get_head_block()

	transaction = EosTransaction(
	  ref_block_num=block['block_num'] & 65535,
	  ref_block_prefix=block['ref_block_prefix'],
	  actions=[action]
	)

	response = await rpc.sign_and_push_transaction(
	  transaction, keys=[contract_account.key]
	)
	# chat.send(f'{response}')             # print the full response after SUCCESS
	
	response = str(response).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
	# print(response)               # print the full response after replacing single with double quotes
	'''
		Here, as the response o/p is not a valid JSON giving error like this:
		Error:
			Parse error on line 1:
			...producer_block_id": None, "receipt": {"s
			-----------------------^
			Expecting 'STRING', 'NUMBER', 'NULL', 'TRUE', 'FALSE', '{', '[', got 'undefined'

		So, capture txn_id by char no. i.e. {"transaction_id": "14e310c6e296560202ec808139d7e1b06901616f35b5c4a36ee0a4f065ec72a6"
	'''
	chat.send(f"\nView the transaction here: https://bloks.io/transaction/{response[20:84]}") if chain_type== "eos-mainnet" else chat.send(f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{response[20:84]}")          # print the txn_id for successful transaction

# ===================================================func for tip ACTION===================================================================
async def tip(
		from_id,
		to_id,
		from_username,
		to_username,
		quantity,
		memo,
		chat
	):
	contract_account = EosAccount(
	  name=tip_eosio_ac,
	  private_key=tip_ac_private_key
	)

	action = types.EosAction(
		account=tip_eosio_ac,
		name=tip_action,
		authorization=[contract_account.authorization(tip_ac_key_perm)],
		data={
			'from_id': from_id,
			'to_id': to_id,
			'from_username': from_username,
			'to_username': to_username,
			'quantity': quantity,
			'memo': memo
		}
	)

	rpc = EosJsonRpc(url=Chain_URL)
	block = await rpc.get_head_block()

	transaction = EosTransaction(
	  ref_block_num=block['block_num'] & 65535,
	  ref_block_prefix=block['ref_block_prefix'],
	  actions=[action]
	)

	response = await rpc.sign_and_push_transaction(
	  transaction, keys=[contract_account.key]
	)
	# chat.send(f'{response}')             # print the full response after SUCCESS
	
	response = str(response).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
	# print(response)               # print the full response after replacing single with double quotes
	'''
		Here, as the response o/p is not a valid JSON giving error like this:
		Error:
			Parse error on line 1:
			...producer_block_id": None, "receipt": {"s
			-----------------------^
			Expecting 'STRING', 'NUMBER', 'NULL', 'TRUE', 'FALSE', '{', '[', got 'undefined'

		So, capture txn_id by char no. i.e. {"transaction_id": "14e310c6e296560202ec808139d7e1b06901616f35b5c4a36ee0a4f065ec72a6"
	'''
	chat.send(f"\nView the transaction here: https://bloks.io/transaction/{response[20:84]}") if chain_type== "eos-mainnet" else chat.send(f"\nView the transaction here: https://{chain_name}.bloks.io/transaction/{response[20:84]}")          # print the txn_id for successful transaction


# ===================================================command: /balance===========================================================================
@bot.command("balance")
def balance_command(chat, message, args):
	"""Show your token balance"""
	try:
		# push txn
		asyncio.get_event_loop().run_until_complete(balance(chat.id, chat))

	except EosRpcException as e:
		e = str(e).replace("\'", "\"")
		code_idx = e.find('code')
		code_val = int(e[code_idx+7:(code_idx+14)])
		# print(code_idx)
		# print(code_val)
		# print(type(code_val))
		if code_idx != -1:			# found "code" key
			if code_val == 3010001:						# Case-1: invalid name
				chat.send("Sorry! Your EOSIO account name doesn\'t exist on this chain.")
			elif code_val == 3050003:					# Case-1: incorrect quantity or symbol
				chat.send("Sorry! Your EOSIO account doesn\'t have any balances corresponding to parsed quantity or symbol on this chain.")
			elif code_val == 3080004:
				chat.send("Sorry! The contract account \'tippertipper\' doesn\'t have enough CPU to handle this activity on this chain. Please contact the Bot owner {bot.owner}.")
			else:
				chat.send("Sorry! Some other Exception occured. Please contact the Bot owner {bot.owner}.")
		else:						# NOT found "code" key
			chat.send("Sorry! No code no. is present in the error. Please contact the Bot owner {bot.owner}.")
	except EosAccountDoesntExistException:
		chat.send(f'Your EOSIO account name doesn\'t exist on this chain.')
	except EosAssertMessageException as e:
		e = str(e).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
		# chat.send(f"{str(e)}", syntax="plain")      # print full error dict
		chat.send(f"Assertion Error msg --> {json.loads(e)['details'][0]['message']}")          # print the message
	except EosDeadlineException:
		chat.send(f'Transaction timed out. Please try again.')

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
		# chat.send(f"arg0: {args[0]}\narg1: {args[1]}\narg2: {args[2]}")        # for testing
		try:
			# push txn
			asyncio.get_event_loop().run_until_complete(withdraw(chat.id, message.sender.username, args[0], args[1] + " " + args[2], "", chat))

		except EosRpcException as e:
			e = str(e).replace("\'", "\"")
			code_idx = e.find('code')
			code_val = int(e[code_idx+7:(code_idx+14)])
			# print(code_idx)
			# print(code_val)
			# print(type(code_val))
			if code_idx != -1:			# found "code" key
				if code_val == 3010001:						# Case-1: invalid name
					chat.send("Sorry! Your EOSIO account name doesn\'t exist on this chain.")
				elif code_val == 3050003:					# Case-1: incorrect quantity or symbol
					chat.send("Sorry! Your EOSIO account doesn\'t have any balances corresponding to parsed quantity symbol pair on this chain.")
				elif code_val == 3080004:
					chat.send("Sorry! The contract account \'tippertipper\' doesn\'t have enough CPU to handle this activity on this chain. Please contact the Bot owner {bot.owner}.")
				else:
					chat.send("Sorry! Some other Exception occured. Please contact the Bot owner {bot.owner}.")
			else:						# NOT found "code" key
				chat.send("Sorry! No code no. is present in the error. Please contact the Bot owner {bot.owner}.")
		except EosAccountDoesntExistException:
			chat.send(f'Your EOSIO account name doesn\'t exist on this chain.')
		except EosAssertMessageException as e:
			e = str(e).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
			# chat.send(f"{str(e)}", syntax="plain")      # print full error dict
			chat.send(f"Assertion Error msg --> {json.loads(e)['details'][0]['message']}")          # print the message
		except EosDeadlineException:
			chat.send(f'Transaction timed out. Please try again.')
		except EosRamUsageExceededException:
			chat.send(f'Transaction requires more RAM than what???s available on the account. Please contact the Bot owner {bot.owner}.');
		except EosTxCpuUsageExceededException:
			chat.send(f'Not enough EOS were staked for CPU. Please contact the Bot owner {bot.owner}.');
		except EosTxNetUsageExceededException:
			chat.send(f'Not enough EOS were staked for NET. Please contact the Bot owner {bot.owner}.');

	else:
		chat.send("Please enter withdrawal request in this format: /withdraw ACCOUNT AMOUNT SYMBOL e.g.", syntax="plain")
		chat.send("/withdraw tipuser11111 1.0000 EOS")

# ===================================================command: /withdrawmemo===========================================================================
@bot.command("withdrawmemo")
def withdrawmemo_command(chat, message, args):
	"""
		Withdraw your EOSIO token from this bot to your EOSIO account with a memo
		NOTE: Please don't use 'space' in between words in `memo`. Instead, use 'underscore', 'hyphen', etc.
		
		Demo:
		=====
		User: 
			/withdrawmemo tipuser11111 1.0000 EOS pay-bill
		Bot:
			DONE!
	"""
	if len(args) == 4:
		# chat.send(f"arg0: {args[0]}\narg1: {args[1]}\narg2: {args[2]}\narg3: {args[3]}", syntax="plain")        # for testing
		try:
			# push txn
			asyncio.get_event_loop().run_until_complete(withdraw(chat.id, message.sender.username, args[0], args[1] + " " + args[2], args[3], chat))

		except EosRpcException as e:
			e = str(e).replace("\'", "\"")
			code_idx = e.find('code')
			code_val = int(e[code_idx+7:(code_idx+14)])
			# print(code_idx)
			# print(code_val)
			# print(type(code_val))
			if code_idx != -1:			# found "code" key
				if code_val == 3010001:						# Case-1: invalid name
					chat.send("Sorry! Your EOSIO account name doesn\'t exist on this chain.")
				elif code_val == 3050003:					# Case-1: incorrect quantity or symbol
					chat.send("Sorry! Your EOSIO account doesn\'t have any balances corresponding to parsed quantity symbol pair on this chain.")
				elif code_val == 3080004:
					chat.send("Sorry! The contract account \'tippertipper\' doesn\'t have enough CPU to handle this activity on this chain. Please contact the Bot owner {bot.owner}.")
				else:
					chat.send("Sorry! Some other Exception occured. Please contact the Bot owner {bot.owner}.")
			else:						# NOT found "code" key
				chat.send("Sorry! No code no. is present in the error. Please contact the Bot owner {bot.owner}.")
		except EosAccountDoesntExistException:
			chat.send(f'Your EOSIO account name doesn\'t exist on this chain.')
		except EosAssertMessageException as e:
			e = str(e).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
			# chat.send(f"{str(e)}", syntax="plain")      # print full error dict
			chat.send(f'Assertion Error msg --> {json.loads(e)["details"][0]["message"]}')          # print the message
		except EosDeadlineException:
			chat.send(f'Transaction timed out. Please try again.')
		except EosRamUsageExceededException:
			chat.send(f'Transaction requires more RAM than what???s available on the account. Please contact the Bot owner {bot.owner}.');
		except EosTxCpuUsageExceededException:
			chat.send(f'Not enough EOS were staked for CPU. Please contact the Bot owner {bot.owner}.');
		except EosTxNetUsageExceededException:
			chat.send(f'Not enough EOS were staked for NET. Please contact the Bot owner {bot.owner}.');
	else:
		chat.send("Please enter withdrawal request (with memo) in this format: /withdrawmemo ACCOUNT AMOUNT SYMBOL MEMO e.g.", syntax="plain") 
		chat.send("/withdrawmemo tipuser11111 1.0000 EOS pay_bill", syntax="plain")

# ===================================================command: /tip===========================================================================
@bot.command("tip")
def tip_command(chat, message, args):
	"""
		Tip your EOSIO token from this bot to a user (with telegram id) along with a memo
		NOTE: Please don't use 'space' in between words in `memo`. Instead, use 'underscore', 'hyphen', etc.
		
		Demo:
		=====
		User: 
			/tip 768743431 0.1000 EOS restaurant-tip-for-excellent-service
		Bot:
			DONE!
	"""
	if len(args) == 4:
		# chat.send(f"arg0: {args[0]}\narg1: {args[1]}\narg2: {args[2]}\narg3: {args[3]}")        # for testing
		try:
			# push txn
			asyncio.get_event_loop().run_until_complete(tip(chat.id, args[0], message.sender.username, "optional", args[1] + " " + args[2], args[3], chat))

		except EosRpcException as e:
			e = str(e).replace("\'", "\"")
			code_idx = e.find('code')
			code_val = int(e[code_idx+7:(code_idx+14)])
			# print(code_idx)
			# print(code_val)
			# print(type(code_val))
			if code_idx != -1:			# found "code" key
				if code_val == 3010001:						# Case-1: invalid name
					chat.send("Sorry! Your EOSIO account name doesn\'t exist on this chain.")
				elif code_val == 3050003:					# Case-1: incorrect quantity or symbol
					chat.send("Sorry! Your EOSIO account doesn\'t have any balances corresponding to parsed quantity symbol pair on this chain.")
				elif code_val == 3080004:
					chat.send("Sorry! The contract account \'tippertipper\' doesn\'t have enough CPU to handle this activity on this chain. Please contact the Bot owner {bot.owner}.")
				else:
					chat.send("Sorry! Some other Exception occured. Please contact the Bot owner {bot.owner}.")
			else:						# NOT found "code" key
				chat.send("Sorry! No code no. is present in the error. Please contact the Bot owner {bot.owner}.")
		except EosAccountDoesntExistException:
			chat.send(f'Your EOSIO account name doesn\'t exist on this chain.')
		except EosAssertMessageException as e:
			e = str(e).replace("\'", "\"")            # replace single quotes (') with double quotes (") to make it as valid JSON & then extract the 'message' value.
			# chat.send(f"{str(e)}", syntax="plain")      # print full error dict
			chat.send(f'Assertion Error msg --> {json.loads(e)["details"][0]["message"]}')          # print the message
		except EosDeadlineException:
			chat.send(f'Transaction timed out. Please try again.')
		except EosRamUsageExceededException:
			chat.send(f'Transaction requires more RAM than what???s available on the account. Please contact the Bot owner {bot.owner}.');
		except EosTxCpuUsageExceededException:
			chat.send(f'Not enough EOS were staked for CPU. Please contact the Bot owner {bot.owner}.');
		except EosTxNetUsageExceededException:
			chat.send(f'Not enough EOS were staked for NET. Please contact the Bot owner {bot.owner}.');
	else:
		chat.send("Please enter tip request (with memo) in this format: /tip RECEIVER_ID AMOUNT SYMBOL MEMO e.g.", syntax="plain")
		chat.send("/tip 768743431 0.1000 EOS restaurant_tip_for_excellent_service", syntax="plain")


# ================================================MAIN===========================================================================
if __name__ == "__main__":
	bot.run()
