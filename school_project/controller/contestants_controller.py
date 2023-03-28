from school_project import app
from school_project.controller.user_controller import User
from school_project.model.queens_model import Queen
from school_project.model.comment_model import Comment
from flask import render_template,session, request,redirect,jsonify,flash
from flask_cors import CORS
cors = CORS(app)

@app.route('/states')
def view_states():
    if 'user_id' not in session:
        flash("Please log in to see this page")
        return redirect("/")
    queen = Queen.get_all_queens()
    return render_template("contestants.html", queen = queen, user = User.get_user_by_id(session['user_id']))


@app.route('/contestants/<data>')
def view_queens_in_state(data):
    state = Queen.get_all_queens_in_state(data)
    print(data)
    state_name = state[0]['state']
    print(state_name)
    return render_template('queen_in_state.html', state = state, state_name =state_name)



# @app.route('/insert_queen')
# def add_a_queen():
#     return render_template('index.html')

# @app.route('/insert_queen', methods = ['POST'])
# def add_queen():
    
#     contestants = request.get_json()
#     print('line 27')
    
#     Queen.save_queen_api(contestants)

#     return redirect('/insert_queen')