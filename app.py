import os
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///members.sqlite3'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)

class members(db.Model):
    id = db.Column('member_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    membershipYears = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    status = db.Column(db.String(100))
    gamesWon = db.Column(db.Integer)
    favoriteGame = db.Column(db.String(150))
    highestScore = db.Column(db.Integer)

    def __init__(self, name, membershipYears, phone, status, gamesWon, favoriteGame, highestScore):
        self.name = name
        self.membershipYears = membershipYears
        self.phone = phone
        self.status = status
        self.gamesWon = gamesWon
        self.favoriteGame = favoriteGame
        self.highestScore = highestScore

db.create_all()

global_member = members('A', 1, 911, 'master', 200, 'Citadels', 2055)

@app.route('/', methods=['GET', 'POST'])
def opening2():
    global global_member
    if request.method == 'POST':
        if 'Search_By_gender' in request.form:
            if not request.form['gender']:
                flash('Please enter all the gender fields', 'error')
            else:
                searchGender = request.form['gender']
                memberList = db.session.query(members).filter(members.gender == searchGender).all()
                return render_template('ReadMembers.html', message='Test', members=memberList)

        elif 'Search_By_Name' in request.form:
            if not request.form['name']:
                flash('Please enter all the name fields', 'error')
            else:
                searchName = request.form['name']
                member = db.session.query(members).filter(members.name == searchName).first()
                return render_template('search.html', message='Test', member=member)

        elif 'Delete_Member' in request.form:
            if not request.form['name']:
                flash('Please enter all the name fields', 'error')
            else:
                searchName = request.form['name']
                member = db.session.query(members).filter(members.name == searchName).first()
                global_member = member
                return redirect(url_for('delete2', member=member))

        elif 'Update_Member' in request.form:
            if not request.form['name']:
                flash('Please enter all the name fields', 'error')
            else:
                searchName = request.form['name']
                member = db.session.query(members).filter(members.name == searchName).first()
                global_member = member
                return redirect(url_for('update2', member=member))

        elif 'Increment_Member_Age' in request.form:
            if not request.form['name']:
                flash('Please enter all the name fields', 'error')
            else:
                searchName = request.form['name']
                member = db.session.query(members).filter(members.name == searchName).first()
                global_member = member
                return redirect(url_for('increment_age2', member=member))

    all_data3 = db.session.query(members).all()
    return render_template('index.html', message='test', members=all_data3)

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')

@app.route('/delete2', methods=['GET', 'POST'])
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
    return render_template('DeleteMembers.html', member=searchMember)

@app.route('/update2', methods=['GET', 'POST'])
def update2():
    searchName = 'abc'
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:
            updateName = request.form['name']
            member = db.session.query(members).filter(members.name == updateName).first()
            member.city = request.form['city']
            member.addr = request.form['addr']
            member.age = request.form['age']
            db.session.commit()

            print('Record was successfully updated')
            return redirect(url_for('show_all'))
    searchMember = global_member

    return render_template('UpdateMembers.html', student=searchMember)

@app.route('/increment_age2', methods=['GET', 'POST'])
def increment_age2():
    searchName = 'abc'
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:
            updateName = request.form['name']
            member = db.session.query(members).filter(members.name == updateName).first()
            age = int(request.form['age'])
            member.age = age + 1
            db.session.commit()
            return redirect(url_for('show_all'))

    searchMember = global_member
    return render_template('IncrementMembership.html', student=searchMember)

@app.route('/show_all', methods=['GET', 'POST'])
def show_all():
    all_data = members.query.all()  # Query all members from the database
    return render_template('ReadMembers.html', message='test', students=all_data)


@app.route('/initial_table_data', methods=['GET', 'POST'])
def initial_table_data():
    if request.method == 'POST':
        print('here')
        members_data = [
            ('Ivan', 1, 911, 'master', 200, 'Citadels', 2055),
            ('Elena', 2, 922, 'beginner', 150, 'Chess', 1900),
            ('John', 3, 933, 'advanced', 300, 'Monopoly', 1800),
            ('Sophia', 1, 944, 'master', 250, 'Risk', 2100),
            ('Michael', 2, 955, 'beginner', 180, 'Catan', 1950),
            ('Olivia', 3, 966, 'advanced', 280, 'Ticket to Ride', 2000),
            ('William', 1, 977, 'master', 220, 'Scrabble', 1900),
            ('Emma', 2, 988, 'beginner', 160, 'Uno', 1800),
            ('Alexander', 3, 999, 'advanced', 320, 'Poker', 2050),
            ('Ava', 1, 1000, 'master', 240, 'Codenames', 1950)
        ]
        # Create instances of members and add them to the database session
        for data in members_data:
            member_instance = members(*data)
            db.session.add(member_instance)
        db.session.commit()
        flash('Initial Table Data Added')

    return render_template('InitialData.html')

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        # Check if 'name' and 'age' keys exist in the form data
        if not request.form.get('name') or not request.form.get('age'):
            flash('Please enter both name and age', 'error')
        else:
            # Retrieve values from form data
            name = request.form['name']
            age = request.form['age']

            # Create a new member instance
            member = members(name=name, age=age)

            # Add the member to the database session
            db.session.add(member)
            db.session.commit()

            flash('Member added successfully')

            return redirect(url_for('show_all'))

    return render_template('CreateMembers.html')

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=True, port=server_port, host='0.0.0.0')

