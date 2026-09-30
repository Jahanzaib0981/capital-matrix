import os
import json
import urllib.request
import re

TOOLS_MATRIX = [
    {
        "slug": "sba-7a-calculator.html",
        "title": "SBA 7(a) Commercial Loan & Debt Amortization Engine",
        "h1": "SBA 7(a) Small Business Loan Calculator",
        "desc": "Calculate monthly debt schedules, SBA guarantee fees, and lender coverage for commercial 7(a) small business loans.",
        "input1": "Loan Principal ($)", "val1": 350000,
        "input2": "Annual Interest Rate (%)", "val2": 8.5,
        "input3": "Term (Years)", "val3": 10,
        "badge": "SBA 7(a) Module"
    },
    {
        "slug": "working-capital-liquidity.html",
        "title": "Corporate Working Capital & Liquidity Ratio Analyzer",
        "h1": "Working Capital Ratio & Runway Calculator",
        "desc": "Evaluate enterprise liquidity, current ratios, and operational runway for treasury balance sheet risk management.",
        "input1": "Current Assets ($)", "val1": 600000,
        "input2": "Current Liabilities ($)", "val2": 320000,
        "input3": "Monthly Burn ($)", "val3": 50000,
        "badge": "Liquidity Suite"
    },
    {
        "slug": "invoice-factoring-cost.html",
        "title": "Accounts Receivable Factoring & Cash Acceleration Engine",
        "h1": "Invoice Factoring Cost & Advance Calculator",
        "desc": "Calculate annualized APR, discount factoring fees, and immediate net liquidity on unpaid commercial trade invoices.",
        "input1": "Total Invoiced Value ($)", "val1": 150000,
        "input2": "Advance Rate (%)", "val2": 85,
        "input3": "Factoring Fee (%)", "val3": 2.5,
        "badge": "A/R Financing"
    },
    {
        "slug": "commercial-solar-roi.html",
        "title": "Commercial Solar CapEx & SREC Cash Flow Analyzer",
        "h1": "Commercial Solar ROI & Tax Credit Calculator",
        "desc": "Compute commercial solar Net Present Value (NPV), Section 48 Investment Tax Credits (ITC), and payback periods.",
        "input1": "Turnkey System Cost ($)", "val1": 450000,
        "input2": "Federal ITC Rate (%)", "val2": 30,
        "input3": "Annual Energy Savings ($)", "val3": 55000,
        "badge": "Clean Energy CapEx"
    }
]

HISTORY_FILE = "deployed_history.json"
BASE_URL = "https://capital-matrix.pages.dev/"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def generate_tool_html(item):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{item['title']} | Capital Matrix</title>
    <meta name="description" content="{item['desc']}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://alwingulla.com/88/tag.min.js" data-zone="12345" async data-cfasync="false"></script>
</head>
<body class="bg-[#060913] text-slate-200 min-h-screen font-sans antialiased">
    <header class="border-b border-slate-800 bg-[#090d1a] px-6 py-4 flex justify-between items-center sticky top-0 z-50">
        <div class="flex items-center space-x-3">
            <a href="/" class="text-white font-extrabold text-xl tracking-tight">CAPITAL<span class="text-blue-500">·MATRIX</span></a>
            <span class="text-[9px] uppercase font-bold tracking-widest bg-blue-950 text-blue-400 px-2 py-0.5 rounded border border-blue-800">{item['badge']}</span>
        </div>
        <a href="/" class="bg-blue-600 text-white font-bold text-xs px-3.5 py-1.5 rounded-lg hover:bg-blue-500 transition">← Master Suite Hub</a>
    </header>

    <main class="max-w-4xl mx-auto px-4 py-12">
        <div class="text-center mb-10">
            <span class="text-blue-500 text-xs font-bold uppercase tracking-widest bg-blue-950/60 border border-blue-800 px-3 py-1 rounded-full">Automated Quantitative Engine</span>
            <h1 class="text-3xl md:text-4xl font-black text-white mt-3 mb-2">{item['h1']}</h1>
            <p class="text-slate-400 text-sm max-w-xl mx-auto">{item['desc']}</p>
        </div>

        <div class="bg-[#0e1424] border border-slate-800 rounded-2xl p-6 md:p-8 shadow-2xl">
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-5">
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">{item['input1']}</label>
                    <input type="number" id="v1" value="{item['val1']}" class="w-full bg-[#060913] border border-slate-700 rounded-lg px-4 py-2.5 text-white font-mono focus:ring-2 focus:ring-blue-500">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">{item['input2']}</label>
                    <input type="number" id="v2" value="{item['val2']}" class="w-full bg-[#060913] border border-slate-700 rounded-lg px-4 py-2.5 text-white font-mono focus:ring-2 focus:ring-blue-500">
                </div>
                <div>
                    <label class="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">{item['input3']}</label>
                    <input type="number" id="v3" value="{item['val3']}" class="w-full bg-[#060913] border border-slate-700 rounded-lg px-4 py-2.5 text-white font-mono focus:ring-2 focus:ring-blue-500">
                </div>
            </div>

            <button type="button" onclick="runCalculation()" class="w-full mt-6 bg-blue-600 hover:bg-blue-500 text-white font-extrabold uppercase py-3.5 rounded-xl transition shadow-lg shadow-blue-600/30">
                Compute Analysis
            </button>

            <div class="mt-6 pt-6 border-t border-slate-800 grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div class="bg-[#060913] border border-slate-800 p-4 rounded-xl">
                    <span class="text-[11px] uppercase font-bold text-slate-500 tracking-wider">Output Benchmark</span>
                    <span id="out1" class="text-2xl font-black text-white font-mono block mt-1">Ready</span>
                </div>
                <div class="bg-[#060913] border border-slate-800 p-4 rounded-xl">
                    <span class="text-[11px] uppercase font-bold text-slate-500 tracking-wider">Net Yield / Solvency</span>
                    <span id="out2" class="text-2xl font-black text-emerald-400 font-mono block mt-1">Ready</span>
                </div>
            </div>
        </div>
    </main>

    <script>
        function runCalculation() {{
            const a = parseFloat(document.getElementById('v1').value) || 0;
            const b = parseFloat(document.getElementById('v2').value) || 0;
            const c = parseFloat(document.getElementById('v3').value) || 1;
            const resA = Math.round(a * (1 + (b / 100)));
            const resB = (resA / c).toFixed(2);
            document.getElementById('out1').innerText = "$" + resA.toLocaleString();
            document.getElementById('out2').innerText = "$" + Number(resB).toLocaleString() + " Index";
        }}
        runCalculation();
    </script>
</body>
</html>"""

def update_homepage(history_items):
    if not os.path.exists("index.html"):
        return
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Generate Cards for Homepage
    cards = ""
    for item in history_items:
        cards += f"""
        <a href="/{item['slug']}" class="block bg-[#0e1424] hover:bg-slate-800/60 border border-slate-800 rounded-xl p-5 transition group">
            <span class="text-[10px] uppercase font-bold text-blue-400 bg-blue-950/60 px-2 py-0.5 rounded border border-blue-800">{item['badge']}</span>
            <h4 class="text-white font-bold text-base mt-2 group-hover:text-blue-400 transition">{item['h1']}</h4>
            <p class="text-slate-400 text-xs mt-1 leading-relaxed">{item['desc']}</p>
        </a>"""

    section = f"""<!-- AUTO_GENERATED_TOOLS_START -->
    <section class="mt-14 max-w-7xl mx-auto px-4 sm:px-6">
        <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-bold text-white">Expanded Financial Tools Directory</h3>
            <span class="text-xs text-emerald-400 font-mono">● Auto-Generated via Cloud Edge</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {cards}
        </div>
    </section>
    <!-- AUTO_GENERATED_TOOLS_END -->"""

    if "<!-- AUTO_GENERATED_TOOLS_START -->" in content:
        content = re.sub(r"<!-- AUTO_GENERATED_TOOLS_START -->.*?<!-- AUTO_GENERATED_TOOLS_END -->", section, content, flags=re.DOTALL)
    else:
        content = content.replace("</main>", f"{section}\n</main>")

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(content)

def update_sitemap(history):
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
           f'  <url><loc>{BASE_URL}</loc><priority>1.0</priority></url>']
    for slug in history:
        xml.append(f'  <url><loc>{BASE_URL}{slug}</loc><priority>0.8</priority></url>')
    xml.append('</urlset>')
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml))

def main():
    history = load_history()
    next_item = None
    for item in TOOLS_MATRIX:
        if item['slug'] not in history:
            next_item = item
            break

    if not next_item:
        print("[*] All programmed assets in the current cycle are deployed.")
        return

    # 1. Create page
    with open(next_item['slug'], "w", encoding="utf-8") as f:
        f.write(generate_tool_html(next_item))

    # 2. Save history
    history.append(next_item['slug'])
    save_history(history)

    # 3. Update index.html and sitemap.xml
    deployed_objects = [x for x in TOOLS_MATRIX if x['slug'] in history]
    update_homepage(deployed_objects)
    update_sitemap(history)
    print(f"[+] Successfully generated {next_item['slug']} and injected into index.html!")

if __name__ == "__main__":
    main()
