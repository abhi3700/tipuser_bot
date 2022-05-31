import os
from dotenv import load_dotenv

load_dotenv()  #  take environment variables from .env.

# -------------------------------------------------------------------------------
API_KEY = str(os.getenv('API_KEY'))

# Capture using `$ heroku config | grep REDIS` from the terminal at App's root dir
# Capture using `$ heroku redis:credentials REDIS_URL -a kyctelbot` from the terminal
REDIS_URL = str(os.getenv('REDIS_URL'))

Chain_URL = 'http://jungle3.cryptolions.io:80'      # Jungle Testnet
chain_name = 'jungle3'
chain_type = 'eos-testnet'

# tippertipper eosio_ac
tip_eosio_ac = 'tippertipper'
tip_ac_private_key = str(os.getenv('TIP_AC_PRIVATE_KEY'))
tip_ac_key_perm = 'active'
tip_table = 'accounts'

# ACTION
tip_action = 'tip'
withdraw_action = 'withdraw'
