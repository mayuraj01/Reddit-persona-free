from pathlib import Path
import jinja2
from .model import Persona

_ENV = jinja2.Environment(
    loader=jinja2.PackageLoader("persona"),  # looks for 'templates' inside 'persona'
    autoescape=jinja2.select_autoescape()
)
_TEMPLATE = _ENV.get_template("template.txt.j2")

def render_persona(persona: Persona, outfile: Path) -> None:
    """Write a pretty UX-persona text file."""
    text = _TEMPLATE.render(p=persona)
    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text(text, encoding="utf-8")
