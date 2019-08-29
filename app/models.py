from . import db
from datetime import datetime


class Volumes(db.Model):
    __tablename__ = "volumes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    authors = db.Column(db.String(64))
    publishedDate = db.Column(db.Date)
    industryIdentifiers = db.Column(db.String, unique=True)
    pageCount = db.Column(db.Integer)
    imageLinks = db.Column(db.String)
    language = db.Column(db.String(64))

    def to_json(self):
        json_volumes = {
            'title': self.title,
            'authors': self.authors,
            'publishedDate': self.publishedDate,
            'industryIdentifiers': self.industryIdentifiers,
            'pageCount': self.pageCount,
            'imageLinks': self.imageLinks
        }
        return json_volumes
    
    @staticmethod
    def create_table():
        db.create_all()

    def __repr__(self):
        return '<Volumes %r>' % self.title

