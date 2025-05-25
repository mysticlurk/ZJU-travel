from flask import Flask, request, jsonify, render_template
from autogen import AssistantAgent
import os
from dotenv import load_dotenv
import requests

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("CUSTOM_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("BASE_URL")
os.environ["OPENAI_API_TYPE"] = "openai"
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["SERPER_API_BASE"] = os.getenv("SERPER_URL")

llm_config = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.5,
    "api_key": os.getenv("CUSTOM_API_KEY"),
    "base_url": os.getenv("BASE_URL"),
    "api_type": "openai"
}

assistant = AssistantAgent(
    name="travel_assistant",
    llm_config=llm_config,
    system_message="你是一个专业旅行顾问，根据用户对话动态规划行程。请用简洁明了的方式回答，避免使用过多的HTML标签。"
)

chat_history = [{"role": "system", "content": "你是一个旅行顾问，协助用户多轮制定旅行计划。"}]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")

def get_serper_search_results(query):
    payload = {
        "q": query,
        "gl": "cn",
        "hl": "zh-cn",
        "type": "search",
        "engine": "google"
    }
    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
    }
    
    response = requests.post(os.getenv("SERPER_URL"), json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {}

def format_search_results(search_results):
    """格式化搜索结果，使其更适合手机显示"""
    if not search_results:
        return ""
    
    formatted_text = "<strong>🔍 搜索结果</strong><br><br>"
    
    # 处理答案框
    answer_box = search_results.get("answerBox", None)
    if answer_box:
        snippet = answer_box.get("snippet", "").strip()
        link = answer_box.get("link", "")
        if snippet:
            formatted_text += f"<strong>快速答案：</strong><br>{snippet}<br><br>"
            if link:
                formatted_text += f"<a href='{link}' target='_blank'>查看详细信息</a><br><br>"
    
    # 处理有机搜索结果，限制数量避免信息过载
    organic_results = search_results.get("organic", [])[:3]  # 只取前3个结果
    
    if organic_results:
        formatted_text += "<strong>相关链接：</strong><br>"
        for i, result in enumerate(organic_results, 1):
            title = result.get('title', '').strip()
            link = result.get('link', '')
            snippet = result.get('snippet', '').strip()
            
            if title and link:
                # 限制标题长度
                if len(title) > 40:
                    title = title[:40] + "..."
                
                formatted_text += f"{i}. {title}<br>"
                if snippet:
                    # 限制摘要长度
                    if len(snippet) > 80:
                        snippet = snippet[:80] + "..."
                    formatted_text += f"   {snippet}<br>"
                formatted_text += f"   <a href='{link}' target='_blank'>查看详情</a><br><br>"
    
    return formatted_text

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    
    if not user_input:
        return jsonify({"reply": "请输入内容"})

    chat_history.append({"role": "user", "content": user_input})
    reply_text = ""

    try:
        # 检查是否需要搜索
        search_keywords = ["航班", "酒店", "路线", "查一下", "门票", "交通", "天气", "景点", "餐厅", "美食"]
        needs_search = any(keyword in user_input for keyword in search_keywords)
        
        if needs_search:
            search_results = get_serper_search_results(user_input)
            if search_results:
                search_text = format_search_results(search_results)
                reply_text += search_text

        # 获取AI助手回复
        try:
            assistant_reply = assistant.generate_reply(chat_history)
            assistant_text = assistant_reply.content if hasattr(assistant_reply, "content") else str(assistant_reply)
            
            # 清理AI回复中可能的HTML标签
            assistant_text = assistant_text.replace('<strong>', '').replace('</strong>', '')
            assistant_text = assistant_text.replace('<br>', '\n').replace('<br/>', '\n')
            
            if reply_text:  # 如果有搜索结果
                reply_text += f"<strong>🤖 AI建议</strong><br>{assistant_text}"
            else:
                reply_text = f"<strong>🤖 AI助手</strong><br>{assistant_text}"
            
            chat_history.append({"role": "assistant", "name": "travel_assistant", "content": assistant_text})
            
        except Exception as ai_error:
            print(f"AI Error: {ai_error}")
            if reply_text:  # 如果有搜索结果，就只返回搜索结果
                pass
            else:
                reply_text = "<strong>🤖 AI助手</strong><br>抱歉，我现在无法处理您的请求，请稍后再试。"

        return jsonify({"reply": reply_text})

    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({"reply": f"<strong>[系统]</strong> 出错了：{str(e)}"}), 500

@app.route("/<page>.html")
def serve_page(page):
    try:
        return render_template(f"{page}.html")
    except:
        return f"<h3>未找到页面：{page}.html</h3>", 404

if __name__ == "__main__":
    app.run(debug=True)