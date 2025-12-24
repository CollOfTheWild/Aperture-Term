# ASCII Art and Colors for Model Labs

LOGOS = {
    "meta": {
        "color": "#0668E1",
        "art": [
            '''
   ∞∞∞∞∞∞
 ∞∞      ∞∞
∞  META   ∞
 ∞∞      ∞∞
   ∞∞∞∞∞∞
            ''',
            '''
   oooooo
 oo      oo
o  META   o
 oo      oo
   oooooo
            '''
        ]
    },
    "mistral": {
        "color": "#FDAE4B",
        "art": [
            '''
    _    
   / \   
  / _ \  
 / ___ \ 
/_/   \_\
MISTRAL AI
            ''',
            '''
    _    
   / \   
  / _ \  
 / ___ \ 
/_/   \_\
mistral ai
            '''
        ]
    },
    "google": {
        "color": "#4285F4",
        "art": [
            '''
  G G G
 G     G
G  GEMINI
 G     G
  G G G
            ''',
             '''
  g g g
 g     g
g  gemini
 g     g
  g g g
            '''
        ]
    },
    "openai": {
        "color": "#10A37F",
        "art": [
            '''
   (   )
 (  O  )
( OPENAI )
 (  O  )
   (   )
            ''',
            '''
   /   \
 /  O  \
| OPENAI |
 \  O  /
   \   /
            '''
        ]
    },
     "deepseek": {
        "color": "#4B91F1",
        "art": [
            '''
  /\
 /  \
( DS )
 \  /
  \/
DEEPSEEK
            ''',
            '''
  []
 [  ]
( ds )
 [  ]
  []
deepseek
            '''
        ]
    },
    "qwen": {
        "color": "#6600CC",
        "art": [
            '''
 .---.
| QWEN |
 '---'
ALIBABA
            ''',
             '''
 .---.
| qwen |
 '---'
alibaba
            '''
        ]
    },
    "unknown": {
        "color": "#888888",
        "art": [
             '''
  [?]
UNKNOWN
 MODEL
  [?]
            ''',
             '''
  [!]
UNKNOWN
 MODEL
  [!]
            '''
        ]
    }
}

def get_logo(model_id: str):
    lid = model_id.lower()
    if "llama" in lid or "meta" in lid:
        return LOGOS["meta"]
    if "mistral" in lid or "mixtral" in lid:
        return LOGOS["mistral"]
    if "gemma" in lid or "gemini" in lid or "google" in lid:
        return LOGOS["google"]
    if "gpt" in lid or "openai" in lid:
        return LOGOS["openai"]
    if "deepseek" in lid:
        return LOGOS["deepseek"]
    if "qwen" in lid:
        return LOGOS["qwen"]
    return LOGOS["unknown"]
