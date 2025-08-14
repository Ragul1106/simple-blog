from flask import render_template, redirect, url_for, flash, request
from models import db, Post

def init_routes(app):

    @app.route("/")
    def index():
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template("index.html", posts=posts)

    @app.route("/post/new", methods=["GET", "POST"])
    def create_post():
        if request.method == "POST":
            title = request.form["title"]
            content = request.form["content"]
            author = request.form["author"]

            new_post = Post(title=title, content=content, author=author)
            db.session.add(new_post)
            db.session.commit()
            flash("Post created successfully!", "success")
            return redirect(url_for("index"))

        return render_template("create_post.html")

    @app.route("/post/edit/<int:id>", methods=["GET", "POST"])
    def edit_post(id):
        post = Post.query.get_or_404(id)
        if request.method == "POST":
            post.title = request.form["title"]
            post.content = request.form["content"]
            post.author = request.form["author"]
            db.session.commit()
            flash("Post updated successfully!", "info")
            return redirect(url_for("index"))

        return render_template("edit_post.html", post=post)

    @app.route("/post/delete/<int:id>")
    def delete_post(id):
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully!", "danger")
        return redirect(url_for("index"))
