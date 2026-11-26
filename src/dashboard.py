"""Build a standalone interactive HTML dashboard using Plotly.js."""
from pathlib import Path
import json
import pandas as pd

def main():
    df = pd.read_csv("outputs/dataset_cleaned.csv", parse_dates=["date"])
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    records = df.replace({float("nan"): None}).to_dict(orient="records")
    payload = json.dumps(records, allow_nan=False)
    html = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>COVID-19 Data Analysis Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
body{font-family:Arial,sans-serif;margin:0;background:#f4f6fb;color:#20243a}
header{background:#38206b;color:white;padding:22px 5%}
main{max-width:1200px;margin:24px auto;padding:0 18px}
.controls,.panel{background:white;border-radius:12px;padding:18px;margin-bottom:18px;box-shadow:0 2px 10px #17204412}
select{padding:9px 12px;border:1px solid #bbb;border-radius:7px;font-size:15px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.chart{height:360px}
.note{font-size:13px;color:#555}
@media(max-width:750px){.grid{grid-template-columns:1fr}.chart{height:320px}}
</style></head><body>
<header><h1>COVID-19 Data Analysis &amp; Visualisation</h1><p>Explore reported cases, deaths, population-normalised metrics and data-quality flags.</p></header>
<main><section class="controls"><label for="country"><b>Select country: </b></label>
<select id="country"><option value="ALL">All countries</option></select>
<span class="note">Figures reflect the supplied dataset; flagged records are not silently removed.</span></section>
<div class="grid">
<section class="panel"><h3>Confirmed cases over time</h3><div id="cases" class="chart"></div></section>
<section class="panel"><h3>Deaths over time</h3><div id="deaths" class="chart"></div></section>
<section class="panel"><h3>Cases per 100,000</h3><div id="percapita" class="chart"></div></section>
<section class="panel"><h3>Data-quality anomalies</h3><div id="anomalies" class="chart"></div></section>
</div><p class="note">Educational project only. COVID-19 data may be incomplete, synthetic or inconsistent; do not use this dashboard for medical or policy decisions.</p></main>
<script>
const DATA = __DATA__;
const countries=[...new Set(DATA.map(d=>d.country))].sort();
const select=document.getElementById('country');
countries.forEach(c=>{const o=document.createElement('option');o.value=c;o.textContent=c;select.appendChild(o)});
function render(){
 const chosen=select.value;
 const rows=DATA.filter(d=>chosen==='ALL'||d.country===chosen);
 const names=chosen==='ALL'?countries:[chosen];
 const traces=(field)=>names.map(c=>{const a=rows.filter(d=>d.country===c).sort((x,y)=>x.date.localeCompare(y.date));
 return {x:a.map(d=>d.date),y:a.map(d=>d[field]),mode:'lines',name:c,type:'scatter'};});
 Plotly.newPlot('cases',traces('confirmed'),{margin:{t:15},xaxis:{title:'Date'},yaxis:{title:'Cases'},legend:{orientation:'h'}},{responsive:true});
 Plotly.newPlot('deaths',traces('deaths'),{margin:{t:15},xaxis:{title:'Date'},yaxis:{title:'Deaths'},legend:{orientation:'h'}},{responsive:true});
 const latest=names.map(c=>rows.filter(d=>d.country===c).sort((a,b)=>a.date.localeCompare(b.date)).slice(-1)[0]).filter(Boolean);
 Plotly.newPlot('percapita',[{x:latest.map(d=>d.country),y:latest.map(d=>d.cases_per_100k),type:'bar'}],
 {margin:{t:15,b:100},xaxis:{tickangle:-35},yaxis:{title:'Cases per 100,000'}},{responsive:true});
 Plotly.newPlot('anomalies',[{x:latest.map(d=>d.country),y:latest.map(d=>d.anomaly_count),type:'bar'}],
 {margin:{t:15,b:100},xaxis:{tickangle:-35},yaxis:{title:'Flag count on latest record'}},{responsive:true});
}
select.addEventListener('change',render);render();
</script></body></html>"""
    html = html.replace("__DATA__", payload)
    Path("outputs/dashboard.html").write_text(html, encoding="utf-8")
    print("Created outputs/dashboard.html")

if __name__ == "__main__":
    main()
