Absolutely! Here's a **fully polished README.md** for your `NewAgeBuilder` project — clean, professional, and developer-friendly, with clear setup instructions, fallback options, and highlights of the wow factors you’ve built in.

---

```markdown
# 💡💡 NewAgeBuilder – Conversational Website Creation with AI ✨✨

NewAgeBuilder is a modern no-code web builder inspired by [Lovable.dev](https://lovable.dev), allowing users to create entire websites simply by **chatting**. No code, no drag-and-drop — just describe your vision.

Built with **FastAPI**, **React**, and powered by **Google Gemini** and **OpenAI's ChatGPT**, it delivers a smart, real-time AI web design experience.

---

## 🧠 Key Features

### 🗣️ Conversational Website Generation
Just say what you want — the AI will generate a full structured JSON layout of your site.

### 🧩 Modular, Component-Based Architecture
Each site is made from individual UI components like `Hero`, `Header`, `Section`, `Card`, etc., making it easy to edit or rearrange without breaking layout integrity.

### ✨ Multi-Model LLM Support
Started with Gemini, but added **ChatGPT support** for versatility. The app dynamically switches models to leverage the best of both worlds — a feature Lovable.dev doesn’t offer.

### 🧠 Prompt Intelligence
Automatically detects the **website type** (e.g., ecommerce, blog, portfolio) and injects tailored context into LLM prompts for more accurate, stylish outputs.

### 🛠️ Real-Time Preview & Editing
Includes optional live preview UI. As you type your prompts, watch the layout render instantly.

### 🔧 Smart Edit Mode
Send an existing layout + an update instruction, and the AI will modify only the relevant section intelligently.

### 📡 Live WebSocket Backend
FastAPI + WebSocket enable real-time, stateful conversations with the AI backend.

---

## 🚀 What's Unique / WOW Factors

- ✅ **Multi-model AI Switching (Gemini + ChatGPT)**
- ✅ **Context-aware prompt enhancements** based on site type
- ✅ **Live component editing**
- ✅ **High-fidelity layout output** in structured JSON
- ✅ **Clean UI inspired by Lovable.dev**
- ✅ **Future-ready architecture**: modular and extendable

---

## 📦 Tech Stack

| Layer      | Tech Used                           |
|------------|-------------------------------------|
| Backend    | FastAPI + WebSocket + Python        |
| AI Models  | Google Gemini (`gemini-2.0-flash`) + OpenAI GPT-4 |
| Frontend   | React + Vite + TailwindCSS + MUI    |
| Data       | JSON-based UI Component Trees       |

---

## 🛠️ Setup Instructions

### 1. 🧠 Backend Setup (FastAPI)

```bash
git clone https://github.com/your-username/NewAgeBuilder.git
cd NewAgeBuilder/backend

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add API keys
touch .env
echo "GEMINI_API_KEY=your_gemini_key_here" >> .env
echo "OPENAI_API_KEY=your_openai_key_here" >> .env

# Run server
uvicorn main:app --reload
```

---

### 2. 🎨 Frontend Setup (React + Tailwind + Vite)

```bash
cd ../frontend
npm install
npm run dev
```

⚠️ **Having issues with peer dependencies?**

Try:

```bash
npm install --legacy-peer-deps
```

Or switch to:

```bash
yarn install
yarn dev
# OR
pnpm install
pnpm dev
```

> 💡 Requires Node.js >= 18  
Check your version with `node -v`

---

## 🛠️ Example Prompts

- “Create a hero section with title ‘Welcome to NewAgeBuilder’ and a CTA to start building.”
- “Add a 3-column features section showcasing fast generation, live preview, and export support.”
- “Update the footer to include Twitter and GitHub icons.”
- “Make the background dark and futuristic with neon accent colors.”

---

## 🧪 Folder Structure

```
NewAgeBuilder/
├── backend/
│   ├── main.py              # FastAPI backend with WebSocket and LLM logic
│   ├── .env                 # API keys
│   ├── requirements.txt
│
├── frontend/                # Optional UI live preview
│   ├── src/
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│
└── README.md
```

---

## 🔮 Future Improvements

- 🖼️ AI-generated images or assets for UI (via Gemini Vision / DALL·E)
- 💡 UI component visual editing (drag or inline tweak)
- 🌍 Export to HTML / React source code
- 🧠 Fine-tuned AI persona for style-specific websites (e.g., minimal, vintage, startup)
- 📦 Plugin system for custom components or themes

---

## 🤝 Contributions Welcome

Have ideas? Want to extend support for Claude or LLaMA? Submit a PR!

Let’s build the future of conversational website creation — together.  
✨ Star the repo if you love it!

---

Made with ❤️ by Suvi De Silva
