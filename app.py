from flask import Flask, request, redirect, render_template_string, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"])

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id TEXT PRIMARY KEY,
            title TEXT,
            body TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api/notes", methods=["GET"])
def get_notes():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, body, created_at, updated_at FROM notes ORDER BY updated_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{
        "id": r[0], "title": r[1], "body": r[2],
        "created": r[3].isoformat(), "updated": r[4].isoformat()
    } for r in rows])

@app.route("/api/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO notes (id, title, body) VALUES (%s, %s, %s)",
        (data["id"], data.get("title", ""), data.get("body", ""))
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "created"})

@app.route("/api/notes/<note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE notes SET title=%s, body=%s, updated_at=NOW() WHERE id=%s",
        (data.get("title", ""), data.get("body", ""), note_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "updated"})

@app.route("/api/notes/<note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id=%s", (note_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "deleted"})

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Notes – Task 3.3</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Segoe UI', sans-serif; background: #f5f5f0; display: flex; height: 100vh; overflow: hidden; }

    .sidebar {
      width: 260px; min-width: 260px;
      background: #fff;
      border-right: 1px solid #e8e8e3;
      display: flex; flex-direction: column;
    }
    .sidebar-header {
      padding: 16px;
      border-bottom: 1px solid #e8e8e3;
      display: flex; align-items: center; justify-content: space-between;
    }
    .sidebar-header span { font-size: 12px; font-weight: 600; color: #999; letter-spacing: 0.08em; text-transform: uppercase; }
    .note-count { font-size: 11px; background: #f0f0eb; color: #888; padding: 2px 8px; border-radius: 10px; }
    .note-list { flex: 1; overflow-y: auto; padding: 8px; }
    .note-item {
      padding: 10px 12px; border-radius: 8px;
      cursor: pointer; margin-bottom: 4px;
      border: 1px solid transparent;
    }
    .note-item:hover { background: #f5f5f0; }
    .note-item.active { background: #f0f0eb; border-color: #e0e0d8; }
    .note-item-title { font-size: 13px; font-weight: 600; color: #1a1a1a; margin-bottom: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .note-item-preview { font-size: 12px; color: #888; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .note-item-date { font-size: 11px; color: #bbb; margin-top: 4px; }
    .note-item-empty { font-size: 12px; color: #bbb; font-style: italic; }

    .main { flex: 1; display: flex; flex-direction: column; background: #fff; }
    .toolbar {
      padding: 12px 20px;
      border-bottom: 1px solid #e8e8e3;
      display: flex; align-items: center; gap: 8px;
    }
    .btn {
      font-size: 13px; padding: 6px 14px; border-radius: 8px;
      border: 1px solid #e0e0d8;
      background: #fff; color: #1a1a1a; cursor: pointer;
    }
    .btn:hover { background: #f5f5f0; }
    .btn.primary { background: #1a1a1a; color: #fff; border-color: #1a1a1a; }
    .btn.primary:hover { background: #333; }
    .btn.danger { color: #c0392b; border-color: #f5c6c6; }
    .btn.danger:hover { background: #fff5f5; }
    .spacer { flex: 1; }
    .saved { font-size: 12px; color: #27ae60; }

    .editor-area { flex: 1; padding: 28px 32px; display: flex; flex-direction: column; gap: 12px; overflow: hidden; }
    #note-title {
      font-size: 22px; font-weight: 600; color: #1a1a1a;
      border: none; outline: none; background: transparent; width: 100%;
      font-family: 'Segoe UI', sans-serif;
    }
    #note-title::placeholder { color: #ccc; }
    .divider { height: 1px; background: #e8e8e3; }
    #note-body {
      flex: 1; font-size: 15px; line-height: 1.75; color: #333;
      border: none; outline: none; background: transparent;
      resize: none; width: 100%;
      font-family: 'Segoe UI', sans-serif;
    }
    #note-body::placeholder { color: #ccc; }

    .empty-state {
      flex: 1; display: flex; flex-direction: column;
      align-items: center; justify-content: center; gap: 10px;
      color: #ccc;
    }
    .empty-state .icon { font-size: 36px; }
    .empty-state p { font-size: 14px; }

    .status-bar {
      padding: 8px 20px;
      border-top: 1px solid #e8e8e3;
      display: flex; gap: 16px; align-items: center;
    }
    .status-bar span { font-size: 12px; color: #bbb; }
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-header">
      <span>Notes</span>
      <span class="note-count" id="note-count">0</span>
    </div>
    <div class="note-list" id="note-list"></div>
  </div>

  <div class="main">
    <div class="toolbar">
      <button class="btn primary" onclick="newNote()">+ New note</button>
      <div class="spacer"></div>
      <span class="saved" id="saved-indicator" style="display:none">Saved</span>
      <button class="btn danger" id="delete-btn" onclick="deleteNote()" style="display:none">Delete</button>
    </div>

    <div id="editor-area" class="editor-area" style="display:none; flex-direction:column;">
      <input id="note-title" placeholder="Note title" maxlength="80" oninput="onEdit()" />
      <div class="divider"></div>
      <textarea id="note-body" placeholder="Start writing..." oninput="onEdit()"></textarea>
    </div>

    <div id="empty-state" class="empty-state">
      <div class="icon">✏️</div>
      <p>Select a note or create a new one</p>
    </div>

    <div class="status-bar" id="status-bar" style="display:none">
      <span id="word-count">0 words</span>
      <span id="char-count">0 characters</span>
      <span id="note-date"></span>
    </div>
  </div>

<script>
  let notes = [];
  let activeId = null;
  let saveTimer = null;

  function uid() { return Date.now().toString(36) + Math.random().toString(36).slice(2); }

  function fmt(ts) {
    const d = new Date(ts);
    const now = new Date();
    const diff = now - d;
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return Math.floor(diff/60000) + 'm ago';
    if (diff < 86400000) return Math.floor(diff/3600000) + 'h ago';
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  }

  function esc(s) {
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  async function loadNotes() {
    const res = await fetch('/api/notes');
    notes = await res.json();
    renderList();
  }

  function renderList() {
    const list = document.getElementById('note-list');
    document.getElementById('note-count').textContent = notes.length;
    list.innerHTML = '';
    if (!notes.length) {
      list.innerHTML = '<p style="padding:16px;font-size:13px;color:#bbb">No notes yet</p>';
      return;
    }
    notes.forEach(n => {
      const el = document.createElement('div');
      el.className = 'note-item' + (n.id === activeId ? ' active' : '');
      const title = n.title || 'Untitled';
      const preview = n.body ? n.body.replace(/\\n/g,' ').slice(0,60) : '';
      el.innerHTML = `
        <div class="note-item-title">${esc(title)}</div>
        ${preview ? `<div class="note-item-preview">${esc(preview)}</div>` : '<div class="note-item-empty">No content</div>'}
        <div class="note-item-date">${fmt(n.updated)}</div>
      `;
      el.onclick = () => openNote(n.id);
      list.appendChild(el);
    });
  }

  function openNote(id) {
    activeId = id;
    const n = notes.find(x => x.id === id);
    if (!n) return;
    document.getElementById('note-title').value = n.title || '';
    document.getElementById('note-body').value = n.body || '';
    document.getElementById('editor-area').style.display = 'flex';
    document.getElementById('empty-state').style.display = 'none';
    document.getElementById('status-bar').style.display = 'flex';
    document.getElementById('delete-btn').style.display = '';
    document.getElementById('saved-indicator').style.display = 'none';
    updateStats();
    renderList();
  }

  async function newNote() {
    const n = { id: uid(), title: '', body: '', created: new Date().toISOString(), updated: new Date().toISOString() };
    await fetch('/api/notes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(n)
    });
    notes.unshift(n);
    openNote(n.id);
    document.getElementById('note-title').focus();
  }

  async function deleteNote() {
    if (!activeId) return;
    await fetch('/api/notes/' + activeId, { method: 'DELETE' });
    notes = notes.filter(x => x.id !== activeId);
    activeId = null;
    document.getElementById('editor-area').style.display = 'none';
    document.getElementById('empty-state').style.display = 'flex';
    document.getElementById('status-bar').style.display = 'none';
    document.getElementById('delete-btn').style.display = 'none';
    renderList();
  }

  function onEdit() {
    if (!activeId) return;
    const n = notes.find(x => x.id === activeId);
    if (!n) return;
    n.title = document.getElementById('note-title').value;
    n.body  = document.getElementById('note-body').value;
    n.updated = new Date().toISOString();
    updateStats();
    renderList();
    document.getElementById('saved-indicator').style.display = 'none';
    clearTimeout(saveTimer);
    saveTimer = setTimeout(async () => {
      await fetch('/api/notes/' + activeId, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: n.title, body: n.body })
      });
      document.getElementById('saved-indicator').style.display = '';
      setTimeout(() => { document.getElementById('saved-indicator').style.display = 'none'; }, 1500);
    }, 600);
  }

  function updateStats() {
    const body = document.getElementById('note-body').value;
    const words = body.trim() ? body.trim().split(/\s+/).length : 0;
    document.getElementById('word-count').textContent = words + ' word' + (words !== 1 ? 's' : '');
    document.getElementById('char-count').textContent = body.length + ' char' + (body.length !== 1 ? 's' : '');
    const n = notes.find(x => x.id === activeId);
    if (n) document.getElementById('note-date').textContent = 'Edited ' + fmt(n.updated);
  }

  loadNotes();
</script>
</body>
</html>
"""

init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
