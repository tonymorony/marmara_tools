from marmara_lib import *
import time
import subprocess

mcl_proxy = def_credentials("MCL")

pubkeys_and_balances = marmara_pubkey_balance(mcl_proxy)

pubkeys_to_clear = {}

for pubkey in pubkeys_and_balances:
    if pubkeys_and_balances[pubkey] > 30:
        pubkeys_to_clear[pubkey] = pubkeys_and_balances[pubkey]

print(str(len(pubkeys_to_clear)) + " pubkeys to clear:")
print(pubkeys_to_clear)

for pubkey in pubkeys_to_clear:
    print("Stopping daemon")
    mcl_proxy.stop()
    time.sleep(15)
    print("Starting daemon with " + pubkey + " pubkey")
    print("To unlock " + str(pubkeys_to_clear[pubkey]) + " MCL")
    subprocess.call(['./komodod', '-ac_name=MCL', '-ac_supply=2000000', '-ac_cc=2', '-addnode=37.148.210.158',
                     '-addnode=37.148.212.36', '-addressindex=1', '-spentindex=1', '-ac_marmara=1',
                     '-ac_staked=75', '-ac_reward=3000000000', '-pubkey='+pubkey, '-daemon'])
    # dirty way, it's better to add function which will check if daemon is app
    time.sleep(30)
    mcl_proxy = def_credentials("MCL")
    unlock_hash = mcl_proxy.marmaraunlock(pubkeys_to_clear[pubkey])
    try:
        unlock_txid = mcl_proxy.sendrawtransaction(unlock_hash)
    except Exception as e:
        print(e)
        print(unlock_hash)
    print("Unlock txid: " + unlock_txid)