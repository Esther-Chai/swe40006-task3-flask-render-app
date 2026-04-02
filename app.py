from flask import Flask
import os

app = Flask(__name__)

SECRET_MESSAGE = os.environ.get("SECRET_MESSAGE", "No secret set")
STUDENT_NAME = os.environ.get("STUDENT_NAME", "Student")

@app.route("/")
def home():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Task 3.2 – Flask App</title>
      <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
          font-family: 'Segoe UI', sans-serif;
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
        }}
        .card {{
          background: white;
          border-radius: 16px;
          padding: 48px;
          text-align: center;
          box-shadow: 0 20px 60px rgba(0,0,0,0.2);
          max-width: 500px;
          width: 90%;
        }}
        .badge {{
          display: inline-block;
          background: #f5576c;
          color: white;
          font-size: 12px;
          font-weight: 600;
          padding: 4px 12px;
          border-radius: 20px;
          letter-spacing: 1px;
          text-transform: uppercase;
          margin-bottom: 20px;
        }}
        h1 {{ font-size: 2rem; color: #1a1a2e; margin-bottom: 12px; }}
        p  {{ color: #666; line-height: 1.6; margin-bottom: 16px; }}
        .env-box {{
          background: #fff7ed;
          border: 1px solid #fed7aa;
          border-radius: 8px;
          padding: 16px;
          margin: 16px 0;
          text-align: left;
        }}
        .env-box span {{ font-weight: 600; color: #ea580c; }}
        .status {{
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          background: #f0fdf4;
          border: 1px solid #86efac;
          border-radius: 8px;
          padding: 12px 20px;
          color: #16a34a;
          font-weight: 600;
          margin-top: 20px;
        }}
        .dot {{
          width: 10px; height: 10px;
          background: #22c55e;
          border-radius: 50%;
          animation: pulse 1.5s infinite;
        }}
        @keyframes pulse {{
          0%, 100% {{ opacity: 1; }}
          50%       {{ opacity: 0.4; }}
        }}
      </style>
    </head>
    <body>
      <div class="card">
        <div class="badge">Task 3.2</div>
        <h1>⚙️ Flask on Render</h1>
        <p>A Python/Flask web app deployed with environment variables and auto-deploy via Git push.</p>
        <div class="env-box">
          <p>👤 Student: <span>{STUDENT_NAME}</span></p>
          <p>🔐 Secret Message: <span>{SECRET_MESSAGE}</span></p>
        </div>
        <div class="status">
          <div class="dot"></div>
          Flask App Running
        </div>
      </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
