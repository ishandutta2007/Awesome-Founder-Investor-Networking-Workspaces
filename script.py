import os
import re
import subprocess
import urllib.request
import json
import time

repo_dir = r"C:\Users\ishan\Documents\Projects\Awesome-Founder-Investor-Networking-Workspaces"
readme_path = os.path.join(repo_dir, "README.md")
assets_dir = os.path.join(repo_dir, "assets")

def run_git(cmd_str):
    print("Running:", cmd_str)
    cmds = cmd_str.split(";") if ";" in cmd_str else cmd_str.split("&&")
    for cmd in cmds:
        cmd = cmd.strip()
        if not cmd:
            continue
        prefix = "git --git-dir=.git --work-tree=. "
        full_cmd = cmd.replace("git ", prefix, 1)
        subprocess.run(full_cmd, cwd=repo_dir, shell=True, check=True)

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# ==========================================
# Step 1: SaaS Products
# ==========================================
saas_table_regex = re.compile(r"\| SaaS Product \| Description \| Pricing Model \| Free Tier / Limit \|\n\| :--- \| :--- \| :--- \| :--- \|\n(?:\|.*?\|\n)+")

saas_data = [
    {"name": "**[PitchBook](https://pitchbook.com/)**", "desc": "Advanced platform for comprehensive financial data and research.", "price": "Paid (~$12,000+/year)", "free": "No permanent free tier; limited trials or academic access only.", "size_val": 30000000000, "size_str": "$30B+"},
    {"name": "**[AngelList](https://www.angellist.com/)**", "desc": "Advanced platform for startups and investors, accelerator-specific tools.", "price": "Varies by raised capital", "free": "Free for startups with <$1M raised; free basic investor profiles.", "size_val": 4000000000, "size_str": "$4B"},
    {"name": "**[Dealroom.co](https://dealroom.co/)**", "desc": "Advanced platform for startup data and ecosystem insights.", "price": "Paid (~€12,600/year)", "free": "No permanent free tier; 3-7 day free trial available.", "size_val": 50000000, "size_str": "$50M+"},
    {"name": "**[Exitfund](https://exitfund.com/)**", "desc": "Founder-focused platform connecting startups with investors and providing tools for efficient fundraising workflows.", "price": "Free", "free": "100% free for startups and investors (no carry/management fees).", "size_val": 10000000, "size_str": "$10M"},
    {"name": "**[Lyncbuild](https://lyncbuild.com/)**", "desc": "Intelligent networking workspace that matches founders with the right investors using AI and manages warm intros and deal flow.", "price": "Early Access (Currently Free)", "free": "All core features are free during the early access phase.", "size_val": 5000000, "size_str": "$5M"},
    {"name": "**[EasyVC](https://easyvc.com/)**", "desc": "Simplified workspace that helps founders find and connect with relevant venture capital firms.", "price": "Paid (Standard/Premium)", "free": "Free trial for setup; messaging with investors requires a paid plan.", "size_val": 2000000, "size_str": "$2M"},
    {"name": "**[Fundverse](https://fundverse.ai/)**", "desc": "Comprehensive platform for founder-investor collaboration, deal tracking, and intelligent matchmaking.", "price": "Performance-based", "free": "$0 upfront; platform fee only on successfully funded campaigns.", "size_val": 1000000, "size_str": "$1M"},
    {"name": "**[iKomatch](https://ikomatch.com/)**", "desc": "AI-powered investor matching and networking workspace designed specifically for startup fundraising.", "price": "Freemium / Success Fee", "free": "Free registration and basic access; success fees for cohort programs.", "size_val": 1000000, "size_str": "$1M"},
    {"name": "**[Signal by NFX](https://www.nfx.com/signal)**", "desc": "Highly regarded investor-founder matching and deal flow platform from NFX with strong network intelligence.", "price": "100% Free", "free": "Entirely free community tool; no hidden costs or subscriptions.", "size_val": 0, "size_str": "N/A (Community/VC)"},
    {"name": "**[FundBoard](https://fundboard.io/)**", "desc": "Collaborative deal flow and investor networking platform for startups and funds.", "price": "Free (Inactive)", "free": "Previously free; currently listed as out of business (July 2021).", "size_val": -1, "size_str": "$0 (Inactive)"},
]

saas_data = sorted(saas_data, key=lambda x: x["size_val"], reverse=True)

new_saas_table = "| SaaS Product | Description | Pricing Model | Free Tier / Limit | Company Size (Revenue/Valuation) |\n"
new_saas_table += "| :--- | :--- | :--- | :--- | :--- |\n"
for item in saas_data:
    new_saas_table += f"| {item['name']} | {item['desc']} | {item['price']} | {item['free']} | {item['size_str']} |\n"

content = saas_table_regex.sub(new_saas_table, content)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git('git add . ; git commit -m "Added company size and sorted the SaaS based on that" ; git push')


# ==========================================
# Step 2: Open-Source GitHub Projects stars
# ==========================================
def get_stars(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get('stargazers_count', 0)
    except Exception as e:
        print(f"Error fetching {owner}/{repo}: {e}")
        return 0

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

section1_start = content.find("### 🛠️ Dedicated Founder-Investor Networking & Deal Flow Tools")
section2_start = content.find("### 🌟 Additional Strong Open-Source Options")
section_end = content.find("## 🙌 How to Contribute")

sec1 = content[section1_start:section2_start]
sec2 = content[section2_start:section_end]

def process_section(sec_text):
    lines = sec_text.split("\n")
    blocks = []
    current_block = []
    for line in lines:
        if line.startswith("- "):
            if current_block:
                blocks.append("\n".join(current_block))
            current_block = [line]
        elif line.strip() == "" and current_block:
            current_block.append(line)
        elif current_block:
            current_block.append(line)
    if current_block:
        blocks.append("\n".join(current_block))
    
    header_text = []
    bullet_blocks = []
    
    for b in blocks:
        if b.startswith("- "):
            bullet_blocks.append(b)
        else:
            if not bullet_blocks:
                header_text.append(b)
            else:
                pass 

    parsed_blocks = []
    for b in bullet_blocks:
        match = re.search(r"https://github\.com/([^/]+)/([^/\)]+)", b)
        stars = -1
        if match:
            owner, repo = match.groups()
            repo = repo.split('"')[0].split("'")[0]
            stars = get_stars(owner, repo)
            badge = f" [![Stars](https://img.shields.io/github/stars/{owner}/{repo}?style=social&color=white)](https://github.com/{owner}/{repo}/stargazers)"
            b = re.sub(r"(\[.*?\]\(https://github\.com/[^/]+/[^/\)]+\)\**)", r"\1" + badge, b)
        parsed_blocks.append((stars, b))
    
    parsed_blocks = sorted(parsed_blocks, key=lambda x: x[0], reverse=True)
    return "\n".join(header_text) + "\n" + "\n".join([x[1] for x in parsed_blocks]) + "\n"

new_sec1 = process_section(sec1)
new_sec2 = process_section(sec2)

content = content[:section1_start] + new_sec1 + new_sec2 + content[section_end:]

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git('git add . ; git commit -m "Added github stars and sorted the opensource based on that" ; git push')


# ==========================================
# Step 3: Decorate with emojis & dynamic SVG banner
# ==========================================
if not os.path.exists(assets_dir):
    os.makedirs(assets_dir)

svg_banner = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200" width="100%" height="100%">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ff7e5f;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#feb47b;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#6a11cb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#2575fc;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="800" height="200" fill="url(#grad1)" rx="15" ry="15">
    <animate attributeName="fill" values="url(#grad1);url(#grad2);url(#grad1)" dur="5s" repeatCount="indefinite" />
  </rect>
  <text x="50%" y="40%" font-family="Arial, sans-serif" font-size="40" font-weight="bold" fill="white" text-anchor="middle">
    Awesome Founder &amp; Investor Workspaces
  </text>
  <text x="50%" y="65%" font-family="Arial, sans-serif" font-size="20" fill="white" text-anchor="middle">
    Curated list of SaaS and Open-Source tools for startup fundraising
  </text>
  <circle cx="100" cy="100" r="10" fill="white" opacity="0.5">
    <animate attributeName="cy" values="100;80;100" dur="2s" repeatCount="indefinite" />
  </circle>
  <circle cx="700" cy="100" r="10" fill="white" opacity="0.5">
    <animate attributeName="cy" values="100;120;100" dur="3s" repeatCount="indefinite" />
  </circle>
</svg>"""

with open(os.path.join(assets_dir, "banner.svg"), "w", encoding="utf-8") as f:
    f.write(svg_banner)

with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('## 🌟 Top Founder & Investor Networking Workspaces Ecosystem', '<div align="center">\n  <img src="assets/banner.svg" alt="Banner" />\n</div>\n\n## 🌟 Top Founder & Investor Networking Workspaces Ecosystem 🚀')
content = content.replace('**Curated List of SaaS Products', '✨ **Curated List of SaaS Products')
content = content.replace('**Keywords**:', '🔑 **Keywords**:')
content = content.replace('**Examples** include', '💡 **Examples** include')
content = content.replace('**Open-source emphasis**:', '🌍 **Open-source emphasis**:')

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git('git add . && git commit -m "added emojis and banner" && git push')

# ==========================================
# Step 4: SEO and Left Badges
# ==========================================
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

left_badges = '<a href="https://github.com/ishandutta2007/Awesome-Awesome-Awesome"><img src="https://img.shields.io/badge/Awesome-%E2%9C%94-blueviolet?style=flat-square&logo=github" alt="Awesome"/></a><a href="https://discord.gg/jc4xtF58Ve"><img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a>\n'

content = content.replace('[![Awesome](https://cdn.rawgit.com/sindresorhus', left_badges + '[![Awesome](https://cdn.rawgit.com/sindresorhus')

content = content.replace('## 🌟 Top Founder & Investor Networking Workspaces Ecosystem 🚀', '## 🌟 Top Founder & Investor Networking Workspaces Ecosystem 🚀\n\n<!-- SEO Optimization: Explore the best CRM and deal flow management tools for startups, VCs, angel investors, and founders. Find AI-powered matchmaking platforms and open-source alternatives. -->')

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git('git add . && git commit -m "seo optimised and badges to left added" && git push')

# ==========================================
# Step 5: Right Badges
# ==========================================
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

right_badge = '\n<a href="https://github.com/ishandutta2007"><img alt="GitHub followers" src="https://img.shields.io/github/followers/ishandutta2007?label=Follow" /></a>'
content = content.replace('[![GitHub forks](https://img.shields.io/github/forks/ishandutta2007/Awesome-Founder-Investor-Networking-Workspaces.svg?style=flat-square)](https://github.com/ishandutta2007/Awesome-Founder-Investor-Networking-Workspaces/network)',
'[![GitHub forks](https://img.shields.io/github/forks/ishandutta2007/Awesome-Founder-Investor-Networking-Workspaces.svg?style=flat-square)](https://github.com/ishandutta2007/Awesome-Founder-Investor-Networking-Workspaces/network)' + right_badge)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git('git add . && git commit -m "badges to right added" && git push')

# ==========================================
# Step 6: Star History
# ==========================================
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

new_star_history = """##  Star History
<div align="center">
<a href="https://www.star-history.com/?repos=ishandutta2007%2FAwesome-Founder-Investor-Networking-Workspaces&type=date&legend=bottom-right">
<picture>
<source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-Founder-Investor-Networking-Workspaces&type=date&theme=dark&legend=bottom-right" />
<source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-Founder-Investor-Networking-Workspaces&type=date&legend=bottom-right" />
<img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ishandutta2007/Awesome-Founder-Investor-Networking-Workspaces&type=date&legend=bottom-right" />
</picture>
</a>
</div>
"""

old_star_history_regex = re.compile(r"## 📈 Star History\n\n<div align=\"center\">[\s\S]*?</div>\n\n")
if old_star_history_regex.search(content):
    content = old_star_history_regex.sub(new_star_history + "\n\n", content)
else:
    content = content.replace("---\n\n**Made for founders", new_star_history + "\n\n---\n\n**Made for founders")

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git('git add . ; git commit -m "star history added" ; git push')

# ==========================================
# Step 7: Fix chartrepos
# ==========================================
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("chartrepos", "chart?repos")

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git('git add . ; git commit -m "fixed star plot" ; git push')

# ==========================================
# Step 8: Fix awesome link
# ==========================================
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("https://github.com/sindresorhus/awesome", "https://github.com/ishandutta2007/Awesome-Awesome-Awesome")

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

run_git('git add . ; git commit -m "invalid awesome link fixed" ; git push')

print("All done!")
