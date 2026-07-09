from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# ==========================================
# 1. OUR MINI DATABASE
# ==========================================
clients_db = [
    {"client_id": "Amazon B2B", "avg_cycle": 14, "days_since_last": 10},
    {"client_id": "Stark Industries", "avg_cycle": 30, "days_since_last": 45},
    {"client_id": "Wayne Enterprises", "avg_cycle": 90, "days_since_last": 120},
    {"client_id": "Dunder Mifflin", "avg_cycle": 20, "days_since_last": 19},
    {"client_id": "Pied Piper", "avg_cycle": 45, "days_since_last": 100}
]

# ==========================================
# 2. THE BIG BRAIN PYTHON LOGIC 🧠
# ==========================================
def analyze_churn_risk(clients):
    analyzed_data = []
    
    for c in clients:
        avg_cycle = float(c['avg_cycle'])
        days_since_last = float(c['days_since_last'])
        
        risk_threshold = avg_cycle * 1.25
        is_at_risk = days_since_last > risk_threshold
        
        if is_at_risk:
            status = "Gonna bounce"
            if days_since_last > (avg_cycle * 2):
                action = "Code Red! Call CEO 🚨"
            else:
                action = "Offer 10% Discount 💸"
        else:
            status = "Chillin"
            action = "Monitor Account"
            
        analyzed_data.append({
            "client_id": c['client_id'],
            "avg_cycle": int(avg_cycle),
            "days_since_last": int(days_since_last),
            "status": status,
            "recommended_action": action
        })
        
    return sorted(analyzed_data, key=lambda x: x['status'] == 'Chillin')

# ==========================================
# 3. THE FRONTEND UI (Ultra-Modern Dark Mode SaaS)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>B2B Churn Radar </title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts: Inter -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        body { font-family: 'Inter', sans-serif; }
        /* Custom scrollbar for that premium feel */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #0f172a; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #475569; }
    </style>
</head>
<body class="bg-slate-950 text-slate-300 min-h-screen flex flex-col selection:bg-indigo-500 selection:text-white">
    
    <!-- Sticky Glassmorphism Navigation -->
    <nav class="sticky top-0 z-50 bg-slate-900/70 backdrop-blur-lg border-b border-slate-800">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-20">
                <div class="flex items-center gap-3">
                    <div class="bg-indigo-500/20 p-2 rounded-lg border border-indigo-500/50">
                        <i class="fa-solid fa-radar text-indigo-400 text-xl animate-pulse"></i>
                    </div>
                    <span class="font-bold text-2xl tracking-tight text-white">Churn<span class="text-indigo-400">Radar</span></span>
                </div>
                <div class="flex items-center gap-4">
                    <div class="text-right hidden sm:block">
                        <p class="text-xs text-slate-500 uppercase tracking-widest font-semibold">Protected Revenue</p>
                        <p class="text-emerald-400 font-bold text-xl">${{ '{:,}'.format(clients|length * 15000) }}</p>
                    </div>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-10 grid grid-cols-1 xl:grid-cols-3 gap-8 flex-grow">
        
        <!-- Left Column: Controls & Visuals -->
        <div class="xl:col-span-1 space-y-8">
            
            <!-- Quick Chart Card -->
            <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-[0_8px_30px_rgb(0,0,0,0.4)] hover:-translate-y-1 transition duration-300">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-bold text-white"><i class="fa-solid fa-chart-pie mr-2 text-slate-400"></i>Portfolio Health</h3>
                </div>
                <div class="relative h-56 w-full flex justify-center">
                    <canvas id="churnChart"></canvas>
                </div>
            </div>

            <!-- Add Client Form Card -->
            <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-[0_8px_30px_rgb(0,0,0,0.4)] hover:-translate-y-1 transition duration-300">
                <h3 class="text-lg font-bold text-white mb-6"><i class="fa-solid fa-flask mr-2 text-slate-400"></i>Test New Client</h3>
                <form action="/add" method="POST" class="space-y-5">
                    <div>
                        <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Company Name</label>
                        <div class="relative">
                            <i class="fa-solid fa-building absolute left-4 top-3.5 text-slate-500"></i>
                            <input type="text" name="client_id" required placeholder="e.g. Netflix" 
                                class="w-full pl-11 pr-4 py-3 bg-slate-950 border border-slate-700 rounded-xl text-white placeholder-slate-600 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition">
                        </div>
                    </div>
                    <div class="flex gap-4">
                        <div class="flex-1">
                            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Usual Cycle (Days)</label>
                            <input type="number" name="avg_cycle" required placeholder="30" min="1" 
                                class="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-xl text-white placeholder-slate-600 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition text-center">
                        </div>
                        <div class="flex-1">
                            <label class="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Days Since</label>
                            <input type="number" name="days_since_last" required placeholder="45" min="0" 
                                class="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-xl text-white placeholder-slate-600 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition text-center">
                        </div>
                    </div>
                    <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3.5 px-6 rounded-xl shadow-[0_0_15px_rgba(79,70,229,0.4)] hover:shadow-[0_0_25px_rgba(79,70,229,0.6)] transition duration-300 flex items-center justify-center gap-2">
                        <i class="fa-solid fa-microchip"></i> Run AI Analysis
                    </button>
                </form>
            </div>
        </div>

        <!-- Right Column: The Data Table -->
        <div class="xl:col-span-2">
            <div class="bg-slate-900 border border-slate-800 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.4)] overflow-hidden h-full flex flex-col">
                <div class="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-900/50">
                    <h3 class="text-xl font-bold text-white"><i class="fa-solid fa-users mr-2 text-indigo-400"></i>Client Pipeline</h3>
                    <span class="bg-slate-800 text-slate-300 text-xs px-3 py-1 rounded-full font-semibold border border-slate-700">{{ clients|length }} Active</span>
                </div>
                
                <div class="overflow-x-auto flex-grow">
                    <table class="min-w-full divide-y divide-slate-800">
                        <thead class="bg-slate-950/50">
                            <tr>
                                <th class="px-6 py-5 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Client Info</th>
                                <th class="px-6 py-5 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Vibe Check</th>
                                <th class="px-6 py-5 text-left text-xs font-bold text-slate-400 uppercase tracking-wider">Action Plan</th>
                                <th class="px-6 py-5 text-center text-xs font-bold text-slate-400 uppercase tracking-wider">Manage</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800 bg-slate-900">
                            {% if clients|length == 0 %}
                            <tr><td colspan="4" class="px-6 py-16 text-center text-slate-500"><i class="fa-solid fa-ghost text-4xl mb-3 opacity-20"></i><br>All quiet. Add a client to see the magic.</td></tr>
                            {% endif %}
                            
                            {% for client in clients %}
                            <tr class="hover:bg-slate-800/60 transition duration-200 group">
                                <td class="px-6 py-5">
                                    <div class="font-bold text-white text-lg group-hover:text-indigo-300 transition">{{ client.client_id }}</div>
                                    <div class="text-sm text-slate-400 mt-1">
                                        <i class="fa-regular fa-clock mr-1"></i> Buys every <span class="font-bold text-slate-300">{{ client.avg_cycle }}</span> days. 
                                        Last seen <span class="font-bold text-slate-300">{{ client.days_since_last }}</span> days ago.
                                    </div>
                                </td>
                                <td class="px-6 py-5 whitespace-nowrap">
                                    {% if client.status == 'Gonna bounce' %}
                                        <!-- Neon Red Badge -->
                                        <span class="px-3 py-1.5 inline-flex items-center gap-1.5 text-xs font-bold rounded-md bg-rose-500/10 text-rose-400 border border-rose-500/30 shadow-[0_0_10px_rgba(244,63,94,0.15)]">
                                            <i class="fa-solid fa-circle-exclamation animate-pulse"></i> {{ client.status }}
                                        </span>
                                    {% else %}
                                        <!-- Neon Green Badge -->
                                        <span class="px-3 py-1.5 inline-flex items-center gap-1.5 text-xs font-bold rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                                            <i class="fa-solid fa-shield-check"></i> {{ client.status }}
                                        </span>
                                    {% endif %}
                                </td>
                                <td class="px-6 py-5">
                                    {% if client.status == 'Gonna bounce' %}
                                        <span class="text-xs bg-indigo-500/20 text-indigo-300 font-bold px-3 py-1.5 rounded-md border border-indigo-500/30 inline-block shadow-[0_0_10px_rgba(99,102,241,0.1)]">
                                            <i class="fa-solid fa-bolt mr-1"></i>{{ client.recommended_action }}
                                        </span>
                                    {% else %}
                                        <span class="text-xs text-slate-500 font-medium italic">
                                            <i class="fa-solid fa-mug-hot mr-1"></i>{{ client.recommended_action }}
                                        </span>
                                    {% endif %}
                                </td>
                                <td class="px-6 py-5 text-center">
                                    <form action="/delete/{{ client.client_id }}" method="POST" class="inline">
                                        <button type="submit" class="text-slate-500 hover:text-rose-400 font-bold w-8 h-8 flex items-center justify-center rounded-full hover:bg-rose-500/10 transition duration-300" title="Delete Client">
                                            <i class="fa-solid fa-trash-can"></i>
                                        </button>
                                    </form>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- Script to draw the chart with Dark Mode styling! -->
    <script>
        // Set Chart.js defaults for Dark Mode
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.font.family = "'Inter', sans-serif";
        
        const total = {{ clients|length }};
        const bouncing = {{ clients|selectattr("status", "equalto", "Gonna bounce")|list|length }};
        const chillin = total - bouncing;

        const ctx = document.getElementById('churnChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Healthy', 'At Risk'],
                datasets: [{
                    data: [chillin, bouncing],
                    backgroundColor: ['#10b981', '#f43f5e'], // Neon Emerald and Rose
                    borderColor: '#0f172a', // Matches bg-slate-950
                    borderWidth: 4,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { 
                        position: 'bottom', 
                        labels: { padding: 20, usePointStyle: true, pointStyle: 'circle', font: { weight: 'bold' } } 
                    }
                },
                cutout: '75%',
                layout: { padding: 10 }
            }
        });
    </script>
</body>
</html>
"""

# ==========================================
# 4. SERVER ROUTING 
# ==========================================
@app.route('/')
def dashboard():
    risk_data = analyze_churn_risk(clients_db)
    return render_template_string(HTML_TEMPLATE, clients=risk_data)

@app.route('/add', methods=['POST'])
def add_client():
    new_client = {
        "client_id": request.form['client_id'],
        "avg_cycle": int(request.form['avg_cycle']),
        "days_since_last": int(request.form['days_since_last'])
    }
    clients_db.append(new_client)
    return redirect(url_for('dashboard'))

@app.route('/delete/<client_id>', methods=['POST'])
def delete_client(client_id):
    global clients_db
    clients_db = [c for c in clients_db if c['client_id'] != client_id]
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    print("🚀 Firing up the Cyberpunk SaaS web app! Let's goooo...")
    app.run(debug=True, port=5000)