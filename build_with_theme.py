import json

print("Generando HTML con fondo personalizado, logo y colores TBC verdes...")

# Load data
with open('leveling_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert data to JavaScript
route_js = json.dumps(data['route'], ensure_ascii=False, indent=4)
intro_js = json.dumps(data['introduction'], ensure_ascii=False, indent=4)

# Create the complete HTML with TBC green theme
html = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TBC Leveling Logbook | 60-70 Guide</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Roboto:wght@300;400;500&display=swap">
</head>
<body>
    <div class="container">
        <header>
            <div class="header-logo">
                <img src="tbc_logo.webp" alt="TBC Logo" class="logo">
            </div>
            <h1>TBC Leveling Logbook</h1>
            <p class="subtitle">Your Complete Guide from 60 to 70</p>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value" id="progress-percent">0%</div>
                    <div class="stat-label">Progress</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="tasks-completed">0/0</div>
                    <div class="stat-label">Tasks Completed</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="estimated-level">60</div>
                    <div class="stat-label">Estimated Level</div>
                </div>
            </div>
        </header>

        <div class="controls">
            <div class="filters">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="quest">Quests</button>
                <button class="filter-btn" data-filter="dungeon">Dungeons</button>
                <button class="filter-btn" data-filter="grind">Grind</button>
                <button class="filter-btn" data-filter="milestone">Milestones</button>
                <button class="filter-btn" data-filter="other">Other</button>
            </div>
            <input type="text" class="search-box" id="search-box" placeholder="🔍 Search tasks...">
        </div>

        <div class="main-content">
            <div class="route-section">
                <h2 class="section-title">📜 Leveling Route</h2>
                <div id="task-list" class="task-list"></div>
            </div>

            <div class="sidebar">
                <div class="calculator-panel">
                    <h3 class="panel-title">🧮 XP Calculator</h3>
                    <div class="calculator-input">
                        <input type="number" id="current-level" placeholder="Current" min="60" max="70" value="60">
                        <input type="number" id="target-level" placeholder="Target" min="60" max="70" value="70">
                    </div>
                    <div class="xp-result">
                        <div class="xp-result-value" id="xp-needed">0</div>
                        <div class="xp-result-label">XP Needed</div>
                    </div>
                    <table class="xp-table">
                        <thead>
                            <tr>
                                <th>Level</th>
                                <th>XP Total</th>
                            </tr>
                        </thead>
                        <tbody id="xp-table-body"></tbody>
                    </table>
                </div>

                <div class="info-panel" id="info-panel">
                    <h3 class="panel-title">ℹ️ Information</h3>
                </div>
            </div>
        </div>
    </div>

    <script>
        // ===== EMBEDDED DATA =====
        const DATA = {{
            "introduction": {intro_js},
            "route": {route_js}
        }};

        console.log('[TBC] Data loaded:', DATA.route.length, 'tasks');

        // ===== STATE =====
        let completedTasks = new Set();
        let currentFilter = 'all';
        let searchQuery = '';

        // ===== STORAGE =====
        function loadProgress() {{
            const saved = localStorage.getItem('tbc-leveling-progress');
            if (saved) completedTasks = new Set(JSON.parse(saved));
        }}

        function saveProgress() {{
            localStorage.setItem('tbc-leveling-progress', JSON.stringify([...completedTasks]));
        }}

        // ===== TASK MANAGEMENT =====
        function toggleTask(taskId) {{
            if (completedTasks.has(taskId)) {{
                completedTasks.delete(taskId);
            }} else {{
                completedTasks.add(taskId);
            }}
            saveProgress();
            renderTasks();
            updateStats();
        }}

        // ===== RENDERING =====
        function renderTasks() {{
            const taskList = document.getElementById('task-list');
            taskList.innerHTML = '';

            const filteredTasks = DATA.route.filter(task => {{
                const matchesFilter = currentFilter === 'all' || task.type === currentFilter;
                const matchesSearch = searchQuery === '' ||
                    task.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                    (task.notes && task.notes.toLowerCase().includes(searchQuery.toLowerCase()));
                return matchesFilter && matchesSearch;
            }});

            console.log(`[TBC] Rendering ${{filteredTasks.length}} tasks`);

            filteredTasks.forEach(task => {{
                const taskEl = document.createElement('div');
                taskEl.className = `task-item ${{task.type}} ${{completedTasks.has(task.id) ? 'completed' : ''}}`;

                const checkbox = document.createElement('div');
                checkbox.className = `checkbox ${{completedTasks.has(task.id) ? 'checked' : ''}}`;
                checkbox.setAttribute('data-task-id', task.id);

                const typeLabel = document.createElement('span');
                typeLabel.className = `task-type ${{task.type}}`;
                typeLabel.textContent = task.type;

                const taskName = document.createElement('div');
                taskName.className = 'task-name';
                taskName.textContent = task.name;

                const taskContent = document.createElement('div');
                taskContent.className = 'task-content';
                taskContent.appendChild(typeLabel);
                taskContent.appendChild(taskName);

                if (task.notes) {{
                    const notes = document.createElement('div');
                    notes.className = 'task-notes';
                    notes.textContent = task.notes;
                    taskContent.appendChild(notes);
                }}

                if (task.rewards) {{
                    const rewards = document.createElement('div');
                    rewards.className = 'task-rewards';
                    rewards.textContent = '💰 ' + task.rewards;
                    taskContent.appendChild(rewards);
                }}

                const taskHeader = document.createElement('div');
                taskHeader.className = 'task-header';
                taskHeader.appendChild(checkbox);
                taskHeader.appendChild(taskContent);

                taskEl.appendChild(taskHeader);
                taskList.appendChild(taskEl);
            }});

            console.log(`[TBC] Rendered ${{filteredTasks.length}} tasks`);
        }}

        function updateStats() {{
            const total = DATA.route.length;
            const completed = completedTasks.size;
            const percent = Math.round((completed / total) * 100);
            const estimatedLevel = 60 + Math.floor((completed / total) * 10);

            document.getElementById('progress-percent').textContent = percent + '%';
            document.getElementById('tasks-completed').textContent = `${{completed}}/${{total}}`;
            document.getElementById('estimated-level').textContent = estimatedLevel;
        }}

        function renderInfoSections() {{
            const infoPanel = document.getElementById('info-panel');
            infoPanel.innerHTML = '<h3 class="panel-title">ℹ️ Information</h3>';

            const intro = DATA.introduction;
            
            if (intro.general_tips) {{
                const section = document.createElement('div');
                section.className = 'info-section';
                section.innerHTML = '<h3>General Tips</h3>';
                const ul = document.createElement('ul');
                intro.general_tips.forEach(tip => {{
                    const li = document.createElement('li');
                    li.textContent = tip;
                    ul.appendChild(li);
                }});
                section.appendChild(ul);
                infoPanel.appendChild(section);
            }}

            if (intro.key_requirements) {{
                const section = document.createElement('div');
                section.className = 'info-section';
                section.innerHTML = '<h3>Key Requirements</h3>';
                const ul = document.createElement('ul');
                intro.key_requirements.forEach(req => {{
                    const li = document.createElement('li');
                    li.textContent = req;
                    ul.appendChild(li);
                }});
                section.appendChild(ul);
                infoPanel.appendChild(section);
            }}
        }}

        // ===== XP CALCULATOR =====
        const XP_TABLE = {{
            61: 494000, 62: 574700, 63: 614400, 64: 650300, 65: 682300,
            66: 710200, 67: 734100, 68: 753700, 69: 768900, 70: 779700
        }};

        function calculateXP() {{
            const currentLevel = parseInt(document.getElementById('current-level').value) || 60;
            const targetLevel = parseInt(document.getElementById('target-level').value) || 70;

            let totalXP = 0;
            for (let level = currentLevel + 1; level <= targetLevel; level++) {{
                totalXP += XP_TABLE[level] || 0;
            }}

            document.getElementById('xp-needed').textContent = totalXP.toLocaleString();
        }}

        function renderXPTable() {{
            const tbody = document.getElementById('xp-table-body');
            for (let level = 61; level <= 70; level++) {{
                const row = document.createElement('tr');
                row.innerHTML = `<td>${{level}}</td><td>${{XP_TABLE[level].toLocaleString()}}</td>`;
                tbody.appendChild(row);
            }}
        }}

        // ===== EVENT HANDLERS =====
        function setupFilters() {{
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentFilter = btn.dataset.filter;
                    renderTasks();
                }});
            }});
        }}

        function setupSearch() {{
            document.getElementById('search-box').addEventListener('input', (e) => {{
                searchQuery = e.target.value;
                renderTasks();
            }});
        }}

        function setupCalculator() {{
            document.getElementById('current-level').addEventListener('input', calculateXP);
            document.getElementById('target-level').addEventListener('input', calculateXP);
        }}

        function setupCheckboxDelegation() {{
            document.addEventListener('click', function(event) {{
                const checkbox = event.target.closest('.checkbox');
                if (checkbox) {{
                    const taskId = parseInt(checkbox.getAttribute('data-task-id'));
                    if (!isNaN(taskId)) {{
                        console.log('[TBC] Checkbox clicked, Task ID:', taskId);
                        toggleTask(taskId);
                    }}
                }}
            }});
        }}

        // ===== INITIALIZATION =====
        function init() {{
            loadProgress();
            renderInfoSections();
            renderXPTable();
            renderTasks();
            updateStats();
            setupFilters();
            setupSearch();
            setupCalculator();
            setupCheckboxDelegation();
            calculateXP();
        }}

        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', init);
        }} else {{
            init();
        }}
    </script>

    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            /* TBC Green Theme - Fel Green colors */
            --tbc-green: #00FF96;
            --tbc-green-dark: #00CC77;
            --tbc-green-darker: #009955;
            --tbc-green-light: #66FFBB;
            --bg-dark: #0a0e0a;
            --bg-darker: #050805;
            --bg-panel: rgba(10, 25, 15, 0.85);
            --bg-panel-hover: rgba(15, 30, 20, 0.95);
            --purple: #9370DB;
            --gold: #FFD700;
            --blue: #4169E1;
            --red: #DC143C;
            --text-primary: #E8FFE8;
            --text-secondary: #B0D0B0;
            --border: rgba(0, 255, 150, 0.3);
            --shadow: 0 8px 32px rgba(0, 255, 150, 0.2);
        }}

        body {{
            font-family: 'Roboto', sans-serif;
            background-image: url('fondo.avif');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: var(--text-primary);
            min-height: 100vh;
            position: relative;
        }}

        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            z-index: 0;
        }}

        .container {{ 
            max-width: 1400px; 
            margin: 0 auto; 
            padding: 20px; 
            position: relative;
            z-index: 1;
        }}

        header {{
            text-align: center;
            padding: 30px 20px;
            background: var(--bg-panel);
            border: 2px solid var(--border);
            border-radius: 15px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow);
        }}

        .header-logo {{
            margin-bottom: 20px;
        }}

        .logo {{
            max-width: 200px;
            height: auto;
            filter: drop-shadow(0 0 20px rgba(0, 255, 150, 0.5));
        }}

        h1 {{
            font-family: 'Cinzel', serif;
            font-size: 3rem;
            background: linear-gradient(135deg, var(--tbc-green) 0%, var(--tbc-green-light) 50%, var(--tbc-green) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-shadow: 0 0 30px rgba(0, 255, 150, 0.5);
        }}

        .subtitle {{ color: var(--text-secondary); font-size: 1.2rem; margin-top: 10px; }}

        .stats {{ display: flex; justify-content: center; gap: 30px; margin-top: 20px; flex-wrap: wrap; }}
        .stat-value {{ font-size: 2rem; font-weight: bold; color: var(--tbc-green); text-shadow: 0 0 10px rgba(0, 255, 150, 0.5); }}
        .stat-label {{ color: var(--text-secondary); font-size: 0.9rem; margin-top: 5px; }}

        .controls {{
            background: var(--bg-panel);
            border: 2px solid var(--border);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow);
        }}

        .filters {{ display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }}

        .filter-btn {{
            padding: 10px 20px;
            border: 2px solid var(--border);
            background: var(--bg-darker);
            color: var(--text-primary);
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .filter-btn:hover {{ 
            background: var(--bg-panel-hover); 
            border-color: var(--tbc-green); 
            box-shadow: 0 0 15px rgba(0, 255, 150, 0.3);
        }}
        
        .filter-btn.active {{ 
            background: var(--tbc-green); 
            color: var(--bg-dark); 
            border-color: var(--tbc-green);
            box-shadow: 0 0 20px rgba(0, 255, 150, 0.5);
        }}

        .search-box {{
            width: 100%;
            padding: 12px 20px;
            background: var(--bg-darker);
            border: 2px solid var(--border);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 1rem;
        }}

        .search-box:focus {{
            outline: none;
            border-color: var(--tbc-green);
            box-shadow: 0 0 15px rgba(0, 255, 150, 0.3);
        }}

        .main-content {{ display: grid; grid-template-columns: 1fr 350px; gap: 30px; }}
        @media (max-width: 1024px) {{ .main-content {{ grid-template-columns: 1fr; }} }}

        .route-section, .calculator-panel, .info-panel {{
            background: var(--bg-panel);
            border: 2px solid var(--border);
            border-radius: 15px;
            padding: 30px;
            backdrop-filter: blur(10px);
            box-shadow: var(--shadow);
        }}

        .section-title, .panel-title {{
            font-family: 'Cinzel', serif;
            font-size: 1.8rem;
            color: var(--tbc-green);
            margin-bottom: 20px;
            text-shadow: 0 0 10px rgba(0, 255, 150, 0.5);
        }}

        .task-list {{ display: flex; flex-direction: column; gap: 15px; }}

        .task-item {{
            background: var(--bg-darker);
            border: 2px solid var(--border);
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
        }}

        .task-item:hover {{ 
            border-color: var(--tbc-green); 
            transform: translateX(5px); 
            box-shadow: 0 0 15px rgba(0, 255, 150, 0.2);
        }}
        
        .task-item.completed {{ opacity: 0.6; }}
        .task-item.completed .task-name {{ text-decoration: line-through; }}

        .task-header {{ display: flex; align-items: flex-start; gap: 15px; }}

        .checkbox {{
            width: 24px;
            height: 24px;
            border: 2px solid var(--tbc-green);
            border-radius: 5px;
            cursor: pointer;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            margin-top: 3px;
        }}

        .checkbox:hover {{ 
            background: rgba(0, 255, 150, 0.1); 
            transform: scale(1.1); 
            box-shadow: 0 0 10px rgba(0, 255, 150, 0.3);
        }}
        
        .checkbox.checked {{ 
            background: var(--tbc-green); 
            box-shadow: 0 0 15px rgba(0, 255, 150, 0.5);
        }}
        
        .checkbox.checked::after {{ 
            content: '✓'; 
            color: var(--bg-dark); 
            font-size: 16px; 
            font-weight: bold; 
        }}

        .task-content {{ flex: 1; }}

        .task-type {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 5px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}

        .task-type.quest {{ background: var(--gold); color: var(--bg-dark); }}
        .task-type.dungeon {{ background: var(--purple); color: white; }}
        .task-type.milestone {{ background: var(--red); color: white; }}
        .task-type.grind {{ background: var(--tbc-green); color: var(--bg-dark); }}
        .task-type.other {{ background: var(--blue); color: white; }}

        .task-name {{ font-size: 1.1rem; font-weight: 500; margin-bottom: 8px; white-space: pre-wrap; }}
        .task-notes {{ color: var(--text-secondary); font-size: 0.9rem; margin-top: 8px; line-height: 1.6; white-space: pre-wrap; }}
        .task-rewards {{ color: var(--tbc-green); font-size: 0.9rem; margin-top: 8px; white-space: pre-wrap; }}

        .sidebar {{ display: flex; flex-direction: column; gap: 20px; }}

        .calculator-input {{ display: flex; gap: 10px; margin-bottom: 15px; }}
        .calculator-input input {{
            flex: 1;
            padding: 10px;
            background: var(--bg-darker);
            border: 2px solid var(--border);
            border-radius: 5px;
            color: var(--text-primary);
            text-align: center;
        }}

        .calculator-input input:focus {{
            outline: none;
            border-color: var(--tbc-green);
            box-shadow: 0 0 10px rgba(0, 255, 150, 0.3);
        }}

        .xp-result {{
            background: var(--bg-darker);
            border: 2px solid var(--tbc-green);
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(0, 255, 150, 0.2);
        }}

        .xp-result-value {{ 
            font-size: 2rem; 
            font-weight: bold; 
            color: var(--tbc-green); 
            text-shadow: 0 0 10px rgba(0, 255, 150, 0.5);
        }}
        
        .xp-result-label {{ color: var(--text-secondary); font-size: 0.9rem; margin-top: 5px; }}

        .xp-table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
        .xp-table th, .xp-table td {{ padding: 8px; text-align: center; border-bottom: 1px solid var(--border); }}
        .xp-table th {{ color: var(--tbc-green); font-weight: 600; }}
        .xp-table td {{ color: var(--text-secondary); }}

        .info-section {{ margin-bottom: 20px; }}
        .info-section h3 {{ color: var(--tbc-green); font-size: 1rem; margin-bottom: 10px; }}
        .info-section ul {{ list-style: none; padding-left: 0; }}
        .info-section li {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-bottom: 8px;
            padding-left: 20px;
            position: relative;
        }}
        .info-section li::before {{ content: '▸'; position: absolute; left: 0; color: var(--tbc-green); }}
    </style>
</body>
</html>'''

# Write the file
with open('index_complete.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✓ Archivo generado con tema TBC verde: index_complete.html")
print(f"✓ Tamaño: {len(html):,} bytes")
print(f"✓ Fondo: fondo.avif")
print(f"✓ Logo: tbc_logo.webp")
print(f"✓ Color principal: Verde Fel (#00FF96)")
print("\n¡LISTO!")
