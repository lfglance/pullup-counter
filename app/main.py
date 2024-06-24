from datetime import datetime, timedelta
from random import randint

from flask import Flask, render_template, request, redirect

from app.models import Pullup
from app.helpers import log


app = Flask(__name__)


@app.route("/")
def index():
    """
    Load the dashboard with pullups/pushups data.
    If a form was submitted, capture the data and 
    store in the database, redirecting back home.
    """
    pullups = Pullup.select().order_by(Pullup.date.asc())
    if request.args:
        log("Found form submission")
        d = request.args.get('date')
        dd = datetime.fromisoformat(d.rstrip("Z") + "+00:00")
        p = Pullup.create(
            date=dd,
            clean=request.args.get("clean", 0),
            negative=request.args.get("negative", 0),
            pushup=request.args.get("pushup", 0)
        )
        p.save()
        log(f"Created pullup object {p.id}")
        return redirect("/")
    return render_template("index.html", pullups=pullups)


@app.route("/generate")
def generate():
    """
    Iterate over the past N days and randomly create
    fake pullup and pushup data for testing purposes.
    Intended to be used as an AJAX request and not 
    rendered in the browser.
    """
    res = []
    now = datetime.now()
    log("Generating dummy data")
    for i in range(30):
        day = now - timedelta(days=i)
        for _ in range(randint(0, 8)):
            hour = randint(0, 23)
            minute = randint(0, 59)
            rand_time = day.replace(hour=hour, minute=minute)
            p = Pullup.create(
                date=rand_time,
                clean=randint(0, 20),
                negative=randint(0, 20),
                pushup=randint(0, 20)
            )
            p.save()
            res.append(p.id)
    log(f"Created {len(res)} pullup objects")
    return "ok"


@app.route("/delete")
def delete():
    """
    Delete all of the data in the database.
    """
    pullups = Pullup.select()
    log(f"Deleting {pullups.count()} pullup objects")
    for pullup in pullups:
        pullup.delete_instance()
    return "ok"


if __name__ == "__main__":
    app.run()