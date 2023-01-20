from flask import Flask
from flask import render_template
from flask import request
from flask import url_for, flash, redirect
import ai21

ai21.api_key = "WPdqS4g8dDE8DluGB8rKxk1UVYEuAfwR"

app = Flask(__name__)

messages = [{'title': 'Message One', 'content': 'These are your summary'}]


@app.route('/')
def index():
  return render_template('index.html', messages=messages)


@app.route('/create/', methods=('GET', 'POST'))
def create():
  if request.method == 'POST':
    article = request.form['article']
    content = summary_text("Write a insight of the article : " + article)

    if not article:
      flash("Article is required")
    else:
      messages.append({'title': article, 'content': content})
      return redirect(url_for('index'))
  return render_template('create.html')


def summary_text(article):
  response = ai21.Completion.execute(model="j1-grande",
                                     custom_model="article_Summarizer",
                                     prompt=article,
                                     maxTokens=300,
                                     temperature=0.7)
  generated_summary = response['completions'][0]['data']['text']

  return generated_summary


if __name__ == '__main__':
  app.run()