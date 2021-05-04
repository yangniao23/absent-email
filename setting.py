#!/usr/bin/env python3
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

to_addr = os.environ.get("to_addr") #送信先のメールアドレス
token = os.environ.get("token") #API使用時のトークン
secret_key = os.environ.get("secret_key") #Flaskのシークレットキー
basicauth_user = os.environ.get("user") #BASIC認証のユーザ名
basicauth_pass = os.environ.get("password") #BASIC認証のパスワード