import re

# Read the HTML file
with open('index_complete.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=== DIAGNÓSTICO COMPLETO ===\n")

# 1. Check total tasks in DATA
tasks = re.findall(r'"id":\s*(\d+)', content)
print(f"1. Total task IDs found: {len(tasks)}")
print(f"   First ID: {tasks[0] if tasks else 'None'}")
print(f"   Last ID: {tasks[-1] if tasks else 'None'}\n")

# 2. Check if DATA.route exists
if '"route": [' in content:
    print("2. ✓ DATA.route array found\n")
else:
    print("2. ❌ DATA.route array NOT found\n")

# 3. Check if renderTasks function exists
if 'function renderTasks()' in content:
    print("3. ✓ renderTasks() function found\n")
else:
    print("3. ❌ renderTasks() function NOT found\n")

# 4. Check checkbox implementation
if 'data-task-id' in content:
    print("4. ✓ Checkboxes use data-task-id\n")
else:
    print("4. ❌ Checkboxes still use onclick\n")

# 5. Check event delegation
if 'setupCheckboxDelegation' in content:
    print("5. ✓ Event delegation configured\n")
else:
    print("5. ❌ Event delegation NOT configured\n")

# 6. Check for syntax errors in DATA
data_match = re.search(r'const DATA = ({.*?});', content, re.DOTALL)
if data_match:
    data_str = data_match.group(1)
    # Check for common JSON errors
    if data_str.count('{') == data_str.count('}'):
        print("6. ✓ Balanced braces in DATA\n")
    else:
        print(f"6. ❌ UNBALANCED braces: { data_str.count('{') } open, { data_str.count('}') } close\n")
    
    if data_str.count('[') == data_str.count(']'):
        print("7. ✓ Balanced brackets in DATA\n")
    else:
        print(f"7. ❌ UNBALANCED brackets: { data_str.count('[') } open, { data_str.count(']') } close\n")
else:
    print("6. ❌ Could not extract DATA object\n")

# 8. Extract a sample task to verify structure
sample_task = re.search(r'{\s*"id":\s*4,.*?"rewards":\s*.*?}', content, re.DOTALL)
if sample_task:
    print("8. Sample task (ID 4):")
    print(sample_task.group(0)[:200] + "...\n")
else:
    print("8. ❌ Could not find sample task\n")

# 9. Check if there are any obvious JavaScript errors
if 'const DATA = {' in content and '};' in content:
    print("9. ✓ DATA object appears to be properly closed\n")
else:
    print("9. ❌ DATA object may not be properly closed\n")

print("\n=== RECOMENDACIÓN ===")
print("Si solo ves 15 tareas, el problema es probablemente:")
print("1. Caché del navegador (Ctrl + Shift + R)")
print("2. Error de JavaScript que detiene el renderizado")
print("3. Filtro activo que está ocultando tareas")
