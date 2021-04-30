from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import os
import base64
from dotenv import load_dotenv
load_dotenv()
 
# .envから環境変数を読み込む
sendgrid_api_key = os.environ.get('API_KEY')
from_address = os.environ.get('FROM')
to_list = os.environ.get('TOS').split(',')
 
# メッセージの構築
message = Mail()
 
# 各宛先と、対応するSubstitutionタグを指定
fullname_list = ['田中 太郎', '佐藤 次郎', '鈴木 三郎']
familyname_list = ['田中', '佐藤', '鈴木']
place_list = ['中野', '目黒', '中野']
     
for num in range(len(to_list)):
    message.to = To(to_list[num], fullname_list[num], p = num)
 
    message.substitution = [
        Substitution('fullname', fullname_list[num], p = num),
        Substitution('familyname', familyname_list[num], p = num),
        Substitution('place', place_list[num], p = num),
        ]
 
# 送信元を設定
message.from_email = From(from_address, '送信者名')
 
# 件名を設定
message.subject = Subject('[sendgrid-python-example] フクロウのお名前はfullnameさん')
 
# 本文（テキストパートとHTMLパート）を指定
message.content = Content(MimeType.text, 'familyname さんは何をしていますか？\r\n 彼はplaceにいます。')
message.content = Content(MimeType.html, '<strong>familyname さんは何をしていますか？</strong><br />彼はplaceにいます。')
     
# カテゴリ情報を付加
message.category = Category('Category1')
     
# カスタムヘッダを指定
message.header = Header('X-Sent-Using', 'SendGrid-API')
     
message.attachment = Attachment(FileContent(encoded_file),
                                FileName('owl.gif'),
                                FileType('image/gif'),
                                Disposition('attachment'))
 
# メール送信を行い、レスポンスを表示
sendgrid_client = SendGridAPIClient(sendgrid_api_key)
response = sendgrid_client.send(message = message)
print(response.status_code)
print(response.body)
print(response.headers)
