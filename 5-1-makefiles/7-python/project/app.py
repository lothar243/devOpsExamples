from flask import Flask
from pathlib import Path

app = Flask(__name__)

DB_PATH = Path("project/sharespace.db")


@app.route("/")
def index():
    if DB_PATH.exists():
        contents = DB_PATH.read_text()
        return f"""
        <h1>ShareSpace App</h1>
        <p><strong>Database file exists.</strong></p>
        <pre>{contents}</pre>
        """
    else:
        return """
        <h1>ShareSpace App</h1>
        <p style="color:red;"><strong>Database file does NOT exist.</strong></p>
        """


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

