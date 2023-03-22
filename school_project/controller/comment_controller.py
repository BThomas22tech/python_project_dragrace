from school_project import app
from flask import render_template,session, request,redirect,session,flash
from school_project.model.comment_model import Comment
from school_project.model.queens_model import Queen


@app.route('/save_comment/<int:queen_id>', methods = ['POST'])
def save_comment(queen_id):
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


@app.route('/add_comment/<int:id>')
def add_comment(id):

    comment = Queen.get_one_queen_comment(id)
    return render_template('comments.html', queen = comment)

@app.route('/delete_comment/<int:id>')
def delete_comment(id):
    data ={
        'id': id
    }
    Comment.delete_comment(data)
    queen_comments = Queen.get_one_queen_comment(id)
    return redirect(f'/states')
# want redirect to go to add_comment.

@app.route('/edit_comment/<int:id>')
def edit_a_comment(id):
    data = {
        "id":id
    }
    comment = Comment.get_one_comment(data)
    Comment.edit_comment(request.form)
    return render_template("edit_comment.html", comment = comment)

@app.route('/edited_comment/<int:id>', methods=['post'])
def edited_a_comment(id):
    data = {"id": id,
        'queen_id': request.form['queen_id'],
        'user_id': request.form['user_id'],
        'comment': request.form['comment'],
    }
    print(data)
    Comment.edit_comment(data)
    return redirect("/states")