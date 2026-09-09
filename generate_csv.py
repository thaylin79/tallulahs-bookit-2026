import json, re, csv
from datetime import date

CLIENT_KEY = "ng1WxsRuosjf6lc9J10Sv5fyWy3UkNKK"
TODAY = date(2026, 8, 24)

with open("test.json") as f:
    data = json.load(f)

rows = []
total_pages = 0
checkout_dates = []

for rec in data:
    d = rec["solrData"]
    title = d.get("title", "")
    checkout = rec.get("checkout_gmt", "")
    if checkout:
        checkout_dates.append(checkout)

    pages_display = ""
    for v in d.get("sm_bib_varfields", []):
        if v.startswith("300"):
            m = re.search(r"([0-9]+)\s*pages", v)
            if m:
                pages_display = m.group(1)
                total_pages += int(m.group(1))
            else:
                m2 = re.search(r"\{\{a\}\}\s*([^:]+):", v)
                pages_display = m2.group(1).strip() if m2 else v
            break

    isbn_list = d.get("isbn") or []
    isbn = isbn_list[0] if isbn_list else ""
    bib_id = rec.get("bib_id", "")
    cover_url = (
        f"https://discover.bklynlibrary.org/api/covers/jacket"
        f"?client={CLIENT_KEY}&isbn={isbn}&bibid={bib_id}"
        if isbn and bib_id else ""
    )

    rows.append([title, checkout, pages_display, cover_url])

first_checkout = min(checkout_dates) if checkout_dates else None
if first_checkout:
    y, m, d_ = map(int, first_checkout.split("-"))
    delta = TODAY - date(y, m, d_)
    days = delta.days
    years = days // 365
    months = (days % 365) // 30
    remaining_days = (days % 365) % 30
    time_since = f"{years}y {months}m {remaining_days}d ({days} days total)"
else:
    time_since = "N/A"

with open("checkouts.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Title", "Date Checked Out", "Number of Pages", "Cover Image"])
    w.writerows(rows)
    w.writerow([])
    w.writerow(["Total number of books", len(rows)])
    w.writerow(["Total number of pages", total_pages])
    w.writerow(["Time since first checkout", time_since])

print("Done. First checkout:", first_checkout, "Total pages:", total_pages, "Books:", len(rows))
