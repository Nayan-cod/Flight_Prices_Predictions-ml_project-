from flask_wtf import FlaskForm
import pandas as pd
from wtforms import  SelectField,DateField,TimeField,IntegerField,SubmitField,StringField, PasswordField
from wtforms.validators import DataRequired,InputRequired, Length


train=pd.read_csv("data/train.csv")
val=pd.read_csv("data/val.csv")
X_data=pd.concat([train,val],axis=0).drop(columns="price")


class InputForm(FlaskForm):
    airline=SelectField (label="Airline",choices=X_data.airline.unique().tolist(),
    validators=[DataRequired()])

    date_of_journey=DateField(label="Date_of_Journey",validators=[DataRequired()])

    source=SelectField (label="Source",choices=X_data.source.unique().tolist(),
    validators=[DataRequired()])

    destination=SelectField (label="Destination",choices=X_data.destination.unique().tolist(),
    validators=[DataRequired()])

    dep_time=TimeField(label="Departure Time",validators=[DataRequired()])

    arrival_time=TimeField(label="Arrival Time",validators=[DataRequired()])

    duration=IntegerField(label="Duration",validators=[DataRequired()])

    total_stops=IntegerField(label="Total Stops",validators=[DataRequired()])

    additional_info=SelectField (label="Additional Info",choices=X_data.additional_info.unique().tolist(),
    validators=[DataRequired()])

    submit=SubmitField("Pridict")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    submit = SubmitField('Login')



class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    submit = SubmitField('Register')