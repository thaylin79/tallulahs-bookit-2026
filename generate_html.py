import csv, json, html

rows = []
summary = {}
with open("checkouts.csv", newline="") as f:
    r = csv.reader(f)
    header = next(r)
    for row in r:
        if not row:
            continue
        if row[0] in ("Total number of books", "Total number of pages", "Time since first checkout"):
            summary[row[0]] = row[1]
            continue
        rows.append({"title": row[0], "date": row[1], "pages": row[2], "cover": row[3]})

def sort_key(b):
    date = b["date"]
    is_real_date = len(date) == 10 and date[4] == "-" and date[7] == "-"
    return (1 if is_real_date else 0, date if not is_real_date else "".join(f"{9-int(c) if c.isdigit() else c}" for c in date))

rows.sort(key=sort_key)

def card(book):
    title = html.escape(book["title"])
    date = html.escape(book["date"])
    pages = html.escape(book["pages"])
    cover = html.escape(book["cover"]) if book["cover"] else ""
    img = f'<img src="{cover}" alt="Cover of {title}" loading="lazy" onerror="this.style.display=\'none\'; this.nextElementSibling.style.display=\'flex\';">' if cover else ""
    return f"""
    <li class="card">
      <div class="cover-wrap">
        {img}
        <div class="cover-fallback" style="display:{'none' if cover else 'flex'};">No cover</div>
      </div>
      <div class="card-body">
        <h3 class="card-title">{title}</h3>
        <dl class="meta">
          <div><dt>Checked out</dt><dd>{date}</dd></div>
          <div><dt>Pages</dt><dd>{pages}</dd></div>
        </dl>
      </div>
    </li>"""

cards_html = "\n".join(card(b) for b in rows)

html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Summer Reading Wrap-Up!</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --sun: #ffb703;
    --sky: #4cc9f0;
    --coral: #ff6b6b;
    --leaf: #2ec4b6;
    --grape: #7b2cbf;
    --ink: #26324a;
    --card-bg: #ffffff;
    --border: #ffe066;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: "Nunito", -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(180deg, #bde0fe 0%, #caf0f8 35%, #fff3bf 100%);
    color: var(--ink);
    min-height: 100vh;
  }}
  header {{
    padding: 2.5rem 1.5rem 2rem;
    max-width: 1100px;
    margin: 0 auto;
    text-align: center;
  }}
  h1 {{
    font-family: "Baloo 2", "Nunito", sans-serif;
    font-weight: 800;
    margin: 0 0 0.4rem;
    font-size: clamp(1.8rem, 5vw, 2.8rem);
    color: var(--grape);
    text-shadow: 2px 2px 0 #fff3bf;
  }}
  .subtitle {{
    font-family: "Baloo 2", sans-serif;
    font-weight: 600;
    color: var(--ink);
    margin: 0 0 1.75rem;
    font-size: clamp(1rem, 2.5vw, 1.3rem);
  }}
  .stats {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1.1rem;
    max-width: 780px;
    margin: 0 auto;
  }}
  .stat {{
    background: var(--card-bg);
    border: 3px solid var(--border);
    border-radius: 16px;
    padding: 1.1rem 1rem;
    box-shadow: 0 4px 0 rgba(0,0,0,0.06);
  }}
  .stat .icon {{ font-size: 1.8rem; display: block; margin-bottom: 0.15rem; }}
  .stat .value {{
    font-family: "Baloo 2", sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--coral);
  }}
  .stat .label {{
    font-size: 0.85rem;
    color: var(--ink);
    font-weight: 600;
    margin-top: 0.15rem;
  }}
  main {{
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 1.5rem 3rem;
  }}
  .section-title {{
    font-family: "Baloo 2", sans-serif;
    font-weight: 700;
    color: var(--grape);
    font-size: 1.3rem;
    margin: 0.5rem 0 1rem;
    text-align: center;
  }}
  ul.grid {{
    list-style: none;
    margin: 0;
    padding: 0;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.4rem;
  }}
  .card {{
    background: var(--card-bg);
    border: 3px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 0 rgba(0,0,0,0.06);
    transition: transform 0.15s ease;
  }}
  .card:hover {{ transform: translateY(-3px) rotate(-0.5deg); }}
  .cover-wrap {{
    aspect-ratio: 2 / 3;
    background: linear-gradient(135deg, #ffe066, #ffb703);
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }}
  .cover-wrap img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}
  .cover-fallback {{
    color: #8a6d00;
    font-size: 0.85rem;
    font-weight: 600;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0.5rem;
  }}
  .card-body {{
    padding: 0.75rem 0.9rem 1rem;
    flex: 1;
    display: flex;
    flex-direction: column;
  }}
  .card-title {{
    font-family: "Baloo 2", sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    line-height: 1.3;
    margin: 0 0 0.5rem;
    min-height: 2.5em;
    color: var(--ink);
  }}
  dl.meta {{
    margin: auto 0 0;
    font-size: 0.8rem;
    color: #5b6478;
  }}
  dl.meta div {{
    display: flex;
    justify-content: space-between;
    padding: 0.2rem 0;
    border-top: 1px dashed var(--border);
  }}
  dl.meta div:first-child {{ border-top: none; }}
  dl.meta dt {{ font-weight: 600; }}
  dl.meta dd {{ margin: 0; text-align: right; }}
</style>
</head>
<body>
<header>
  <h1>🌞 Good job on this summer's reading! 🏖️</h1>
  <p class="subtitle">Here's what you've done this summer</p>
  <div class="stats">
    <div class="stat">
      <span class="icon">📚</span>
      <div class="value">{html.escape(summary.get("Total number of books", "-"))}</div>
      <div class="label">Books read</div>
    </div>
    <div class="stat">
      <span class="icon">📖</span>
      <div class="value">{html.escape(summary.get("Total number of pages", "-"))}</div>
      <div class="label">Pages read</div>
    </div>
    <div class="stat">
      <span class="icon">☀️</span>
      <div class="value">{html.escape(summary.get("Time since first checkout", "-"))}</div>
      <div class="label">Of summer reading fun</div>
    </div>
  </div>
</header>
<main>
  <p class="section-title">🏆 Your Reading Adventures 🏆</p>
  <ul class="grid">
    {cards_html}
  </ul>
</main>
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html_doc)

print("Wrote index.html with", len(rows), "books")
