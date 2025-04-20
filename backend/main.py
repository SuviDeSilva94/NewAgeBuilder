from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
import json
import os
import traceback
import google.generativeai as genai
from dotenv import load_dotenv
import re
import random

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

responses = []

# Load environment variables
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env file")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

for m in genai.list_models():
    print(m.name, m.supported_generation_methods)

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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def extract_json_from_response(response_text: str) -> str:
    print("[AI] Raw response before cleanup:", response_text)
    cleaned = re.sub(r"```(?:json)?", "", response_text).strip()
    cleaned = cleaned.replace("```", "").strip()
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
    
async def process_prompt_with_ai(prompt: str, components: Optional[List[Dict]] = None) -> Dict:
    try:
        print(f"[AI] Processing prompt: {prompt}")

        type_specific_guidance = {
        "ecommerce": """
        If the website is eCommerce, make sure it includes:
        - Product grid or featured products
        - Categories or filters
        - Add to cart buttons
        - Promotions or banners
        - Clear CTAs like "Buy Now"
        """,
            "saas": """
        If the website is for SaaS, include:
        - Product explanation section
        - Pricing plans
        - Testimonials
        - Feature highlights
        - Call-to-action like "Start Free Trial"
        """,
            "portfolio": """
        If it's a portfolio, include:
        - Intro section with name & tagline
        - Project gallery
        - Skills/technologies
        - Contact form
        """,
            "blog": """
        If it's a blog, include:
        - Blog post previews (title, image, excerpt)
        - Categories/tags
        - About section
        - Newsletter signup
        """,
            "general": ""
        }
        
        # Detect type and get relevant guidance
        site_type = detect_website_type(prompt)
        extra_guidance = type_specific_guidance.get(site_type, "")
        print(f"[AI] Detected website type: {site_type}")


        system_prompt = """
You are a senior UI/UX engineer and AI assistant web developer.

{extra_guidance}

ALWAYS:
- Analyze and research websites in a similar domain or category.
- Ensure all components are relevant and visually consistent with each other.
- Think critically and creatively to design modern, user-friendly UI sections.
- Prioritize layout balance, clear hierarchy, and aesthetic harmony.
- Optimize for real-world usability, mobile responsiveness, and accessibility.

Your job is to generate or edit structured UI components in JSON format based on the user's natural language prompt.

GOAL:
Output a valid JSON array representing the UI structure of a webpage — either fully new or with updates to an existing structure.

OUTPUT FORMAT RULES:
- Output MUST be a single JSON array: [ {...}, {...}, ... ]
- Each object MUST follow this schema pattern:

{
  "type": "ComponentType",
  "title": "Optional title",
  "subtitle": "Optional subtitle",
  "content": "Optional content or description",
  "image": "Optional image path",
  "backgroundImage": "Optional background image path (only for Hero)",
  "cta": { "label": "", "href": "", "style": { ... } },
  "style": { "backgroundColor": "#hex", "color": "#hex", ... },
  ...other valid props per component
}

IMAGE HANDLING:
- Always use full URL paths for images (e.g., https://picsum.photos/200/300).
- Hero components must use "backgroundImage" instead of "image".
- Logos and image blocks must use:
  "logo": { "src": "https://...", "alt": "Logo Alt" }
- Use "src" for images only, not "link" or other fields.

STYLE RULES:
- "style" must always be a valid object.
  Example: "style": { "backgroundColor": "#FF5722" }
- Common style keys: backgroundColor, color, padding, margin, borderRadius, fontSize, textAlign

TEXT COLOR DEFAULTING:
- If backgroundColor is dark (e.g., black or dark gray), default text color to white: "#ffffff"
- If backgroundColor is light (e.g., white or cream), default text color to black: "#000000"
- Apply this to all components including Hero, Section, ContactForm, etc.

NAVIGATION BAR DEFAULT STYLE:
- Header (navigation) components must use:
  "style": {
    "backgroundColor": "#000000",
    "color": "#ffffff",
    "position": "sticky",
    "top": 0,
    "zIndex": 1000,
    "padding": "1rem",
    "display": "flex",
    "justifyContent": "space-between",
    "alignItems": "center"
  }

CONTACT FORM DEFAULT STYLE:
- If no background or text color is provided, use:
  "style": {
    "backgroundColor": "#2c2b2b",
    "color": "black",
    "padding": "2rem",
    "borderRadius": "8px"
  }

- ContactForm fields (minimum sample):
  "fields": [
    { "label": "Name", "type": "text", "required": true },
    { "label": "Email", "type": "email", "required": true },
    { "label": "Phone Number", "type": "tel", "required": false },
    { "label": "Message", "type": "textarea", "required": true }
  ]

SUPPORTED COMPONENT TYPES:
- Hero: title, subtitle, backgroundImage, CTA
- Header: logo, navigation, optional CTA
- Section: layout block (testimonials, features), grid/flex/default layout
- Card: inside Section, with title, image, content
- Text: stylable block of text
- Image: static image block with src, alt
- Pricing: title + plans [ { name, price, features[] } ]
- ContactForm: with fields and CTA
- Table: title, columns, rows
- Footer: content, socialLinks [ { icon, link } ]

DO NOT:
- Use markdown syntax (e.g., no ```json)
- Include explanation or comments
- Use "component":..., "props":... structure
- Duplicate components unnecessarily when editing

IF THE PROMPT IS FOR EDITING:
- Modify only the relevant component(s) passed in.
- Avoid duplication. Match by type, id, or title.

IF THE PROMPT IS FOR CREATION:
- Generate a full layout with proper structure, flow, and visual appeal.

FULL PAGE BACKGROUND RULE:
- If prompt mentions "site background", "make the website red", or similar:
  Wrap all components inside a parent Section:
  {
    "type": "Section",
    "style": { "backgroundColor": "red" },
    "children": [ ... ]
  }

RESPONSIVE DESIGN GUIDELINES:
- All components must render well on mobile, tablet, and desktop.
- Use responsive CSS values: rem, %, auto, maxWidth, etc.
- Layout components should use grid or flex properties with fallback responsiveness.
- Ensure content (including forms and buttons) resizes and aligns gracefully.

EXAMPLE STYLE:
"style": {
  "padding": "2rem",
  "textAlign": "center",
  "maxWidth": "1200px",
  "margin": "0 auto"
}

WRAPPING COMPONENTS:
- When applying a global background Section, also use:
"style": {
  "padding": "2rem",
  "backgroundColor": "#hex",
  "minHeight": "100vh",
  "width": "100%",
  "boxSizing": "border-box"
}

REAL-WORLD WEBSITE QUALITY & MODERN INSPIRATION:
- Design should resemble modern websites like Stripe, Airbnb, Notion, Shopify, Apple, Linear, Vercel, Framer.
- Follow best practices:
  - Clear hierarchy
  - Ample whitespace
  - Balanced contrast
  - Strong typography
  - Clean layout flow

Preferred layout flow for full sites:
1. Header (logo, navigation, CTA)
2. Hero (headline, subtext, CTA, background)
3. Features Section (3 to 4 cards in grid or flex)
4. Testimonials or Trust Section
5. Pricing (if relevant)
6. ContactForm or Newsletter Signup
7. Footer

IMAGE SOURCES (use full URLs):
- https://source.unsplash.com
- https://picsum.photos
- https://placeimg.com

VISUAL ACCESSIBILITY RULE:
- Always
A single raw JSON array only. No extra explanation, no markdown, no wrappers.
"""

        user_parts = [
            system_prompt,
            "User prompt:",
            prompt
        ]

        if components:
            user_parts.append("Existing page layout as JSON:")
            user_parts.append(json.dumps(components))
            user_parts.append("Update this layout according to the prompt.")
            print("[AI] Mode: EDIT")
        else:
            user_parts.append("Generate a brand new layout from scratch.")
            print("[AI] Mode: CREATE")

        response = model.generate_content(user_parts)
        response_text = response.text.strip()

        print(f"[AI] Raw response: {response_text}")
        responses.append(response_text)

        clean_json_str = extract_json_from_response(response_text)
        component_list = json.loads(clean_json_str)
        print("[AI] Parsed component list:", component_list)

        if not isinstance(component_list, list):
            component_list = [component_list]

        return {
            "action": "update_component",
            "mode": "edit" if components else "create",
            "message": f"Generated {len(component_list)} component(s)",
            "payload": component_list
        }

    except Exception as e:
        error_msg = f"AI processing failed: {str(e)}"
        traceback.print_exc()
        return {
            "action": "update_component",
            "message": "Failed to generate component(s)",
            "payload": [
                {
                    "type": "text",
                    "content": error_msg
                }
            ]
        }

@app.get("/responses")
async def get_all_responses():
    return {"responses": responses}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print(f"[WS] Received: {data}")

            if data.get("type") in ["prompt", "edit"]:
                prompt_text = data.get("content", "").strip()
                components = data.get("components") if "components" in data else None
                if prompt_text:
                    print(f"[WS] MODE: {'edit' if components else 'create'}")
                    ai_response = await process_prompt_with_ai(prompt_text, components)
                    await websocket.send_json(ai_response)
                else:
                    await websocket.send_json({"error": "Prompt is empty"})
            else:
                await websocket.send_json({"error": "Unsupported message type"})

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
