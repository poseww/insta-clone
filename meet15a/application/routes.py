from flask import render_template, redirect, url_for, flash, request, make_response, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os


from application import app
from application.models import *
from application.forms import *
from application.utils import save_image

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect(url_for('profile', username=username))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/<string:username>')
@login_required
def profile(username):
    form =  EditPostForm()

    user = User.query.filter_by(username=username).first()
    reverse_posts = Post.query.filter_by(author_id=user.id).all()

    return render_template('profile.html', title=f'{current_user.fullname} Profile', posts=reverse_posts)



@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditProfileForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        if form.username.data != user.username:
            user.username = form.username.data
        user.fullname = form.fullname.data
        user.bio = form.bio.data

        if form.profile_pic.data:
            file = form.profile_pic.data
            
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user.profile_pic = filename

        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('profile', username=current_user.username))
    
    form.username.data = current_user.username
    form.fullname.data = current_user.fullname
    form.bio.data = current_user.bio
    
    return render_template('edit.html', title=f'Edit {current_user.username} Profile', form=form)

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = CreatePostForm()

    # if form.validate_on_submit():
    #     post = Post(
    #         author_id = current_user.id,
    #         caption = form.caption.data
    #     )
    #     post.photo = save_image(form.post_pic.data)
    #     db.session.add(post)
    #     db.session.commit()
    #     flash('Your image has been posted 😁!', 'success')

    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author_id = current_user.id)\
                        .order_by(Post.post_date.desc())\
                        .paginate(page=page, per_page=3)

    

    return render_template('index.html', title='Home', form=form, posts=posts)

@app.route('/create_post', methods=['GET', 'POST'])
@login_required  # This assumes you're using Flask-Login for user authentication
def create_post():
    form = CreatePostForm()

    if form.validate_on_submit():
        post = Post(
            author_id=current_user.id,
            caption=form.caption.data
        )
        post.photo = save_image(form.post_pic.data)
        db.session.add(post)
        db.session.commit()
        flash('Your image has been posted 😁!', 'success')
        return redirect(url_for('index'))  # Redirect to the home page

    return render_template('create_post.html', title='Create Post', form=form)



@app.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', title='SignUp', form=form)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/like', methods=['GET', 'POST'])
@login_required
def like():
    data = request.json
    post_id = int(data['postId'])
    like = Like.query.filter_by(user_id=current_user.id,post_id=post_id).first()
    if not like:
        like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        return make_response(jsonify({"status" : True}), 200)
    
    db.session.delete(like)
    db.session.commit()
    return make_response(jsonify({"status" : False}), 200)


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = form.email.data

        # Check if email exists in the user data
        user = User.query.filter_by(email=email).first()

        if user:
            # Process the password reset (simplified example, in reality, you would handle this securely)
            flash('Reset password link has been sent to your email.', 'success')
            return redirect(url_for('login'))

        else:
            flash("Email not found. Please check again.")

        # No need for db.session.commit() in this case unless you are making changes to the database.

    return render_template('forgot_password.html', title='forgot_password', form=form)
    
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = EditPostForm()

    post = Post.query.get(post_id)
    if form.validate_on_submit():
        post.caption = form.caption.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('profile', username=current_user.username))

    elif request.method == 'GET':
        form.caption.data = post.caption

    return render_template('edit_post.html', title='Edit Post', form=form, post=post)


@app.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        if user.password != form.old_password.data:
            flash("ur old password is wrong")
        user.password = form.new_password.data
        user.password_Confirm = form.confirm_new_password.data

        db.session.commit()
        flash("password has been reset", 'success')
        return redirect(url_for('profile', username=current_user.username))
    
    return render_template('reset_pass.html', title='Reset Password', form=form)



if __name__ == '__main__':
    app.run(debug=True)