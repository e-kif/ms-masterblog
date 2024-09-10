from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
with open(os.path.join('storage', 'blog_posts.json'), 'r') as file:
    blog_posts = json.loads(file.read())
# blog_posts = []


@app.route('/')
def hello_world():
    return render_template('index.html', posts=blog_posts)


def get_data_from_post_form():
    author = request.form.get('author')
    title = request.form.get('title')
    content = request.form.get('post')
    return author, title, content


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        author, title, content = get_data_from_post_form()
        if not blog_posts:
            post_id = 1
        else:
            post_id = blog_posts[-1]['id'] + 1
        post_dict = {'id': post_id,
                     'author': author,
                     'title': title,
                     'content': content}
        blog_posts.append(post_dict)
        return redirect('/')
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            return redirect('/')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    if request.method == 'POST':
        author, title, content = get_data_from_post_form()
        for post in blog_posts:
            if post['id'] == post_id:
                post['author'] = author
                post['title'] = title
                post['content'] = content
                return redirect('/')

    for post in blog_posts:
        if post['id'] == post_id:
            return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run()
