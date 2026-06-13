import io

css_path = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\static\css\styles.css"

with io.open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

# Replace the specific CSS rules in the media query
# We need to change:
# .header-container { flex-direction: column; ... }
# to:
# .header-container { flex-direction: row; flex-wrap: wrap; justify-content: space-between; align-items: center; ... }

# We also need to change:
# .mobile-top-bar { width: 100%; }
# to:
# .mobile-top-bar { width: auto; }

# And remove margin-bottom from lang-selector-container
# .lang-selector-container { align-self: center; margin-bottom: 5px; }

# Since we might have multiple definitions, let's replace the whole @media (max-width: 992px) block or just find & replace specific strings.

css_content = css_content.replace(
    """.mobile-top-bar {
    display: none;
    width: 100%;
    justify-content: space-between;
    align-items: center;
}""",
    """.mobile-top-bar {
    display: none;
    width: auto; /* changed */
    justify-content: flex-start;
    align-items: center;
}"""
)

css_content = css_content.replace(
    """    .header-container {
        flex-direction: column;
        gap: 15px;
        padding: 15px 10px;
        height: auto;
    }""",
    """    .header-container {
        flex-direction: row; /* changed */
        flex-wrap: wrap; /* changed */
        justify-content: space-between; /* changed */
        align-items: center;
        gap: 15px;
        padding: 15px 10px;
        height: auto;
    }"""
)

css_content = css_content.replace(
    """    .lang-selector-container {
        align-self: center;
        margin-bottom: 5px;
    }""",
    """    .lang-selector-container {
        align-self: center;
        margin-bottom: 0;
    }"""
)

css_content = css_content.replace(
    """    .nav-links {
        display: none; /* Hide by default */
        flex-direction: column;
        width: 100%;""",
    """    .nav-links {
        display: none; /* Hide by default */
        flex-direction: column;
        width: 100%;
        order: 3; /* Push to bottom row */"""
)

with io.open(css_path, "w", encoding="utf-8") as f:
    f.write(css_content)

print("styles.css updated to keep language dropdown beside menu.")
