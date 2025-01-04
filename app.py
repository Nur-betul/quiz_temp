import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class Profile(db.Model):
    # Id : Field which stores unique id for every row in database table.
    # first_name: Used to store the first name if the user
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=True, nullable=False)
    best_score = db.Column(db.Integer, nullable=False)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Name : {self.first_name}, Best Score: {self.best_score}"

# Ana sayfa route'u
@app.route("/", methods=["GET", "POST"])
def quiz():
    score = 0
    best_score = 0
    username = "dht"
    if request.method == "POST":
        # Formdan gelen verileri al
        username = request.form.get("username")
        question1 = request.form.get("question1")
        question2 = request.form.get("question2")
        question3 = request.form.get("question3")

        CORRECT_ANSWERS = {
            "question1": "tensorflow", 
            "question2": "cnn",  
            "question3": "spacy" 
        }

        # Doğru cevapları kontrol et
        score = 0
        if question1 == CORRECT_ANSWERS["question1"]:
            score += 10
        else:
            score += 0
        if question2 == CORRECT_ANSWERS["question2"]:
            score += 10
        else:
            score += 0
        if question3 == CORRECT_ANSWERS["question3"]:
            score += 10
        else:
            score += 0

        # Kullanıcının mevcut kaydını veritabanında ara
        profile = Profile.query.filter_by(first_name=username).first()

        if profile:
            # Eğer mevcut bir kayıt varsa ve yeni skor daha yüksekse güncelle
            if score > profile.best_score:
                profile.best_score = score
                db.session.commit()
            best_score= profile.best_score
        else:
            # Eğer kayıt yoksa yeni bir kullanıcı oluştur
            profile = Profile(
                first_name=username,
                best_score=score
            )
            db.session.add(profile)
            db.session.commit()
            best_score= profile.best_score
        
        if request.method == "POST":
            print(request.form)
        
        profile2 = Profile(first_name="Test", best_score=50)
        db.session.add(profile2)
        db.session.commit()
        print("Veritabanına kayıt yapıldı!")


    
    
    # return render_template("quiz_template.html")
    return render_template("quiz_template.html", best_score=best_score, username=username)


if __name__ == "__main__":
    app.run()