from school_project.config.mysqlconnection import connectToMySQL
from flask import flash

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.posted_by = []
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( first_name, last_name, email,password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, now(),now());"
        return connectToMySQL('dragrace').query_db(query,data)
    
    @classmethod
    def get_by_email(cls, data):
        query = "Select * from users where email = %(email)s;"
        results = connectToMySQL('dragrace').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls,data):
        query = "select * from users where users.id = %(id)s;"
        results = connectToMySQL('dragrace').query_db(query, {'id':data})
        if len(results)<1:
            return False
        return cls(results[0])
    

        

    @staticmethod
    def validate_user_reg(user_reg):
        is_valid = True # we assume this is true
        if len(user_reg['first_name']) < 3:
            flash("first name must be at least 3 characters.")
            is_valid = False
        if len(user_reg['last_name']) < 3:
            flash("last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user_reg['email']):
            flash("Invalid email address")
            is_valid = False
        if not PW_REGEX.match(user_reg['password']):
            flash("""password must be at least 8 characters.
            Have an uppercase, lowercase, and at least one number, and a special character""")
            is_valid = False
        return is_valid