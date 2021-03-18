# tipuser_bot
A Telegram Bot for tipping user using an EOSIO blockchain.

## Features
* deposit fund to the bot's eosio account with any memo, from outside chat interface via blockchain.
	- [NOT Recommended] basically into tip eosio account tippertipper from outside (i.e. telegram chat) by mentioning a memo as "deposit fund"
* `/addac (account)`: add your eosio account into DB.
* `/listacs`: list eosio accounts added.
* `/balance` - show your account (saved in DB) balance. If multiple accounts, then parse the eosio_ac_name like this `/balance <eosio_ac_name>`
* `/withdraw (amount)`: withdraw money to your a/c
	- token transfer happens using `cleoswt push action eosio.token transfer '["tippertipper", "tipuser11111", "5.0000 EOS", "transfer 5 EOS as per the request"]' -p tippertipper@systemkey`
	- [ ] parse the message_id as request_id into memo.
* `/tip (receiver_ac, qty, memo)`: give receiver's eosio account (say `tipuser11112`) so that the amount can be transferred from user's fund to an receiver account with a custom msg.
	- token transfer happens using `cleoswt push action eosio.token transfer '["tippertipper", "tipuser11112", "2.0000 EOS", "transfer 2 EOS as per the request"]' -p tippertipper@systemkey`

## Coding
* to get the eosio_ac_name of a user, just run the query on redis DB by telegram_id
* to get the balance of a user, just capture the eosio_ac_name by querying on redis DB as per telegram_id & then `cleos get account <eosio_ac_name>`

## Database
* Cloud: Redis on Heroku

## Contracts
* [tippertipper](https://github.com/abhi3700/eosio_tipuser_contracts)

## References