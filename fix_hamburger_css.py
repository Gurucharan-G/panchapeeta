import io

css_path = r"c:\Users\Bhoja\.gemini\antigravity-ide\scratch\panchapeetas\peethas\static\css\styles.css"

with io.open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

# Make hamburger button look like lang selector
css_content = css_content.replace(
    """.hamburger-btn {
    background: var(--gold);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: var(--radius);
    font-weight: 600;
    cursor: pointer;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 6px;
}""",
    """.hamburger-btn {
    background-color: rgba(255, 255, 255, 0.85);
    color: var(--text);
    border: 1px solid rgba(184, 134, 11, 0.25);
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 600;
    cursor: pointer;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: all 0.3s ease;
}
.hamburger-btn:hover {
    background-color: rgba(184, 134, 11, 0.1);
    border-color: var(--gold);
    color: var(--gold);
}"""
)

# Bring them closer together
css_content = css_content.replace(
    """    .header-container {
        flex-direction: row; /* changed */
        flex-wrap: wrap; /* changed */
        justify-content: space-between; /* changed */
        align-items: center;
        gap: 15px;
        padding: 15px 10px;
        height: auto;
    }""",
    """    .header-container {
        flex-direction: row; /* changed */
        flex-wrap: wrap; /* changed */
        justify-content: center; /* keep them close */
        align-items: center;
        gap: 15px;
        padding: 12px 10px;
        height: auto;
    }"""
)

with io.open(css_path, "w", encoding="utf-8") as f:
    f.write(css_content)

print("styles.css updated for uniform buttons and centered layout.")
