"""
Flask To-Do App — app.py
Storage: todos.md (parsed on startup, written on every mutation)
"""

import os
import re
import uuid
from datetime import datetime
from flask import Flask, jsonify, request, render_template, abort, send_from_directory

app = Flask(__name__)

TODO_FILE = os.path.join(os.path.dirname(__file__), "todos.md")

LISTS = []

PRIORITY_TAGS = {"#urgent", "#high", "#medium", "#low", "#daily"}
LAST_RESET_FILE = os.path.join(os.path.dirname(__file__), "last_reset.txt")


def _extract_meta(text: str):
    """Parse priority tag and @assignee from task text. Returns (priority, assignee, is_daily, clean_text)."""
    priority = None
    assignee = None
    is_daily = False
    words = text.split()
    clean_words = []
    
    for word in words:
        w = word.lower()
        if w in PRIORITY_TAGS:
            if w == "#daily":
                is_daily = True
            else:
                priority = w[1:]
            continue
        if w.startswith("@"):
            assignee = w[1:]
            continue
        clean_words.append(word)
        
    return priority, assignee, is_daily, " ".join(clean_words)


def parse_md(path: str):
    """Parse todos.md → LISTS in-memory state."""
    lists = []
    if not os.path.exists(path):
        return lists

    current_list = None
    order = 0
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if line.startswith("## "):
                name = line[3:].strip()
                current_list = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "tasks": [],
                }
                lists.append(current_list)
                order = 0
                continue
            if current_list is not None and re.match(r"^- \[[ x]\] ", line):
                done = line[3] == "x"
                raw_text = line[6:].strip()
                priority, assignee, is_daily, clean_text = _extract_meta(raw_text)
                current_list["tasks"].append({
                    "id": str(uuid.uuid4()),
                    "text": clean_text,
                    "done": done,
                    "priority": priority,
                    "assignee": assignee,
                    "is_daily": is_daily,
                    "order": order,
                })
                order += 1

    return lists


def save_md(path: str, lists):
    """Serialize LISTS → todos.md."""
    lines = []
    for lst in lists:
        lines.append(f"## {lst['name']}")
        sorted_tasks = sorted(lst["tasks"], key=lambda t: t["order"])
        for task in sorted_tasks:
            mark = "x" if task["done"] else " "
            text = task["text"]
            if task.get("priority"):
                text += f" #{task['priority']}"
            if task.get("is_daily"):
                text += " #daily"
            if task.get("assignee"):
                text += f" @{task['assignee']}"
            lines.append(f"- [{mark}] {text}")
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))



def _seed_default():
    """Create a default todos.md if none exists."""
    if not os.path.exists(TODO_FILE):
        with open(TODO_FILE, "w", encoding="utf-8") as f:
            f.write(
                "## Personal\n"
                "- [ ] Buy groceries #low\n"
                "- [ ] Read a book #medium\n"
                "\n"
                "## Work\n"
                "- [ ] Review pull requests #urgent @alice\n"
                "- [x] Set up project repo #high\n"
                "\n"
            )


_seed_default()
LISTS = parse_md(TODO_FILE)



def _find_list(list_id: str):
    return next((l for l in LISTS if l["id"] == list_id), None)


def _find_task(task_id: str):
    for lst in LISTS:
        for task in lst["tasks"]:
            if task["id"] == task_id:
                return lst, task
    return None, None


def _state_json():
    return jsonify({"lists": LISTS})



def check_and_reset_daily_tasks():
    """Reset tasks containing #daily if a new day has started."""
    today = datetime.now().strftime("%Y-%m-%d")
    last_reset = ""
    if os.path.exists(LAST_RESET_FILE):
        with open(LAST_RESET_FILE, "r") as f:
            last_reset = f.read().strip()

    if last_reset != today:
        changed = False
        for lst in LISTS:
            for task in lst["tasks"]:
                if task.get("is_daily") and task["done"]:
                    task["done"] = False
                    changed = True
        
        if changed:
            save_md(TODO_FILE, LISTS)
        
        with open(LAST_RESET_FILE, "w") as f:
            f.write(today)

@app.route("/")
def index():
    check_and_reset_daily_tasks()
    return render_template("index.html")


@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), "assets"), filename)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(os.path.dirname(__file__), "assets"), "todo.png", mimetype="image/png")


@app.route("/api/state", methods=["GET"])
def get_state():
    return _state_json()



@app.route("/api/lists", methods=["POST"])
def create_list():
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    if not name:
        abort(400, "List name required")
    new_list = {"id": str(uuid.uuid4()), "name": name, "tasks": []}
    LISTS.append(new_list)
    save_md(TODO_FILE, LISTS)
    return jsonify(new_list), 201


@app.route("/api/lists/<list_id>", methods=["PUT"])
def rename_list(list_id):
    lst = _find_list(list_id)
    if not lst:
        abort(404)
    data = request.get_json(force=True)
    name = (data.get("name") or "").strip()
    if not name:
        abort(400, "List name required")
    lst["name"] = name
    save_md(TODO_FILE, LISTS)
    return jsonify(lst)


@app.route("/api/lists/<list_id>", methods=["DELETE"])
def delete_list(list_id):
    lst = _find_list(list_id)
    if not lst:
        abort(404)
    LISTS.remove(lst)
    save_md(TODO_FILE, LISTS)
    return jsonify({"deleted": list_id})



@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(force=True)
    list_id = data.get("list_id")
    text = (data.get("text") or "").strip()
    if not list_id or not text:
        abort(400, "list_id and text required")
    lst = _find_list(list_id)
    if not lst:
        abort(404)
    priority, assignee, is_daily, clean_text = _extract_meta(text)
    max_order = max((t["order"] for t in lst["tasks"]), default=-1)
    task = {
        "id": str(uuid.uuid4()),
        "text": clean_text,
        "done": False,
        "priority": priority,
        "assignee": assignee,
        "is_daily": is_daily,
        "order": max_order + 1,
    }
    lst["tasks"].append(task)
    save_md(TODO_FILE, LISTS)
    return jsonify(task), 201


@app.route("/api/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    lst, task = _find_task(task_id)
    if not task:
        abort(404)
    data = request.get_json(force=True)
    if "text" in data:
        raw_text = data["text"].strip()
        priority, assignee, is_daily, clean_text = _extract_meta(raw_text)
        task["text"] = clean_text
        task["priority"] = priority
        task["assignee"] = assignee
        task["is_daily"] = is_daily
    if "done" in data:
        task["done"] = bool(data["done"])
    save_md(TODO_FILE, LISTS)
    return jsonify(task)


@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    lst, task = _find_task(task_id)
    if not task:
        abort(404)
    lst["tasks"].remove(task)
    save_md(TODO_FILE, LISTS)
    return jsonify({"task": task, "list_id": lst["id"]})


@app.route("/api/tasks/reorder", methods=["POST"])
def reorder_tasks():
    """Body: { list_id, ordered_ids: [id, id, ...] }"""
    data = request.get_json(force=True)
    lst = _find_list(data.get("list_id"))
    if not lst:
        abort(404)
    ordered_ids = data.get("ordered_ids", [])
    id_to_task = {t["id"]: t for t in lst["tasks"]}
    for idx, tid in enumerate(ordered_ids):
        if tid in id_to_task:
            id_to_task[tid]["order"] = idx
    save_md(TODO_FILE, LISTS)
    return jsonify({"ok": True})


@app.route("/api/tasks/restore", methods=["POST"])
def restore_task():
    """Undo delete — re-insert task. Body: { task, list_id }"""
    data = request.get_json(force=True)
    lst = _find_list(data.get("list_id"))
    if not lst:
        abort(404)
    task = data.get("task")
    if not task:
        abort(400)
    max_order = max((t["order"] for t in lst["tasks"]), default=-1)
    task["order"] = max_order + 1
    lst["tasks"].append(task)
    save_md(TODO_FILE, LISTS)
    return jsonify(task), 201

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False, port=5100)
