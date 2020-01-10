import os
from flask import Flask, render_template, request, make_response, redirect, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename
from src.session import generateHashFileName, generateSession
from src.its_model.user_manager import UserManager
from login_required import login_required


def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Auth-Token, Content-Type,Authorization'
    return response

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.after_request(after_request)
    app.config.update(
        MONGO_URI = "mongodb://127.0.0.1:27017/its",
        MONGO_DBNAME = "its"
    )
    os.makedirs(os.path.join(app.instance_path, 'htmlfi'), exist_ok=True)

    from src.issue import issue_bp
    from src.user import user_bp
    from src.project import project_bp
    app.register_blueprint(issue_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(project_bp)

    from mongo import mongo
    mongo.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        print(secure_filename("asdjiasdjoi"))

    @app.route('/file', methods=["POST"])
    @login_required
    def save_file():
        f = request.files['file']
        hashedName = generateHashFileName(secure_filename(f.filename))
        f.save(os.path.join(app.instance_path, 'htmlfi', hashedName))
        return {"info": "success",
                "payload": '/file/' + hashedName}

    @app.route('/file/<file_name>', methods=["GET"])
    def get_file(file_name):
        return send_file(os.path.join(app.instance_path, 'htmlfi', secure_filename(file_name)))

    @app.route('/sign_up', methods=["POST"])
    def sign_up():
        userManager = UserManager()
        payload = request.get_json()
        try:
            userManager.createUser(request.get_json())
        except:
            return failure("Username exists")
        return success("Create account succeed")
        
    @app.route('/sign_in', methods=["POST"])
    def sign_in():
        result = mongo.db.user_profile.find_one({"username": request.get_json()["username"],
                                                "password": request.get_json()["password"]})
        if result is None:
            response = {"info": "failure",
                        "payload": "Username or password invalid."}
        else:
            session = generateSession(str(result["_id"]), result["username"])     # Secret session mix
            cookies = {'id': result["username"], 'session': session}
            mongo.db.session.insert_one(cookies)
            response = make_response({"info": "success",
                "id": result["username"]})
            response.set_cookie('id', cookies["id"], domain='127.0.0.1')
            response.set_cookie('session', cookies["session"], domain='127.0.0.1')

        return response

    @app.route('/sign_out', methods=["POST"])
    def sign_out():
        id = request.cookies.get('id')
        session = request.cookies.get('session')
        result = mongo.db.session.remove({"id": id, "session": session})
        response = make_response("Sign out")
        response.set_cookie('id', '', expires=0)
        response.set_cookie('session', '', expires=0)
        return response

    @app.route('/sign_in', methods=["GET"])
    def sign_in_page():
        id = request.cookies.get('id')
        session = request.cookies.get('session')
        if id and session:
            result = mongo.db.session.find_one({"id": id, "session": session})
            if not result is None:
                return redirect('/' + id)
        return getPage("")


    # a simple page that says hello
    @app.route('/', defaults={'path': ''}, methods=["GET"])
    def root(path):
        return redirect('/sign_in')

    @app.route('/<path:path>', methods=["GET"])
    def getPage(path):
        if path != "" and "/static/" in path:
            return send_from_directory("static", path.split("/static/")[1])
        else:
            return render_template("index.html")

    # @app.route('/issue/new', methods=["POST"])
    # def addNewIssue():
    #     issueData = request.get_json()
    #     query = {"project_id": issueData["project_id"],
    #              "title": issueData["issue"],
    #              "comment": issueData["comment"]}
    #     try:
    #         mongo.db.issue.insert(query)
    #     except:
    #         return {"info": "failed to submit a new issue"}
    #     return {"info": "Submitted a new issue"}

    return app
