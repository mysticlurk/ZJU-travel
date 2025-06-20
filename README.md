# 旅行AI助手

一个轻量化、一站式的浙大旅行网站，聚焦紫金港校区，接入智能AI助手，整合导览、景点解说、路线规划等功能，以极简交互和本土化设计提升用户体验。

---

## 功能特点

- **登录页面**：模拟登录入口，未来可扩展为用户系统
- **选择身份**：根据不同的用户身份呈现适合这一群体的界面和功能
- **首页**：展示校园景点，最新的校园活动，点击图标可跳转到对应的功能
- **AI对话**：基于大模型自动规划旅行内容
- **联网搜索**：对航班、酒店、门票等问题可自动触发联网搜索，向用户提供整合后的信息以及相关的链接
- **导航功能**：帮助用户规划路线，并展示途径的景点
- **日程表**：用户可以规划行程路线，还可以上传图片、视频和文字记录旅行过程
- **其他功能**：钱包功能、校友徽章、时空留言墙等

---

## 安装说明



### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量 `.env`
```
CUSTOM_API_KEY=你的OpenAI API Key
BASE_URL=https://api.openai.com/v1
SERPER_API_KEY=你的联网搜索Key
SERPER_URL = "https://google.serper.dev/search"

```

### 3. 启动服务
```bash
python main.py
```
访问：http://127.0.0.1:5000/  
可打开浏览器开发人员工具，选择切换设备仿真来模拟手机显示

---

## 项目结构
```
Z-Journey/
├── main.py
├── .env
├── templates/
│   ├── login.html           # 登录界面
│   ├── identity.html        # 选择身份
│   ├── home.html            # 首页
│   ├── chat.html            # AI对话界面
│   ├── map.html             # 导航界面
│   └── schedule.html        # 日程表
├── static/                # 静态文件目录（CSS/图片等）
└── requirements.txt       # Python依赖
```

---

## 未来可扩展方向
- 用户注册与行程历史保存
- 地图路径规划（接入高德/百度）
- AI 推荐酒店/航班卡片展示
- 行程生成 PDF/导出功能
- 接入天气api
---

## License
MIT License

---

