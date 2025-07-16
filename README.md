# 🧠 Reddit Persona Extractor (with Ollama)
This project builds a user persona by analyzing a Reddit user's posts and comments using local LLMs via Ollama.
It extracts structured insights like age, location, motivations, goals, frustrations, and personality traits — with source citations.

# 📦 Features
    1.Scrapes Reddit comments & posts
    2.Extracts facts using regex (age, occupation, etc.)
    3.Generates deep insights using local LLMs (via Ollama)
    4.Outputs clean .txt persona files
    5.Fully offline LLM (no OpenAI API needed)

# 🛠️ Setup Instructions
  1. 🔧 Install Ollama
      Go to https://ollama.com/download and install for your OS.
      After installation, run the model:

      bash
      ollama run llama3

  2. 💻 Clone the Repository
      bash
      git clone https://github.com/your-username/reddit-persona.git
      cd reddit-persona
     
  3. 🐍 Create and Activate a Virtual Environment
      bash
      python -m venv venv
      .\venv\Scripts\activate   # Windows
      OR
      source venv/bin/activate  # Mac/Linux
     
  4. 📥 Install Dependencies
      bash
      pip install -r requirements.txt
     
  5. 🔐 Configure Environment Variables
    Create a .env file in the root directory:

     env
      REDDIT_CLIENT_ID=your_reddit_app_id
      REDDIT_CLIENT_SECRET=your_reddit_app_secret
      REDDIT_USER_AGENT=persona-script
      
      OLLAMA_URL=http://localhost:11434
      OLLAMA_MODEL=llama3
      You can create Reddit API credentials here: https://www.reddit.com/prefs/apps

  # 🚀 How to Run
  To generate a persona for any public Reddit profile, run:
  bash
    python main.py https://www.reddit.com/user/<username>/

📁 Folder Structure
    bash

reddit-persona/
│
├── main.py                     # Entry script
├── .env                        # Environment variables
├── requirements.txt            # Python dependencies
├── examples/                   # Output folder
├── persona/
│   ├── scraper.py              # Reddit API scraping
│   ├── extractor.py            # Regex + LLM persona generation
│   ├── model.py                # Persona dataclass
│   ├── renderer.py             # Jinja2 .txt output
│   ├── templates/
│   │   └── template.txt.j2     # Text template format

📌 Notes
This works entirely offline (after model is downloaded via Ollama).
Ensure Ollama is running (ollama run llama3) before running the script.
If LLM output format breaks, regex-extracted fields will still be used.
