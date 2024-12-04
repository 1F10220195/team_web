# 必要なモジュールの import
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import requests
import os
OPENAI_API_KEY = 'IHK92nGI3dUJJiiPT0XFv_KMzS8QyOpkTqbnaBpqwHM5nSmeKmqOuIFgEGc9ItPneA4jVffl2wtguOck9Zv6Qng'
OPENAI_API_BASE = 'https://api.openai.iniad.org/api/v1'
chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE, model_name='gpt-4o-mini', temperature=0)
messages = [
    HumanMessage(content='Pythonの特徴について教えてください'),
]
result = chat.invoke(messages)
result

# 必要なモジュールの import
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

# 環境変数からAPIキーとベースURLを取得
OPENAI_API_KEY = os.getenv("IHK92nGI3dUJJiiPT0XFv_KMzS8QyOpkTqbnaBpqwHM5nSmeKmqOuIFgEGc9ItPneA4jVffl2wtguOck9Zv6Qng")
OPENAI_API_BASE = os.getenv("https://api.openai.iniad.org/api/v1")

# ChatOpenAIの初期化
chat = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    openai_api_base=OPENAI_API_BASE,
    model_name='gpt-4',  # または適切なモデル名を指定
    temperature=0
)

# メッセージリスト
messages = [
    HumanMessage(content='Pythonの特徴について教えてください'),
]

# APIを呼び出して結果を取得
result = chat.invoke(messages)

# 結果を表示
print(result)
