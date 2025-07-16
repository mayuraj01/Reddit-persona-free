import argparse
from pathlib import Path
from persona.scraper import fetch_history
from persona.extractor import build_persona
from persona.renderer import render_persona

def cli() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a UX-style user persona from a Reddit profile."
    )
    parser.add_argument("profile_url", help="Full Reddit profile URL")
    parser.add_argument("-n", "--limit", type=int, default=250,
                        help="Maximum posts + comments to fetch (default: 250)")
    parser.add_argument("-o", "--out", default=".", help="Output directory")
    args = parser.parse_args()

    username = args.profile_url.rstrip("/").split("/")[-1]
    history = fetch_history(username, args.limit)
    persona = build_persona(username, history)

    out_file = Path(args.out) / f"{username}_persona.txt"
    render_persona(persona, out_file)
    print(f"✅  Persona saved to {out_file.resolve()}")

if __name__ == "__main__":
    cli()
