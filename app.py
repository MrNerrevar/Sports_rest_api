from sanic import Sanic
from routes.sports import sport_bp
from routes.events import event_bp
from routes.selections import selection_bp

app = Sanic(__name__)
app.blueprint(sport_bp)
app.blueprint(event_bp)
app.blueprint(selection_bp)

# Run the app
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
