# ImagineInk-AI-Comic-Generator

ImagineInk is an AI-powered storytelling and comic generation platform built using a modular pipeline. It uses Hugging Face Transformer LLMs for story generation and Stable Diffusion for comic panels, converting user prompts into coherent narratives with illustrated outputs.

\# ImagineInk

\### AI-Powered Interactive Storytelling \& Comic Generation



> \*Turn your imagination into stories and comics — effortlessly.\*



!\[Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square\&logo=python)

!\[FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?style=flat-square\&logo=fastapi)

!\[PyQt6](https://img.shields.io/badge/PyQt6-GUI-purple?style=flat-square)

!\[PyTorch](https://img.shields.io/badge/PyTorch-Inference-red?style=flat-square\&logo=pytorch)

!\[SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?style=flat-square\&logo=sqlite)

!\[License](https://img.shields.io/badge/License-Academic-orange?style=flat-square)



\---



\## About



\*\*ImagineInk\*\* is an AI-powered desktop application that bridges the gap between imagination and content creation. Users simply provide a prompt or idea, and the system generates a complete story — which can then be automatically converted into a multi-panel visual comic strip.



The system supports multiple story genres including \*\*Horror\*\*, \*\*Mystery\*\*, \*\*Fantasy\*\*, and \*\*Fairytale\*\*, and uses state-of-the-art AI models for both story and image generation — all running locally with GPU acceleration.



> Submitted as B.Tech Final Year Project at \*\*Banasthali Vidyapith, Rajasthan\*\*

> Under the supervision of \*\*Dr. Sneha Asopa\*\*, Assistant Professor, Department of Computer Science.



\---



\## Demo



\### Story Prompt

"Rescuing a princess from the haunted forest."



\### Generated Comic

!\[panel 1](panel\_0.png)



\## Team



| Name | Roll Number |

|------|-------------|

| Riya Agarwal | BTBTC23251 |

| Ruchi | BTBTC23316 |

| Suhani Mishra | BTBTC23195 |

| Tanvi Dureja | BTBTC23146 |

| Trisha Chaturvedi | BTBTC23335 |



\---



\## Features



\- \*\*AI Story Generation\*\* — Generate complete stories from simple prompts using a fine-tuned Gemma 2b-it LLM

\- \*\*Genre Selection\*\* — Choose from Horror, Mystery, Fantasy, or Fairytale

\- \*\*Comic Panel Generation\*\* — Convert stories into illustrated comic panels using Stable Diffusion

\- \*\*Speech Bubble Generation\*\* — Automatically adds speech bubbles to comic panels

\- \*\*Multi-Panel Comic Layout\*\* — Panels assembled into a final comic page using PIL

\- \*\*Regeneration Option\*\* — Regenerate story or comic with one click

\- \*\*Generation History\*\* — View, search, filter, and manage all previously created content

\- \*\*Export Options\*\* — Download stories as PDF/TXT and comics as JPEG/PNG

\- \*\*User Authentication\*\* — Secure login and signup with SHA-256 hashed passwords

\- \*\*Project Management\*\* — Organize stories and comics under named projects

\- \*\*GPU Accelerated Inference\*\* — FP16 + CUDA + attention slicing for fast generation



\---



\## System Architecture



ImagineInk follows a \*\*layered MVC architecture\*\*:



```

+--------------------------------------------------+

|           PyQt6 Desktop UI (Frontend)            |

|  Login · Signup · Dashboard · History · Comics   |

+--------------------------------------------------+

|           FastAPI REST Backend                   |

|    /generate-story  ·  /generate-comic           |

+--------------------------------------------------+

|            AI Service Layer                      |

|  +-----------------+    +----------------------+ |

|  |  Gemma 2b-it    |    |   Stable Diffusion   | |

|  |  (LoRA + PEFT)  |    |  (Image Generation)  | |

|  |  Story Model    |    |  Comic Panel Model   | |

|  +-----------------+    +----------------------+ |

|         |                         |              |

|   Panel Extraction Engine                        |

|   Comic Layout Engine (PIL)                      |

|   Speech Bubble Renderer                         |

+--------------------------------------------------+

|        Data Access Layer (SQLite)                |

|  Users · Projects · Prompts · Comics · Exports   |

+--------------------------------------------------+

```



\---



\## Tech Stack



| Component | Technology |

|-----------|------------|

| GUI / Frontend | PyQt6 |

| Backend / API | FastAPI + Uvicorn |

| Story Generation | Gemma 2b-it (fine-tuned with LoRA + PEFT) |

| Comic Generation | Stable Diffusion 2.1 |

| NLP Framework | HuggingFace Transformers |

| Image Framework | HuggingFace Diffusers |

| Fine-tuning | PEFT (Parameter Efficient Fine Tuning) |

| Image Processing | PIL / Pillow, OpenCV |

| Database | SQLite |

| Training Framework | PyTorch (FP16 + CUDA) |

| Language | Python 3.10+ |



\---



\## Hardware Requirements



\*\*Minimum:\*\*

\- Processor: Intel Core i5

\- RAM: 8 GB

\- Storage: 20 GB free space

\- GPU: NVIDIA GPU with 4 GB VRAM

\- Display: 1280 x 720



\*\*Recommended:\*\*

\- Processor: Intel Core i7

\- RAM: 16 GB

\- Storage: 20+ GB free space

\- GPU: NVIDIA RTX / DGX with 8 GB VRAM

\- Display: 1920 x 1080



\*\*Used for Development \& Deployment:\*\*

\- NVIDIA DGX Server (Backend deployed and tested on DGX)



\---



\## Optimizations Used



\- FP16 (float16) inference for reduced memory usage

\- CUDA GPU acceleration

\- Attention slicing for Stable Diffusion

\- Gradient checkpointing during training

\- Efficient prompt engineering for panel generation



\---



\## Installation



\### 1. Clone the Repository



```bash

git clone https://github.com/Riyaagarwal29/ImagineInk.git

cd ImagineInk

```



\### 2. Create Conda Environment



```bash

conda create -n imagineink python=3.10

conda activate imagineink

```



\### 3. Install Dependencies



```bash

pip install -r requirements.txt

```



\### 4. Download AI Models



Download and place models inside the `models/` folder:



\*\*Gemma 2b-it\*\* (Story Generation):

```

https://huggingface.co/google/gemma-2b-it

Place in: models/gemma-2b-it/

```



\*\*LoRA Adapter Weights\*\* (Fine-tuned):

```

Place in: models/model/

```



\*\*Stable Diffusion 2.1\*\* (Comic Generation):

```

https://huggingface.co/stabilityai/stable-diffusion-2-1

Place in: models/stable\_diffusion\_local/

```



\### 5. Start the Backend Server



```bash

cd backend

uvicorn api\_server:app --host 0.0.0.0 --port 8000

```



\- Backend runs at: `http://127.0.0.1:8000`

\- Health check: `http://127.0.0.1:8000/health`

\- API docs (Swagger UI): `http://127.0.0.1:8000/docs`



\### 6. Launch the Frontend



```bash

python main.py

```



\---



\## Project Structure



```

ImagineInk/

|

+-- backend/                          # FastAPI Backend

|   +-- api\_server.py                 # API routes (/generate-story, /generate-comic)

|   +-- model\_service.py              # Gemma 2b-it story generation

|   +-- comic\_service.py              # Stable Diffusion comic pipeline

|   +-- story\_service.py              # Story worker thread (PyQt signal)

|   +-- auth.py                       # Login validation, password hashing

|   +-- database.py                   # SQLite CRUD operations

|   +-- dataset\_loader.py             # Training data loader

|   +-- train.py                      # LoRA fine-tuning script

|   +-- comic\_output/                 # Generated comic images saved here

|

+-- models/                           # AI Model weights (not tracked by git)

|   +-- gemma-2b-it/                  # Base Gemma model

|   +-- model/                        # LoRA adapter weights

|   +-- stable\_diffusion\_local/       # Stable Diffusion model

|

+-- dataset/                          # Custom training dataset (stories)

|

+-- frontend/                         # PyQt6 GUI

|   +-- main.py                       # App entry point

|   +-- login\_page.py                 # Login screen

|   +-- signup\_page.py                # Signup screen

|   +-- main\_app.py                   # Main dashboard

|   +-- history\_page.py               # Generation history

|   +-- ui/

|   |   +-- dialogs.py                # Error/success dialogs

|   |   +-- comic\_window.py           # Comic viewer window

|   +-- assets/                       # Background images, icons

|

+-- requirements.txt

+-- README.md

```



\---



\## Generation Pipeline



```

1\. User enters prompt + selects genre

&#x20;          |

2\. FastAPI backend receives request

&#x20;          |

3\. Fine-tuned Gemma 2b-it generates full story

&#x20;          |

4\. Story auto-saved to SQLite database

&#x20;          |

5\. Panel Extraction Engine splits story into scenes

&#x20;          |

6\. Image prompts created for each panel

&#x20;          |

7\. Stable Diffusion generates panel images (1024x768)

&#x20;          |

8\. Speech bubbles added to each panel (PIL)

&#x20;          |

9\. Multi-panel comic layout assembled

&#x20;          |

10\. Comic saved to comic\_output/ folder

&#x20;          |

11\. User can export as PDF / JPEG / PNG

```



\---



\## Database Schema



The system uses \*\*SQLite\*\* with the following 5 tables:



| Table | Key Columns | Description |

|-------|-------------|-------------|

| `users` | user\_id, username, email, password\_hash | User accounts |

| `projects` | project\_id, user\_id, title | Story projects |

| `prompts` | prompt\_id, project\_id, original\_prompt, generated\_story, mode | Stories |

| `comics` | comic\_id, prompt\_id, comic\_path | Comic panel paths |

| `export\_history` | history\_id, project\_id, export\_type, file\_path | Export records |



\---



\## Testing



All modules were tested and passed:



| Test Case | Status |

|-----------|--------|

| Login Authentication (valid credentials) | Pass |

| Invalid Login (wrong credentials) | Pass |

| User Registration (new account) | Pass |

| Story Generation (prompt input) | Pass |

| Story Regeneration | Pass |

| Comic Generation (story to panels) | Pass |

| Database Storage (story saved) | Pass |

| Generation History Retrieval | Pass |

| Export Feature (PDF / Image) | Pass |

| System Performance (large prompt) | Pass |



\---



\## Future Improvements



\- Web-based deployment of the application

\- Multi-page comic generation

\- Style customization for comics

\- Character consistency across panels

\- Faster diffusion inference

\- Mobile app version



\---



\## Requirements



```

fastapi

uvicorn

torch

transformers

diffusers

accelerate

peft

pillow

requests

pydantic

huggingface\_hub

sentencepiece

safetensors

scipy

numpy

xformers

opencv-python

PyQt6

sqlite3

reportlab

textwrap

```



\---



\## References



\- Google DeepMind, \*Gemma: Open Models based on Gemini Research\*, 2024

\- \[HuggingFace Transformers](https://huggingface.co/docs/transformers)

\- \[HuggingFace Diffusers](https://huggingface.co/docs/diffusers)

\- \[PEFT Documentation](https://huggingface.co/docs/peft)

\- \[FastAPI Documentation](https://fastapi.tiangolo.com/)

\- \[PyQt6 Documentation](https://doc.qt.io/qtforpython/)

\- \[Stable Diffusion — Stability AI](https://stability.ai/)

\- \[SQLite Documentation](https://www.sqlite.org/docs.html)

\- Ian Goodfellow, Yoshua Bengio, Aaron Courville, \*Deep Learning\*, MIT Press, 2016



\---



\## Institution



\*\*Department of Computer Science\*\*

Banasthali Vidyapith, Rajasthan

B.Tech Final Year Project — 2025–2026



\---



\## License



This project is licensed under the MIT License.  

See the LICENSE file for details.

\## Model \& Third-Party Licenses



This project uses pre-trained models from Hugging Face, Google (Gemma), and Stability AI (Stable Diffusion).  

These models are subject to their respective licenses and usage terms.



\*Made with love by Team ImagineInk\*



\*Create • Imagine • Visualize\*

