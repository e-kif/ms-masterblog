from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
# blog_posts = []
STORAGE_FILE = os.path.join('storage', 'blog_posts.json')
with open(STORAGE_FILE, 'r') as file:
    blog_posts = json.loads(file.read())


def get_data_from_post_form():
    fields = ['author', 'title', 'content', 'likes', 'dislikes']
    return [request.form.get(field) for field in fields]


def fetch_post_by_id(post_id):
    for post in blog_posts:
        if post['id'] == post_id:
            return post


def update_storage_file():
    with open(STORAGE_FILE, 'w') as handle:
        handle.write(json.dumps(blog_posts))


@app.route('/')
def hello_world():
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        author, title, content = tuple(list(get_data_from_post_form()[:3]))
        if not blog_posts:
            post_id = 1
        else:
            post_id = blog_posts[-1]['id'] + 1
        post_dict = {'id': post_id,
                     'author': author,
                     'title': title,
                     'content': content}
        blog_posts.append(post_dict)
        update_storage_file()
        return redirect('/')
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    blog_posts.remove(fetch_post_by_id(post_id))
    update_storage_file()
    return redirect('/')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        author, title, content, likes, dislikes = get_data_from_post_form()
        post = fetch_post_by_id(post_id)
        post['author'] = author
        post['title'] = title
        post['content'] = content
        if likes:
            post['likes'] = 0
        if dislikes:
            post['dislikes'] = 0
        update_storage_file()
        return redirect('/')
    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def like_post(post_id):
    fetch_post_by_id(post_id)['likes'] += 1
    update_storage_file()
    return redirect('/')


@app.route('/dislike/<int:post_id>')
def dislike_post(post_id):
    fetch_post_by_id(post_id)['dislikes'] += 1
    update_storage_file()
    return redirect('/')


if __name__ == '__main__':
    app.run()
