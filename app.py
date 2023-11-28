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
    gender = db.Column(db.String(100))
    membershipYears = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    status = db.Column(db.String(100))
    gamesWon = db.Column(db.Integer)
    favoriteGame = db.Column(db.String(150))
    highestScore = db.Column(db.Integer)

    def __init__(self, name, gender, membershipYears, phone, status, gamesWon, favoriteGame, highestScore):
        self.name = name
        self.gender = gender
        self.membershipYears = membershipYears
        self.phone = phone
        self.status = status
        self.gamesWon = gamesWon
        self.favoriteGame = favoriteGame
        self.highestScore = highestScore

db.create_all()

global_member = members('Garry', 'male', 1, 911, 'master', 200, 'Citadels', 2055)

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
            member.gender = request.form['gender']  # Update this line
            member.status = request.form['status']
            member.membershipYears = request.form['membershipYears']
            # Update other fields as needed
            db.session.commit()

            print('Record was successfully updated')
            return redirect(url_for('show_all'))
    searchMember = global_member

    return render_template('UpdateMembers.html', member=searchMember)


@app.route('/increment_age2', methods=['GET', 'POST'])
def increment_age2():
    searchName = 'abc'
    if request.method == 'POST':
        if not request.form['name']:
            flash('Please enter all the fields', 'error')
        else:
            updateName = request.form['name']
            member = db.session.query(members).filter(members.name == updateName).first()
            membershipYears = int(request.form['membershipYears'])
            member.membershipYears = membershipYears + 1
            db.session.commit()
            return redirect(url_for('show_all'))

    searchMember = global_member
    return render_template('IncrementMembership.html', member=searchMember)

@app.route('/show_all', methods=['GET', 'POST'])
def show_all():
    all_data = members.query.all()
    print("All data retrieved:", all_data)
    return render_template('ReadMembers.html', message='test', members=all_data)



@app.route('/initial_table_data', methods=['GET', 'POST'])
def initial_table_data():
    if request.method == 'POST':
        print('here')
        members_data = [
            ('Ivan','Male', 1, 911, 'master', 200, 'Citadels', 2055),
            ('Elena','Female', 2, 922, 'beginner', 150, 'Chess', 1900),
            ('John','Male', 3, 933, 'advanced', 300, 'Monopoly', 1800),
            ('Sophia','Female', 1, 944, 'master', 250, 'Risk', 2100),
            ('Michael','Male', 2, 955, 'beginner', 180, 'Catan', 1950),
            ('Olivia','Female', 3, 966, 'advanced', 280, 'Ticket to Ride', 2000),
            ('William','Male', 1, 977, 'master', 220, 'Scrabble', 1900),
            ('Emma','Female', 2, 988, 'beginner', 160, 'Uno', 1800),
            ('Alexander','Male', 3, 999, 'advanced', 320, 'Poker', 2050),
            ('Ava','Female', 1, 1000, 'master', 240, 'Codenames', 1950)
        ]
        # Create instances of members and add them to the database session
        for data in members_data:
            member_instance = members(*data)
            db.session.add(member_instance)
        db.session.commit()
        flash('Initial Table Data Added')

        # Print the contents of the database for debugging
    all_data = members.query.all()
    print("All data in the database:", all_data)

    return render_template('InitialData.html')

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        # Collect data from the form
        name = request.form.get('name')
        gender = request.form.get('gender')
        membership_years = request.form.get('membershipYears')
        phone = request.form.get('phone')
        status = request.form.get('status')
        games_won = request.form.get('gamesWon')
        favorite_game = request.form.get('favoriteGame')
        highest_score = request.form.get('highestScore')

        # Create a new members object with the collected data
        member = members(
            name=name,
            gender=gender,
            membershipYears=membership_years,
            phone=phone,
            status=status,
            gamesWon=games_won,
            favoriteGame=favorite_game,
            highestScore=highest_score
        )

        # Add the new member to the session and commit the changes
        db.session.add(member)
        db.session.commit()

        flash('Member added successfully')  # Optionally, provide feedback to the user

        return redirect(url_for('show_all'))

    return render_template('CreateMembers.html')


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=True, port=server_port, host='0.0.0.0')

