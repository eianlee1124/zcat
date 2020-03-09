#!/usr/bin/env python3

import ssl
import json
import websocket

class WebSocketAPI(object):
    
    def __init__(self):
        sslopt = {"cert_reqs": ssl.CERT_NONE}
        self.ws = websocket.WebSocket(sslopt=sslopt)
        
    @property
    def connected(self):
        return self.ws.connected
        
    def connect(self, url):
        """주어진 url에 웹소켓 연결을 만든다.
        """
        self.ws.connect(url)
        
    def send(self, payload):
        """주어진 payload를 연결 대상으로 전송.
        """
        self.ws.send(json.dumps(payload))
        
    def recv(self):
        """메시지 수신 이벤트가 발생하면 json으로 포맷팅 후 반환.
        """
        return json.loads(self.ws.recv())