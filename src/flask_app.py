import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
print("Initializing Flask app, please wait.")

from flask import Flask, render_template, request, send_file, jsonify
from models.predict import enhance_image
import io

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        # Gets file object
        image_file = request.files["image"]

        if image_file:
            try:
                # Calls the enhance_image function to enhance the input
                enhanced_image = enhance_image(image_file)

                # Loads the file in memory
                img_io = io.BytesIO()
                enhanced_image.save(img_io, "PNG")
                img_io.seek(0)

                # Returns the enhanced image to the webpage
                return send_file(img_io, mimetype=f'image/png')
            except Exception as e:
                return jsonify({"Error": f"Error while saving file: {e}"}), 500

    # Returns the index.html template
    return render_template("index.html")


if __name__ == "__main__":
    app.run(use_reloader=False, use_debugger=False)
