from flask import Flask, render_template, request, redirect

app = Flask(__name__)
blog_posts = []


@app.route('/')
def hello_world():

    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        post = request.form.get('post')
        if not blog_posts:
            post_id = 1
        else:
            post_id = blog_posts[-1]['id'] + 1
        post_dict = {'id': post_id,
                     'author': author,
                     'title': title,
                     'content': post}
        blog_posts.append(post_dict)

        return redirect('/')

    return render_template('add.html')


if __name__ == '__main__':
    app.run()
