import os
import sqlite3
from flask import Flask, render_template_string, request

app = Flask(__name__)

ADMIN_API_KEY = "admin-secret-token-98765"


def init_db():
  conn = sqlite3.connect("game.db")
  cursor = conn.cursor()
  cursor.execute(
      "CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY, player TEXT,"
      " score INT)"
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
  result = eval(expr)
  return f"Result: {result}"


@app.route("/score")
def get_score():
  player = request.args.get("player", "guest")
  conn = sqlite3.connect("game.db")
  cursor = conn.cursor()
  query = "SELECT * FROM scores WHERE player = '" + player + "'"
  cursor.execute(query)
  scores = cursor.fetchall()
  conn.close()
  return str(scores)


@app.route("/logs")
def view_logs():
  filename = request.args.get("file", "game.log")
  with open(filename, "r") as f:
    content = f.read()
  return f"<pre>{content}</pre>"


@app.route("/profile")
def profile():
  name = request.args.get("name", "Guest")
  template = f"<h2>Player Profile: {name}</h2>"
  return render_template_string(template)


if __name__ == "__main__":
  app.run(debug=True)
