from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, Form, DateField, IntegerField
from wtforms.validators import DataRequired


class VolumeSearchForm(FlaskForm):
    choices = [('title', 'title'),
               ('authors', 'authors'),
               ('language', 'language'),
               ('publishDate', 'publishDate')]
    select = SelectField('Search:', choices=choices)
    search = StringField('')
    submit = SubmitField('Search')


class SearchApiGoogleForm(FlaskForm):
    choices = [('intitle', 'intitle'),
               ('inauthor', 'inauthor'),
               ('inpublisher', 'inpublisher'),
               ('subject', 'subject'),
               ('isbn', 'isbn'),
               ('lccn', 'lccn'),
               ('oclc', 'oclc')]
    select = SelectField(choices=choices)
    search_q = StringField('q')
    search = StringField('')
    submit = SubmitField('Add')


class AddVolumeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Authors', validators=[DataRequired()])
    publishedDate = DateField('Published Date (format yyyy-mm-dd)', format='%Y-%m-%d')
    isbn_10 = IntegerField('ISBN 10', validators=[DataRequired()])
    isbn_13 = IntegerField('ISBN 13', validators=[DataRequired()])
    pageCount = IntegerField('Page Count', validators=[DataRequired()])
    small_thumbnail = StringField('Small Thumbnail', validators=[DataRequired()])
    thumbnail = StringField('Thumbnail', validators=[DataRequired()])
    language = StringField("Language", validators=[DataRequired()])
    submit = SubmitField('Submit')
