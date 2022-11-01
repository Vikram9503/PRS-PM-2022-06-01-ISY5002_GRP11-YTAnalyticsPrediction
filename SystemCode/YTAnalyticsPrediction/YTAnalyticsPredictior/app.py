from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
import pandas as pd
import consume as consumeModel
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        #print("f.filename:"+f.filename)
        usrvideofile=f.filename
        upload_status = "File Uploaded"
    return render_template("home.html")


@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        pr_like_counts,pr_view_counts= consumeModel.PredictLikeandView(usrvideofile)
        #prediction_text="Your Video View Counts would be {} ".format(pr_view_counts)+" Your Video Like Counts Would be {}".format(pr_like_counts)
        #print(prediction_text)
        return render_template('home.html',prediction_text="Your Video View Counts would be {} ".format(pr_view_counts)+" &  Like Counts Would be {}".format(pr_like_counts)
                               )

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
