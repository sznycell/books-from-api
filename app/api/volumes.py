from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Volumes
from . import api


@api.route('/volumes/')
def get_all_volumes():
    volumes = Volumes.query.all()
    return jsonify({'volumes': [volume.to_json() for volume in volumes]})


@api.route('/volumes/title/<title>')
def get_volumes_title(title):
    volumes = Volumes.query.filter(Volumes.title.like('%{}%'.format(title)))
    return jsonify({'volumes': [volume.to_json() for volume in volumes]})


@api.route('/volumes/authors/<authors>')
def get_volumes_authors(authors):
    volumes = Volumes.query.filter(Volumes.authors.like('%{}%'.format(authors)))
    return jsonify({'volumes': [volume.to_json() for volume in volumes]})


@api.route('/volumes/language/<language>')
def get_volumes_language(language):
    volumes = Volumes.query.filter(Volumes.language.like('%{}%'.format(language)))
    return jsonify({'volumes': [volume.to_json() for volume in volumes]})


@api.route('/volumes/publishedDate/<publishedDate>')
def get_volumes_publishedDate(publishedDate):
    volumes = Volumes.query.filter(Volumes.publishedDate.like('%{}%'.format(publishedDate)))
    return jsonify({'volumes': [volume.to_json() for volume in volumes]})
