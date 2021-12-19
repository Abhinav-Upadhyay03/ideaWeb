from flask import Blueprint, render_template, request, redirect
from flask.helpers import flash, url_for
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import text
from .models import Comment, Post, User
from . import db

views = Blueprint('views',__name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', user = current_user, posts=posts)

@views.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        text = request.form.get('text')

        if not text:
            flash("Post cannot be empty!", category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()            
            flash("Post created!", category='success')
            return redirect(url_for('views.home'))
        
    return render_template('create_post.html', user=current_user)

@login_required
@views.route('/delete-post/<id>')
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist!", category='error')
    elif current_user.id != post.author:
        flash("You do nothave the permission to delete this post!", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted!!!", category='success')
    
    return redirect(url_for('views.home'))

@login_required
@views.route('/posts/<username>')
def posts(username):
    user = User.query.filter_by(username=username).first()
        
    if not user:
        flash("No user found!", category= 'error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template('posts.html', user=current_user, posts=posts, username=username)

@login_required
@views.route('/create-comment/<post_id>', methods = ['POST'])
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comments cannot be empty', category='error')
    else:
        post = Post.query.filter_by(id=post_id)

        if not post:
            flash("Post not found", category='error')
        else:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment was added!", category='success')

    return redirect(url_for('views.home'))

@login_required
@views.route('/like-post/<post_id>')
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if not post:
        flash("Post not found", category='error')
    else:
        post.likes += 1
        db.session.commit()
        flash("Post liked!", category='success')

    return redirect(url_for('views.home'))
