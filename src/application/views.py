"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect, jsonify
from flask.views import View, MethodView
from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from forms import ExampleForm
from models import ExampleModel, SavedNames


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)

@app.context_processor
def context_processor():
    d = {'user': users.get_current_user()}
    if not d['user']:
        d['login_url'] = users.create_login_url("/")
    else:
        d['logout_url'] = users.create_logout_url("/")
        d['admin'] = users.is_current_user_admin()
    return d

def home():
    controls = [
        {"id": "phonetics-spellability", "name": "Spellability", "weight": 40},
        {"id": "phonetics-pronounceability", "name": "Pronounceability", "weight": 10},
        {"id": "history-timelessness", "name": "Timelessness", "weight": 20},
        {"id": "history-relevancy", "name": "Relevancy", "weight": 30},
        {"id": "history-rarity", "name": "Rarity", "weight": 10},
        {"id": "internet-googlability", "name": "Googlability", "weight": 8},
        {"id": "internet-availability", "name": "Availability", "weight": 4},
        {"id": "meaning-secularity", "name": "Secularity", "weight": 30},
        {"id": "beauty-palindromicity", "name": "Palindromicity", "weight": 20},
        {"id": "beauty-initialization", "name": "Initialization", "weight": 1},
        {"id": "speed-shortness", "name": "Shortness", "weight": 20},
        {"id": "speed-recitability", "name": "Recitability", "weight": 4},
        {"id": "speed-nicklessness", "name": "Nicklessness", "weight": 15},
        {"id": "speed-nickedness", "name": "Nickedness", "weight": 10},
        {"id": "culture-chineseness", "name": "Chineseness", "weight": 4},
        {"id": "culture-genderedness", "name": "Genderedness", "weight": 20},
    ]
    return render_template('home.html', **locals())

class SavedNamesView(MethodView):
    @login_required
    def get(self):
        user = users.get_current_user()
        key = user.user_id()
        saved_names = SavedNames.get_or_insert(key, user=key)
        return jsonify(saved_names.to_dict())

    @login_required
    def post(self):
        liked = request.form.getlist('liked[]')
        hated = request.form.getlist('hated[]')
        user = users.get_current_user()
        key = user.user_id()
        saved_names = SavedNames.get_or_insert(key, user=key)
        saved_names.liked = liked
        saved_names.hated = hated
        saved_names.put()
        return jsonify(saved_names.to_dict())

app.add_url_rule('/saved_names/', view_func=SavedNamesView.as_view('saved_names'))

def list_names():
    """List all liked names for all users."""
    all_saved_names = SavedNames.query().fetch(100)
    return render_template('list_names.html', all_saved_names=all_saved_names, len=len)


def say_hello(username):
    """Contrived example to demonstrate Flask's url routing capabilities"""
    return 'Hello %s' % username

@login_required
def list_examples():
    """List all examples"""
    examples = ExampleModel.query()
    form = ExampleForm()
    if form.validate_on_submit():
        example = ExampleModel(
            example_name=form.example_name.data,
            example_description=form.example_description.data,
            added_by=users.get_current_user()
        )
        try:
            example.put()
            example_id = example.key.id()
            flash(u'Example %s successfully saved.' % example_id, 'success')
            return redirect(url_for('list_examples'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_examples'))
    return render_template('list_examples.html', examples=examples, form=form)


@login_required
def edit_example(example_id):
    example = ExampleModel.get_by_id(example_id)
    form = ExampleForm(obj=example)
    if request.method == "POST":
        if form.validate_on_submit():
            example.example_name = form.data.get('example_name')
            example.example_description = form.data.get('example_description')
            example.put()
            flash(u'Example %s successfully saved.' % example_id, 'success')
            return redirect(url_for('list_examples'))
    return render_template('edit_example.html', example=example, form=form)


@login_required
def delete_example(example_id):
    """Delete an example object"""
    example = ExampleModel.get_by_id(example_id)
    if request.method == "POST":
        try:
            example.key.delete()
            flash(u'Example %s successfully deleted.' % example_id, 'success')
            return redirect(url_for('list_examples'))
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')
            return redirect(url_for('list_examples'))


@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'Super-seekrit admin page.'


@cache.cached(timeout=60)
def cached_examples():
    """This view should be cached for 60 sec"""
    examples = ExampleModel.query()
    return render_template('list_examples_cached.html', examples=examples)


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

