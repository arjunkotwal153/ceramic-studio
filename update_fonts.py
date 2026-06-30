import re
import os

css_files = [
    r'c:\Users\PC\Downloads\ceramic studio\css\style.css',
    r'c:\Users\PC\Downloads\ceramic studio\css\responsive.css'
]

def convert_to_clamp(match):
    original = match.group(0)
    value = float(match.group(1))
    unit = match.group(2)
    
    # Don't convert if it's already a clamp or 0
    if value == 0:
        return original
        
    if unit == 'px':
        min_val = max(10, value * 0.8) # 80% or 10px
        vw_val = value / 10 # heuristic
        return f"font-size: clamp({min_val:.1f}px, {vw_val:.2f}vw + 0.5rem, {value}px)"
    elif unit == 'rem':
        min_val = max(0.8, value * 0.7)
        vw_val = value * 2
        return f"font-size: clamp({min_val:.2f}rem, {vw_val:.2f}vw + 0.5rem, {value}rem)"
    return original

for filepath in css_files:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match font-size: 15px or font-size: 1.5rem (but not clamp)
    # We do a lookbehind to ensure we aren't already in a clamp
    new_content = re.sub(r'font-size:\s*([\d.]+)(px|rem)(?!\s*\()', convert_to_clamp, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated {filepath}")
