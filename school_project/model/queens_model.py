from school_project.config.mysqlconnection import connectToMySQL
from school_project.model.comment_model import Comment
from school_project.model.user_model import User
from flask import flash


class Queen:
    def __init__(self, data):
        self.id = data['id']
        self.season = data['season']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.age = data['age']
        self.city_name = data['city_name']
        self.state_name = data['state_name']
        self.placement = data['placement']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.queen_id = []
        self.user_comments = []

    @classmethod
    def save_queen_api(cls, queen_data):
        queens = []
        query = "insert into queens(season,first_name, last_name, age, city_name, state_name,  placement, updated_at, created_at) values(%(season)s,%(first_name)s, %(last_name)s, %(age)s, %(city_name)s,%(state_name)s,%(placement)s, current_timestamp(),current_timestamp());"
        for queen in queen_data:
            queen_data = {
                'season': queen['Season'],
                'first_name': queen['Contestant']['first_name'],
                'last_name': queen['Contestant']['last_name'],
                'age': queen['Age'],
                'city_name': queen['Hometown']['city'],
                'state_name': queen['Hometown']['state'],
                'placement': queen['Outcome'],
            }
            queens.append(queen_data)
            connectToMySQL('dragrace').query_db(query, queen_data)
        print(queens)

        return queens

    @classmethod
    def get_all_queens(cls):
        query = "select * from queens group by state_name;"
        return connectToMySQL('dragrace').query_db(query)
    
    @classmethod
    def get_all_queens_in_state(cls, data):
        query = "SELECT * FROM queens LEFT JOIN comments ON queens.id = comments.queen_id WHERE state_name = %(state_name)s GROUP BY queens.id;"
        results = connectToMySQL('dragrace').query_db(query, data={'state_name': data})
        for row in results:
            row['state'] = row.pop('state_name')  # Add a new 'state' key to the row with the value of 'state_name'
        return results



    @classmethod
    def get_one_queen_comment(cls, data):
        query = """select * from queens left join comments on queens.id = comments.queen_id 
        left join users on users.id = comments.user_id where queens.id = %(id)s;"""
        results = connectToMySQL('dragrace').query_db(query, data={'id': data})
        queen = cls(results[0])

        for comment in results:
            user_data = {
                "id": comment["users.id"],
                "first_name": comment["users.first_name"],
                "last_name": comment["users.last_name"],
                "email": comment["email"],
                "password": comment["password"],
                "created_at": comment["users.created_at"],
                "updated_at": comment["users.updated_at"],

            }
            user = User(user_data)
            comment_data = {

                "id": comment["comments.id"],
                "queen_id": comment["queen_id"],
                "user_id": comment["user_id"],
                "comment": comment["comment"],
                "created_at": comment["comments.created_at"],
                "updated_at": comment["comments.updated_at"],


            }
            comment_instance = Comment(comment_data)
            comment_instance.creator = user
            queen.user_comments.append(comment_instance)

            queen.queen_id = comment_instance

        return queen