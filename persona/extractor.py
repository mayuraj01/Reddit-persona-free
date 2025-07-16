"""
Turn raw Reddit history into a populated `Persona` object.

Strategy
--------
1. Quick regexes for very explicit facts (age, location, name, occupation).
2. Pass the *whole* history to a local LLM via Ollama to infer:
   - motivations (with 0‒10 importance scores)
   - goals (list)
   - frustrations (list)
   - personality (Big‑5 style, values 0‒1)
3. Store citations for every fact.
"""
import os
import re
import textwrap
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv

from .model import Persona, Citation

load_dotenv()
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# ---------- simple patterns ----------------------------------

AGE_RE = re.compile(r"\bI['’`]?m (\d{2})\b")                 # I'm 27
LOC_RE = re.compile(r"\b(?:live|living|based) in ([A-Z][\w ,.]+)", re.I)
OCC_RE = re.compile(r"\bI['’`]?m a[n]? ([A-Za-z ]+)\b")       # I'm a software engineer
NAME_RE = re.compile(r"My name is ([A-Z][a-z]+)")             # My name is Alex

# ---------- local LLM helper ---------------------------------

def _ollama(prompt: str) -> str:
    """Stream a completion from the local Ollama server (sync)."""
    resp = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=300,
    )
    resp.raise_for_status()
    return resp.json()["response"]

# ---------- public function ----------------------------------

def build_persona(username: str, history: List[Dict]) -> Persona:
    p = Persona(username=username)

    # -- rule‑based extraction -------------------------------------------------
    for item in history:
        body = item["body"]
        cite: Citation = {"kind": item["type"], "url": item["permalink"]}

        if not p.age and (m := AGE_RE.search(body)):
            p.add_fact("age", m.group(1), cite)
        if not p.location and (m := LOC_RE.search(body)):
            p.add_fact("location", m.group(1).strip(". "), cite)
        if not p.occupation and (m := OCC_RE.search(body)):
            p.add_fact("occupation", m.group(1).strip(), cite)
        if not p.name and (m := NAME_RE.search(body)):
            p.add_fact("name", m.group(1).strip(), cite)

    # -- LLM‑based extraction --------------------------------------------------
    joined = "\n=====  POST OR COMMENT  =====\n".join(  # keep below ~8k tokens
        f"{h['type'].upper()}: {h['body'][:2000]}" for h in history[:80]
    )

    system_prompt = textwrap.dedent(f"""\
    You are an expert UX researcher.

    Based ONLY on the Reddit content below, return a persona in this strict JSON format:

    {{
      "motivations": {{
        "Self-Improvement": 9,
        "Financial Security": 8
      }},
      "goals": [
        "Build side projects",
        "Learn machine learning"
      ],
      "frustrations": [
        "Toxic communities",
        "Lack of time"
      ],
      "personality": {{
        "Introvert": 0.83,
        "Thinking": 0.72
      }}
    }}

    DO NOT include any explanations or other text. Return ONLY JSON.
""")


    user_prompt = system_prompt + "\n\n### REDDIT HISTORY START ###\n" + joined

    llm_raw = _ollama(user_prompt)
    print("\n🔍 LLM RAW OUTPUT:\n", llm_raw)  # 👈 ADD THIS FOR DEBUGGING

    try:
        llm_json: Dict[str, Any] = __import__("json").loads(llm_raw)
    except Exception:
        # very rare; if parsing fails just leave fields empty but keep citation
        llm_json = {}

    # merge into Persona object
    cite_llm: Citation = {"kind": "llm", "url": "N/A"}

    for label, default in (
        ("motivations", {}),
        ("goals", []),
        ("frustrations", []),
        ("personality", {}),
    ):
        value = llm_json.get(label, default)
        setattr(p, label, value)
        p.citations[label] = [cite_llm]

    return p
