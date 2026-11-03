import sys, json, pathlib

md = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2])

HTML = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Campus Café — Project proposal v3</title>
<style>
@page{size:Letter;margin:.55in .6in .6in}
body{font-family:"Segoe UI",Arial,sans-serif;color:#201F1E;font-size:9.6pt;line-height:1.42;
 -webkit-print-color-adjust:exact;print-color-adjust:exact;max-width:7.3in;margin:0 auto}
h1{font-size:19pt;margin:0 0 .04in;font-weight:600;border-bottom:2px solid #0F6CBD;padding-bottom:.05in}
h2{font-size:12.5pt;margin:.24in 0 .07in;padding-left:.09in;border-left:4px solid #0F6CBD;font-weight:600;break-after:avoid}
h3{font-size:10.5pt;margin:.14in 0 .05in}
p{margin:.04in 0 .07in}
blockquote{margin:.08in 0;padding:.05in .14in;border-left:3px solid #C7E0F4;background:#EFF6FC;color:#0B4F8A}
blockquote p{margin:.02in 0}
table{border-collapse:collapse;width:100%;font-size:8.3pt;margin:.06in 0 .1in;break-inside:auto}
tr{break-inside:avoid}
th{background:#F3F2F1;text-align:left;padding:3px 6px;border-bottom:1px solid #C8C6C4}
td{padding:3px 6px;border-bottom:1px solid #E1DFDD;vertical-align:top}
code{font-family:Consolas,monospace;font-size:.9em;background:#F3F2F1;padding:0 3px;border-radius:3px}
hr{border:0;border-top:1px solid #E1DFDD;margin:.14in 0}
ul,ol{margin:.03in 0 .08in;padding-left:1.3em}
li{margin-bottom:.03in}
.mermaid{text-align:center;margin:.1in 0;break-inside:avoid}
.mermaid svg{max-width:100%;height:auto;max-height:6.2in}
em{color:#605E5C}
</style></head><body><div id="c"></div>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
<script>
const md = __MD__;
const r = new marked.Renderer();
const baseCode = r.code.bind(r);
r.code = function(code, lang){ if(lang==='mermaid'){ return '<div class="mermaid">'+code+'</div>'; } return baseCode(code, lang); };
document.getElementById('c').innerHTML = marked.parse(md, {renderer: r});
mermaid.initialize({startOnLoad:false, theme:'neutral', flowchart:{htmlLabels:true, useMaxWidth:true}, fontFamily:'Segoe UI, Arial'});
mermaid.run({querySelector:'.mermaid'}).then(()=>{document.title += ' ';document.body.setAttribute('data-done','1');});
</script></body></html>"""
out.write_text(HTML.replace("__MD__", json.dumps(md)), encoding="utf-8")
print("ok")
