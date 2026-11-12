import ast
import html
import operator
import os
import sqlite3
from flask import Flask, request

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


_allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node):
  if isinstance(node, ast.Constant):
    return node.value
  elif isinstance(node, ast.Num):  
    return node.n
  elif isinstance(node, ast.BinOp):
    return _allowed_operators[type(node.op)](
        _eval_node(node.left), _eval_node(node.right)
    )
  elif isinstance(node, ast.UnaryOp):
    return _allowed_operators[type(node.op)](_eval_node(node.operand))
  else:
    raise TypeError(f"Unsupported operation")


@app.route("/calc")
def calculator():
  expr = request.args.get("expr", "0")
  try:
    node = ast.parse(expr, mode="eval")
    result = _eval_node(node.body)
  except Exception:
    return "Invalid calculation expression", 400
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
  ALLOWED_LOGS = ["game.log", "error.log", "access.log"]

  if filename not in ALLOWED_LOGS:
    return "Access denied", 403

  filepath = os.path.join("logs", filename)
  if not os.path.exists(filepath):
    return "Log file not found", 404

  with open(filepath, "r") as f:
    content = f.read()
  return f"<pre>{content}</pre>"


@app.route("/profile")
def profile():
  name = request.args.get("name", "Guest")
  safe_name = html.escape(name)
  return f"<h2>Player Profile: {safe_name}</h2>"


if __name__ == "__main__":
  app.run(debug=False)
