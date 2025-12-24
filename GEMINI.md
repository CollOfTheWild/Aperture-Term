# PROJECT: APERTURE-TERM (The Cognition Dashboard)

## 1. MISSION PROFILE
**Goal:** Build a Textual-based TUI (Terminal User Interface) that acts as a "System 2" wrapper for local LLMs. It is designed to look like a Sci-Fi flight deck (Cyberpunk/Aperture Science aesthetic) while providing advanced features like web-search context injection and hardware telemetry.

**Target Hardware:**
* **Dev (Current):** GTX 970 (4GB VRAM). *Constraint: Must be highly optimized, small models only.*
* **Prod (Dec 29, 2025):** RTX 3090 (24GB VRAM). *Goal: High-speed inference, larger models.*
* **OS:** Linux/WSL (Primary).

**Deadline:** MVP must be functional by December 29, 2025.

---

## 2. ARCHITECTURE & STACK

### Core Technologies
* **Language:** Python 3.10+
* **Frontend (TUI):** `textual` (CSS-driven TUI framework), `rich` (Rendering).
* **Backend (LLM):** `llama-cpp-python` (with CUDA/cuBLAS bindings).
* **Tools:** `duckduckgo-search` (Web context), `nvidia-ml-py` (NVIDIA stats), `psutil` (System stats).

### File Structure (Strict Adherence)
```text
aperture-term/
├── app.py                 # Main Entry Point (The Grid Layout)
├── requirements.txt       # Dependencies
├── assets/
│   └── theme.json         # CSS Variable definitions
├── components/            # UI Widgets (One file per panel)
│   ├── __init__.py
│   ├── armory.py          # [Top-Left] Model Loader & Config
│   ├── context_swarm.py   # [Top-Right] Search & RAG Tools
│   ├── flight_deck.py     # [Bot-Left] Chat Interface
│   └── telemetry.py       # [Bot-Right] Hardware Vitals
└── backend/               # Logic Layer
    ├── __init__.py
    ├── llm_wrapper.py     # Llama.cpp class (Threaded/Async)
    └── search_tool.py     # Search logic
```
3. COMPONENT SPECIFICATIONS (MVP)
A. The Grid (app.py)
Layout: 2x2 Grid.

Row 1 (40% height): Armory (50%) | Context Swarm (50%)

Row 2 (60% height): Flight Deck (50%) | Telemetry (50%)

Styling: Dark theme (#0f111a background). Heavy borders. Vim-style keybindings for navigation (TAB to cycle, j/k to scroll).

B. The Armory (components/armory.py)
Function: Loads/Unloads GGUF models.

Features:

Display current model name and quantization.

Visual "Neofetch" card (ASCII art) for the loaded model family (Llama, Mistral, etc.).

Logic: Must handle model loading in a separate thread to avoid freezing the TUI.

C. The Flight Deck (components/flight_deck.py)
Function: Main chat interface.

Features:

Input box at the bottom.

Scrolling log for chat history.

System 2 Logic: User types -> Input locks (Red/Yellow state) -> Context Fetch (optional) -> Inference -> Stream output token-by-token.

D. Context Swarm (components/context_swarm.py)
Function: Manual Search Tool (MVP).

Features:

User can type /search <query> in the main chat or focus this panel to search.

Results (Snippets) are displayed here.

Selected results are injected into the next prompt's system context.

E. Telemetry (components/telemetry.py)
Function: Hardware monitoring.

Features:

GPU: Use pynvml to show VRAM usage (Used/Total) and Temp.

CPU/RAM: Use psutil.

Update Rate: 1Hz (1 second interval).

4. CRITICAL CODING GUIDELINES
Async/Threading is Mandatory: llama-cpp-python is blocking. ALL inference and loading calls must be wrapped in asyncio.to_thread or a Worker class so the TUI animation never stutters.

CUDA Installation: Do not use standard pip for llama-cpp. Always use: CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python

Error Handling: If the GPU runs OOM (Out of Memory), catch the exception gracefully and display a Red Toast notification in the TUI. Do not crash to desktop.

Aesthetics: Use rich for coloring logs. Text should be Amber (#ffb86c) or Cyan (#8be9fd) depending on state (Thinking vs. Output).

5. DEVELOPMENT SPRINT (Dec 24 - Dec 29)
Phase 1: Skeleton & Layout (Get the boxes on screen). [COMPLETED]

Phase 2: Telemetry & Search (Get the easy data flowing). [IN PROGRESS]

Phase 3: The LLM Backend (Threaded loading & inference).

Phase 4: Integration (Connecting Chat Input -> Backend -> UI).

6. USER CONTEXT
The user is a "Solutions Engineer" with a strong background in self-hosting (Homelab) and hardware. They prefer "Cyberpunk/Industrial" aesthetics. They are moving from a GTX 970 to a 3090.