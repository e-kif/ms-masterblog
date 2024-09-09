from flask import Flask, render_template

app = Flask(__name__)
blog_posts = [{}, {}]


@app.route('/')
def hello_world():

    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run()
