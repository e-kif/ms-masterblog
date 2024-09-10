from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
# blog_posts = []
filename = os.path.join('storage', 'blog_posts.json')
print(filename)
with open(filename, 'r') as file:
    blog_posts = json.loads(file.read())
# blog_posts = []


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


@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break
    return redirect('/')


if __name__ == '__main__':
    app.run()
