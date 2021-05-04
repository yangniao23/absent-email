# absent-email
欠席者を連絡する．

## 使い方
uwsgiとnginxで動かします．

app.py:
	${smtpserver}: SMTPサーバのドメイン名 ex: smtp.example.com
	${mailserver_domain}: メールのドメイン名 ex: example.com
	${username}: SMTPサーバのユーザ名 
		※ ユーザ名がドメイン名を含む形 ex: user@example.com のような形の場合，
		106,122,163行目の${mailserver_domail}の消去が必要．
	${password}: SMTPサーバのパスワード

namelist.json:
	適当に書き換えてください．

absent-email.service:
	ユーザ名，パスあたりを適当に書き換えてください．

myapp.ini:
	chdirを適当に書き換えてください．

nginx/:
	${domain}: ドメイン名 ex: example.com

nginxのインストール後，上の参考にもろもろ設定をしたら
```
sudo ln -sf $(pwd)/absent-email.service /etc/systemd/system/absent-email.service
sudo systemctl daemon-reload
sudo systemctl enable --now absent-email
```