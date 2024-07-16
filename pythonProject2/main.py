from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///TODO.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class TODO(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    desc = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"{self.title} - {self.desc}"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/LOGIN", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["DESC"]
        db.session.add(TODO(title=title, desc=desc))
        db.session.commit()
    alltodo = TODO.query.all()
    return render_template("index.html", alltodo=alltodo)


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = TODO.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/LOGIN")


@app.route("/update", methods=["POST", "GET"])
def update():
    pass
    #sno = request.form[""]
    #alltodo = TODO.query.filter_by(sno=sno).first()
    #return render_template("index.html", alltodo=alltodo)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
