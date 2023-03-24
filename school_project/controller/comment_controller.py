from school_project import app
from flask import render_template,session, request,redirect,session,flash
from school_project.model.comment_model import Comment
from school_project.model.queens_model import Queen
from flask import url_for

@app.route('/save_comment/<int:queen_id>', methods = ['POST'])
def save_comment(queen_id):
    if not Comment.validate_comment(request.form):
        return redirect(f'/add_comment/{queen_id}')  #url needs to redirect back to add comment. id's are different.
    
    queen_data = {
        'user_id': session['user_id'],
        'queen_id': queen_id,
        'comment': request.form['comment'],
        'updated_at' : 'updated_at',
        'created_at' :'created_at'
    }
    print(queen_data)
    Comment.save_comment(queen_data)
    return redirect(f'/add_comment/{queen_id}')


@app.route('/add_comment/<int:queen>')
def add_comment(queen):
    if 'user_id' not in session:
        flash("Please log in to see this page")
    comment = Queen.get_one_queen_comment(queen)
    return render_template('comments.html', queen = comment)

@app.route('/delete_comment/<int:comment_id>')
def delete_comment(comment_id):
    if 'user_id' not in session:
        flash("Please log in to see this page")
    data ={
        'id': comment_id
    }
    comments = Comment.get_one_comment(data)
    Comment.delete_comment(data)
    # Queen.get_one_queen_comment(id)
    return redirect(f'/add_comment/{comments.queen_id}') # want redirect to go to add_comment.

@app.route('/edit_comment/<int:comment_id>')
def edit_a_comment(comment_id):
    if 'user_id' not in session:
        flash("Please log in to see this page")

    data = {
        "id":comment_id
    }
    comment = Comment.get_one_comment(data)
    Comment.edit_comment(request.form)
    return render_template("edit_comment.html", comment = comment)

@app.route('/edited_comment/<int:comment_id>', methods=['post'])
def edited_a_comment(comment_id):
    data = {"id": id,
        'queen_id': request.form['queen_id'],
        'user_id': request.form['user_id'],
        'comment': request.form['comment'],
    }
    if not Comment.validate_comment(data):
        return redirect(f'/edit_comment/{comment_id}')
    print(data)
    comments = Comment.get_one_comment(data)
    Comment.edit_comment(data)
    return redirect(f"/add_comment/{comments.queen_id}")