# AI 化学老师 V1 🧪

高中化学 AI 提分讲解 + 错题本系统

## 技术栈
- **后端**: Python 3.10+ / FastAPI / Uvicorn
- **AI 模型**: LM Studio (OpenAI API 兼容模式)
- **数据库**: SQLite
- **前端**: 纯 HTML + JS + **KaTeX + marked** (公式与 Markdown 渲染)

## 快速开始

```bash
cd ai-chemistry-teacher
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

浏览器访问 http://localhost:8000，确保 LM Studio 已运行在 localhost:1234

## 项目结构
```
ai-chemistry-teacher/
├── backend/
│   ├── main.py          # FastAPI 应用
│   ├── database.py      # SQLite 数据库
│   ├── llm_service.py   # LLM 调用
│   └── prompt.py        # AI 教学 System Prompt
├── frontend/
│   ├── index.html       # 解题页 (KaTeX + Markdown)
│   ├── wrong.html       # 错题本页
│   └── detail.html      # 错题详情页 (KaTeX + Markdown)
├── data.db              # SQLite 数据库（自动生成）
└── requirements.txt
```

## API 接口
- `POST /api/explain` - AI 化学讲解
- `POST /api/wrong/save` - 保存错题
- `GET /api/wrong/list` - 获取错题列表
- `GET /api/wrong/{id}` - 获取错题详情
- `DELETE /api/wrong/{id}` - 删除错题
- `GET /api/health` - 健康检查
