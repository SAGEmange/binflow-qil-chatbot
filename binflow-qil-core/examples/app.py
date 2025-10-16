from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from jinja2 import Template
import json, time

app = FastAPI(title="Binflow QIL Chatbot")

HTML = Template('''
<!doctype html>
<title>Binflow QIL Chatbot</title>
<h2>Binflow QIL Chatbot (local rules)</h2>
<form onsubmit="send(event)">
  <input id="msg" placeholder="Say something..." style="width:70%">
  <button>Send</button>
</form>
<pre id="log"></pre>
<hr>
<h3>Upload Data Pass (JSON)</h3>
<input type="file" id="file" />
<pre id="dp"></pre>
<script>
async function send(e){
  e.preventDefault();
  const m = document.getElementById('msg').value;
  const r = await fetch('/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({message:m})});
  const j = await r.json();
  document.getElementById('log').textContent += "\\nYou: " + m + "\\nBot: " + j.reply + "\\n";
  document.getElementById('msg').value = '';
}
document.getElementById('file').addEventListener('change', async (e)=>{
  const f = e.target.files[0];
  const fd = new FormData(); fd.append('file', f);
  const r = await fetch('/datapass', {method:'POST', body:fd});
  const t = await r.text();
  document.getElementById('dp').textContent = t;
});
</script>
''')

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML.render()

class ChatIn(BaseModel):
    message: str

def binflow_reply(msg: str) -> str:
    msg_l = msg.lower()
    if "pattern" in msg_l or "binflow" in msg_l:
        return "I see a repeating pattern. Use F→S→L→P→T. What's your current state?"
    if "state" in msg_l:
        return "Pick one micro-action you can finish in 5 minutes. Then Pause(P) and export a Data Pass."
    if "data pass" in msg_l or "export" in msg_l:
        return "From Core, run examples/run_demo.py to create a Data Pass, then upload it here."
    return "Tell me your smallest repeatable loop. We'll formalize it and produce a Data Pass."

@app.post("/chat")
def chat(inp: ChatIn):
    return JSONResponse({"reply": binflow_reply(inp.message)})

@app.post("/datapass")
async def datapass(file: UploadFile = File(...)):
    try:
        raw = await file.read()
        j = json.loads(raw)
        snap = j.get("snapshot", {})
        t = j.get("timestamp", 0)
        nodes = snap.get("nodes", {})
        when = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t)) if t else "N/A"
        return f"DataPass OK | nodes={len(nodes)} | t={when} UTC"
    except Exception as e:
        return f"Parse error: {e}"
