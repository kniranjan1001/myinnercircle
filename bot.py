import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from datetime import datetime
from typing import Dict, List
from decimal import Decimal

# Logging configuration
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID'))  # Your Telegram user ID

RECORD = {
    'Bob': 'Whale', 
    'Alice': 'High invest', 
    'MeganSmith': 'High invest', 
    'Wil': 'High invest', 
    'Ram': 'Best 4 Me', 
    'Shyam': 'Best 4 Me', 
    'Lakshman': 'Best 4 Me', 
    'Arjun': 'Best 4 Me', 
    'Krishna': 'Best 4 Me', 
    'Radha': 'Best 4 Me', 
    'AlexBrown': 'Best 4 Me', 
    'CharlieDavis': 'Best 4 Me', 
    'Ryan': 'Best 4 Me', 
    'Oliver': 'Best 4 Me', 
    'Sophia': 'Best 4 Me', 
    'Emma': 'Best 4 Me', 
    'Dia': 'Best 4 Me', 
    'Eth': 'Best 4 Me', 
    'Ivy': 'Best 4 Me', 
    "Leo": "Best 4 Me",
    'Sita': 'Lowprofit', 
    'James': 'Lowprofit', 
    'Charlotte': 'Lowprofit', 
    'Liam': 'Lowprofit', 
    'Nat': 'Lowprofit', 
    'Hanuman': 'desprate', 
    'Sugriv': 'desprate', 
    'Taylor': 'desprate', 
    'Amelia': 'desprate', 
    'Benjamin': 'desprate', 
    'Fio': 'desprate', 
    'Cha': 'Whale', 
    'Vibhishan': 'Risk Checker', 
    'Lorence': 'Risk Checker', 
    'Mia': 'Risk Checker', 
    'Kar': 'Risk Checker', 
    'Oli': 'Risk Checker', 
    'Ali': 'Whale', 
    'Geo': 'Whale', 
    'Han': 'Whale', 
    'Jac': 'Whale', 
    'Leo': 'Whale', 
    "Max": "Whale",
    "Ben": "Whale",
    'Mol': 'OnlyProfit', 
    'Pau': 'OnlyProfit',
    "Aya": "OnlyProfit",
    "Tom": "Small Invest",
    "Sam": "Small Invest",
    "Joe": "Small but loss",
    "Raj": "Small Invest",
    "Kay": "Small Invest",
    "Tim": "Small Invest",
    "Zoe": "Small Invest",
    "BetWithSizeYt":"Youtuber",
    "raju":"OnlyProfit",
    "SkyE" : "OnlyProfit",
    "Sto" : "Lowprofit",
    "JadeP" : "Small Invest",
    "Vivid" : "OnlyProfit",
    "Solar" : "Desperate",
    "Velv" : "Small Invest",
    "Echo" : "Desperate",
    "Crimso" : "Whale",
    "Emeral" : "Whale",
    "AmberD" : "Whale",
    "Glaze" : "He Knows",
    "AuraSt" : "OnlyProfit",
    "Brigh" : "OnlyProfit",
    "NMhS": "Small Invest",
    "ZxQJ": "He Knows",
    "kYJf": "OnlyProfit",
    "hx2X": "Risk Checker",
    "qk2B": "Whale",
    "qT6d": "Whale",
    "Gj1N": "Risk Checker",
    "d6f9": "Whale",
    "w6eM": "He Knows",
    "r8Q7": "He Knows",
    "u2K8": "He Knows",
    "iB8z": "He Knows",
    "Yt2w": "Whale",
    "Z1K3": "He Knows"
}


# wallet address
WALLET_NAMES = {
    "DQvkTJRCb7kJE1Aw1BCiXekgBymhVW5ZK9p6Mk678Ujd":"Pro",
    "GghbeTXXvAjrsRqTe5maywtBT1XPRnR45R8VxAK2YtcG": "Bob",
    "EbNr5s54pCUFzEyBDjJWwqYQc7R5E8udmPEpDLwpbjKq": "Alice",
    "8gx4VKzNVjenF2t7wikTHjwWEUt6mjJT4xmaSZKuCzCG": "Ram",
    "A6EcV1ZhbGwNp6FYEXw4TaTyfVd8ASNGC1xiXL2Dz5zF": "Shyam",
    "AgfjAqBTKMGHAr1ZxjK8NWyMMp2EyyoS3wkYPYTUBjT5": "Lakshman",
    "6ocX9nqdTLjm99HXXFVfucshcvWVo7h8BFQDwk9R12xu": "Krishna",
    "6ESwF2ouiH7Vz2uRkzBXftY6Ko9jdqvebMvTFUG2Bthy": "Radha",
    "Engi2TDft8C6R33RMn9YpBeNqxzqpyzKiXQBAsQZPZpw": "Sita",
    "3e4VMNkFwT8t6vVVGLHYWYhhUGQtcACR1F1NrWMwY8eF": "Hanuman",
    "BtxnBqqgCnDQfXLJeijdJm2GdNz3iFEqKAkMw3SuJtNG": "Sugriv",
    "CYEtWTAX4W25MiSQZBwKeH1NLEnEUnzRAbNbNzkdnzVt": "Vibhishan",
    "5XboKCwuw8diGX1jHZnpx2hn319TwbmmxGtQVbHBCv56": "MeganSmith",
    "GvD5HiZuNcZvny8zhUXStLwEiWmA2spbikj22wEN5LYR": "AlexBrown",
    "Egm9KLWURmXjDEitMVucUnHCVex5NeZ5M3gT4CCb2Q1V": "CharlieDavis",
    "BQ39hZo1eZsnaxGSUdk7MFnJoVsJd1ifCNEUqzY2aSjs": "Taylor",
    "FxMW8ZfcDi4Wiqr6G2SuARGkS5ZxvMhvRzjRgc5G2UDM":"Lorence",
    "AzSEDJRzm6b2VBcc2dJYuZxGRRehgXssFEuYsidEULsP":"Ryan",
    "3jyZhrBjD27vWEByutBoZaYmBemM5J7ikkYod6GTsXkM": "William",
    "HdxkiXqeN6qpK2YbG51W23QSWj3Yygc1eEk2zwmKJExp": "Oliver",
    "7RX26gmCt74rnGFeuBVrUBUFSDn6mNnmUJfZStqaR8Pq": "Sophia",
    "6WqWYTRh28mJEeHQnECfzhQvhF9XskoPU5fqsA49wkMV": "Emma",
    "E7Dq1L6zgDi5sJjqekeUzwC1TXRj8NUuk9QNdhUB3LNt": "James",
    "BF9WdfRe5iGsPXVAbaX5uDykb53iQUVkuJ1dtX2V9vHk": "Charlotte",
    "j1oeQoPeuEDmjvyMwBmCWexzCQup77kbKKxV59CnYbd": "Liam",
    "G2upvNYaDkzvXWy7s6zZZhHXj4gtJsfYRHCXY89W2wuv": "Amelia",
    "2s1xW3rvrtQ3Ez4Z3iPnzUDMPGfWMFkK2Cs2urgGxrCy": "Benjamin",
    "DeCgQaBCSpHUoX7ng3MGYiPxdcfgU5HyB38cabVwF57o": "Mia",
    "CUqjTmYihCAMuwmqNvb2jKBC3bUR5J2Ek3Xw1qF5Gsb3": "Ali",
    "3cMMeEEAMdN2JGDDSSrPULjZo3VU63qqPMmtr9aJYUTg": "Bell",
    "6f26GAALkqNXL5HG89KfRr7YpR1ToLanecSwgV4YMaUa": "Cha",
    "8HxD27P2ptQCExud5jrvDzsgMxBRugKLMMmPBzXJHLuy": "Dia",
    "HJ8hsEsvXoK7KFNAS2Wb5698Xo5KB2VcU3sot479gnvZ": "Eth",
    "2MFHzt6QrzrEUJimf4K5X1Net6x9x4qjpEVpMb9zRNon": "Fio",
    "BZe5jVcBq1hdhTkqSvif8asHdmsvtduhAzU1wnhJApRY": "Geo",
    "3jyZhrBjD27vWEByutBoZaYmBemM5J7ikkYod6GTsXkM": "Wil",
    "Aq43gJ4vQjtbjzzZ3TFCEmXSeX1YJs94gprhTv4qfrT": "Han",
    "DQmMnakiKr1YNE2gcpggLCzBrauBwFbQkAaao2FTbjgp": "Ivy",
    "4uRzzVH85U8ZSXbNoHLg1KgJEor2ZUUw8Dbezew3JMv1": "Jac",
    "4632BMWY69AkVHxN1XLKVuLrednYiLccuMeoXnQBMA7Z": "Kar",
    "7awxPFThpN2uLuJf4VeDiVZVL34gxMWqDAqYaABn3Nnh": "Leo",
    "DfMxre4cKmvogbLrPigxmibVTTQDuzjdXojWzjCXXhzj": "Mol",
    "GXMZn221jxKTX2aYhNxsoctQZVVYTLo2mYoq2hC5edZv": "Nat",
    "F7RV6aBWfniixoFkQNWmRwznDj2vae2XbusFfvMMjtbE": "Oli",
    "CrkK539YNKbsCRWYnH5oEs8Nnn66BjgkdvFEZ8mQ58gk": "Pau",
    "5orb9NyiJCmacGCGQyVesuASWUpXGiD3hXpY2iXP18cW": "Tom",
    "DzfNo1qoGx4rYXbwS273tmPaxZMibr8iSrdw4Mvnhtv4": "Sam",
    "xQHjfWLhzwG8HPgfLbJRom1RDfWMjm3WZyaiWc5KMHr": "Joe",
    "215nhcAHjQQGgwpQSJQ7zR26etbjjtVdW74NLzwEgQjP": "Max",
    "FbVbRbGqLk7DtprRHV1THa26ynoRZjUC6RuAxT9yaohM": "Ben",
    "S2JsYadaV5iB4A86wXhvArs8jb2kSbWA9pCmz7ALGQW": "Leo",
    "4dCezdQ36jM9QRkysytrWabqV27hcNkrdg92bdDbht9o": "Raj",
    "7cZWHHHjkujZ47Hn6JmT3W92rUXJGify4ezcBu4ExFdd": "Aya",
    "j1oeQoPeuEDmjvyMwBmCWexzCQup77kbKKxV59CnYbd": "Kay",
    "GLvCLzzEq3mMTrVWXuqm1nNRTQq6dH8DNd4ZHq7Sik3o": "Tim",
    "6sBVDn72viydq292Zdx2xQCCcUsFfHJ6ie98fjTGXwjW": "Zoe",
    "C8WtJP4YveQbza5k1otS7BNFQ6My4pjVwecApCEQCNQi": "Anex",
    "HyfkumvdB4AwtxVv5aNEDvB9SFMGxE1BCfTANvxCZMS7": "lopb",
    "DQvkTJRCb7kJE1Aw1BCiXekgBymhVW5ZK9p6Mk678Ujd": "Even",
    "2k6YMgPtBcpJ2gM8JuS84EJbdSHatCGzHj9WisjPz4c1": "Peon",
    "7wiqcDbgtBjQcgtVSDArDbhbWX1RXrnArQvekncRCNve": "Maxi",
    "GdG2anTVwLdDtM9XEKWUeuLy1mMGknJPzcqqW1qg7xrH": "Olaf",
    "HfDEtudyCwJTFaBQbJXqonFk6XfBUN8q9B9b7ddT9w6N": "Zen",
    "DPJQ3TCMS3Zg25dQ23ttgzKifxjs4NU6gM1NcFCVnkEt": "Ray",
    "AAhnidQyZbh2ej1Ubqc3DAP7oKM72akPzxtYpaZpUe8r":"BWithS",
    "5vMYfZJUsZd1Raj2fA76rGjEkdj3f8sv47GAsrkYkyqd":"raju",
    "A6xcYiqjchhd6VsFseznKhJ6gMufPWWrzkQj4rEzaa7E" : "SkyE",
    "BiJRfySs3L5tSWWmF93iMiJTyNvxmTU2U9Z5SHcSUJ2L" : "Sto",
    "DHN3s48zqhKBUP641dcPHP2h79ehtTwgqYf25NDeD4Br" : "JadeP",
    "9XvBYSKetT98zByzcDcm4qscZ1fTaogwdaTEnLbADZHG" : "Vivid",
    "3zmXMdcJBpU2tESBuE41AUc8gpTcSYa9J76Lmxdnwtrw" : "Solar",
    "CeoexdLDkYm7YnSSNUBbr9jdW2rwk583UgLzb8ScWAzP" : "Velv",
    "BYmsf5FcgDLWWHvSwxTcuuEpezyMATRZcXdoEb3h4dCE" : "Echo",
    "AvMG3ZxJYmKph6TW6XHptmmRTdKHCDGdJuMEAcyxAybJ" : "Crimso",
    "Di5dhYckFTKrSEnwtRAYi4yQfneQV7ca3TvWMKJuNfVd" : "Emeral",
    "DChxWPbRoLD6KM69vtsDjjRNPtWfo2nmGaGCh3Pv86h3" : "AmberD",
    "52kPsnhTpjHZucGUQy4YDm8g9ykXPMC47iNVSVRscikb" : "Glaze",
    "24uaZqjK16p9QA3Bs43GvXKFhb6GZdkRAdZVuLKttMLm" : "AuraSt",
    "DsrBGtyBsW15CfSAfWa4AKZ4rvFDPHSzJEbDeL8ymQMB" : "Brigh",
    "CPep14XgaDDNRMnP8ZjHVkvkhZPasRNYFEtDHvDpvnjR": "NMhS",
    "AarBPxKrHNfmkLvpY4r9J3ig8RqNXza7h4t9WTdFFS9Y": "ZxQJ",
    "E2RURCtEr75E53c793HXdmos8dU5Yy9mNAEBMHogWjFb": "kYJf",
    "47unSLWuZAosMnE9By9zmmrbDzYHqjfgPzPErTXqBDth": "hx2X",
    "CYBkqMfdNGeJYc2k3EbHGmBvqAvB5GUMgG6xSZSqmp5u": "qk2B",
    "AxBdvyt94ttxAfvr1d1zcCVevwaDH9QUeonDmcMiprZ7": "qT6d",
    "CnXyVN5j6Z4t67uwFVLG7fnxy8ACR4AoxxfgtcoBxsBn": "Gj1N",
    "DdTzGZke6CqtD6mnmEmNZiMxFFDEb3eizTYjB2pNMQAk": "d6f9",
    "An7UQr7K4KDQJkADoHxyqKqUjUN8yDPJRzpj4MLG4vWU": "w6eM",
    "2VUcurnU8tYEb7ehZKkRqYVpbXf7pBZpnMnPMFN7oCh2": "r8Q7",
    "5mJqiSaowzGHfFjVNF5nU6JhXjYww9VEK9Zwpc4j4Wa2": "u2K8",
    "6ywypvibd7ZhLdJXHxPi4PAY6Mi4yCk66vVgDFmyXcud": "iB8z",
    "578ZFJoH75jkPCVupRvwZAzbVHVMbKL4P7MKuG9iWEtH": "Yt2w",
    "EPNRJQpMPLKDP4oGoTeBJy8uAc4Z8XoKqbNTnQ3dzNVT": "Z1K3"
    
}


# Define categories and wallet IDs
CATEGORIES = {
    "High invest": ["GghbeTXXvAjrsRqTe5maywtBT1XPRnR45R8VxAK2YtcG","EbNr5s54pCUFzEyBDjJWwqYQc7R5E8udmPEpDLwpbjKq","5XboKCwuw8diGX1jHZnpx2hn319TwbmmxGtQVbHBCv56",
     "3jyZhrBjD27vWEByutBoZaYmBemM5J7ikkYod6GTsXkM","S2JsYadaV5iB4A86wXhvArs8jb2kSbWA9pCmz7ALGQW"
     ],
    "Best 4 Me": [
        "8gx4VKzNVjenF2t7wikTHjwWEUt6mjJT4xmaSZKuCzCG", "A6EcV1ZhbGwNp6FYEXw4TaTyfVd8ASNGC1xiXL2Dz5zF",
        "AgfjAqBTKMGHAr1ZxjK8NWyMMp2EyyoS3wkYPYTUBjT5", "EP6RiDr27fNDtTkFbofZhtVojyMS9DC9b41VyfvtEQV7",
        "6ocX9nqdTLjm99HXXFVfucshcvWVo7h8BFQDwk9R12xu", "6ESwF2ouiH7Vz2uRkzBXftY6Ko9jdqvebMvTFUG2Bthy","S2JsYadaV5iB4A86wXhvArs8jb2kSbWA9pCmz7ALGQW",
        "GvD5HiZuNcZvny8zhUXStLwEiWmA2spbikj22wEN5LYR","Egm9KLWURmXjDEitMVucUnHCVex5NeZ5M3gT4CCb2Q1V","AzSEDJRzm6b2VBcc2dJYuZxGRRehgXssFEuYsidEULsP","HdxkiXqeN6qpK2YbG51W23QSWj3Yygc1eEk2zwmKJExp","7RX26gmCt74rnGFeuBVrUBUFSDn6mNnmUJfZStqaR8Pq","6WqWYTRh28mJEeHQnECfzhQvhF9XskoPU5fqsA49wkMV","8HxD27P2ptQCExud5jrvDzsgMxBRugKLMMmPBzXJHLuy","HJ8hsEsvXoK7KFNAS2Wb5698Xo5KB2VcU3sot479gnvZ","3jyZhrBjD27vWEByutBoZaYmBemM5J7ikkYod6GTsXkM","DQmMnakiKr1YNE2gcpggLCzBrauBwFbQkAaao2FTbjgp"
    ],
    "Lowprofit": ["Engi2TDft8C6R33RMn9YpBeNqxzqpyzKiXQBAsQZPZpw", "A6EcV1ZhbGwNp6FYEXw4TaTyfVd8ASNGC1xiXL2Dz5zF","E7Dq1L6zgDi5sJjqekeUzwC1TXRj8NUuk9QNdhUB3LNt","BF9WdfRe5iGsPXVAbaX5uDykb53iQUVkuJ1dtX2V9vHk","j1oeQoPeuEDmjvyMwBmCWexzCQup77kbKKxV59CnYbd","GXMZn221jxKTX2aYhNxsoctQZVVYTLo2mYoq2hC5edZv","BiJRfySs3L5tSWWmF93iMiJTyNvxmTU2U9Z5SHcSUJ2L"],
    "desprate": ["3e4VMNkFwT8t6vVVGLHYWYhhUGQtcACR1F1NrWMwY8eF", "BtxnBqqgCnDQfXLJeijdJm2GdNz3iFEqKAkMw3SuJtNG","BQ39hZo1eZsnaxGSUdk7MFnJoVsJd1ifCNEUqzY2aSjs","G2upvNYaDkzvXWy7s6zZZhHXj4gtJsfYRHCXY89W2wuv","2s1xW3rvrtQ3Ez4Z3iPnzUDMPGfWMFkK2Cs2urgGxrCy","2MFHzt6QrzrEUJimf4K5X1Net6x9x4qjpEVpMb9zRNon","6f26GAALkqNXL5HG89KfRr7YpR1ToLanecSwgV4YMaUa","3zmXMdcJBpU2tESBuE41AUc8gpTcSYa9J76Lmxdnwtrw","BYmsf5FcgDLWWHvSwxTcuuEpezyMATRZcXdoEb3h4dCE"],
    "Risk Checker": ["CYEtWTAX4W25MiSQZBwKeH1NLEnEUnzRAbNbNzkdnzVt","FxMW8ZfcDi4Wiqr6G2SuARGkS5ZxvMhvRzjRgc5G2UDM","DeCgQaBCSpHUoX7ng3MGYiPxdcfgU5HyB38cabVwF57o","4632BMWY69AkVHxN1XLKVuLrednYiLccuMeoXnQBMA7Z","F7RV6aBWfniixoFkQNWmRwznDj2vae2XbusFfvMMjtbE","47unSLWuZAosMnE9By9zmmrbDzYHqjfgPzPErTXqBDth", "CnXyVN5j6Z4t67uwFVLG7fnxy8ACR4AoxxfgtcoBxsBn"],
    "Whale":["CUqjTmYihCAMuwmqNvb2jKBC3bUR5J2Ek3Xw1qF5Gsb3","3cMMeEEAMdN2JGDDSSrPULjZo3VU63qqPMmtr9aJYUTg","6f26GAALkqNXL5HG89KfRr7YpR1ToLanecSwgV4YMaUa","BZe5jVcBq1hdhTkqSvif8asHdmsvtduhAzU1wnhJApRY","Aq43gJ4vQjtbjzzZ3TFCEmXSeX1YJs94gprhTv4qfrT","6f26GAALkqNXL5HG89KfRr7YpR1ToLanecSwgV4YMaUa","4uRzzVH85U8ZSXbNoHLg1KgJEor2ZUUw8Dbezew3JMv1","7awxPFThpN2uLuJf4VeDiVZVL34gxMWqDAqYaABn3Nnh","DQmMnakiKr1YNE2gcpggLCzBrauBwFbQkAaao2FTbjgp","215nhcAHjQQGgwpQSJQ7zR26etbjjtVdW74NLzwEgQjP","FbVbRbGqLk7DtprRHV1THa26ynoRZjUC6RuAxT9yaohM","DQvkTJRCb7kJE1Aw1BCiXekgBymhVW5ZK9p6Mk678Ujd","2k6YMgPtBcpJ2gM8JuS84EJbdSHatCGzHj9WisjPz4c1","7wiqcDbgtBjQcgtVSDArDbhbWX1RXrnArQvekncRCNve","AvMG3ZxJYmKph6TW6XHptmmRTdKHCDGdJuMEAcyxAybJ","Di5dhYckFTKrSEnwtRAYi4yQfneQV7ca3TvWMKJuNfVd","DChxWPbRoLD6KM69vtsDjjRNPtWfo2nmGaGCh3Pv86h3","DdTzGZke6CqtD6mnmEmNZiMxFFDEb3eizTYjB2pNMQAk", "AxBdvyt94ttxAfvr1d1zcCVevwaDH9QUeonDmcMiprZ7", "CYBkqMfdNGeJYc2k3EbHGmBvqAvB5GUMgG6xSZSqmp5u", "5mJqiSaowzGHfFjVNF5nU6JhXjYww9VEK9Zwpc4j4Wa2", "578ZFJoH75jkPCVupRvwZAzbVHVMbKL4P7MKuG9iWEtH", "EPNRJQpMPLKDP4oGoTeBJy8uAc4Z8XoKqbNTnQ3dzNVT"],
    "OnlyProfit" :["DfMxre4cKmvogbLrPigxmibVTTQDuzjdXojWzjCXXhzj","CrkK539YNKbsCRWYnH5oEs8Nnn66BjgkdvFEZ8mQ58gk","7cZWHHHjkujZ47Hn6JmT3W92rUXJGify4ezcBu4ExFdd","DQvkTJRCb7kJE1Aw1BCiXekgBymhVW5ZK9p6Mk678Ujd","C8WtJP4YveQbza5k1otS7BNFQ6My4pjVwecApCEQCNQi","GdG2anTVwLdDtM9XEKWUeuLy1mMGknJPzcqqW1qg7xrH","DPJQ3TCMS3Zg25dQ23ttgzKifxjs4NU6gM1NcFCVnkEt","5vMYfZJUsZd1Raj2fA76rGjEkdj3f8sv47GAsrkYkyqd","A6xcYiqjchhd6VsFseznKhJ6gMufPWWrzkQj4rEzaa7E","9XvBYSKetT98zByzcDcm4qscZ1fTaogwdaTEnLbADZHG","24uaZqjK16p9QA3Bs43GvXKFhb6GZdkRAdZVuLKttMLm","DsrBGtyBsW15CfSAfWa4AKZ4rvFDPHSzJEbDeL8ymQMB","E2RURCtEr75E53c793HXdmos8dU5Yy9mNAEBMHogWjFb"] ,
    "Small Invest":["DzfNo1qoGx4rYXbwS273tmPaxZMibr8iSrdw4Mvnhtv4","5orb9NyiJCmacGCGQyVesuASWUpXGiD3hXpY2iXP18cW","4dCezdQ36jM9QRkysytrWabqV27hcNkrdg92bdDbht9o","j1oeQoPeuEDmjvyMwBmCWexzCQup77kbKKxV59CnYbd","GLvCLzzEq3mMTrVWXuqm1nNRTQq6dH8DNd4ZHq7Sik3o","6sBVDn72viydq292Zdx2xQCCcUsFfHJ6ie98fjTGXwjW","HfDEtudyCwJTFaBQbJXqonFk6XfBUN8q9B9b7ddT9w6N","DHN3s48zqhKBUP641dcPHP2h79ehtTwgqYf25NDeD4Br","CeoexdLDkYm7YnSSNUBbr9jdW2rwk583UgLzb8ScWAzP","CPep14XgaDDNRMnP8ZjHVkvkhZPasRNYFEtDHvDpvnjR"],
    "Small but loss":["xQHjfWLhzwG8HPgfLbJRom1RDfWMjm3WZyaiWc5KMHr"],
    "He Knows":["HyfkumvdB4AwtxVv5aNEDvB9SFMGxE1BCfTANvxCZMS7","52kPsnhTpjHZucGUQy4YDm8g9ykXPMC47iNVSVRscikb","AarBPxKrHNfmkLvpY4r9J3ig8RqNXza7h4t9WTdFFS9Y", "2VUcurnU8tYEb7ehZKkRqYVpbXf7pBZpnMnPMFN7oCh2", "An7UQr7K4KDQJkADoHxyqKqUjUN8yDPJRzpj4MLG4vWU", "6ywypvibd7ZhLdJXHxPi4PAY6Mi4yCk66vVgDFmyXcud"],
    "Youtuber":["AAhnidQyZbh2ej1Ubqc3DAP7oKM72akPzxtYpaZpUe8r"]

}


# Track last transaction hashes to avoid duplicates
last_transaction_hashes = set()

# Map to store token_symbol: [wallet_names]
token_wallet_map: Dict[str, List[str]] = {}
# Map to store token_symbol -> (token_address, count)
token_count_map: Dict[str, Dict[str, int]] = {}
MAX_MAP_SIZE = 13

API_URL_TEMPLATE = "https://gmgn.ai/api/v1/wallet_activity/sol?type=buy&type=sell&wallet={wallet_id}&limit=1&cost=1"

HEADERS = {
    # ":authority": "gmgn.ai",
    # ":method": "GET",
    # ":path": "/api/v1/gas_price/sol",
    # ":scheme": "https",
   "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cookie": "_ga=GA1.1.210426056.1735150179; _ga_0XM0LYXGC8=GS1.1.1735915339.43.1.1735921930.0.0.0; cf_clearance=_snv_XeaCXpsdhSCWZBYPCf1LoWOdItCSW9AE0Xfhns-1735923994-1.2.1.1-1.6yeiDpLLPjphmIUVcWr9XrbnWHO9xuCH3GQgyhgOcqGeqe4mnP1WfvWxVggyi_0.XvVGWh9KUs5MDCSr8CY4rBil5KP5.4itHVWeoaNYhLYLkI3EViwl4gg5Vri99nZ1vrk2S_hH8CFqHWPvSns6_49wOuxcJUEsggbb4xOQC2M49_geirZxMIryZ15SvaHsXkWwkvvYdNBdTmI7u0rUIab9g4Ha3GKcoDwcbg8ca0VdilM9IwPd8anpB9rqtF_qajPGpjdBFJKrm1wS6MJOEiilyuhMbpUp4o_Xwjibv6sP_XPMuGQQbhdJcBYA3Zez47iba9XuWV.udYFfQu6SzCbx56fvT1QiW5ZnV4IRPgmbLH0rbOOj2zFaodYbQFJCXv2CtDpYf8YwyeDT1TZFrTD8nFvJi_UISQDE6adhG3yzs6vGHJ3.13as.75H1_9gNkNsbDS26EmVi378DNRg; __cf_bm=E_kBrQ6uLsR83LdXABM_z5Hldhr08JwfbcEMnVNXyQY-1735924010-1.0.1.1-Nxt1WbmqCjAT6EUz3BDprMUezWPpv_Trzwezq9yJtng0.ysXjZ_3N5JgPkCY1OnYD4sCZ4HFu0.15B0a2dEhqA",
    "priority": "u=0, i",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-arch": '""',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"131.0.6778.205"',
    "sec-ch-ua-full-version-list": '"Google Chrome";v="131.0.6778.205", "Chromium";v="131.0.6778.205", "Not_A Brand";v="24.0.0.0"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-model": '"Nexus 5"',
    "sec-ch-ua-platform": '"Android"',
    "sec-ch-ua-platform-version": '"6.0"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
}

# {
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "accept-encoding": "gzip, deflate, br, zstd",
#     "accept-language": "en-US,en;q=0.9",
#     "cookie": "_ga=GA1.1.210426056.1735150179; cf_clearance=LzMreOGg6iqKfg_eQWGhH7ruPFdk2n2VMMWYGAjEXEE-1735637835-1.2.1.1-IMu8i1vesXH_VGzd7BH9Z0ynYLlCgoK6BZ0__R5VkepNaIzNsKGWCy50hup42_Rk5fckhb5fgsuyjh1fC4027yJyysKEFBx2XfMM9ObU3L.Ke62d4zHMt9xevr.Kh2wBCWldDlJ.w42e9mVAB3UXz8LfXXzv1tWY3mQ.T.cmtBXQooF.54F042jQirPkyoFYjOL6A5I.SvxMV_Pq4ZWwW6hPWXJMGyQBM05oWODY8ZN8yYX_n5aHLRRmKWy9Jnt_UJOacEazatolCStIiiDoVRKu3h1wcb9eQqrkmRGYxoMTFTQYkYE6lniNW0S8bEoX4MYk1Sxi.hWUyy_twtdGeLB948N1sKrpwXEtdah1A86igbE0lZYLwhp9PIRnRRwn5qlHCR6Wof_k1qGbjLlQgQ; _ga_0XM0LYXGC8=GS1.1.1735637838.36.1.1735639682.0.0.0; __cf_bm=E04AhdHtbV6YkxcjAP1YTOVCbGFOEg3gGGKB5EigTzk-1735660026-1.0.1.1-Zs.Ha.sT2NxxKNk_F5XsjRVDaQqdS4.4ep8Bz68QC5XnOliBTIMu8GGZ.eVP8_.6H1dfSCfNC2U6IggA.iSktQ",
#     "priority": "u=0, i",
#     "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
#     "sec-ch-ua-arch": '""',
#     "sec-ch-ua-bitness": '"64"',
#     "sec-ch-ua-full-version": '"131.0.6778.205"',
#     "sec-ch-ua-full-version-list": '"Google Chrome";v="131.0.6778.205", "Chromium";v="131.0.6778.205", "Not_A Brand";v="24.0.0.0"',
#     "sec-ch-ua-mobile": "?1",
#     "sec-ch-ua-model": '"Nexus 5"',
#     "sec-ch-ua-platform": '"Android"',
#     "sec-ch-ua-platform-version": '"6.0"',
#     "sec-fetch-dest": "document",
#     "sec-fetch-mode": "navigate",
#     "sec-fetch-site": "none",
#     "sec-fetch-user": "?1",
#     "upgrade-insecure-requests": "1",
#     "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
# }

# Convert timestamp to readable time
def convert_timestamp(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

# Fetch transactions for a wallet
def fetch_wallet_activity(wallet_id: str) -> list:
    url = API_URL_TEMPLATE.format(wallet_id=wallet_id)
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if data["code"] == 0 and "activities" in data["data"]:
            return data["data"]["activities"]
    except Exception as e:
        logger.error(f"Error fetching data for wallet {wallet_id}: {e}")
    return []

# Update token_wallet_map with a new transaction
def update_token_wallet_map(token_symbol: str, wallet_name: str):
    current_time = datetime.utcnow().timestamp()

    if token_symbol not in token_wallet_map:
        token_wallet_map[token_symbol] = []

    # Update the wallet list for the token
    token_wallet_map[token_symbol] = [
        entry for entry in token_wallet_map[token_symbol]
        if entry[0] != wallet_name  # Remove any old entries for this wallet
    ]
    token_wallet_map[token_symbol].append((wallet_name, current_time))

    # Maintain map size
    while len(token_wallet_map) > MAX_MAP_SIZE:
        oldest_token = None
        oldest_time = float('inf')

        for key, wallets in token_wallet_map.items():
            if len(wallets) == 1 and wallets[0][1] < oldest_time:
                oldest_token = key
                oldest_time = wallets[0][1]

        if oldest_token:
            del token_wallet_map[oldest_token]

# Function to reset the map
async def resetCommand(update: Update, context: CallbackContext)-> None:
    token_wallet_map.clear()
    await update.message.reply_text("🤖 Cleared map captain")  # Clear the map
    # print("Map has been reset.")
    # print("Unknown command.")            

# Monitor wallets and send updates
async def monitor_wallets(context: CallbackContext) -> None:
    bot = context.bot
    chat_id = context.job.data  # Retrieve chat_id from job data
    for category, wallets in CATEGORIES.items():
        for wallet in wallets:
            transactions = fetch_wallet_activity(wallet)
            wallet_name = WALLET_NAMES.get(wallet, wallet[-4:])
            for tx in transactions:
                tx_hash = tx["tx_hash"]
                if tx_hash in last_transaction_hashes:
                    continue  # Skip if already processed
                last_transaction_hashes.add(tx_hash)

                # Extract transaction details
                timestamp = convert_timestamp(tx["timestamp"])
                event_type = tx["event_type"]
                token_symbol = tx["token"]["symbol"]
                token_adress = tx["token"]["address"]
                token_amount = tx["token_amount"]
                price_usd = tx["price_usd"]

                 # Update the token-wallet map
                if event_type == "buy":
                    update_token_wallet_map(token_symbol, wallet_name)
                    # Increment token count
                    if token_symbol in token_count_map:
                        token_count_map[token_symbol]['count'] += 1
                    else:
                        token_count_map[token_symbol] = {"address": token_adress, "count": 1}
                elif event_type == "sell":
                    # Decrement token count if it exists
                    if token_symbol in token_count_map:
                        token_count_map[token_symbol]['count'] -= 1
                        # Remove the token if the count reaches 0
                        if token_count_map[token_symbol]['count'] <= 0:
                            del token_count_map[token_symbol]

                # Determine the emoji based on event_type
                emoji = "🟢" if event_type.lower() == "buy" else "🔴"    

                # Format and send the message
                message = (
                     f"📣*{emoji}=====>{category} ||🕒{timestamp}<===*\n"
                    f"💵 `{wallet}`\n"
                    f"🫣 {wallet_name}  ===> {event_type} \n"
                    f"🪙: `{token_adress}`\n"
                    f"🔹 Token: {token_symbol}\n"
                    f"🔹 Token Amount: {token_amount}\n"
                    f"🔹 Price Usdt: {price_usd}\n"
                    f"💸Ttl: {round(Decimal(token_amount) * Decimal(price_usd), 8)} "
                )
                await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

# For token command
async def tokens_command(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if user.id != ADMIN_USER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return
    if not token_count_map:
        await update.message.reply_text("No tokens tracked yet.")
        return

    # Sort tokens by count (descending)
    sorted_tokens = sorted(
        token_count_map.items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )

    # Take only the top 7 tokens
    top_tokens = sorted_tokens[:7]

    # Generate the output message
    message_lines = [
        f"🪙 {token_symbol} - {data['address']} - {data['count']}"
        for token_symbol, data in top_tokens
    ]
    message = "\n".join(message_lines)

    await update.message.reply_text(message)

# Function to fetch the current SOL price in USD
def get_sol_price_usd() -> float:
    url = "https://gmgn.ai/api/v1/gas_price/sol"
    sol_headers = {
        # ":authority": "gmgn.ai",
        # ":method": "GET",
        # ":path": "/api/v1/gas_price/sol",
        # ":scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "cookie": "_ga=GA1.1.210426056.1735150179; _ga_0XM0LYXGC8=GS1.1.1735924426.44.1.1735924464.0.0.0; __cf_bm=OYq8hRmFqyKVLeKLmohQznZcYBNzjmsUeffpvtYVhRw-1735924458-1.0.1.1-pCXu2sKU1WeuZSY24DAjTO1TLj7L7jA2r47ORTKm9dQhm4QDU.Vm0Y2thVmT1yg5Tu25b8wUU3j.h409HzZ8Ag; cf_clearance=534SJJcptBeZoLuIsbXeIOM5VsEbKOG1.M1GlHCKWpo-1735924456-1.2.1.1-BiDXGlViZpnBvmHNmc_JL.r1Bbxh46aFX0RMnfrtZk482keKV9dtRi3Js.41F0szdmJF.8Kyzbk2JLZjGLTOmsbgpkNqOp9No7ahAS7ELrTD__E_vyf0hGzFlToRV60BBdbXGlCaNTdOwAXzE8VWP23OQdejTycEaz87PWPMy7SAusQgYNrWS.kRWhxt1iXPZE6V5ziSXZg37aIwGRbvYct7HWBn_tIkRNesNBxNBPy6RHmo1QQ.k432jKJpmg5MReuD5o1IkxxpshOA7hU.73wacTvn4vbTu.6kzM0v9pogcBt2HPjCietxwhNd0DofjGDMEF.EanSoMe_Qn54pr87cu3P7it7sJBT1YAJBzFW1DviKCwJHOAq.f0XVc60fbwIWLd_GHD8nlk7LOQqk1jMUggzv8yvuppvLfENfSPiqq63ESBEeRvitPJRQMejQGCRE_qIReYXgeGl7_a_0Bw",
        "priority": "u=0, i",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-arch": '""',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-full-version": '"131.0.6778.205"',
        "sec-ch-ua-full-version-list": '"Google Chrome";v="131.0.6778.205", "Chromium";v="131.0.6778.205", "Not_A Brand";v="24.0.0.0"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-model": '"Nexus 5"',
        "sec-ch-ua-platform": '"Android"',
        "sec-ch-ua-platform-version": '"6.0"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
    }
    response = requests.get(url,headers=sol_headers)
    if response.status_code == 200:
        data = response.json()
        return float(data["data"]["native_token_usd_price"])
    else:
        raise Exception("Failed to fetch SOL price from API.")

# Async function to handle the /convert command
async def convert_command(update: Update, context: CallbackContext) -> None:
  
    try:
        # Ensure the command has a parameter
        if not context.args:
            await update.message.reply_text("Usage: /convert <value>sol or <value>usd")
            return

        # Parse the value and unit (e.g., "1sol" or "1usd")
        input_value = context.args[0].lower()
        if input_value.endswith("sol"):
            amount = float(input_value[:-3])
            sol_to_usd = get_sol_price_usd()
            usd_value = amount * sol_to_usd
            await update.message.reply_text(f"{amount} SOL = ${usd_value:.2f} USD.")
        elif input_value.endswith("usd"):
            amount = float(input_value[:-3])
            sol_to_usd = get_sol_price_usd()
            sol_value = amount / sol_to_usd
            await update.message.reply_text(f"${amount} USD = {sol_value:.6f} SOL.")
        else:
            await update.message.reply_text("Invalid format. Use /convert <value>sol or <value>usd.")
    except ValueError:
        await update.message.reply_text("Invalid number format. Please use a valid number (e.g., 1sol or 1usd).")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")
               

async def summary(update: Update, context: CallbackContext) -> None:
    if not token_wallet_map:
        await update.message.reply_text("The token-wallet map is currently empty.")
        return

    # Check if token_wallet_map values are strings (expected behavior)
    for token_symbol, wallets in token_wallet_map.items():
        if not isinstance(wallets, str):
            # If not strings, convert them to comma-separated strings (assuming list)
            if isinstance(wallets, list):
                wallets = ', '.join(str(wallet) for wallet in wallets)
            else:
                # Handle unexpected data type with a warning
                await update.message.reply_text(f"Warning: Unexpected data type in token_wallet_map for {token_symbol}")
                continue  # Skip this entry

    summary_message = "\n".join(
        f"{i + 1}. {token_symbol}: {[RECORD.get(name, 'Unknown Category')  for name, _ in wallets]}" 
        for i, (token_symbol, wallets) in enumerate(token_wallet_map.items()) 
        if isinstance(wallets, list)  # Ensure wallets is a list
    )
    await update.message.reply_text(summary_message)

# Start monitoring command
async def start_monitoring(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user = update.message.from_user
    if user.id != ADMIN_USER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return
    if context.job_queue:
        context.job_queue.run_repeating(monitor_wallets, interval=60, first=0, data=chat_id)
        await update.message.reply_text("✅ Monitoring started! You will receive live updates on wallet activity.")
    else:
        await update.message.reply_text("❌ Failed to start monitoring. Job queue is not initialized.")

#Function to understand m,k,b   
def parse_value(value: str) -> float:
    """
    Converts a string with suffixes like 'k', 'm', 'b' into a float.
    Examples:
        "1.23k" -> 1230
        "1.23m" -> 1230000
        "1.23b" -> 1230000000
    """
    value = value.lower().strip()
    if value.endswith('k'):
        return float(value[:-1]) * 1_000
    elif value.endswith('m'):
        return float(value[:-1]) * 1_000_000
    elif value.endswith('b'):
        return float(value[:-1]) * 1_000_000_000
    else:
        return float(value)  # Return as is if no suffix

# Function to calculate profit and total amount
def calculate_profit(invested_amount: float, marketcap_init: float, marketcap_final: float) -> dict:
    if marketcap_init <= 0:
        raise ValueError("Initial market capitalization must be greater than zero.")
    multiplier = marketcap_final / marketcap_init
    total_amount = invested_amount * multiplier
    profit = total_amount - invested_amount
    profit_percentage = (profit / invested_amount) * 100
    return {
        "profit": profit,
        "total_amount": total_amount,
        "profit_percentage": profit_percentage
    }

# Command handler for /profit
async def profit_command(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    if user.id != ADMIN_USER_ID:
        await update.message.reply_text("You are not authorized to use this command.")
        return
    try:
        # Parse arguments from the command
        args = context.args
        if len(args) != 3:
            await update.message.reply_text("Usage: /profit <invested_amount> <marketcap_init> <marketcap_final>")
            return

        # Convert inputs to appropriate types using the helper function
        invested_amount = parse_value(args[0])
        marketcap_init = parse_value(args[1])
        marketcap_final = parse_value(args[2])

        # Calculate profit and total amount
        result = calculate_profit(invested_amount, marketcap_init, marketcap_final)
        profit = result["profit"]
        total_amount = result["total_amount"]
        profit_percentage = result["profit_percentage"]

        # Respond with the calculated values
        await update.message.reply_text(
            f"Profit💲: ${profit:.2f}\n"
            f"Total Amount💸: ${total_amount:.2f}\n"
            f"Profit Percentage😎: {profit_percentage:.2f}%"
        )

    except ValueError as e:
        await update.message.reply_text(f"Error: {e}")
    except Exception as e:
        await update.message.reply_text("An error occurred. Please check your inputs and try again.")

async def track_command(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /track <wallet_address>")
        return

    new_wallet_id = context.args[0]
    url = f"https://gmgn.ai/api/v1/wallet_activity/sol?type=buy&type=sell&wallet={new_wallet_id}&limit=9&cost=9"

    try:
        # Fetch data from the API
        response = requests.get(url,headers=HEADERS)
        
        # Parse the JSON response
        data = response.json()
        if data["code"] != 0:
            await update.message.reply_text("Failed to fetch data. Please try again later.")
            return

        activities = data["data"]["activities"]

        if not activities:
            await update.message.reply_text(f"No transaction data found for wallet: ")
            return

        # Format the response
        message_lines = ["===>Transaction Details"]
        for idx, activity in enumerate(activities, start=1):
            symbol = activity["token"]["symbol"]
            event_type = activity["event_type"]
            cost_usd = activity["cost_usd"]
            message_lines.append(f"{idx}.🪙 {symbol}  -> {event_type}  ->💲{cost_usd}")

        message = "\n".join(message_lines)
        await update.message.reply_text(message)

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Handle /start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🤖 Welcome! Use /monitor to start receiving updates \n /summary to view the token-wallet map \n /profit <invesment> <initmarketcap> <finalmarketcap> for finding profit in trading /tokens to get latest track of tokens being traded \n /convert <value>sol or /convert <value>usd to convert values \n /track <wallet_address> to get top 6 transactions data ")

def main():
    # Create the Application with a JobQueue enabled
    application = Application.builder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("monitor", start_monitoring))
    application.add_handler(CommandHandler("summary", summary))
    application.add_handler(CommandHandler('reset',resetCommand))
    application.add_handler(CommandHandler("profit", profit_command))
    application.add_handler(CommandHandler("tokens", tokens_command))
    application.add_handler(CommandHandler("convert", convert_command))
    application.add_handler(CommandHandler("track",track_command))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
