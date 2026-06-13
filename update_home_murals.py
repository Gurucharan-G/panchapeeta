import io
import re

home_path = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\templates\peethas\home.html"

with io.open(home_path, "r", encoding="utf-8") as f:
    home_content = f.read()

murals_pattern = r'(<div class="hero-mural mural-left reveal">.*?</div>\s*<div class="hero-mural mural-right reveal">.*?</div>)'

if '<div class="murals-mobile-container">' not in home_content:
    home_content = re.sub(murals_pattern, r'<div class="murals-mobile-container">\n        \1\n    </div>', home_content, flags=re.DOTALL)
    with io.open(home_path, "w", encoding="utf-8") as f:
        f.write(home_content)
    print("home.html updated to wrap murals.")
else:
    print("home.html already updated.")
