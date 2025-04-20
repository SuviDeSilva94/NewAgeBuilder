💡 NewAgeBuilder – Conversational Website Creation with AI ✨
NewAgeBuilder is a modular, no-code web builder inspired by Lovable.dev, powered by Google Gemini.

It allows users to create and edit entire websites just by chatting — no code required.

🧠 Key Features
🗣️ Natural Language Website Generation
Simply describe what you want, and the AI will turn it into structured UI components.

🧩 Modular & Component-Based Architecture
Each website is built from composable components (e.g., Hero, Header, Section, Card, Footer), enabling fine-grained editing of any section without breaking the whole layout.

✍️ Smart Editing Mode
You can update existing layouts by sending both the layout and a new instruction. The AI intelligently updates only relevant sections.

⚡ Live WebSocket Communication
Real-time communication with the backend enables a chat-driven website-building experience.

🔍 (Optional) Live Preview Support
Integrates easily with frontend UIs that render components or full HTML in real-time for instant feedback.

🔧 No-Code Builder Experience
Designed for non-technical users, startups, or marketers to prototype or publish landing pages with ease.

🧪 Structured JSON Output
Output is always in clean, standardized JSON format — ideal for rendering in modern frontend frameworks.

🏗️ Tech Stack
Backend: Python + FastAPI + WebSocket

AI Model: Google Gemini (gemini-2.0-flash)

Prompting Strategy: System prompt + user intent + optional existing layout

Frontend (optional): React + MUI with split-pane live preview

🚀 Quick Start
bash
Copy
Edit
git clone https://github.com/your-username/NewAgeBuilder.git
cd NewAgeBuilder

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your Gemini API key to .env
echo 'GEMINI_API_KEY=your_api_key_here' > .env

# Run the backend
uvicorn main:app --reload
🛠️ Example Prompts
“Create a hero section with title ‘Welcome to NewAgeBuilder’ and a CTA to start building.”

“Add a 3-column features section showcasing fast generation, live preview, and export support.”

“Update the footer to include Twitter and GitHub icons.”

📁 Folder Structure
bash
Copy
Edit
backend/
  ├── main.py        # FastAPI server with WebSocket
  ├── .env           # API key
  ├── requirements.txt
frontend/
  └── (Optional) React-based live preview UI
🤝 Contributions Welcome
NewAgeBuilder is open to community contributions — help build the future of conversational no-code tools.
