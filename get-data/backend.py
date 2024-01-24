from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import asyncio
import os

from pytok.tiktok import PyTok
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = Flask(__name__, template_folder=os.path.abspath('../templates'))

pretrained = "mdhugol/indonesia-bert-sentiment-classification"

model = AutoModelForSequenceClassification.from_pretrained(pretrained)
tokenizer = AutoTokenizer.from_pretrained(pretrained)

sentiment_analysis = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

async def fetch_user_data(username):
    async with PyTok() as api:
        user = api.user(username=username)
        user_data = await user.info()
        return user_data

async def fetch_and_save_user_data(username, user_filename="info_user.json"):
    user_data = await fetch_user_data(username)
    with open(user_filename, "w") as f:
        json.dump(user_data, f)

async def get_comments(video_id, author_id):
    async with PyTok(headless=False) as api:
        comments = []
        async for comment in api.video(id=video_id, username=author_id).comments(count=200):
            comments.append(comment)
        return comments

def parse_tiktok_link(tiktok_link):
    parts = tiktok_link.split('/')
    video_id = parts[-1]
    author_id = parts[3].replace('@', '')
    return video_id, author_id

def get_text_only(data):
    arr = []
    for i in data:
        arr.append(i['text'])
        if i['reply_comment'] is not None:
            for j in i['reply_comment']:
                arr.append(j['text'])
    return arr

def get_sentimen(text):
  label_index = {'LABEL_0': 'positive', 'LABEL_1': 'neutral', 'LABEL_2': 'negative'}
  result = sentiment_analysis(text)
  status = label_index[result[0]['label']]
  return status

def save_sentimen(text):
    arr = []
    for i in text:
        arr.append(get_sentimen(str(i)))
    with open("sentimen.json", "w") as f:
        json.dump(arr, f)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/get_user_data', methods=['POST'])
def get_user_data():
    username = request.form['username']
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_and_save_user_data(username))
    return redirect(url_for('index'))

@app.route('/get_info_data')
def get_info_data():
    with open('info_user.json', 'r') as file:
        info_data = json.load(file)
    return jsonify(info_data)

@app.route('/get_komentar_post', methods=['GET', 'POST'])
def get_komentar_post():
    if request.method == 'POST':
        tiktok_link = request.form['tiktok_link']
        video_id, author_id = parse_tiktok_link(tiktok_link)

        if video_id and author_id:
            comments = asyncio.run(get_comments(video_id, author_id))
            with open("komentar.json", "w") as f:
                json.dump(comments, f)
            # page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
            # total_komen = len(comments)
            # pagination = Pagination(page=page, per_page=per_page, total=total_komen, css_framework='bootstrap4')
            # comment_display = comments[offset: offset + per_page]
            return render_template('resultKomen.html', komentar=comments)
        else:
            return render_template('index.html')
    else:
        with open('komentar.json', 'r') as file:
            komentar = json.load(file)
        return render_template('resultKomen.html', komentar=komentar)


@app.route('/get_sentimen_prediksi', methods=['GET', 'POST'])
def get_sentimen_prediksi():
    if request.method == 'POST':
        with open('komentar.json', 'r') as file:
            komentar = json.load(file)
        text_komen = get_text_only(komentar)
        save_sentimen(text_komen)
        with open('sentimen.json', 'r') as file:
            sentimen = json.load(file)
        return render_template('resultSentimen.html', sentimen=sentimen)
    else:
        with open('sentimen.json', 'r') as file:
            sentimen = json.load(file)
        return render_template('resultSentimen.html', sentimen=sentimen)

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, port=5500)