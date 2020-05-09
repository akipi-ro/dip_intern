# coding: utf-8
import os, shutil
from flask import Flask, request, redirect, url_for, render_template, Markup
from werkzeug.utils import secure_filename
import numpy as np
import pandas as pd
import pickle
from sklearn.externals import joblib
import csv
import urllib.request
import tempfile
from flask import Flask, send_file, make_response, send_from_directory

UPLOAD_FOLDER = "./static/excel/"
ALLOWED_EXTENSIONS = {"csv"}
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/result", methods=["GET","POST"])
def result():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(url_for("index"))
        file = request.files["file"]
        if not allowed_file(file.filename):
            print(file.filename + ": File not allowed!")
            return redirect(url_for("index"))
        if "file" in request.files:
            df_file = pd.read_csv(file,encoding="utf-8")
            df_file_2 = df_file.drop(["お仕事No."],axis = 1)

            df_file_2=df_file_2.dropna(how="all",axis=1)
            
            df_file_2=df_file_2.drop(["掲載期間　開始日","掲載期間　終了日","動画コメント","応募資格"
            ,"派遣会社のうれしい特典","お仕事のポイント（仕事PR）","（派遣先）職場の雰囲気","期間･時間　備考"
            ,"勤務地　最寄駅2（駅名）","勤務地　最寄駅2（沿線名）","（紹介予定）雇用形態備考","（紹介予定）休日休暇","勤務地　最寄駅1（駅名）","給与/交通費　備考"
            ,"休日休暇　備考","（派遣）応募後の流れ","期間・時間　勤務時間","（派遣先）概要　事業内容","（紹介予定）年収・給与例","勤務地　最寄駅1（沿線名）"
            ,"動画タイトル","仕事内容","（派遣先）配属先部署","動画ファイル名","（派遣先）勤務先写真ファイル名","（紹介予定）待遇・福利厚生"
            ,"勤務地　備考","拠点番号","お仕事名","（紹介予定）入社時期","期間・時間　勤務開始日"
            ,"（派遣先）概要　勤務先名（漢字）","学校・公的機関（官公庁）"],axis=1)
            df_file_2=df_file_2.fillna(0)

            x2_array = np.array(df_file_2)
            
            rfr = pd.read_csv("model.pickle")

            y2_pread = rfr.predict(x2_array)

            pread_format = pd.DataFrame({"お仕事No.":df_file["お仕事No."],"応募数 合計":y2_pread})

            pread=pread_format.to_csv("Answer",index=False)
    else:
        return redirect(url_for("index"))

@app.route('/report1/<string:report_id>', methods=['GET'])
def report1(report_id):
    downloadFileName = 'report1_' + report_id + '.csv'
    downloadFile = 'test_x.csv'
    XLSX_MIMETYPE = 'application/vnd.ms-Excel'
    return send_file(downloadFile, as_attachment = True,
        attachment_filename = downloadFileName,
        mimetype = XLSX_MIMETYPE)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
