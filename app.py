import os

from sam.sam import app

if __name__ == "__main__":
    app.workers = 1
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
