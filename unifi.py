import json
import requests
import multiprocessing
from flask import Flask
from flask import request
from flask import Response
from urllib.parse import quote_plus
import math
from tronapi import Tron
from tronapi import HttpProvider
import time
import psycopg2
import os
import ecdsa
import base58
import ecdsa
import random
from Crypto.Hash import keccak
from decimal import Decimal

full_node = HttpProvider('https://api.trongrid.io')
solidity_node = HttpProvider('https://api.trongrid.io')
event_server = HttpProvider('https://api.trongrid.io')
tron = Tron(full_node=full_node,
                solidity_node=solidity_node,
                event_server=event_server)

###FUTURE DEVELOPMENT###
# from tronapi import Tron
# from tronapi import HttpProvider
# from selenium import webdriver
# from time import sleep
# import os
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.touch_actions import TouchActions
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
bottoken= ""
TELEGRAM_WEBSITE = "https://api.telegram.org/bot" + bottoken
UNIFI_WEB="https://tron.unifiprotocol.com/api/v1/pools/tron"
UNIFI_DATA=requests.get(UNIFI_WEB).json()
f = open("offlinedata.txt", "r")
a=f.read()
f.close()
UNIFI_DATA_OFFLINE=json.loads(a)
fee = 0.000001
app=Flask(__name__)
def INSERT_COMMAS(number):
    return '{:,}'.format(number)
def truncate(number) -> float:
    stepper = 10.0 ** 2
    number=math.trunc(stepper * float(number)) / stepper
    return number
def GENERATE_WALLET():
    def keccak256(data):
        hasher = keccak.new(digest_bits=256)
        hasher.update(data)
        return hasher.digest()
    def get_signing_key(raw_priv):
        return ecdsa.SigningKey.from_string(raw_priv, curve=ecdsa.SECP256k1)
    def verifying_key_to_addr(key):
        pub_key = key.to_string()
        primitive_addr = b'\x41' + keccak256(pub_key)[-20:]
        # 0 (zero), O (capital o), I (capital i) and l (lower case L)
        addr = base58.b58encode_check(primitive_addr)
        return addr
    #a = tron.trx.send_transaction("TDnv1zYAvuc1Nef42wMVUuVeF276S8ZP4A", 1.69)'
    while True:
        raw = bytes(random.sample(range(0, 256), 32))
        # raw = bytes.fromhex('a0a7acc6256c3..........b9d7ec23e0e01598d152')
        key = get_signing_key(raw)
        addr = verifying_key_to_addr(key.get_verifying_key()).decode()
        break
    return {"address":addr,"privateKey":raw.hex(),"hexAddress": base58.b58decode_check(addr.encode()).hex()}
# def GET_APPROVE(TELE_ID):
#     select = '''SELECT
#                 approve
#                 FROM
#                 telegram
#                 WHERE
#                 {}= %s ;
#                               '''.format("teleid")
#     cursor.execute(select, (TELE_ID,))
#     keys = cursor.fetchall()
#     if bool(keys) == False:
#         return False
#     elif None in keys[0] or "no" in :
#         return False
#     else:
#         return keys
def SEND_ACCOUNT_DETAILS(TELE_ID,PUBLIC_KEY,PRIVATE_KEY):
        SEND_ACCOUNT_TEXT="Account details:\n\nPublic Key: <b>{}</b>\n\n\n Private Key: <b>{}</b>\n\nKeep your private key safe !".format(PUBLIC_KEY,PRIVATE_KEY)
        requests.post(TELEGRAM_WEBSITE + "/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(TELE_ID,SEND_ACCOUNT_TEXT))
def SEND_TRANSACTION(privatekey,publickey,RIVAL_publickey,TIP_AMOUNT):
        full_node = HttpProvider('https://api.trongrid.io')
        solidity_node = HttpProvider('https://api.trongrid.io')
        event_server = HttpProvider('https://api.trongrid.io')
        tron = Tron(full_node=full_node,
                    solidity_node=solidity_node,
                    event_server=event_server)
        tron.private_key = privatekey
        tron.default_address = publickey
        SEND_WINNINGS = tron.trx.send_transaction(RIVAL_publickey, float(TIP_AMOUNT))  ## Comment out 10**6
        return SEND_WINNINGS
def SEND_TRANSACTION_DETAILS(USERNAME,RIVAL_USERNAME,TELE_ID,RIVAL_TELE_ID,TIP_AMOUNT):
        TRANSACTION_DETAILS_TEXT="<a href=\"tg://user?id={}\">@{}</a> sent <b>{}</b> <b>TRX</b> to <a href=\"tg://user?id={}\">@{}</a> .".format(TELE_ID,SANITISE_TEXT(USERNAME),TIP_AMOUNT,RIVAL_TELE_ID,SANITISE_TEXT(RIVAL_USERNAME))
        response_body = requests.post(TELEGRAM_WEBSITE + "/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(CHAT_ID, TRANSACTION_DETAILS_TEXT))
        response_body = response_body.json()

def SEND_FAILED_TRANSACTION_DETAILS(USERNAME,RIVAL_USERNAME,TELE_ID):
        TRANSACTION_DETAILS_TEXT = "<a href=\"tg://user?id={}\">@{}</a> to <a href=\"tg://user?id={}\">@{}</a> transaction failed .".format(
            TELE_ID, SANITISE_TEXT(USERNAME),RIVAL_TELE_ID, SANITISE_TEXT(RIVAL_USERNAME))
        response_body = requests.post(TELEGRAM_WEBSITE + "/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(CHAT_ID,TRANSACTION_DETAILS_TEXT))
        response_body = response_body.json()
def MAKE_ACCOUNT(TELE_ID,REAL_USERNAME,FIRST_NAME):
        NEW_ADDRESS=GENERATE_WALLET()
        PUBLICKEY=NEW_ADDRESS["address"]
        PRIVATEKEY=NEW_ADDRESS["privateKey"]
        HEX=NEW_ADDRESS["hexAddress"]
        REAL_USERNAME = "#" if REAL_USERNAME == "##EMPTY##" else REAL_USERNAME
        INSERT_MAKE_ACCOUNT='''INSERT INTO telegram (teleid,messageid,chatid,hex,publickey,privatekey,username,timestampChallenge,first_name,approve) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'''
        VALUES=(str(TELE_ID),"INACTIVE","INACTIVE",HEX,PUBLICKEY,PRIVATEKEY,REAL_USERNAME,str(time.time()),FIRST_NAME,"no")
        cursor.execute(INSERT_MAKE_ACCOUNT,VALUES)
        connection.commit()
def SEND_DATA(TOKEN_INFO):
    token=TOKEN_INFO["name"]
    price=TOKEN_INFO["price"]
    against_token=TOKEN_INFO["againstTokenAddress"]
    token1_liquidity=TOKEN_INFO["liquidityA"]
    token2_liquidity=TOKEN_INFO["liquidityB"]
    volume=TOKEN_INFO["volume"]
    contractaddress=TOKEN_INFO["contractAddress"]
    PAGE_WEB_REFERENCE="https://tron.unifiprotocol.com/liquidity/pool/join/" + contractaddress
    PAGE_REFERENCE="<a href=\"{}\">{}</a>".format(PAGE_WEB_REFERENCE,token+"/"+against_token)
    DATA_TEXT=PAGE_REFERENCE+"\n\nPrice : {} {}\n\nLiquidity :\n{} - {}\n{} - {}\n\nVolume : {} {}".format(INSERT_COMMAS(truncate(price)),against_token,against_token,INSERT_COMMAS(int(float(token2_liquidity))),token,INSERT_COMMAS(int(float(token1_liquidity))),INSERT_COMMAS(int(float(volume))),token)
    if token.casefold() == "uptrx" and against_token.casefold()== "trx":
        UNIFI_WEB_REDEEM = "https://api.sesameseed.org/votes/unifi/getPrice"
        UNIFI_REDEEM_DATA = requests.get(UNIFI_WEB_REDEEM).json()
        TOTAL_SUPPLY = UNIFI_REDEEM_DATA["trx"]["TotalSupply"]
        DATA_TEXT=PAGE_REFERENCE+"\n\nPrice : {} {}\n\nLiquidity : {} - {}\n                  {} - {}\n\nVolume : {} {}\n\nTotal Supply : {} UP\n\nMarket Cap : {} {}".format(INSERT_COMMAS(truncate(price)),against_token,against_token,INSERT_COMMAS(int(float(token2_liquidity))),token,INSERT_COMMAS(int(float(token1_liquidity))),INSERT_COMMAS(int(float(volume))),token,INSERT_COMMAS(int(float(TOTAL_SUPPLY))),INSERT_COMMAS(int(float(price)*float(TOTAL_SUPPLY))),against_token)
    return DATA_TEXT
def SANITISE_TEXT(TEXT):
    TEXT = TEXT.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")
    return quote_plus(TEXT)
def INSUFFICIENT_FUNDS(TELE_ID):
        INSUFFICIENT_FUNDS_TEXT = "<a href=\"tg://user?id={}\">{}</a>\nInsufficient funds. /account to view your account details .".format(TELE_ID, SANITISE_TEXT(USERNAME))
        RESPONSE_BODY=requests.post(
            TELEGRAM_WEBSITE + "/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(CHAT_ID,INSUFFICIENT_FUNDS_TEXT))
def ACCOUNT_PRESENT(parameter):
        query="teleid"if type(parameter) == int else "username"
        parameter=str(parameter) if type(parameter)==int else parameter
        select = '''SELECT
                    publickey,privatekey
                    FROM
                    telegram
                    WHERE 
                    {}= %s ;
                                  '''.format(query)
        cursor.execute(select,(parameter,))
        keys=cursor.fetchall()
        if bool(keys) == False:
            return  False
        elif None in keys[0]:
            return False
        else:
            return keys
def READ():
        select = '''SELECT
             {} 
         FROM
           telegram
           ORDER BY SrNo ASC;
         '''.format("update_id")
        cursor.execute(select)
        update_id_list = cursor.fetchall()
        LAST_ID = update_id_list[0][0]
        return LAST_ID
def UPDATE_INFO(TELE_ID,REAL_USERNAME,FIRST_NAME):
        if REAL_USERNAME=="##EMPTY##":
           REAL_USERNAME="#"
        else:
            pass
        TELE_ID=str(TELE_ID)
        cursor.execute(
            "UPDATE telegram SET username=%s,first_name=%s WHERE teleid=%s",
            (REAL_USERNAME,FIRST_NAME,TELE_ID))
        connection.commit()
def SEND_TOKEN_DOESNOT_EXIST(TELE_ID, USERNAME):
    SEND_TOKEN_DOESNOT_EXIST_TEXT="<a href=\"tg://user?id={}\">@{}</a>\nNo matching token . Check if the syntax is correct .".format(TELE_ID,SANITISE_TEXT(USERNAME))
    requests.post(
        TELEGRAM_WEBSITE + "/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(CHAT_ID,
                                                                                    SEND_TOKEN_DOESNOT_EXIST_TEXT))
def SEND_WRONG_DECIMALS(TELE_ID,USERNAME,decimals):
    SEND_WRONG_DECIMALS_TEXT = "<a href=\"tg://user?id={}\">@{}</a>\nToken can have a maximum of {} decimal places .".format(
        TELE_ID, SANITISE_TEXT(USERNAME),decimals)
    requests.post(
        TELEGRAM_WEBSITE + "/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(CHAT_ID,
                                                                                    SEND_WRONG_DECIMALS_TEXT))
def CONNECTION():
    DATABASE_URL = os.environ['DATABASE_URL']
    my_connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    return my_connection
def SEND_TOKEN(contractaddress,amount,tokenaddress):
    try:
        approve = tron.transaction_builder.trigger_smart_contract(contract_address=tron.address.to_hex(tokenaddress),
                                                              function_selector='approve(address,uint256)',
                                                              fee_limit=1000000,
                                                              call_value=0,
                                                              parameters=[
                                                                  {'type': 'address', 'value': contractaddress},{'type': 'uint256', 'value': amount}
                                                              ]
                                                              )
        tron.trx.sign_and_broadcast(approve['transaction'])
        txn = tron.transaction_builder.trigger_smart_contract(contract_address=tron.address.to_hex(contractaddress),
                                                              function_selector='Sell(uint256)',
                                                              fee_limit=5000000,
                                                              call_value=0,
                                                              parameters=[
                                                                  {'type': 'uint256', 'value': amount},
                                                              ]
                                                              )
        transaction=tron.trx.sign_and_broadcast(txn['transaction'])

        return transaction
    except:
        return False
def BUY_TOKEN(contractaddress,amount,tokenaddress,publickey):
    try:
        approve = tron.transaction_builder.trigger_smart_contract(contract_address=tron.address.to_hex(tokenaddress),
                                                              function_selector='approve(address,uint256)',
                                                              fee_limit=10000000,
                                                              call_value=0,
                                                              parameters=[
                                                                  {'type': 'address', 'value': contractaddress},{'type': 'uint256', 'value': amount}
                                                              ]
                                                              )
        tron.trx.sign_and_broadcast(approve['transaction'])
        txn = tron.transaction_builder.trigger_smart_contract(contract_address=tron.address.to_hex(contractaddress),
                                                              function_selector='Buy(address)',
                                                              fee_limit=50000000,
                                                              call_value=amount,
                                                              parameters=[
                                                                  {'type': 'address', 'value':publickey },
                                                              ]
                                                              )
        transaction=tron.trx.sign_and_broadcast(txn['transaction'])

        return transaction
    except:
        return False
def getEstimatedSellReceiveAmount(amount,contractaddress):
    txn = tron.transaction_builder.trigger_smart_contract(
        contract_address=tron.address.to_hex(contractaddress),
        function_selector='getEstimatedSellReceiveAmount(uint256)',
        fee_limit=90000,
        call_value=0,
        parameters=[
            {'type': 'uint256', 'value': amount}
        ]
    )
    value='{:.6f}'.format(int(txn["constant_result"][0], 16) / 10 ** 6)
    value=str(value[::-1])
    for _ in range(6):
        if _=="0":
            value=value.replace("0","",1)
        else:
            break
    return value[::-1]
def getEstimatedBuyReceiveAmount(amount,contractaddress,decimals):
    txn = tron.transaction_builder.trigger_smart_contract(
        contract_address=tron.address.to_hex(contractaddress),
        function_selector='getEstimatedBuyReceiveAmount(uint256)',
        fee_limit=90000,
        call_value=0,
        parameters=[
            {'type': 'uint256', 'value': amount}
        ]
    )
    value="{"+":.{}f".format(decimals)+"}"
    value = value.format(int(txn["constant_result"][0], 16) / 10 ** decimals)
    value = str(value[::-1])
    for _ in range(decimals):
        if _ == "0":
            value = value.replace("0", "", 1)
        else:
            break
    return value[::-1]
def CHECK_ACCOUNT_BALANCE(publickey):
        hex=tron.address.to_hex(publickey)
        payload = {"address":"{}".format(hex)}
        payload=json.dumps(payload)
        headers = {'content-type': 'application/json'}
        url = "https://api.trongrid.io/wallet/getaccount"
        RESPONSE_ACCOUNT_INFO = requests.request("POST", url, data=payload, headers=headers)
        RESPONSE_ACCOUNT_INFO=RESPONSE_ACCOUNT_INFO.json()
        if "balance" not in RESPONSE_ACCOUNT_INFO :
            TRON_BALANCE = 0
        else:
            TRON_BALANCE = RESPONSE_ACCOUNT_INFO["balance"]
            TRON_BALANCE = TRON_BALANCE / 10 ** 6
        return TRON_BALANCE
def index(TELEGRAM_MESSAGE):
    BOT_USERNAME = "@PriceCheckerTradingBot"
    global connection
    global cursor
    global CHAT_ID
    global USERNAME
    global fee
    global RIVAL_TELE_ID
    if "callback_query" in TELEGRAM_MESSAGE:
        message = TELEGRAM_MESSAGE["callback_query"]
        CHAT_ID = message["message"]["chat"]["id"]
        TYPE = message["message"]["chat"]["type"]
        messageid = message["message"]["message_id"]

    else:
        message = TELEGRAM_MESSAGE["message"]
        CHAT_ID = message["chat"]["id"]
        TYPE = message["chat"]["type"]
        messageid = message["message_id"]
    if "username" not in message["from"]:
        USERNAME = message["from"]["first_name"]
        REAL_USERNAME = "##EMPTY##"
    else:
        USERNAME = message["from"]["username"]
        REAL_USERNAME = USERNAME
    FIRST_NAME = message["from"]["first_name"]
    TELE_ID = message["from"]["id"]
    update_id = TELEGRAM_MESSAGE["update_id"]
    connection=CONNECTION()
    cursor=connection.cursor()
    last_id = READ()
    #### TELE_ID , USERNAME KEPT FOR FUTURE DEVELOPMENT
    if last_id<update_id:
        cursor.execute("UPDATE telegram SET update_id= %s  WHERE SrNo= %s ", (update_id, 1))
        connection.commit()
        UPDATE_INFO(TELE_ID, REAL_USERNAME, FIRST_NAME)
        if "callback_query" in TELEGRAM_MESSAGE:
            calltoken=TELEGRAM_MESSAGE["callback_query"]["data"]
            callback_query_id = TELEGRAM_MESSAGE["callback_query"]["id"]
            if "CANCELMESSAGE" in calltoken:
                caller_id=int(calltoken.replace("CANCELMESSAGE","") )
                if caller_id == TELE_ID:
                     requests.post(TELEGRAM_WEBSITE + "/deleteMessage?message_id={}&chat_id={}".format(int(messageid), CHAT_ID))
                else:
                    requests.post(TELEGRAM_WEBSITE + "/answerCallbackQuery", data={"callback_query_id": callback_query_id})
            elif "!" in calltoken: #REFRESH

                transactioncode=calltoken[1]
                TRANSACTION_TEXT="SELL👍" if transactioncode=="s" else "BUY👍"
                calltoken=calltoken.replace(transactioncode,"",1)
                contractaddresscode = calltoken.replace("!", "").split(";")[0]
                for x in UNIFI_DATA_OFFLINE:
                    if (x["contractaddresscode"]==contractaddresscode):
                        contractaddress=x["contractAddress"]
                        decimals=x["decimals"] if transactioncode=="s" else 6
                        decimals_token=x["decimals"]
                name = calltoken.replace("!", "",1).split(";")[1]
                amount=int(calltoken.replace("!", "",1).split(";")[2])
                caller_id=int(calltoken.replace("!", "",1).split(";")[3])
                amount_display=str(amount)
                if len(amount_display)>=decimals:
                    amount_display=amount_display[:-1*decimals]+"."+amount_display[-1*decimals:]
                elif amount/10**decimals <1:
                    amount_display = "0."+"0"*(decimals-len(amount_display))+amount_display
                amount_display="0"+amount_display if amount_display[0]=="." else amount_display
                ACCOUNT=ACCOUNT_PRESENT(TELE_ID)
                tron.private_key=ACCOUNT[0][1]
                tron.default_address = ACCOUNT[0][0]
                recieving_trx=getEstimatedSellReceiveAmount(amount,contractaddress) if transactioncode=="s" else getEstimatedBuyReceiveAmount(amount,contractaddress,decimals_token)
                TRANSACTION_DIRECTION_TEXT="\nSell " if transactioncode=="s" else "\nBuy "
                index_username=message["message"]["text"].index(TRANSACTION_DIRECTION_TEXT)
                if index_username==1:
                    USERNAME_INSERT=TRANSACTION_DIRECTION_TEXT
                else:
                    USERNAME_INSERT=message["message"]["text"][0:index_username]
                if transactioncode=="s":
                    REFRESH_TEXT = "<a href=\"tg://user?id={}\">{}</a>{} <code>{}</code> {} for <code>{}</code> TRX . ".format(caller_id,USERNAME_INSERT,TRANSACTION_DIRECTION_TEXT,amount_display,name, recieving_trx)
                else:
                    REFRESH_TEXT = "<a href=\"tg://user?id={}\">{}</a>{} <code>{}</code> {} with <code>{}</code> TRX . ".format(caller_id,USERNAME_INSERT,TRANSACTION_DIRECTION_TEXT,recieving_trx,name, amount_display)
                a=requests.post(
                            TELEGRAM_WEBSITE + "/editMessageText",
                            data={"text": REFRESH_TEXT, "parse_mode": "HTML","message_id":int(messageid),
                                  "chat_id": "{}".format(CHAT_ID),
                                  "reply_markup": json.dumps(
                                      {"inline_keyboard": [[{"text": "{}".format(TRANSACTION_TEXT),
                                                                         "callback_data": "${}{};{};{}".format(transactioncode,TELE_ID,contractaddresscode,amount)},{"text": "{}".format("CANCEL❌"),
                                                                         "callback_data": "{}{}".format("CANCELMESSAGE",TELE_ID)},{"text": "{}".format("REFRESH🔄"),
                                                                         "callback_data": "{}{}{};{};{};{}".format("!",transactioncode,contractaddresscode,name,amount,TELE_ID)}]]})})

                requests.post(
                    TELEGRAM_WEBSITE + "/answerCallbackQuery", data={"callback_query_id": callback_query_id})

            elif "$" in calltoken:
                transactioncode = calltoken[1]
                calltoken = calltoken.replace(transactioncode, "", 1)
                calltoken=calltoken.replace("$", "",1)
                contractaddresscode = calltoken.split(";")[1]
                for x in UNIFI_DATA_OFFLINE:
                    if (x["contractaddresscode"] == contractaddresscode):
                        contractaddress = x["contractAddress"]
                        decimals = x["decimals"]
                caller_id=int(calltoken.split(";")[0])
                amount=int(calltoken.split(";")[2])
                if TELE_ID==caller_id:
                    ACCOUNT=ACCOUNT_PRESENT(TELE_ID)
                    if ACCOUNT is False:
                        MAKE_ACCOUNT(TELE_ID,REAL_USERNAME,FIRST_NAME)
                        INSUFFICIENT_FUNDS(TELE_ID)

                    elif CHECK_ACCOUNT_BALANCE(ACCOUNT[0][0])<fee+0.1:
                        INSUFFICIENT_FUNDS(TELE_ID)
                    else:
                        tron.private_key = ACCOUNT[0][1]
                        tron.default_address = ACCOUNT[0][0]
                        for data_iterations in UNIFI_DATA:
                            if contractaddress==data_iterations["contractAddress"]:
                                tokenaddress=data_iterations["tokenAddress"]
                        status=SEND_TOKEN(contractaddress,amount,tokenaddress) if transactioncode=="s" else BUY_TOKEN(contractaddress,amount,tokenaddress,ACCOUNT[0][0])
                        if status is False:
                            TRANSACTION_FAILED_TEXT= "Transaction failed.Please check if you have provided correct amount ."
                            requests.post(
                                TELEGRAM_WEBSITE + "/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(TELE_ID,
                                                                                                            TRANSACTION_FAILED_TEXT))
                        else:
                            TRANSACTION_TRACKER_TEXT=SANITISE_TEXT("Transaction sent. Track it here ➟") +" <a href=\"{}\">{}</a>".format(SANITISE_TEXT("https://tronscan.org/#/transaction/"+status["txid"]),status["txid"])
                            requests.post(
                                TELEGRAM_WEBSITE + "/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(TELE_ID,
                                                                                                            TRANSACTION_TRACKER_TEXT))
                    requests.post(
                        TELEGRAM_WEBSITE + "/deleteMessage?message_id={}&chat_id={}".format(int(messageid), CHAT_ID))

            # elif "/redeem" in calltoken:
            #     UNIFI_WEB_REDEEM = "https://api.sesameseed.org/votes/unifi/getPrice"
            #     UNIFI_REDEEM_DATA = requests.get(UNIFI_WEB_REDEEM).json()
            #     REDEEM_PRICE = UNIFI_REDEEM_DATA["trx"]["VirtualPrice"]
            #     PAGE_REFERENCE = "<a href=\"{}\">{}</a>".format("https://tron.unifiprotocol.com/up", "Redeem here")
            #     REDEEM_TEXT = " 🆙 Redeem= <code>{}</code> TRX\n".format(INSERT_COMMAS(float(REDEEM_PRICE))) + PAGE_REFERENCE
            #     requests.post(
            #         TELEGRAM_WEBSITE + "/editMessageText",
            #                 data={"text": REDEEM_TEXT, "parse_mode": "HTML",
            #                       "chat_id": "{}".format(CHAT_ID),"message_id":int(messageid),
            #               "reply_markup": json.dumps(
            #                   {"inline_keyboard": [[{"text": "{}".format("REFRESH 🔄"),
            #                                          "callback_data": "{}".format("/redeem")}, ]]})})
            #     requests.post(
            #         TELEGRAM_WEBSITE + "/answerCallbackQuery", data={"callback_query_id": callback_query_id})
            else:
                for _ in UNIFI_DATA:
                    if (_["name"].casefold() == calltoken.casefold()) :
                        calltoken=calltoken+"TRX"
                    if (_["name"].casefold() in calltoken.casefold()) and (_["againstTokenAddress"].casefold() in calltoken.casefold()):
                        DATA_TEXT = SEND_DATA(_)
                        requests.post(
                            TELEGRAM_WEBSITE + "/editMessageText",
                            data={"text": DATA_TEXT, "parse_mode": "HTML",
                                  "chat_id": "{}".format(CHAT_ID),"message_id":int(messageid),
                                  "reply_markup": json.dumps(
                                      {"inline_keyboard": [[{"text": "{}".format("REFRESH 🔄"),
                                                             "callback_data": "{}".format(_["name"]+_["againstTokenAddress"])}, ]]})})
                        requests.post(
                            TELEGRAM_WEBSITE + "/answerCallbackQuery", data={"callback_query_id": callback_query_id})
                        break

        elif "text" not in message:
            pass
        elif USERNAME :
            TEXT = message["text"]
            TEXT = TEXT.replace(BOT_USERNAME, '')
            if TEXT.replace(" ","")=="/commands" :
                BUY_SELL_COMMANDS_TEXT="Use /sell <amount> <token>\n📜Example: /sell 10 SEED\n\nUse /buy <token> with <amount> TRX\n📜Example: /buy SEED with 10 TRX"
                TOKEN_PAIR_COMMAND_TEXT="\n\nUse /p {} to retrieve price/volume/liquidity data for any token pair.\n📜Example: /p SEEDUP".format(SANITISE_TEXT("<token pair>"))
                ABOUT_TEXT=SANITISE_TEXT("Use /p <token name> to get token info on Unifi.\n📜Example: /p SEED.\n\nUse /account to get your account details (DM bot).\n\n💸 TRADING FUNCTIONS:\n\nUse /sell <amount> <token>\n📜Example: /sell 10 SEED\n\nUse /buy <token> with <amount> TRX\n📜Example: /buy SEED with 10 TRX\n\n")+"Developed by-\n<a href=\"tg://user?id=1234\">@Raj</a>"
                requests.post(TELEGRAM_WEBSITE + "/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(CHAT_ID, ABOUT_TEXT))
            elif TEXT.replace(" ","")[0:2]=="/p":
                TEXT = TEXT.replace(" ", "")
                calltoken=TEXT.replace("/p","").casefold()
                calltoken="UPtrx" if calltoken=="up" else calltoken
                for _ in UNIFI_DATA:
                    if (_["name"].casefold() == calltoken.casefold()) :
                        calltoken=calltoken+"TRX"
                    if (_["name"].casefold() in calltoken.casefold()) and (_["againstTokenAddress"].casefold() in calltoken.casefold()):
                        DATA_TEXT=SEND_DATA(_)
                        requests.post(
                            TELEGRAM_WEBSITE + "/sendmessage",
                            data={"text": DATA_TEXT, "parse_mode": "HTML",
                                  "chat_id": "{}".format(CHAT_ID),
                                  "reply_markup": json.dumps(
                                      {"inline_keyboard": [[{"text": "{}".format("REFRESH 🔄"),
                                                             "callback_data": "{}".format(_["name"]+_["againstTokenAddress"])}, ]]})})
                        break
            elif TEXT.replace(" ","")=="/redeem":
                UNIFI_WEB_REDEEM="https://api.sesameseed.org/votes/unifi/getPrice"
                UNIFI_REDEEM_DATA=requests.get(UNIFI_WEB_REDEEM).json()
                REDEEM_PRICE=UNIFI_REDEEM_DATA["trx"]["VirtualPrice"]
                PAGE_REFERENCE = "<a href=\"{}\">{}</a>".format("https://tron.unifiprotocol.com/up","Redeem here")
                REDEEM_TEXT=" 🆙 Redeem= <code>{}</code> TRX\n".format(INSERT_COMMAS(float(REDEEM_PRICE)))+PAGE_REFERENCE
                requests.post(
                    TELEGRAM_WEBSITE + "/sendmessage",
                    data={"text": REDEEM_TEXT, "parse_mode": "HTML",
                          "chat_id": "{}".format(CHAT_ID),
                          "reply_markup": json.dumps(
                              {"inline_keyboard": [[{"text": "{}".format("REFRESH 🔄"),
                                                     "callback_data": "{}".format("/redeem")}, ]]})})
            elif TEXT=="/links":
                PAGE_REFERENCE = "<a href=\"{}\">{}</a>\n<a href=\"{}\">{}</a>".format("https://unifiprotocol.com/","Visit Unifi website","https://sesameseed.org","Visit Sesameseed website")
                requests.post(TELEGRAM_WEBSITE + "/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(CHAT_ID, PAGE_REFERENCE))
            elif TEXT[0:6].casefold() == "/sell " or (TEXT[0:5].casefold() == "/buy " and TEXT.split(" ")[2]=="with" and TEXT.split(" ")[4].casefold()=="trx" and len(TEXT.split(" "))==5):
                transactioncode="s" if TEXT[0:6].casefold() == "/sell " else "b"
                TEXT=TEXT.replace("/sell ","",1) if transactioncode=="s" else TEXT.replace("/buy ","",1)
                if transactioncode == "b":
                    tokenname=TEXT.split(" ")[0]
                    TEXT=TEXT.replace(tokenname,"",1).replace(" ","",1).replace("with ","")
                amount=""
                ACCOUNT=ACCOUNT_PRESENT(TELE_ID)
                if ACCOUNT is not False:
                            tron.private_key = ACCOUNT[0][1]
                            tron.default_address = ACCOUNT[0][0]
                            decimal_point=False
                            decimal_mark = True
                            for _ in TEXT:
                                if (_.isdigit() is True or( _=="."and decimal_point is False)) :
                                    if _==".":
                                        decimal_point=True
                                    amount=amount+_
                            amount_display=amount
                            if transactioncode=="s":
                                tokenname=TEXT.replace(str(amount),"",1).replace(" ","")
                            count=0
                            for x in UNIFI_DATA_OFFLINE:
                                if x["name"].casefold() == tokenname.casefold():
                                    contractaddress=x["contractAddress"]
                                    decimals=x["decimals"] if transactioncode=="s" else 6
                                    decimals_token=x["decimals"]
                                    if "." in amount:
                                        decimal_places = amount.split(".")[1]
                                        if len(decimal_places)>decimals:
                                            SEND_WRONG_DECIMALS(TELE_ID,USERNAME,decimals)
                                            decimal_mark=False
                                            break
                                        else:
                                            amount=amount.replace(".","")+"0"*(decimals-len(decimal_places))
                                    else:
                                        amount=int(amount)*10**decimals
                                    amount=int(amount)
                                    break
                                count += 1
                            if count!=len(UNIFI_DATA_OFFLINE) and decimal_mark is True:
                                recieving_trx=getEstimatedSellReceiveAmount(amount,contractaddress) if transactioncode=="s" else getEstimatedBuyReceiveAmount(amount,contractaddress,decimals_token)
                                TRANSACTION_DIRECTION_TEXT = "\nSell " if transactioncode == "s" else "\nBuy "
                                if transactioncode=="s":
                                        CONFIRM_TEXT = "<a href=\"tg://user?id={}\">@{}</a>{} <code>{}</code> {} for <code>{}</code> TRX . ".format(TELE_ID,SANITISE_TEXT(USERNAME),TRANSACTION_DIRECTION_TEXT,amount_display,x["name"],recieving_trx )
                                else:
                                        CONFIRM_TEXT = "<a href=\"tg://user?id={}\">@{}</a>{} <code>{}</code> {} with <code>{}</code> TRX . ".format(TELE_ID,SANITISE_TEXT(USERNAME),TRANSACTION_DIRECTION_TEXT,recieving_trx,x["name"],amount_display )
                                TRANACTION_TEXT="SELL👍" if transactioncode=="s" else "BUY👍"
                                requests.post(
                                            TELEGRAM_WEBSITE + "/sendmessage",
                                            data={"text": CONFIRM_TEXT, "parse_mode": "HTML",
                                                  "chat_id": "{}".format(CHAT_ID),
                                                  "reply_markup": json.dumps(
                                                      {"inline_keyboard": [[{"text": "{}".format(TRANACTION_TEXT),
                                                                             "callback_data": "${}{};{};{}".format(transactioncode,TELE_ID,x["contractaddresscode"],amount)},{"text": "{}".format("CANCEL❌"),
                                                                             "callback_data": "{}{}".format("CANCELMESSAGE",TELE_ID)},{"text": "{}".format("REFRESH🔄"),
                                                                             "callback_data": "{}{}{};{};{};{}".format("!",transactioncode,x["contractaddresscode"],x["name"],amount,TELE_ID)}]]})})

                            elif decimal_mark is True:
                                SEND_TOKEN_DOESNOT_EXIST(TELE_ID,USERNAME)
                            else:
                                pass


                else:
                    MAKE_ACCOUNT(TELE_ID,REAL_USERNAME,FIRST_NAME)
                    INSUFFICIENT_FUNDS(TELE_ID)
            elif TEXT=="/account" :
                    ACCOUNT=ACCOUNT_PRESENT(TELE_ID)
                    if ACCOUNT==False:
                        MAKE_ACCOUNT(TELE_ID,REAL_USERNAME,FIRST_NAME)
                        ACCOUNT = ACCOUNT_PRESENT(TELE_ID)
                        PUBLIC_KEY=ACCOUNT[0][0]
                        PRIVATE_KEY=ACCOUNT[0][1]
                        SEND_ACCOUNT_DETAILS(TELE_ID,PUBLIC_KEY,PRIVATE_KEY)
                    else:
                        PUBLIC_KEY= ACCOUNT[0][0]
                        PRIVATE_KEY = ACCOUNT[0][1]
                        SEND_ACCOUNT_DETAILS(TELE_ID,PUBLIC_KEY,PRIVATE_KEY)
            elif TEXT=="/about"or TEXT.replace(" ","")=="/start":
                ABOUT_UNIFI_TEXT="🤖 PriceCheckerTrading bot is a multifunctional bot that is used to check price and trade using  UNIFI protocol to serve the amazing people of unifi.\nTap /commands to know how to issue commands to me."
                requests.post(TELEGRAM_WEBSITE + "/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(CHAT_ID, SANITISE_TEXT(ABOUT_UNIFI_TEXT)))
            elif "/send" in TEXT[0:5]:
                TEXT = TEXT.replace(" ", "")
                TEXT = TEXT.replace(BOT_USERNAME, "")
                ADDRESS = ACCOUNT_PRESENT(TELE_ID)
                CONFIRMATION = {"result": False}
                UKNOWN_SYNTAX_SEND = ""
                if ADDRESS == False:
                    MAKE_ACCOUNT(TELE_ID, REAL_USERNAME, FIRST_NAME)
                    INSUFFICIENT_FUNDS(TELE_ID)
                else:
                    if "reply_to_message" in message:
                        RIVAL_USERNAME = message["reply_to_message"]["from"]["username"] if "username" not in \
                                                                                            message["reply_to_message"][
                                                                                                "from"]["username"] \
                            else message["reply_to_message"]["from"]["first_name"]
                        TIP_AMOUNT = float(TEXT.replace("/send", ""))
                        if (TIP_AMOUNT * 1000000) % 1000000 != 0:
                            DECIMAL_TOO_LESS_TEXT = "Minimum tron that can be sent is 0.000001 TRX"
                            requests.post(
                                TELEGRAM_WEBSITE + "/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(CHAT_ID,
                                                                                                            DECIMAL_TOO_LESS_TEXT))
                            precision = "fail"
                        else:
                            precision = "pass"
                        RIVAL_TELE_ID = message["reply_to_message"]["from"]["id"]
                        RIVAL_ADDRESS = ACCOUNT_PRESENT(RIVAL_TELE_ID)
                        if RIVAL_ADDRESS == False and precision != "fail":
                            if RIVAL_TELE_ID == TELE_ID:
                                pass
                            elif "username" not in message["reply_to_message"]["from"]["username"]:
                                RIVAL_FIRST_NAME = message["reply_to_message"]["from"]["first_name"]
                                MAKE_ACCOUNT(RIVAL_TELE_ID, "##EMPTY##", RIVAL_FIRST_NAME)
                                RIVAL_ACCOUNT = ACCOUNT_PRESENT(RIVAL_TELE_ID)
                                CONFIRMATION = SEND_TRANSACTION(ADDRESS[0][1], ADDRESS[0][0], RIVAL_ACCOUNT[0][0],
                                                                TIP_AMOUNT)
                            else:
                                RIVAL_FIRST_NAME = message["reply_to_message"]["from"]["first_name"]
                                MAKE_ACCOUNT(RIVAL_TELE_ID, RIVAL_USERNAME, RIVAL_FIRST_NAME)
                                RIVAL_ACCOUNT = ACCOUNT_PRESENT(RIVAL_TELE_ID)
                                CONFIRMATION = SEND_TRANSACTION(ADDRESS[0][1], ADDRESS[0][0], RIVAL_ACCOUNT[0][0],
                                                                TIP_AMOUNT)
                        else:
                            CONFIRMATION = SEND_TRANSACTION(ADDRESS[0][1], ADDRESS[0][0], RIVAL_ADDRESS[0][0],
                                                            TIP_AMOUNT)
                if "result" in CONFIRMATION and CONFIRMATION["result"] == True:
                    SEND_TRANSACTION_DETAILS(USERNAME, RIVAL_USERNAME, TELE_ID, RIVAL_TELE_ID, TIP_AMOUNT)
                elif UKNOWN_SYNTAX_SEND != "":
                    SEND_FAILED_TRANSACTION_DETAILS(USERNAME, RIVAL_USERNAME, TELE_ID)


        ###FUTURE DEVELOPMENT###
        # elif TEXT=="/news":
        #     chrome_options = webdriver.ChromeOptions()
        #     chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        #     chrome_options.add_argument("--headless")
        #     chrome_options.add_argument("--disable-dev-shm-usage")
        #     chrome_options.add_argument("--no-sandbox")
        #     driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),
        #                               chrome_options=chrome_options)
        #     driver.get("https://tron.unifiprotocol.com/liquidity/pool")
        #     sleep(1)
        #     def SCROLL_SEND(count):
        #         count+=1
        #         driver.save_screenshot('twitterss{}.png'.format(count))
        #         multipart_form_data = {
        #         "photo": open("twitterss{}.png".format(count), 'rb'),
        #         }
        #         requests.post(TELEGRAM_WEBSITE + "/sendPhoto",data={"chat_id":TELE_ID}, files=multipart_form_data)
        #         return count
        #     count=0
        #     ActionChains(driver).send_keys(Keys.TAB * 8).perform()
        #     ActionChains(driver).send_keys(Keys.DOWN * 13).perform()
        #     count=SCROLL_SEND(count)
        #     ActionChains(driver).send_keys(Keys.PAGE_DOWN * 1).perform()
        #     ActionChains(driver).send_keys(Keys.DOWN * 23).perform()
        #     # ActionChains(driver).send_keys(Keys.END).perform()
        #     # ActionChains(driver).send_keys(Keys.UP * 4).perform()
        #     SCROLL_SEND(count)

@app.route('/',methods=['POST','GET'])
def main():
                  try:
                        TELEGRAM_MESSAGE=request.json
                        p = multiprocessing.Process(target=index, name="Index", args=(TELEGRAM_MESSAGE,))
                        p.start()
                        p.join(25)
                        if p.is_alive():
                            p.terminate()
                            try:
                                ERROR_TEXT = "ERROR:Request could not be processed. This could be because of heavy traffic or a bad connection. Please try again later. "
                                if "callback_query" in TELEGRAM_MESSAGE:
                                    message = TELEGRAM_MESSAGE["callback_query"]
                                    CHAT_ID = message["message"]["chat"]["id"]
                                else:
                                    message = TELEGRAM_MESSAGE["message"]
                                    CHAT_ID = message["chat"]["id"]
                                TELE_ID = message["from"]["id"]
                                requests.post(TELEGRAM_WEBSITE + "/sendmessage?chat_id={}&text={}".format(CHAT_ID, ERROR_TEXT))
                            finally:
                                return Response("Ok",status=200)
                        else:
                            return Response("Ok",status=200)
                  except:
                      return Response("Ok", status=200)
                  finally:
                        pass
if __name__=="__main__":
     app.run(debug=False)


