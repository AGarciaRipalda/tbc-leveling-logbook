import json
import re

def main():
    print("Generating final HTML with embedded data...")

    # Load data
    try:
        with open('leveling_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded {len(data.get('route', []))} tasks")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Load template
    try:
        with open('index_final.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("index_final.html not found, trying index.html")
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

    # JSON string
    data_json = json.dumps(data, ensure_ascii=False, indent=2)

    # Create new function
    new_function = f'''    // Embedded data
    function loadData() {{
      console.log('[TBC] Loading embedded data...');
      DATA = {data_json};
      console.log('[TBC] Data loaded successfully: ' + (DATA.route ? DATA.route.length : 0) + ' tasks');
      
      // Initialize app
      loadProgress();
      renderInfoSections();
      renderXPTable();
      renderTasks();
      updateStats();
      calculateXP();
    }}'''

    # Replace using regex to find the existing loadData function
    pattern = r'(async\s+)?function\s+loadData\s*\(\)\s*\{'
    match = re.search(pattern, html_content)
    
    if not match:
        print("Could not find function loadData")
        # Fallback: check if we already have embedded data or different name?
        # Maybe just search for 'function loadData'
        return

    print(f"Found function at index {match.start()}")
    
    start_idx = match.start()
    # Find matching brace
    open_braces = 0
    found_first_brace = False
    end_idx = -1
    
    # Start searching for braces from the match
    for i in range(match.end() - 1, len(html_content)):
        char = html_content[i]
        if char == '{':
            open_braces += 1
            found_first_brace = True
        elif char == '}':
            open_braces -= 1
            
        if found_first_brace and open_braces == 0:
            end_idx = i + 1
            break
    
    if end_idx != -1:
        new_html = html_content[:start_idx] + new_function + html_content[end_idx:]
        print("Replacement success!")
    else:
        print("Could not find end of function")
        return

    with open('index_complete.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print(f"Written index_complete.html ({len(new_html):,} bytes)")

if __name__ == "__main__":
    main()
