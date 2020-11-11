"""Main app/routing file for Twitoff"""

from flask import Flask, render_template, request
from .models import DB,User
from .twitter import insert_example_users, add_or_update_user, update_all_users
from .predict import predict_user
from os import getenv


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv('DATABSE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route('/', methods=['POST', 'GET'])
    #@app.route('/', methods=['GET'])
    def root():
        if request.method == 'POST':
            #if "Compare Users" button is clicked
            if "compare_button" in request.form:
                user_add_message=''
                user1, user2 = sorted([request.values['user1'], 
                                    request.values['user2']])
                if user1 == user2:
                    compare_message = 'Cannot compare a user to themselves!'
                else:
                    prediction = predict_user(user1, user2, request.values['tweet_text'])
                    compare_message = f"'{request.values['tweet_text']}' is more likely to be said by {user1 if prediction else user2} than {user2 if prediction else user1}."
            elif "user_button" in request.form:
                compare_message=''
                name= request.values['user_name']
                try:
                    add_or_update_user(name)
                    user_add_message = f"{name} was successfully added!"
                    tweets= User.query.filter(User.name == name).one().tweets
                except Exception as e:
                    user_add_message = f"Error adding {name}: {e}."
                    tweets=[]
        else:
            compare_message = ''
            user_add_message=''
        return render_template('base.html', title='Home', users=User.query.all(), compare_message=compare_message, user_add_message=user_add_message)


    @app.route('/update')
    def update():
        update_all_users()
        return render_template('base.html', title='Users updated!', users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset database!')


    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'], 
                                request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1, user2, request.values['tweet_text'])
            message = f"'{request.values['tweet_text']}' is more likely to be said by {user1 if prediction else user2} than {user2 if prediction else user1}."

        #return render_template('prediction.html', title='Prediction', message=message)
        return render_template('base.html', title='Prediction', message=message)

    
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods = ['GET'])
    def user(name=None, message=''):
        name= name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f"{name} was successfully added!"
            tweets= User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = f"Error adding {name}: {e}."
            tweets=[]
        return render_template('user.html', title=name, tweets=tweets, message=message)
    

    return app

