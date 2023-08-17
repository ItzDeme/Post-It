from flask import Flask, request, Response, make_response, jsonify
from flask_cors import CORS
import requests
import json
import re
import logging
import uuid
import datetime
import firebase_admin
from firebase_admin import credentials, db
from operator import itemgetter, attrgetter

app = Flask(__name__)
CORS(app)



cred = credentials.Certificate("./JellyRollMountainApple.json")
firebase_admin.initialize_app(cred,{"databaseURL": "https://post-it-55b05-default-rtdb.firebaseio.com"})

today= datetime.date.today()

logging.basicConfig(filename = ('debug_log_'+ str(today) +'.log'), level=logging.DEBUG, format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


#members api route
@app.route("/members")
def members():
    return {"members":["Member1","Member2", "Member3"]}


#handles call to register user
@app.route('/register',methods = ['POST', 'GET'])
def register():
    user = "3213bjhkfb1231"
    userSetup = {
        "userName": "TestAccount",
        "email": "test@email.com",
        "Posts": 0
    }

    db.reference(f"users/{user}").update(userSetup)
    return "You are registered!!!"

#handles call to grab all posts
@app.route('/<User>/posts',methods = ['GET'])
def getPosts(User):
    #checks if the user exists, if doesn't it sends 401 unathorized.
    if str(db.reference(f"users/{User}/").get()) == "None":
        return jsonify({"success": False}), 401
    else:
        arrayPosts = db.reference(f"/posts/{User}").get()
        return jsonify(arrayPosts)

#handles call for creating posts
@app.route('/<User>/post',methods = ['POST', 'GET'])
def post(User):
    postHeaders = {}
    time = datetime.datetime.now()
    for key,value in request.headers:
        postHeaders[key] = value
    
        #checks if users has posts.
    if str(db.reference(f"users/{User}/").get()) == "None":
        return jsonify({"success": False}), 401
    else:
        if str(db.reference(f"posts/{User}/").get()) == "None":
            #creates the first post for the user.
            db.reference(f"posts/{User}/Post0").update({"Time": time.strftime("%c"),"Headers": postHeaders, "Body": json.loads(request.data)})
            return jsonify({"success": True}), 204
        else:
            firebaseDataObj = db.reference(f"/posts/{User}").get(shallow=True)
            keys = []
            for key in firebaseDataObj:
                keys.append(int(re.search(r'\d+', key).group()))
            amount = len(keys)
            keys.sort()
            #checks if max amount of post have been made.
            if amount < 10:
                #if max amount of post is not reached it created the next post.
                db.reference(f"posts/{User}/Post{max(keys)+1}").update({"Time": time.strftime("%c"),"Headers": postHeaders, "Body": json.loads(request.data)})
                db.reference(f"users/{User}").update({"Posts": max(keys)+1})
                return jsonify({"success": True}), 204
            else:
                #Removes the oldest post
                db.reference(f"/posts/{User}/Post{keys[0]}").delete()
                #creates a new post
                db.reference(f"posts/{User}/Post{max(keys)+1}").update({"Time": time.strftime("%c"),"Headers": postHeaders, "Body": json.loads(request.data)})
                db.reference(f"users/{User}").update({"Posts": max(keys)+1})
                return jsonify({"success": True}), 204


if __name__ == "__main__":
    app.run(debug=True)