from flask import Flask, url_for, render_template

app = Flask(__name__)


@app.get('/')
def assembly():  # put application's code here
    css_url = url_for('static', filename='style.css')
    return render_template("index.html", css_url=css_url)

@app.post('/')
def pene():
    1+1


if __name__ == '__main__':
    app.run()
