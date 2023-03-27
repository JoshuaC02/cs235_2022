from flask import Flask, render_template, redirect, url_for, session, request, Blueprint, abort
from flask import current_app as app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError 

from password_validator import PasswordValidator

from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.browse import services

browse_blueprint = Blueprint('browse_bp', __name__, url_prefix="/tracks")



@browse_blueprint.route('/browse')
def new_browse():
    #sort browse by default (track_id) on new request to browse
    services.sort_tracks("get_track_id", False, app.repo)
    return redirect(url_for('browse_bp.browse', page = 1))



@browse_blueprint.route('/browse/<page>', methods=['GET', 'POST'])
def browse(page):
    #create forms
    form_left = GoLeft()
    form_right = GoRight()
    drop_down = Filter()

    #convert parsed variables from strings to integers
    page = int(page)
    per_page = 30

    #check if POST method is to go left
    if form_left.submit1.data and form_left.validate():
        if page > 1:
            return redirect(url_for('browse_bp.browse', page = page-1))

    #check if POST method is to go right
    if form_right.submit2.data and form_right.validate():
        if page*per_page < services.get_number_of_tracks(app.repo):
            return redirect(url_for('browse_bp.browse', page = page+1))
    
    #check if POST method is to change filter method
    if drop_down.validate():
        services.change_sort_method(drop_down.filter.data, app.repo)
        return redirect(url_for('browse_bp.browse', page = 1))
        
    #generate new list from POST instructions (or default instructions)
    tracks_new = services.get_list_of_tracks(page, per_page, app.repo)

    #check if returned list has no elements
    if len(tracks_new) == 0:
        abort(404)
    return render_template('browse/browse.html', tracks=tracks_new, goleft=form_left, goright=form_right, drop_down=drop_down)



@browse_blueprint.route('/browse/track/<variable>')
def browse_track(variable):
    track=services.get_track(int(variable), app.repo)
    if track != None:
        return render_template("browse/simple_track.html", track=track, repo=app.repo)
    return abort(404)



@browse_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    return_list = []
    message="Start searching!"

    if search_form.validate_on_submit():
        return_list = services.return_track_from_dict(search_form.search.data, app.repo)
        message="Couldn't find anything!"

    return render_template('browse/search.html', form=search_form, return_list=return_list, length=len(return_list), message=message)



@browse_blueprint.route('/review/<variable>', methods=['GET', 'POST']) #TODO: CHECK FOR PROFANITY?
def add_review(variable):
    if 'username' not in session: #if not logged in, redirect to login page
        return redirect(url_for("authentication_bp.login"))
    if services.get_user(session['username'], app.repo) == None: #if browser thinks they're logged in but the user isn't recognised, raise error
        return redirect(url_for("authentication_bp.login"))
    current_user = services.get_user(session['username'], app.repo)

    current_track = services.get_track(int(variable), app.repo)
    if current_track == None:   #if invalid track, raise 404
        abort(404)

    form=ReviewForm()

    if form.validate_on_submit():
        new_review = services.create_review(current_track, form.review_comment.data, int(form.out_of_5.data), current_user)

        #add Review object to User object
        services.add_review_to_user(current_user, new_review, app.repo)

        #add Review object to Track object
        services.add_review_to_track(current_track, new_review, current_user, app.repo)

        return redirect(url_for('browse_bp.new_browse')) #COULD ADD THE TRACK SUBPAGE HERE?

    return render_template('browse/add_review.html', track_object=current_track, form=form)

@browse_blueprint.route('/recommendations')
def recommendation():
    if 'username' in session:
        if services.get_user(session['username'], app.repo) == None:
            return redirect(url_for('authentication_bp.login'))
        new_track_list = services.recommend_track(session['username'], app.repo)
        track_list_length = len(new_track_list)
        return render_template('browse/recommendation.html', tracks=new_track_list, length=track_list_length)
    return redirect(url_for('authentication_bp.login'))

class GoLeft(FlaskForm):
    submit1 = SubmitField('<')

class GoRight(FlaskForm):
    submit2 = SubmitField('>')

class Filter(FlaskForm):
    filter = SelectField('Filter by:', choices=[("", "Filter by:"), ('get_track_id', 'ID'), ('get_track_name', 'Title'), ('get_track_artist_name', 'Artist'), ('get_track_album_name', 'Album'), ('get_track_rating', 'Review')] )
    submit3 = SubmitField()

class SearchForm(FlaskForm):
    search = StringField('Search for:', [DataRequired(message="Please enter a valid search option")])
    submit = SubmitField('Search!')

class ReviewForm(FlaskForm):
    out_of_5 = SelectField('Rate:', [DataRequired(message="Please choose a rating")], choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    review_comment = StringField('Comment:', [DataRequired(), Length(min=1,max=250,message="Maximum of 250 characters")])
    submit = SubmitField('Confirm')