from models import SessionMaker, User, Todo
from flask import Flask
from flask import request, render_template, redirect, url_for


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        msg = request.args.get("msg")
        return render_template("loginpage.html", msg=msg)
    else:
        session = SessionMaker()
        user = session.query(User).get(request.form["name"])
        if user:
            if user.password == request.form["password"]:
                session.close()
                return redirect(url_for("userpage", user=user.name))
            else:
                msg ="パスワード正しくない"
                return render_template("loginpage.html", msg=msg)
        else:
            msg = "存在しないユーザー"
            return render_template("loginpage.html", msg=msg)


@app.route("/userpage/")
def userpage():
    user = request.args.get("user")
    session = SessionMaker()
    if user:
        msg = "おかえりなさい{}さん。TODOを確認しましょう。".format(user)
        todos = session.query(Todo).filter(Todo.name==user).all()
        session.close()
        return render_template("userpage.html", msg=msg, todos=todos, name=user)
    else:
        session.close()
        return render_template("loginpage.html")


@app.route("/signup/", methods=["GET", "POST"])
def signup():
    name = request.form["name"]
    password = request.form["password"]
    if name and password:
        session = SessionMaker()
        duplication_judge = session.query(User).get(name)
        if duplication_judge:
            msg = "名前が重複してます。別の名前よろ"
            session.close()
            return redirect(url_for("login", msg=msg))    

        else:
            user = User(name=name, password=password)
            session.add(user)
            session.commit()
            msg = "はじめまして{}さん。TODOを作っていきましょう。".format(user.name)
            return render_template("userpage.html", msg=msg, name=user.name)
            
    else:
        msg = "空白埋めて"
        return redirect(url_for("login", msg=msg))


@app.route("/add_todo/", methods = ["GET", "POST"])
def add_todo():
    name = request.form["name"]
    date = request.form["date"]
    body = request.form["body"]
    session = SessionMaker()
    session.add(Todo(name=name, date=date, body=body))
    session.commit()
    session.close()
    return redirect(url_for("userpage", user=name))


@app.route("/delete_todo/", methods = ["GET", "POST"])
def delete_todo():
    id = request.form["id"]
    name = request.form["name"]
    session = SessionMaker()
    session.query(Todo).filter(Todo.id==id).delete()
    session.commit()
    session.close()
    return redirect(url_for("userpage", user=name))
    




if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888, threaded=True)


