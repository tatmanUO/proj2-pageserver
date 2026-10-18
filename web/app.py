from flask import Flask, send_from_directory, request, abort

app = Flask(__name__)

@app.before_request
def check_forbidden_path():
    # Get the original URL path before Flask normalizes it
    raw_path = request.environ.get("RAW_URI", request.path)
    raw_path = raw_path.split("?", 1)[0]

    # Check for forbidden characters
    if "~" in raw_path or "//" in raw_path or ".." in raw_path:
        abort(403)

@app.route("/")
@app.route("/<path:filename>")
def serve_file(filename="index.html"):
    return send_from_directory("DocRoot", filename)

@app.errorhandler(404)
def page_not_found(error):
    return send_from_directory("DocRoot", "404.html"), 404

@app.errorhandler(403)
def forbidden(error):
    return send_from_directory("DocRoot", "403.html"), 403

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")