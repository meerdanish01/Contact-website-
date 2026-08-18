import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
# Change secret_key to something secure
app.secret_key = "danu_gmr_secret_key_123"

# Admin password (Aap ise badal sakte hain)
ADMIN_PASSWORD = "danu@admin123"

DATA_FILE = "data.json"

DEFAULT_DATA = {
    "whatsapp": "https://whatsapp.com/channel/example",
    "telegram": "https://t.me/example",
    "youtube": "https://youtube.com/@example",
    "telegram_admin": "danugamer_admin"
}

def load_links():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump(DEFAULT_DATA, f, indent=4)
        return DEFAULT_DATA
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA

def save_links(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    links = load_links()
    return render_template("index.html", links=links)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    links = load_links()
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "login":
            password = request.form.get("password")
            if password == ADMIN_PASSWORD:
                session["logged_in"] = True
                flash("Login Successful!", "success")
            else:
                flash("Incorrect Password!", "danger")
            return redirect(url_for("admin"))
            
        elif action == "update":
            if not session.get("logged_in"):
                return redirect(url_for("admin"))
                
            new_data = {
                "whatsapp": request.form.get("whatsapp", "").strip(),
                "telegram": request.form.get("telegram", "").strip(),
                "youtube": request.form.get("youtube", "").strip(),
                "telegram_admin": request.form.get("telegram_admin", "").strip().replace("@", "")
            }
            save_links(new_data)
            flash("Links Updated Successfully!", "success")
            return redirect(url_for("admin"))

    return render_template("admin.html", links=links)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("admin"))

if __name__ == "__main__":
    app.run(debug=True)
