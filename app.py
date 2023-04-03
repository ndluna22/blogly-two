from flask import Flask, request, render_template,  redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db,  connect_db, User, Post

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    """Original page"""

    return redirect('/users')


@app.route('/users')
def list_users():
    """List users"""

    users = User.query.all()
    return render_template('users/list.html', users=users)


@app.route('/users/new', methods=['GET'])
def users_form():
    """Form for new users"""

    return render_template('users/newuser.html')


@app.route('/users/new', methods=['POST'])
def new_user():
    """Process form to add new users"""

    first_name = request.form['first_name'],
    last_name = request.form['last_name'],
    image_url = request.form['image_url'] or None

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Show information about the given user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html', user=user)


@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    """Show the edit page for a user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def list_user_edit(user_id):
    """Process the edit form, returning the user to the /users page"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_users(user_id):
    """Delete the user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# POSTS BELOW


@app.route('/users/<int:user_id>/posts/new')
def posts_form(user_id):
    """Show form to add a post for that user."""
    user = User.query.get_or_404(user_id)
    return render_template('posts/newpost.html', user=user)  # newpost.html


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""

    user = User.query.get_or_404(user_id)
    title = request.form['title'],
    content = request.form['content'],

    new_post = Post(title,
                    content, user=user)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')  # takes to user detail


@app.route('/posts/<int:post_id>')
def user_results(post_id):
    """Show a post. Show edit and delete buttons"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/postdetail.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_posts(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/postedit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def post_results(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title'],
    post.content = request.form['content'],

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_posts(user_id):
    """Delete the post."""

    post = Post.query.get_or_404(user_id)
    db.session.delete(post)
    db.session.commit()

    return redirect("/users/<int:user_id>")
