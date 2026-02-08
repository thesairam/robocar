from flask import Flask, abort, redirect, render_template_string, url_for
import atexit
import robo

app = Flask(__name__)

ACTIONS = {
    "start": robo.start,
    "forward": robo.forward,
    "reverse": robo.reverse,
    "left": robo.left,
    "right": robo.right,
    "stop": robo.stop,
}

PAGE_TEMPLATE = """
<!doctype html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>Robot Control</title>
    <style>
        :root { --bg: #0f172a; --panel: #111827; --accent: #22c55e; --text: #e5e7eb; }
        body { margin: 0; font-family: \"Segoe UI\", \"Helvetica Neue\", sans-serif; background: radial-gradient(circle at 20% 20%, #0b1224, var(--bg)); color: var(--text); display: grid; place-items: center; min-height: 100vh; }
        .wrap { width: min(960px, 90vw); padding: 32px; background: linear-gradient(135deg, rgba(34,197,94,0.08), rgba(59,130,246,0.06)); border: 1px solid rgba(255,255,255,0.05); border-radius: 20px; box-shadow: 0 30px 80px rgba(0,0,0,0.35); }
        h1 { margin: 0 0 16px; font-size: 28px; letter-spacing: 0.5px; }
        p { margin: 0 0 20px; color: #cbd5e1; }
        .grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
        form { margin: 0; }
        button { width: 100%; padding: 14px 18px; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; background: rgba(255,255,255,0.04); color: var(--text); font-size: 16px; letter-spacing: 0.3px; cursor: pointer; transition: transform 120ms ease, background 120ms ease, border-color 120ms ease; }
        button:hover { transform: translateY(-2px); background: rgba(34,197,94,0.14); border-color: rgba(34,197,94,0.4); }
        button:active { transform: translateY(0); background: rgba(34,197,94,0.22); }
        .danger { color: #fecdd3; border-color: rgba(248,113,113,0.4); }
        .danger:hover { background: rgba(248,113,113,0.12); border-color: rgba(248,113,113,0.6); }
        @media (max-width: 640px) { h1 { font-size: 24px; } }
    </style>
</head>
<body>
    <div class=\"wrap\">
        <h1>Robo Control Panel</h1>
        <p>Send motor commands from your browser. Buttons fire instantly.</p>
        <div class=\"grid\">
            {% for label, command, cls in buttons %}
            <form method=\"post\" action=\"{{ url_for('handle_action', command=command) }}\">
                <button class=\"{{ cls }}\" type=\"submit\">{{ label }}</button>
            </form>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    button_data = [
        ("Start", "start", ""),
        ("Forward", "forward", ""),
        ("Reverse", "reverse", ""),
        ("Left", "left", ""),
        ("Right", "right", ""),
        ("Stop", "stop", "danger"),
    ]
    return render_template_string(PAGE_TEMPLATE, buttons=button_data)


@app.post("/action/<command>")
def handle_action(command: str):
    action = ACTIONS.get(command)
    if action is None:
        abort(404)
    action()
    return redirect(url_for("index"))


aexit_cleanup_registered = False


def _register_cleanup_once():
    global aexit_cleanup_registered
    if not aexit_cleanup_registered:
        atexit.register(robo.cleanup)
        aexit_cleanup_registered = True


_register_cleanup_once()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
