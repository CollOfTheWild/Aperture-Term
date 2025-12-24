# Aperture-Term

Aperture-Term: The Cognition Dashboard 👁️

      / \
     / _ \      Aperture-Term TERMINAL v0.1
    | / \ |     [CONNECTED]
    | \_/ |     System 2 Wrapper for Llama.cpp
     \___/      
     
Aperture-Term is a Textual-based TUI designed for the /r/UnixPorn generation. It is not just a chat client; it is a Cognition Flight Deck for steering 1B parameter models through complex reasoning tasks using asynchronous context injection and swarm voting.

It is designed to feel like htop met Neofetch inside a Cyberpunk novel.

🖥️ The Interface (The Grid)
Aperture-Term uses a rigid, tiled grid layout optimized for 1080p+ terminal emulators (Alacritty, Kitty, iTerm2).
```
+---------------------------------------+---------------------------------------+
| [MODEL LOADER & CARD]             [1] | [CONTEXT SWARM]                   [2] |
|                                       |                                       |
|  ________                             |  [FETCHING]  > Docker Docs ... [OK]   |
| |  META  |  Llama-3.2-1B-Instruct     |  [FETCHING]  > Python 3.12 ... [80%]  |
| |________|  Quant: Q4_K_M             |  [PENDING]   > "Circadia"  ... [WAIT] |
|             ctx: 8192 / 128k          |                                       |
|                                       |  [KV-CACHE STATUS]                    |
|  > Ready to Inference                 |  ██████████░░░░  65% INJECTED         |
+---------------------------------------+---------------------------------------+
| [SYSTEM 2 CHAT]                   [3] | [TELEMETRY & VIZ]                 [4] |
|                                       |                                       |
| User: How do I configure a [Docker]   |  GPU: [||||||||||] 89%  TMP: 65°C     |
|       container for a [Django] app?   |  RAM: [|||||     ] 12GB / 16GB        |
|                                       |                                       |
| Wheatley: Based on the docs...        |  [LOSS GRAPH - TTT]                   |
|                                       |  | \                                  |
| > [WAITING FOR CONTEXT...]            |  |  \__                               |
|                                       |  |_____\__________                    |
+---------------------------------------+---------------------------------------+
```
[1] Top Left: The Armory (Model Loader)
Hugging Face Browser: A scrollable list of models filtered by your Mac's hardware constraints (e.g., "Fits in 16GB").

Neofetch Cards: When a model loads, display a high-fidelity color ASCII logo of the lab (Meta, Mistral, Google, DeepSeek) alongside specs (Parameters, Quantization, Family).

Hot-Swap: Unload/Load models instantly with vim bindings.

[2] Top Right: The Context Swarm (Async Fetcher)
Real-Time Watcher: As you type in the Chat panel, this panel populates live.
```
Status Indicators:

[SCAN] Scanning input for entropy...

[FETCH] Scraper dispatched (URL visible).

[PARSE] Cleaning HTML/PDF to markdown.

[INJECT] Inserting into hidden System Prompt.
```
Visual Feedback: Items flash Green when fully integrated into the KV Cache.

[3] Bottom Left: The Flight Deck (Chat)

Entropy Highlighting:

Red: High-entropy noun detected, no context found.

Yellow: Fetching in progress.

Cyan: Context secured. Safe to send.

Safety Interlock: The input field locks the ENTER key if red/yellow entities exist, forcing the user to wait for the "Context Lock" (Cyan) before inference begins.

Thinking Viz: Collapsible <thinking> blocks that show the model's internal Chain of Thought (if enabled).

[4] Bottom Right: Telemetry & Vitals

Hardware Monitor: Real-time htop-style bars for GPU Load, Unified Memory pressure, and Temperature sensors.

Context Window: A visual bar showing Used / Available tokens.

Live Graphs:

Swarm Consensus: 3-node voting distribution.

TTT Loss: If Test-Time Training triggers, show the loss curve falling in real-time.

🛠️ The Stack
Frontend: Python + Textual (CSS for TUI).

Rendering: Rich (For ASCII art, markdown parsing, and syntax highlighting).

Backend: MLX (Apple Silicon Native) or llama-cpp-python.

Search: DuckDuckGo / Google Custom Search API.

🎨 Aesthetic & Theming
Aperture-Term supports json based themes. Ships with:

Wheatley (Default): Amber text, CRT scanlines, retro-industrial.

UnixPorn: Dracula/Nord color palette, minimal borders.

Matrix: Green-on-black, falling code animations in the background of empty panels.

⌨️ Keybindings (Vim-Native)
TAB Cycle panels.

j / k Scroll context lists or model lists.

/ Focus input.

:load <model> Quick load command.

:sleep Dump logs and shutdown.
