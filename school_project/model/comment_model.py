from school_project.config.mysqlconnection import connectToMySQL
from flask import flash


class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.queen_id = data['queen_id']
        self.user_id = data['user_id']
        self.comment = data['comment']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        self.creator = None

    @classmethod
    def save_comment(cls, data):
        query = "insert into comments (queen_id, user_id, comment, updated_at, created_at) values (%(queen_id)s, %(user_id)s, %(comment)s, current_timestamp(), current_timestamp());"
        results = connectToMySQL('dragrace').query_db(query, data)
        print(results)
        return results

    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments WHERE comments.id = %(id)s";
        return connectToMySQL('dragrace').query_db(query, data)

    @classmethod
    def edit_comment(cls, data):
        query = "UPDATE comments SET queen_id = %(queen_id)s, user_id = %(user_id)s, comment = %(comment)s, updated_at= current_timestamp() WHERE comments.id = %(id)s";
        return connectToMySQL('dragrace').query_db(query, data)

    @classmethod
    def get_one_comment(cls, data):
        query = "select * from comments where comments.id =%(id)s;"
        results = connectToMySQL('dragrace').query_db(query, data)
        results = cls(results[0])
        print(results)
        return results

    @staticmethod
    def validate_comment(comments):
        is_valid = True  
        if len(comments['comment']) == 0:
            print(comments)
            flash("Comment must be more than 0 characters.")
            is_valid = False
        return is_valid