from datetime import datetime, date
from flask import render_template, session, redirect, url_for, jsonify, request, flash
from . import main
from .forms import VolumeSearchForm, AddVolumeForm, SearchApiGoogleForm
from .. import db
from ..models import Volumes
import requests
import sqlite3
from sqlalchemy import exc


@main.route('/', methods=['GET', 'POST'])
def index():
    form = VolumeSearchForm()
    volumes = Volumes.query.all()
    if form.validate_on_submit():
        query = form.search.data
        field = form.select.data
        if field == "title":
            database_query = Volumes.query.filter(Volumes.title.like('%{}%'.format(query)))
            return render_template("index.html", volumes=database_query, form=form)
        elif field == "authors":
            database_query = Volumes.query.filter(Volumes.authors.like('%{}%'.format(query)))
            return render_template("index.html", volumes=database_query, form=form)
        elif field == "language":
            database_query = Volumes.query.filter(Volumes.language.like('%{}%'.format(query)))
            return render_template("index.html", volumes=database_query, form=form)
        else:
            database_query = Volumes.query.filter(Volumes.publishedDate.like('%{}%'.format(query)))
            return render_template("index.html", volumes=database_query, form=form)
    return render_template("index.html", volumes=volumes, form=form)


@main.route('/add_volume', methods=['GET', 'POST'])
def add_volume():
    form = AddVolumeForm()
    if form.validate_on_submit():
        try:
            title = form.title.data
            author = form.authors.data
            published_date = form.publishedDate.data
            isbn_10 = form.isbn_10.data
            isbn_13 = form.isbn_13.data
            page_count = form.pageCount.data
            small_thumbnail = form.small_thumbnail.data
            thumbnail = form.thumbnail.data
            language = form.language.data
            industry_identifiers = str(isbn_10) + ',' + str(isbn_13)
            image_links = "smallThumbnail " + small_thumbnail + "," + "thumbnail " + thumbnail
            book = Volumes(title=title, authors=author, publishedDate=published_date,
                           industryIdentifiers=industry_identifiers, pageCount=page_count,
                           imageLinks=image_links, language=language)
            db.session.add(book)
            db.session.commit()
            flash("Volume was successfully added to database", "success")
        except exc.IntegrityError:
            db.session().rollback()
            flash("Volume wasn't added because this industry identifiers is in the database", "warning")
            return redirect(url_for('.add_volume'))
        return redirect(url_for('.index'))

    return render_template("add_volume.html", form=form)


@main.route('/google_books_api', methods=['GET', 'POST'])
def books_api_google():
    form = SearchApiGoogleForm()
    if form.validate_on_submit():
        query = form.search_q.data
        key = form.select.data
        query_key = form.search.data
        if query_key:
            link = 'https://www.googleapis.com/books/v1/volumes?q={}+{}:{}'.format(query, key, query_key)
        else:
            link = 'https://www.googleapis.com/books/v1/volumes?q={}'.format(query)
        r = requests.get(link)
        for item in r.json()["items"]:
            try:
                industry_lst = []
                title = item['volumeInfo']["title"]
                author = item['volumeInfo']["authors"]
                published_date = item['volumeInfo']["publishedDate"]
                industry_identifiers = item['volumeInfo']["industryIdentifiers"]
                try:
                    page_count = item['volumeInfo']["pageCount"]
                except KeyError:
                    page_count = None
                image_links = item['volumeInfo']["imageLinks"]
                language = item['volumeInfo']["language"]
                authors = ",".join(author)
                try:
                    pub_date_format = datetime.strptime(published_date, "%Y-%m-%d")
                except ValueError:
                    try:
                        pub_date_format = datetime.strptime(published_date, "%Y-%m")
                    except ValueError:
                        pub_date_format = datetime.strptime(published_date, "%Y")
                for ind in industry_identifiers:
                    industry_lst.append(ind["identifier"])
                industry_str = ",".join(industry_lst)
                image_lst = [k + " " + v for k, v in image_links.items()]
                image_str = ",".join(image_lst)
                book = Volumes(title=title, authors=authors, publishedDate=pub_date_format,
                               industryIdentifiers=industry_str, pageCount=page_count, imageLinks=image_str,
                               language=language)
                db.session.add(book)
                db.session.commit()
                flash("{} was successfully added to database".format(item['volumeInfo']["title"]), "success")
            except exc.IntegrityError:
                db.session().rollback()
                flash("{} is in the database".format(item['volumeInfo']["title"]), "warning")
            except KeyError as e:
                flash("{} wasn't added because {}"
                      " wasn't in Google API".format(item['volumeInfo']["title"], e), "warning")
        flash(link, "success")
        return redirect(url_for('.books_api_google'))

    return render_template("google_books_api.html", form=form)
    #return jsonify(r.json())
