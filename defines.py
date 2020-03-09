import ssl
import base64
import hashlib
import hmac
import time
import itertools
import httplib2
import ujson as json


ASK = "asks"
BID = "bids"
DEFAULT_DEPTH = 10

PORT = 8000
HOST = "127.0.0.1"

sslopt = {"cert_reqs": ssl.CERT_NONE}