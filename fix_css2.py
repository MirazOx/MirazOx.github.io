with open('assets/css/style.css', 'r') as f:
    css = f.read()

# Replace '.beyond-page-hero, /* The main beyond page hero */' with just nothing, so only .beyond-hero has it.
css = css.replace('.beyond-page-hero, /* The main beyond page hero */\n.beyond-hero {', '.beyond-hero {')

with open('assets/css/style.css', 'w') as f:
    f.write(css)
