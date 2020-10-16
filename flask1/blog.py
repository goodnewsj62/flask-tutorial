from flask import Blueprint,url_for,g,session,redirect,render_template,abort,request,flash
from flask1.models import User,Post
from flask1 import models
from flask1 import db
from flask1.forms import UpdateForm,CreateForm
from flask_login import login_required,current_user



blog = Blueprint('blog', __name__)



@blog.route('/home', methods = ['GET'])
def home_page():

    posts = Post.query.order_by(models.Post.date_posted.desc()).all()
    return render_template('post/article.html', posts = posts)


@blog.route('/author/<string:author>',methods = ['GET'])
def author_post(author):
    author = User.query.filter_by(username = author).first()
    posts = Post.query.order_by(models.Post.date_posted.desc()).filter_by(writer = author).all()
    return render_template('post/author.html', posts =posts)

@blog.route('/detail/<int:id>', methods = ['GET'])
def detail_page(id):

    post = Post.query.get_or_404(id)
    return render_template('post/detail.html',post = post)

def check_author(post):
    if g.user != post.writer:
        return abort(403)


@blog.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update_page(id):
    post = Post.query.get_or_404(id)
    check_author(post)
    form = UpdateForm()
    if form.validate_on_submit():
        post.title= form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been successfully updated ')
        return redirect(url_for('blog.detail_page', id = post.id))
    form.title.data = post.title
    form.content.data = post.content
    return render_template('post/update.html', form = form)


@blog.route('/create',methods=['GET','POST'])
@login_required
def create_page():
    form = CreateForm()

    if form.validate_on_submit():
        post = Post(title = form.title.data,content = form.content.data, writer = current_user)
        db.session.add(post)
        db.session.commit()
        flash('post has been created successfully')
        return redirect(url_for('blog.home_page'))
    return render_template('post/create.html', form = form)


@blog.route('/delete/<int:id>',methods=['GET','POST'])
@login_required
def delete_page(id):
    post = Post.query.get_or_404(id)
    check_author(post)
    if request == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('deleted post successfully')
        return redirect(url_for('blog.home_page'))
    return render_template('post/delete.html')