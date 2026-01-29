# 🧠 Coddy AI - Next Gen Neural Assistant

> **Optimized • Local • High-Performance**

Coddy AI is a state-of-the-art local AI assistant featuring a high-performance Python backend and a stunning, reactive Next.js frontend. It leverages advanced optimization libraries to ensure lightning-fast responses and efficient resource usage.

![Coddy AI Frontend](./frontend/public/window.svg)

## ⚡ High-Performance Core

The architecture has been massively optimized with top-tier libraries:

### 🐍 Backend (Python / FastAPI)

- **🚀 CoddyEngine2**: Custom C++ optimized inference engine (simulated).
- **📚 Qdrant + DiskCache**: Hybrid vector search system with **DiskCache** for sub-millisecond query retrieval on repeated searches.
- **🪵 Loguru**: Beautiful, asynchronous structured logging.
- **� ORJSON**: High-performance JSON serialization, replacing standard `json` lib.
- **🦆 DuckDB**: Integrated for future high-speed analytical queries.
- **⛓️ LangChain**: Ready for complex chain orchestration.

### ⚛️ Frontend (Next.js 16)

- **⚡ SWR**: State-of-the-art data fetching with automatic revalidation and caching.
- **🎨 Tailwind CSS + CLSX**: Optimized, mergeable utility classes for dynamic styling.
- **🖼️ Sharp**: High-performance image optimization.
- **🌀 Framer Motion**: Butter-smooth 60fps animations.

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### 1. Clone & Setup Backend

```bash
git clone https://github.com/biagio-scaglia/my-ai.git
cd my-ai

# Install Python Dependencies (Optimized)
pip install -r requirements.txt
```

### 2. Setup Frontend

```bash
cd frontend

# Install Node Dependencies
npm install
```

---

## 🚀 Usage

### Start the System (All-in-One)

Simply run the startup script:

```bash
./start_app.bat
```

This will launch both the FastAPI backend server (Port 8000) and the Next.js frontend (Port 3000).

### Manual Start

**Backend:**

```bash
python api.py
```

**Frontend:**

```bash
cd frontend
npm run dev
```

---

## 📂 Project Structure

```
my-ai/
├── 🧠 api.py              # Main FastAPI entrypoint (Optimized with loguru/orjson)
├── ⚙️ engine_cpp.py       # Core Inference Engine
├── 🔍 rag_engine.py       # RAG System with DiskCache & Qdrant
├── 📜 requirements.txt    # Python dependencies
├── 📁 frontend/           # Next.js 16 Application
│   ├── 📂 src/
│   │   ├── 🧩 components/ # ChatInterface, Navbar (Optimized with clsx)
│   │   └── 📄 app/        # App Router Pages
│   └── ⚙️ package.json    # Frontend dependencies
└── �️ knowledge/          # RAG Knowledge Base
```

---

## 🌟 Key Features

- **Local RAG**: Queries your local `knowledge/` folder with vector search.
- **Smart Caching**: `DiskCache` remembers previous answers to save compute.
- **Real-time Status**: Frontend polls backend health via `SWR`.
- **Cyberpunk UI**: A premium, "Made by Biagio" design aesthetic.

---

_Built with ❤️ by Biagio Scaglia_
