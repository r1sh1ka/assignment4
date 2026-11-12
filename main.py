import html
import os
import sqlite3
from flask import Flask, render_template_string, request

app = Flask(__name__)

ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "default-fallback-key")


def init_db():
  conn = sqlite3.connect("game.db")
  cursor = conn.cursor()
  cursor.execute(
      "CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, player"
      " TEXT, score INT)"
  )
  conn.commit()
  conn.close()


init_db()


@app.route("/")
def index():
  return """
    <h1>Welcome to the Mini Game Arcade!</h1>
    <ul>
        <li><a href="/calc?expr=2+2">Calculator</a></li>
        <li><a href="/score?player=Alice">High Scores</a></li>
        <li><a href="/profile?name=Player1">Player Profile</a></li>
        <li><a href="/logs?file=game.log">View Logs</a></li>
    </ul>
    """


@app.route("/calc")
def calculator():
  expr = request.args.get("expr", "0")
  if not all(c in "0123456789+-*/(). " for c in expr):
    return "Invalid expression characters", 400
  try:
    result = eval(expr)
  except Exception:
    return "Calculation error", 400
  return f"Result: {result}"


@app.route("/score")
def get_score():
  player = request.args.get("player", "guest")
  conn = sqlite3.connect("game.db")
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM scores WHERE player = ?", (player,))
  scores = cursor.fetchall()
  conn.close()
  return str(scores)


@app.route("/logs")
def view_logs():
  filename = request.args.get("file", "game.log")
  safe_filename = os.path.basename(filename)
  filepath = os.path.join("logs", safe_filename)
  if not os.path.exists(filepath):
    return "Log file not found", 404
  with open(filepath, "r") as f:
    content = f.read()
  return f"<pre>{content}</pre>"


@app.route("/profile")
def profile():
  name = request.args.get("name", "Guest")
  safe_name = html.escape(name)
  template = f"<h2>Player Profile: {safe_name}</h2>"
  return render_template_string(template)


if __name__ == "__main__":
  app.run(debug=False)
