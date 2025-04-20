💡💡 **NewAgeBuilder – Conversational Website Creation with AI ✨**✨

**NewAgeBuilder** is a modular, no-code web builder inspired by Lovable.dev — but taken to the next level with **multi-model AI**, **intelligent prompt context**, and **real-time previewing**.

It allows users to create and edit entire websites just by chatting — no code required.

---

🧠 **Key Features**

### 🗣️ Natural Language Website Generation  
Simply describe what you want, and the AI turns it into structured, render-ready UI components.

### ♻ Multi-Model Support: Gemini + ChatGPT  
Started with **Gemini**, and later integrated **ChatGPT** for **multi-model experimentation**. Users can switch between LLMs to get varied creative styles and strengths — a standout feature even beyond Lovable.dev.

### 📙 Modular & Component-Based Architecture  
Websites are built from reusable components (Hero, Header, Section, Card, Pricing, Footer). This structure supports easy updates and real-time customization.

### ✍️ Smart Editing Mode  
Provide the current layout + an instruction — and the AI will surgically update just the necessary parts, intelligently.

### 🧠 Auto Context Detection  
Detects the **type of website** (e.g., eCommerce, SaaS, Blog, Portfolio) based on prompt, and enhances the prompt to generate more accurate layouts.

### ⚡ Real-Time AI via WebSocket  
Live WebSocket communication powers an interactive, chat-driven builder with low-latency updates.

### 🔍 Live Preview Support (Optional)  
Compatible with React-based frontends that render components or full layouts instantly, giving users immediate visual feedback.

### 🖼️ Future: Image Generation for Visual Components  
Plans to integrate UI image generation using Gemini Vision or DALL·E (e.g., for Hero/Illustration/Avatars).

### ♻ Future: Per-Component LLM Tagging  
Highlight which model (Gemini or ChatGPT) generated each section to help users understand LLM behavior.

### 🔧 No-Code Builder Experience  
Ideal for marketers, founders, and designers who want to prototype or publish beautiful websites — no dev help required.

### 🧪 Structured JSON Output  
Output is always clean, standardized JSON — perfect for rendering with React, Vue, or static HTML exports.

---

🛇 **Tech Stack**

- **Backend**: Python + FastAPI + WebSocket  
- **AI Models**: Google Gemini (gemini-2.0-flash), OpenAI GPT-4  
- **Prompting Strategy**: System prompt + inferred intent + optional layout  
- **Frontend (Optional)**: React + MUI (with split-pane live preview)

---

🚀 **Quick Start**

```bash
git clone https://github.com/your-username/NewAgeBuilder.git
cd NewAgeBuilder

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your Gemini and OpenAI API keys
echo 'GEMINI_API_KEY=your_gemini_key_here' >> .env
echo 'OPENAI_API_KEY=your_openai_key_here' >> .env

uvicorn main:app --reload
```

---

🛠️ **Example Prompts**

- “Create a hero section with title ‘Welcome to NewAgeBuilder’ and a CTA to start building.”  
- “Add a 3-column features section showcasing fast generation, live preview, and export support.”  
- “Update the footer to include Twitter and GitHub icons.”  
- “Make the whole site have a clean white background with modern fonts and soft shadows.”  

---

📁 **Folder Structure**

```bash
backend/
  ├── main.py            # FastAPI + WebSocket logic
  ├── utils/             # Helpers for LLM, JSON extraction, etc.
  ├── .env               # API keys

frontend/ (optional)
  └── React-based UI     # Live preview pane & interface
```

---

🌟 **What Makes It Special**

- ♻ Started with Gemini → scaled to **multi-model generation**
- 💡 Added **automatic website type detection**
- 🧠 Clean prompt enhancement improves LLM accuracy
- ⚙️ Real-time AI + structured JSON makes dev handoff easy
- 🌟 Future plans: **image generation**, **React export**, and **LLM introspection per component**

---

🤝 **Contributions Welcome**

Want to help build the future of conversational no-code tools? PRs, ideas, and feedback are all welcome!
