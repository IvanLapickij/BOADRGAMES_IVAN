"""
Welcome to BoardGames Club
"""
import os

from flask import Flask, request, flash, url_for, redirect, render_template

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)

class members(db.Model):
    id = db.Column('member_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    membershipYears = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    status = db.Column(db.String(100))
    gamesWon = db.Column(db.Integer)
    favoriteGame = db.Column(db.String(150))
    highestScore = db.Column(db.Integer)



    def __init__(self, name, gender, membershipYears,phone,status,gamesWon,favoriteGame,highestScore):
        self.name = name
        self.gender = gender
        self.membershipYears = membershipYears
        self.phone = phone
        self.status = status
        self.gamesWon= gamesWon
        self.favoriteGame = favoriteGame
        self.highestScore = highestScore



db.create_all()

global_member=members('A','B',1,911,'master', 200,'Citadels', 2055) # Ensure Opening2, delete2 & update2 are referencing the same member

@app.route('/',methods=['GET', 'POST'])
def opening2():
    global global_member
    if request.method == 'POST':
        if 'Search_By_gender' in request.form:
            if not request.form['gender']:
                flash('Please enter all the gender fields', 'error')
            else:
                searchGender= request.form['gender']
                memberList = db.session.query(members).filter(members.gender == searchGender).all()
                return render_template('show_all.html', message='Test', members=memberList)

        elif 'Search_By_Name' in request.form:
            if not request.form['name']:
                flash('Please enter all the name fields', 'error')
            else:
                searchName= request.form['name']
                member = db.session.query(members).filter(members.name == searchName).first()
                return render_template('search.html', message='Test', member=member)

        elif 'Delete_Member' in request.form:
            if not request.form['name']:
                flash('Please enter all the name fields', 'error')
            else:
                searchName= request.form['name']
                member = db.session.query(members).filter(members.name == searchName).first()
                global_member = member
                return redirect(url_for('delete2', member=member))

        elif 'Update_Member' in request.form:
            if not request.form['name']:
                flash('Please enter all the name fields', 'error')
            else:
                searchName= request.form['name']
                member = db.session.query(members).filter(members.name == searchName).first()
                global_member = member
                return redirect(url_for('update2', member=member))

        elif 'Increment_Member_Age' in request.form:
            if not request.form['name']:
                flash('Please enter all the name fields', 'error')
            else:
                searchName= request.form['name']
                member = db.session.query(members).filter(members.name == searchName).first()
                global_member = member
                return redirect(url_for('increment_age2', member=member))

    all_data3 = db.session.query(members).all()
    return render_template('opening2.html', message='test' ,members=all_data3)

@app.route('/search', methods=['GET', 'POST'])
def search():

    return render_template('search.html')

@app.route('/delete2', methods=[ 'GET','POST'])
def delete2():
    searchName = 'abc'
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:
            searchName = request.form['name']
            member = db.session.query(members).filter(members.name == searchName).first()
            db.session.delete(member)
            db.session.commit()
            return redirect(url_for('show_all'))

    searchMember = global_member
    return render_template('delete2.html', member=searchMember)



@app.route('/update2', methods=[ 'GET','POST'])
def update2():
    searchName = 'abc'
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:
            updateName = request.form['name']
            member = db.session.query(members).filter(members.name == updateName).first()
            member.city = request.form['city']
            member.addr =  request.form['addr']
            member.age  = request.form['age']
            db.session.commit()

            print('Record was successfully updated')
            return redirect(url_for('show_all'))
    searchMember = global_member

    return render_template('update2.html', student=searchMember)


@app.route('/increment_age2', methods=[ 'GET','POST'])
def increment_age2():
    searchName = 'abc'
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:
            updateName = request.form['name']
            member = db.session.query(members).filter(members.name == updateName).first()
            age  = int(request.form['age'])
            member.age = age+1
            db.session.commit()
            return redirect(url_for('show_all'))

    searchMember = global_member
    return render_template('increment_age2.html', student=searchMember)




@app.route('/show_all', methods=['GET', 'POST'])
def show_all():
    all_data3 = db.session.query(members).all()
    return render_template('show_all.html', message='test' ,students=all_data3)


@app.route('/initial_table_data', methods=['GET', 'POST'])
def initial_table_data():
    if request.method == 'POST' :
        print('here')
        db.session.add(members('A','B',1,911,'master', 200,'Citadels', 2055))
        db.session.commit()
        flash('Initial Table Data Added')

    return render_template('initial_table_data.html')



@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            member = members(request.form['name'], request.form['gender'],
                               request.form['addr'], request.form['age'])

            db.session.add(member)
            db.session.commit()
            return redirect(url_for('show_all'))
    return render_template('new.html')




if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')



