"""
LLM 服务模块 - 调用 LM Studio OpenAI API 兼容接口
"""
import requests
from zai import ZhipuAiClient
from .prompt import SYSTEM_PROMPT
#本地大模型用于测试
#LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
#使用智谱AI的接口
# ZHIPU_AI_URL = "https://api.zhipuai.com/v1/chat
api_key = ""
client = ZhipuAiClient(api_key=api_key)
def call_llm(question: str, temperature: float = 0.3) -> str:
    payload = {
        "model": "glm-4.7-flash",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"请讲解以下化学题：{question}"}
        ],
        
        "temperature": temperature
    }
    try:
        #本地大模型访问方式
        #response = requests.post(LM_STUDIO_URL, json=payload, timeout=180)
        # response.raise_for_status()
        #result = response.json()
        #return result["choices"][0]["message"]["content"]  
        #智谱AI访问方式
        response = client.chat.completions.create(**payload)
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
    except requests.exceptions.ConnectionError:
        return (
            "⚠️ 无法连接到 LM Studio，请确保：\n"
            "1. LM Studio 已启动\n"
            "2. 本地服务器已开启（http://localhost:1234）\n"
            "3. 已加载模型并启动 API 服务"
        )
    except requests.exceptions.Timeout:
        return "⚠️ AI 模型响应超时，请稍后重试。"
    except Exception as e:
        return f"⚠️ 请求出错：{str(e)}"
