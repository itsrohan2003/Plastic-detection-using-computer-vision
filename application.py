from flask import Flask, request, render_template, redirect, jsonify, url_for
from flask_jsglue import JSGlue
import util
import os
from werkzeug.utils import secure_filename

application = Flask(__name__)
jsglue = JSGlue(application)  # Initialize JSGlue with the Flask app

util.load_artifacts()

# Home page
@application.route("/")
def home():
    return render_template("home.html")

# Classify waste
@application.route("/classifywaste", methods=["POST"])
def classifywaste():
    if "file" not in request.files:
        return jsonify(error="No file part"), 400

    image_data = request.files["file"]
    if image_data.filename == "":
        return jsonify(error="No selected file"), 400

    # Save the uploaded image
    basepath = os.path.dirname(__file__)
    image_path = os.path.join(basepath, "uploads", secure_filename(image_data.filename))
    image_data.save(image_path)

    predicted_value, details, video1, video2 = util.classify_waste(image_path)
    os.remove(image_path)

    return jsonify(predicted_value=predicted_value, details=details, video1=video1, video2=video2)

# Custom 404 page
@application.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    application.run(debug=True)  # Run the Flask app in debug mode
