from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)


def load_storage_file(filename):
    """Loads blog storage from a JSON file"""
    with open(filename, 'r') as handle:
        return json.loads(handle.read())


def get_data_from_post_form():
    """Gets fields' data from POST from request"""
    fields = ['author', 'title', 'content', 'likes', 'dislikes']
    return [request.form.get(field) for field in fields]


def fetch_post_by_id(post_id):
    """Gets a post from blog_posts list by post_id"""
    for post in blog_posts:
        if post['id'] == post_id:
            return post


def update_storage_file():
    """Saves current blog_posts data into JSON storage file"""
    with open(storage_file, 'w') as handle:
        handle.write(json.dumps(blog_posts))


@app.route('/')
def render_index():
    """Renders the main page of the blog"""
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    """Shows add post form for GET request and updates storage file for POST request"""
    if request.method == 'POST':
        author, title, content = get_data_from_post_form()[:3]
        if not blog_posts:
            post_id = 1
        else:
            post_id = blog_posts[-1]['id'] + 1
        post_dict = {'id': post_id,
                     'author': author,
                     'title': title,
                     'content': content,
                     'likes': 0,
                     'dislikes': 0}
        blog_posts.append(post_dict)
        update_storage_file()
        return redirect('/')
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    """Removes a post from blog's database"""
    blog_posts.remove(fetch_post_by_id(post_id))
    update_storage_file()
    return redirect('/')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    """Renders update post form for GET request and writes changes to a database for POST request"""
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
    """Adds one like to a post with post_id"""
    fetch_post_by_id(post_id)['likes'] += 1
    update_storage_file()
    return redirect('/')


@app.route('/dislike/<int:post_id>')
def dislike_post(post_id):
    """Adds one dislike to a post with post_id"""
    fetch_post_by_id(post_id)['dislikes'] += 1
    update_storage_file()
    return redirect('/')


if __name__ == '__main__':
    """Defines storage file, loads it as blog_posts dictionary and runs the app"""
    storage_file = os.path.join('storage', 'blog_posts.json')
    blog_posts = load_storage_file(storage_file)
    app.run()
