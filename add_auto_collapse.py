import io

html_path = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\templates\peethas\index.html"

with io.open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

js_snippet = """
        // Auto-collapse mobile menu on link click
        document.querySelectorAll('.nav-links .nav-link').forEach(link => {
            link.addEventListener('click', () => {
                const nav = document.querySelector('.nav-links');
                if (nav && nav.classList.contains('open')) {
                    nav.classList.remove('open');
                }
            });
        });
"""

# Insert it before the closing </script> tag if possible
if js_snippet not in html_content:
    if "</script>" in html_content:
        # Find the last </script> tag to inject into
        parts = html_content.rsplit("</script>", 1)
        html_content = parts[0] + js_snippet + "</script>" + parts[1]
        
        with io.open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print("index.html updated with auto-collapse JS.")
    else:
        print("Could not find </script> tag.")
else:
    print("JS snippet already exists.")
