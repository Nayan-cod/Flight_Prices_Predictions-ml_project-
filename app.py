from flask import Flask,url_for,render_template,redirect,request, session, flash
from forms import InputForm,LoginForm
import pandas as pd
import joblib
from forms import RegisterForm

from werkzeug.security import check_password_hash,generate_password_hash
import sqlite3

app=Flask(__name__)
app.secret_key = "secret_key"
app.config["SECRET_KEY"]="secret_key"

model=joblib.load("model.joblib")
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",title="Home")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    form = InputForm()
    if form.validate_on_submit():
        x_new = pd.DataFrame(dict(
            airline=[form.airline.data],
            date_of_journey=[form.date_of_journey.data.strftime("%Y-%m-%d")],
            source=[form.source.data],
            destination=[form.destination.data],
            dep_time=[form.dep_time.data.strftime("%H:%M:%S")],
            arrival_time=[form.arrival_time.data.strftime("%H:%M:%S")],
            total_stops=[form.total_stops.data],
            additional_info=[form.additional_info.data]
        ))
        prediction = model.predict(x_new)[0]
        message = f"The Predicted Price is {prediction:,.0f} INR"
    else:
        message = "Please Provide valid detail!"

    return render_template("predict.html", title="Predict", form=form, output=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (form.username.data,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[2], form.password.data):
            session['username'] = form.username.data
            return redirect(url_for('predict'))  # Redirect directly to Predict
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password)

        try:
            with sqlite3.connect('users.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                flash('Registration successful. Please login.', 'success')
                return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Try a different one.', 'danger')
        except Exception as e:
            flash('Something went wrong: ' + str(e), 'danger')

    return render_template('register.html', form=form)
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__=="__main__":
    app.run(debug=True)