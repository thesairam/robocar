import os
from flask import Flask, abort, redirect, render_template_string, url_for
import atexit
import robo

app = Flask(__name__)

DEFAULT_SPEED = int(getattr(robo, "current_speed", 60))

ACTIONS = {
    "start": robo.start,
    "forward": robo.forward,
    "reverse": robo.reverse,
    "left": robo.left,
    "right": robo.right,
    "turnoff": robo.stop,
}

PAGE_TEMPLATE = """
<!doctype html>
<html lang=\"en\">
<head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>Robot Control</title>
    <style>
        :root { --bg: #0f172a; --panel: #0b1224; --panel-2: #0f172a; --accent: #22c55e; --accent-2: #60a5fa; --text: #e5e7eb; --muted: #cbd5e1; }
        * { box-sizing: border-box; }
        body { margin: 0; font-family: \"Segoe UI\", \"Helvetica Neue\", sans-serif; background: radial-gradient(circle at 20% 20%, #0b1224, var(--bg)); color: var(--text); display: grid; place-items: center; min-height: 100vh; padding: 18px; }
        .wrap { width: min(1000px, 96vw); padding: 28px; background: linear-gradient(135deg, rgba(34,197,94,0.08), rgba(59,130,246,0.06)); border: 1px solid rgba(255,255,255,0.05); border-radius: 20px; box-shadow: 0 30px 80px rgba(0,0,0,0.35); }
        h1 { margin: 0 0 8px; font-size: 28px; letter-spacing: 0.4px; }
        p.sub { margin: 0 0 22px; color: var(--muted); }
        .layout { display: grid; gap: 24px; grid-template-columns: 1fr 280px; align-items: center; }
        .panel { background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02)); border: 1px solid rgba(255,255,255,0.06); border-radius: 18px; padding: 18px; box-shadow: inset 0 1px 0 rgba(255,255,255,0.05); }
        .joystick { position: relative; width: min(320px, 70vw); aspect-ratio: 1 / 1; margin: 0 auto; border-radius: 20px; background: radial-gradient(circle at 50% 45%, rgba(96,165,250,0.12), rgba(17,24,39,0.7)); border: 1px solid rgba(255,255,255,0.05); overflow: hidden; touch-action: none; }
        .ring { position: absolute; inset: 12%; border-radius: 50%; border: 1px dashed rgba(255,255,255,0.12); }
        .knob { position: absolute; left: 50%; top: 50%; width: 96px; height: 96px; margin-left: -48px; margin-top: -48px; border-radius: 30px; background: radial-gradient(circle at 30% 30%, #e0f2fe, #60a5fa); box-shadow: 0 12px 30px rgba(59,130,246,0.35); transition: transform 120ms ease; will-change: transform; }
        .grid-actions { display: grid; gap: 10px; }
        button { width: 100%; padding: 14px 16px; border: 1px solid rgba(255,255,255,0.09); border-radius: 12px; background: rgba(255,255,255,0.05); color: var(--text); font-size: 15px; letter-spacing: 0.3px; cursor: pointer; transition: transform 140ms ease, background 140ms ease, border-color 140ms ease; }
        button:hover { transform: translateY(-1px); background: rgba(34,197,94,0.14); border-color: rgba(34,197,94,0.4); }
        button:active { transform: translateY(0); background: rgba(34,197,94,0.22); }
        .danger { color: #fecdd3; border-color: rgba(248,113,113,0.5); }
        .danger:hover { background: rgba(248,113,113,0.12); border-color: rgba(248,113,113,0.7); }
        .status { display: inline-flex; align-items: center; gap: 8px; padding: 10px 14px; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); color: var(--muted); font-size: 14px; }
        .badge { display: inline-block; padding: 6px 10px; border-radius: 10px; background: rgba(34,197,94,0.14); color: var(--text); border: 1px solid rgba(34,197,94,0.4); font-weight: 600; letter-spacing: 0.3px; }
        .hint { color: var(--muted); font-size: 13px; margin-top: 12px; text-align: center; }
        @media (max-width: 780px) { .layout { grid-template-columns: 1fr; } h1 { font-size: 24px; } .knob { width: 88px; height: 88px; margin-left: -44px; margin-top: -44px; } }
    </style>
</head>
<body>
    <div class=\"wrap\">
        <h1>Robo Control Panel</h1>
        <p class=\"sub\">Drag the joystick to steer. Release keeps the last command; use buttons to start/stop.</p>
        <div class=\"layout\">
            <div class=\"panel\">
                <div class=\"joystick\" data-joystick>
                    <div class=\"ring\"></div>
                    <div class=\"knob\" data-knob></div>
                </div>
                <div class=\"hint\">Tip: works with mouse, touch, and arrow keys.</div>
            </div>
            <div class=\"panel\">
                <div class=\"grid-actions\">
                    <button data-command=\"start\">Start motors</button>
                    <button data-command=\"forward\">Forward</button>
                    <button data-command=\"reverse\">Reverse</button>
                    <button data-command=\"left\">Left</button>
                    <button data-command=\"right\">Right</button>
                    <button class="danger" data-command="turnoff">Turn off</button>
                        <div style="margin-top:10px;">
                            <label for="speed" style="display:block;margin-bottom:6px;color:var(--muted);font-size:13px;">Speed</label>
                            <input id="speed" data-speed type="range" min="0" max="100" value="{{ speed }}" style="width:100%;" />
                            <div style="margin-top:6px;font-size:13px;color:var(--muted);">Current: <span data-speed-value>{{ speed }}</span>%</div>
                        </div>
                </div>
                <div class=\"status\" style=\"margin-top:12px;\">
                    <span class=\"badge\">Live</span>
                    <span data-status>Ready</span>
                </div>
            </div>
        </div>
    </div>
    <script>
        const joystick = document.querySelector('[data-joystick]');
        const knob = document.querySelector('[data-knob]');
        const statusEl = document.querySelector('[data-status]');
        const buttons = document.querySelectorAll('[data-command]');
        const speedInput = document.querySelector('[data-speed]');
        const speedValue = document.querySelector('[data-speed-value]');

        const maxRadius = 90; // pixels from center
        const deadZone = 14; // ignore small jitter
        let pointerId = null;
        let lastCommand = null;

        const setStatus = (text) => { statusEl.textContent = text; };

        const sendCommand = async (cmd) => {
            if (!cmd || cmd === lastCommand) return;
            lastCommand = cmd;
            setStatus(cmd === 'turnoff' ? 'Turned off' : `Command: ${cmd}`);
            try {
                await fetch(`/action/${cmd}`, { method: 'POST' });
            } catch (err) {
                setStatus('Connection issue');
            }
        };

        const moveKnob = (x, y) => {
            knob.style.transform = `translate(${x}px, ${y}px)`;
        };

        const directionFromVector = (x, y) => {
            const dist = Math.hypot(x, y);
            if (dist < deadZone) return null; // stay in last commanded state
            if (Math.abs(x) > Math.abs(y)) {
                return x > 0 ? 'right' : 'left';
            }
            return y > 0 ? 'reverse' : 'forward';
        };

        const handleVector = (clientX, clientY) => {
            const rect = joystick.getBoundingClientRect();
            const x = clientX - (rect.left + rect.width / 2);
            const y = clientY - (rect.top + rect.height / 2);
            const dist = Math.hypot(x, y);
            const clampedDist = Math.min(dist, maxRadius);
            const scale = dist === 0 ? 0 : clampedDist / dist;
            const clampedX = x * scale;
            const clampedY = y * scale;
            moveKnob(clampedX, clampedY);
            const dir = directionFromVector(x, y);
            if (dir) sendCommand(dir);
        };

        const resetKnob = () => {
            moveKnob(0, 0);
            // keep outputs as-is; rely on buttons for start/stop
        };

        joystick.addEventListener('pointerdown', (event) => {
            pointerId = event.pointerId;
            joystick.setPointerCapture(pointerId);
            handleVector(event.clientX, event.clientY);
        });

        joystick.addEventListener('pointermove', (event) => {
            if (event.pointerId !== pointerId) return;
            handleVector(event.clientX, event.clientY);
        });

        const endInteraction = (event) => {
            if (event.pointerId !== pointerId) return;
            pointerId = null;
            joystick.releasePointerCapture(event.pointerId);
            lastCommand = null; // allow re-sending same direction next time
            resetKnob();
        };

        joystick.addEventListener('pointerup', endInteraction);
        joystick.addEventListener('pointercancel', endInteraction);

        buttons.forEach((button) => {
            button.addEventListener('click', () => {
                sendCommand(button.dataset.command);
            });
        });

        const keyMap = {
            ArrowUp: 'forward',
            ArrowDown: 'reverse',
            ArrowLeft: 'left',
            ArrowRight: 'right',
            ' ': 'turnoff'
        };

        const updateSpeed = async (value) => {
                const clamped = Math.max(0, Math.min(100, Number(value)));
                speedValue.textContent = clamped;
            try {
                    await fetch(`/speed/${clamped}`, { method: 'POST' });
            } catch (err) {
                setStatus('Speed update failed');
            }
        };

        if (speedInput) {
            speedInput.addEventListener('input', (event) => {
                updateSpeed(event.target.value);
            });
        }

        document.addEventListener('keydown', (event) => {
            const cmd = keyMap[event.key];
            if (!cmd) return;
            event.preventDefault();
            sendCommand(cmd);
        });

        document.addEventListener('keyup', (event) => {
            const cmd = keyMap[event.key];
            if (!cmd) return;
            event.preventDefault();
            lastCommand = null; // clear so next press re-sends
        });
    </script>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(PAGE_TEMPLATE, speed=DEFAULT_SPEED)


@app.post("/action/<command>")
def handle_action(command: str):
    action = ACTIONS.get(command)
    if action is None:
        abort(404)
    action()
    return redirect(url_for("index"))


@app.post("/speed/<int:value>")
def handle_speed(value: int):
    try:
        robo.set_speed(value)
    except Exception:
        abort(400)
    return ("", 204)


aexit_cleanup_registered = False


def _register_cleanup_once():
    global aexit_cleanup_registered
    if not aexit_cleanup_registered:
        atexit.register(robo.cleanup)
        aexit_cleanup_registered = True


_register_cleanup_once()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
