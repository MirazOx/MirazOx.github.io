import glob

html_files = glob.glob('beyond/*/index.html')

for path in html_files:
    with open(path, 'r') as f:
        content = f.read()
    
    # We want to replace "</div>\n      </div>\n    </section>" with "</div>\n    </section>"
    # Or just replace "</div>\n      </div>" if it appears directly before </section>
    content = content.replace('      </div>\n      </div>\n    </section>', '      </div>\n    </section>')
    
    with open(path, 'w') as f:
        f.write(content)

print(f"Fixed {len(html_files)} files.")
