from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
import json
from dotenv import load_dotenv
import os
import traceback
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
import re
import random

from openai import OpenAI

dummy_responses = [
  {
    "type": "Header",
    "logo": {
      "src": "https://picsum.photos/100/50",
      "alt": "Logo"
    },
    "navigation": [
      { "label": "Home", "link": "#home" },
      { "label": "About", "link": "#about" },
      { "label": "Contact", "link": "#contact" }
    ],
    "callToAction": {
      "label": "Get Started",
      "link": "#start"
    },
    "style": {
      "backgroundColor": "#000",
      "color": "#fff",
      "padding": "1rem",
      "display": "flex",
      "justifyContent": "space-between",
      "alignItems": "center"
    }
  },
  {
    "type": "Hero",
    "title": "Welcome to AI Builder",
    "subtitle": "Build websites with the power of AI",
    "backgroundImage": "https://picsum.photos/1200/400",
    "callToAction": {
      "label": "Try Now",
      "link": "#try",
      "style": {
        "backgroundColor": "#2196f3",
        "color": "#fff",
        "padding": "10px 20px",
        "borderRadius": "4px"
      }
    },
    "style": {
      "textAlign": "center",
      "padding": "4rem 2rem",
      "color": "#fff"
    }
  },
  {
    "type": "Section",
    "title": "Features",
    "layout": "grid",
    "columns": 3,
    "style": {
      "padding": "2rem",
      "backgroundColor": "#f5f5f5"
    },
    "children": [
      {
        "type": "Card",
        "title": "Fast Generation",
        "image": "https://picsum.photos/200/150",
        "content": "Generate UI components instantly with a single prompt."
      },
      {
        "type": "Card",
        "title": "Live Preview",
        "image": "https://picsum.photos/200/151",
        "content": "See what you build in real time as you edit."
      },
      {
        "type": "Card",
        "title": "Export Code",
        "image": "https://picsum.photos/200/152",
        "content": "Export React or HTML code for production use."
      }
    ]
  },
  {
    "type": "Footer",
    "content": "© 2025 AI Builder. All rights reserved.",
    "socialLinks": [
      { "icon": "fab fa-twitter", "link": "https://twitter.com" },
      { "icon": "fab fa-github", "link": "https://github.com" }
    ],
    "style": {
      "backgroundColor": "#111",
      "color": "#fff",
      "textAlign": "center",
      "padding": "1rem"
    }
  }
]

# Load environment variables
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

if not gemini_key:
    raise ValueError("GEMINI_API_KEY is not set in .env file")
if not openai_key:
    raise ValueError("OPENAI_API_KEY is not set in .env file")

# Configure clients
genai.configure(api_key=gemini_key)
gemini_model = genai.GenerativeModel('gemini-2.0-flash')
client = OpenAI()

# Templates
COMPONENT_TEMPLATES = {
    'Header': {
        'type': 'Header',
        'title': '',
        'subtitle': '',
        'logo': '',
        'navigation': [],
        'cta': {}
    },
    'Hero': {
        'type': 'Hero',
        'title': '',
        'subtitle': '',
        'image': '',
        'cta': {}
    },
    'Section': {
        'type': 'Section',
        'id': '',
        'title': '',
        'content': '',
        'image': '',
        'layout': '',
        'items': [],
        'testimonials': [],
        'display': '',
        'columns': 0
    },
    'Pricing': {
        'type': 'Pricing',
        'id': '',
        'title': '',
        'plans': []
    },
    'ContactForm': {
        'type': 'ContactForm',
        'id': '',
        'title': '',
        'fields': [],
        'submitButtonLabel': ''
    },
    'Footer': {
        'type': 'Footer',
        'content': '',
        'socialLinks': []
    },
    'hero': {'type': 'hero', 'title': '', 'subtitle': ''},
    'card': {'type': 'card', 'title': '', 'description': ''},
    'text': {'type': 'text', 'content': ''}
}


# App setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        print("[WS] Connected")
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        print("[WS] Disconnected")
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict):
        print(f"[WS] Broadcasting: {message}")
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

# Helpers
def extract_json_from_response(response_text: str) -> str:
    print("[AI] Raw response before cleanup:", response_text)
    cleaned = re.sub(r"```(?:json)?", "", response_text).replace("```", "").strip()
    print("[AI] Cleaned JSON string:", cleaned)
    return cleaned

def detect_website_type(prompt: str) -> str:
    prompt_lower = prompt.lower()
    if "ecommerce" in prompt_lower or "shop" in prompt_lower or "store" in prompt_lower:
        return "ecommerce"
    elif "saas" in prompt_lower or "software" in prompt_lower or "dashboard" in prompt_lower:
        return "saas"
    elif "portfolio" in prompt_lower or "developer" in prompt_lower or "designer" in prompt_lower:
        return "portfolio"
    elif "blog" in prompt_lower or "articles" in prompt_lower:
        return "blog"
    else:
        return "general"

# Memory of responses
responses = []

# Core processing function
async def process_prompt_with_ai(prompt: str, components: Optional[List[Dict]] = None, model_choice: str = "gemini") -> Dict:
    try:
        print(f"[AI] Processing prompt with model: {model_choice}")
        site_type = detect_website_type(prompt)

        type_specific_guidance = {
    "ecommerce": """
Design a high-converting eCommerce site with:
- A visually appealing product showcase (grid or carousel)
- Filterable categories or tags
- Clear product cards with price, image, and "Add to Cart"
- A promotional banner or featured deal
- Prominent CTAs like "Shop Now", "Buy", or "Get Deal"
- Customer testimonials and trust badges
""",
    "saas": """
Design a sleek, conversion-focused SaaS website that includes:
- A feature-rich Hero with CTA (e.g., "Start Free Trial")
- A section explaining core product features
- Pricing plans in a 3-column layout with CTA buttons
- Testimonials from users or companies
- Integrations or platform logos
- Clean footer with legal links and socials
""",
    "portfolio": """
Design a visually strong portfolio site for a creative professional:
- Hero with name, title (e.g., "Full-Stack Developer"), and CTA
- Project gallery with images and project descriptions
- About section with skills and tech stack
- Testimonials or client quotes
- Contact form with modern styling
""",
    "blog": """
Design a minimal and readable blog layout:
- Hero with blog title and description
- Latest post previews (title, date, image, excerpt)
- Sidebar with categories, tags, or newsletter signup
- Author bio or About section
- Clean footer with social links
""",
    "general": """
Design a clean, modern multi-purpose site:
- A bold Hero with a strong message and CTA
- Features or services section
- Visual testimonials or trust section
- Pricing (if applicable)
- Contact form or newsletter signup
- Footer with essential links
"""
}


        guidance = type_specific_guidance[site_type]
        print(f"[AI] Detected website type: {site_type}")

        system_prompt = f"""
You are a senior UI/UX designer and AI-powered frontend engineer.

TASK:
Translate the users natural language website prompt into a valid JSON array representing UI layout components for a modern, responsive website.

{guidance}

🔥 FOCUS ON MODERN DESIGN:
- Prioritize beautiful layout flow, balanced whitespace, and visual hierarchy
- Design must feel premium — like Stripe, Linear, Notion, Vercel, Framer
- Include responsive layout and attractive styling for each component
- Mobile-friendly spacing, centered alignment, and good readability

🧩 SUPPORTED COMPONENT TYPES:
- Header (with logo, navigation, CTA)
- Hero (title, subtitle, backgroundImage, CTA)
- Section (title, layout, children)
- Card (inside Section or Testimonials)
- Text (styled block text)
- Image (with src and alt)
- Pricing (title, plans array)
- ContactForm (with fields, CTA)
- Footer (content, socialLinks)

📦 COMPONENT FORMAT:
Each object must follow:

{{
  "type": "ComponentType",
  "title": "...",
  "subtitle": "...",
  "content": "...",
  "image": "...",
  "backgroundImage": "...",
  "cta": {{
    "label": "...",
    "href": "...",
    "style": {{ "backgroundColor": "#...", "color": "#..." }}
  }},
  "style": {{
    "backgroundColor": "#...",
    "color": "#...",
    "padding": "...",
    "margin": "...",
    "textAlign": "...",
    ...
  }},
  "children": [ ... ]
}}

🎨 STYLE RULES:
- Always include a "style" object per component and per card
- Use padding (e.g. "2rem"), borderRadius (e.g. "8px"), textAlign
- Set "color" and "backgroundColor" based on contrast best practices
- Use high-quality image URLs (e.g. `https://source.unsplash.com/...`)

🖼 IMAGE RULES:
- Hero uses "backgroundImage"
- Cards or image blocks use "image"
- Logos must be in "logo": {{ "src": "...", "alt": "..." }}

📱 RESPONSIVE DESIGN:
- Use CSS units like rem, %, auto, maxWidth
- Apply grid or flex for layout with mobile fallbacks
- Ensure spacing, alignment, and font sizes scale on devices

✏️ WHEN EDITING EXISTING COMPONENTS:
- Update only the relevant items passed
- Do not repeat unchanged parts
- Match by `type`, `id`, or `title` if available

📌 SPECIAL RULE — FULL BACKGROUND:
If the user prompt says “make the site red” or “background yellow”, wrap all components in:

{{
  "type": "Section",
  "style": {{ "backgroundColor": "red" }},
  "children": [ ... ]
}}

🚫 DO NOT:
- Use markdown (no ```json)
- Add any comments or explanations
- Include invalid JSON

🎯 GOAL:
Output a clean, readable, and **fully valid** JSON array — nothing else.
"""


        # -------------------- OPENAI --------------------
        if model_choice == "openai":
            print("[AI] Mode: Chat GPT - OpenAI")
            messages = [{"role": "system", "content": system_prompt}]

            if components:
                messages.append({
                    "role": "user",
                    "content": f"Update this layout based on the following prompt:\n\n{prompt}\n\nExisting layout:\n{json.dumps(components)}"
                })
            else:
                messages.append({"role": "user", "content": prompt})

            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=2048
            )
            response_text = response.choices[0].message.content.strip()
            print("=== GPT Response Start ===\n")
            print(response_text)
            print("\n=== GPT Response End ===")

        # -------------------- GEMINI --------------------
        else:
            user_parts = [system_prompt, "User prompt:", prompt]

            if components:
                user_parts.append("Existing page layout as JSON:")
                user_parts.append(json.dumps(components))
                user_parts.append("Update this layout according to the prompt.")
                print("[AI] Mode: EDIT")
            else:
                user_parts.append("Generate a brand new layout from scratch.")
                print("[AI] Mode: CREATE")

            response = gemini_model.generate_content(user_parts)
            response_text = response.text.strip()
            print("=== Gemini Response Start ===\n")
            print(response_text)
            print("\n=== Gemini Response End ===")

        # Validation / Cleanup
        if "componentName" in response_text or "properties" in response_text:
            print("[⚠️ WARNING] Response contains non-standard schema keys like 'componentName'")

        responses.append(response_text)
        clean_json = extract_json_from_response(response_text)
        component_list = json.loads(clean_json)

        if not isinstance(component_list, list):
            component_list = [component_list]

        return {
            "action": "update_component",
            "mode": "edit" if components else "create",
            "message": f"Generated {len(component_list)} component(s)",
            "payload": component_list
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "action": "update_component",
            "message": "❌ Failed to generate component(s)",
            "payload": [{"type": "text", "content": str(e)}]
        }


# GET endpoint
@app.get("/responses")
async def get_all_responses():
    return {"responses": responses}

# WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print(f"[WS] Received: {data}")

            prompt_text = data.get("content", "").strip()
            components = data.get("components") if "components" in data else None
            model_choice = data.get("model", "gemini")

            if prompt_text:
                print(f"[WS] MODE: {'edit' if components else 'create'} | MODEL: {model_choice}")
                ai_response = await process_prompt_with_ai(prompt_text, components, model_choice)
                await websocket.send_json(ai_response)
            else:
                await websocket.send_json({"error": "Prompt is empty"})

    except WebSocketDisconnect:
        print("[WS] Client disconnected")
        manager.disconnect(websocket)

    except Exception as e:
        print(f"[WS] Unexpected error: {e}")
        traceback.print_exc()
        try:
            await websocket.send_json({"error": str(e)})
        except:
            pass  # Silently fail if already closed
