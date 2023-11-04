from flask import Flask, render_template, request, redirect, url_for
from flask_flatpages import FlatPages
import controllers

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'notes'
app = Flask(__name__)
flatpages = FlatPages(app=app)
app.config.from_object(__name__)


@app.route('/view/<id>')
def view(id):
    path = '{}/{}'.format(POST_DIR, id)
    post = flatpages.get_or_404(path)
    return render_template('notes/view.html', post=post)


@app.route('/create', methods=['GET', 'POST'])
def create():
    reason = ""
    if request.method == 'POST':
        reason = controllers.create_note(request)
        if reason == "OK":
            return redirect(url_for('index'))
    
    return render_template('notes/create.html', reason=reason)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('not_found.html')


@app.route('/')
def index():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    return render_template('index.html', posts=posts)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=False)