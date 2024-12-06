# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    # TIPS: このconnectメソッドは クライアント側のJavaScriptで、WebSocketクラスが実行されたときに実行される。
    async def connect(self):

        # TIPS: このself.scopeには、クライアント側の情報(認証状態、ユーザー情報、送信先URLなど) が含まれている。
        # django-channels版 request オブジェクトのようなもの
        # ただし、self.scope は辞書であり、request と違って オブジェクトではない 

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # グループに接続を追加している。
        # TIPS: self.channel_layer は settings.pyで指定したチャンネルレイヤーの操作をする
        # TIPS: .group_add() で 接続した人をグループに接続する。
        # TIPS: この self.channel_name は接続ごとに割り当てられた一意の名前
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )


        # TIPS: self.accept() でwebsocket の接続を正式に確立する。connectメソッドで↑のグループ追加をしない場合、↓だけでも良い。
        await self.accept()

    
    # TIPS: このdisconnectはブラウザを閉じる、ページ遷移したときに発動する。
    # WebSocketはステートフル。ステートレスなHTTPと違い、ブラウザ終了、ページ遷移が検知できる。
    async def disconnect(self, close_code):

        # TIPS: 接続をグループから削除している。
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # TIPS: クライアントからメッセージを受け取ったときの処理。
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # TIPS: グループに対して、メッセージを送る。グループに所属している接続ごとに、chat_messageが実行される。
        # TIPS: type には、実行したいメソッドを指定する。
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    # TIPS: 接続に対してメッセージを送信する処理、receiveメソッドから呼び出される。
    async def chat_message(self, event):
        message = event['message']

        # メッセージをJSONにして送信する。(送信先のグループ  はreceive で指定している。)
        await self.send(text_data=json.dumps({
            'message': message
        }))

