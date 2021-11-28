"""
ZTicketViewer index (main) view.

URLs include:
/
"""
import functools
import flask
import requests
from requests.auth import HTTPBasicAuth
from flask import (
    url_for, session, request, render_template, redirect, g, abort,
    )
from werkzeug.exceptions import HTTPException
from zticketviewer.config import TICKETS_DISPLAY_COUNT, TICKETS_FETCH_COUNT
import zticketviewer


@zticketviewer.app.before_request
def load_logged_in_user():
    """Load the logged in user info."""
    user = session.get('user')

    if user is None:
        g.user = None
    else:
        g.user = user


def login_required(view):
    """Customize decorator to make login necessary."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            print("Not Logged In.")
            return redirect(url_for('account_login'))

        return view(**kwargs)

    return wrapped_view


@zticketviewer.app.route('/accounts/login/', methods=('GET', 'POST'))
def account_login():
    """Display /account/login/ route."""
    if g.user is not None:
        return redirect(url_for('show_index', page_num=1))

    if request.method == 'POST':
        user = request.form['emailaddress']
        password = request.form['password']

        req = requests.get(
            "https://zccumink.zendesk.com/api/v2/tickets.json",
            auth=HTTPBasicAuth(username=user, password=password)
        )

        if req.status_code == 200:
            session["user"] = user
            session["password"] = password
            response = req.json()
            session["num_tickets"] = response["count"]

            return redirect(url_for('show_index', page_num=1))

        if req.status_code == 401:
            return render_template('noauth.html')

        abort(req.status_code)

    return render_template('login.html')


@zticketviewer.app.route('/accounts/noauth/', methods=('GET', 'POST'))
def account_noauth():
    """Display /account/noauth/ route."""
    return render_template('noauth.html')


@zticketviewer.app.route('/accounts/logout/', methods=('GET', 'POST'))
def account_logout():
    """Display /account/logout/ route."""
    session.clear()

    return redirect(url_for('account_login'))


@zticketviewer.app.route('/tickets_page/<page_num>/', methods=('GET', 'POST'))
@login_required
def show_index(page_num):
    """Display /tickets_page/<page_num>/ route."""
    context = {}
    if not page_num.isdigit():
        abort(404)
    page_num = int(page_num)
    user = session["user"]
    password = session["password"]
    if (page_num - 1) * TICKETS_DISPLAY_COUNT > session["num_tickets"]:
        abort(404)
    if page_num != 1:
        context["prev_url"] = url_for('show_index', page_num=page_num - 1)
    if page_num * TICKETS_DISPLAY_COUNT < session["num_tickets"]:
        context["next_url"] = url_for('show_index', page_num=page_num + 1)

    api_page_num = (page_num - 1) * TICKETS_DISPLAY_COUNT \
        // TICKETS_FETCH_COUNT + 1
    url = "https://zccumink.zendesk.com/api/v2/tickets.json?page=" \
        + str(api_page_num)
    print("Requesting:", url)
    req = requests.get(
        url,
        auth=HTTPBasicAuth(username=user, password=password)
    )
    if req.status_code != 200:
        abort(req.status_code)
    session["num_tickets"] = req.json()["count"]

    brief_tickets = []
    left_index = (page_num - 1) * TICKETS_DISPLAY_COUNT % TICKETS_FETCH_COUNT
    right_index = page_num * TICKETS_DISPLAY_COUNT % TICKETS_FETCH_COUNT
    guidance = " Page # " + str(page_num)
    if session["num_tickets"] != 0:
        guidance += " | Ticket # %d - %d" % (
            (page_num - 1) * TICKETS_DISPLAY_COUNT,
            min(
                page_num * TICKETS_DISPLAY_COUNT,
                session["num_tickets"]
            )-1
        )
    guidance += " | Total %d tickets" % session["num_tickets"]
    context["guidance"] = guidance
    if right_index == 0:
        right_index = TICKETS_FETCH_COUNT
    for full_ticket in req.json()["tickets"][left_index: right_index]:
        update_time = full_ticket["updated_at"]
        update_time = update_time.replace("T", " ")
        update_time = update_time.replace("Z", "")
        brief_tickets.append({
            "subject": full_ticket["subject"],
            "body": full_ticket["description"],
            "status": full_ticket["status"],
            "priority": full_ticket["priority"]
            if full_ticket["priority"] is not None else "-",
            "type": full_ticket["type"],
            "update_time": update_time,
            "tags": full_ticket["tags"],
            "id": full_ticket["id"],
            "url": url_for('show_ticket', ticket_num=full_ticket["id"])
        })

    context["user"] = user
    context["tickets"] = brief_tickets

    return flask.render_template("index.html", **context)


@zticketviewer.app.route('/ticket/<ticket_num>/', methods=('GET', 'POST'))
@login_required
def show_ticket(ticket_num):
    """Display /ticket/<ticket_num>/ route."""
    context = {}
    if not ticket_num.isdigit():
        abort(404)
    ticket_num = int(ticket_num)
    user = session["user"]
    password = session["password"]
    url = "https://zccumink.zendesk.com/api/v2/tickets/%d.json" % ticket_num
    print("Requesting:", url)
    req = requests.get(
        url,
        auth=HTTPBasicAuth(username=user, password=password)
    )
    if req.status_code != 200:
        abort(req.status_code)
    response = req.json()["ticket"]
    update_time = response["updated_at"]
    update_time = update_time.replace("T", " ")
    update_time = update_time.replace("Z", "")
    ticket_info = {
        "subject": response["subject"],
        "body": response["description"],
        "status": response["status"],
        "priority": response["priority"]
        if response["priority"] is not None else "-",
        "type": response["type"],
        "update_time": update_time,
        "tags": response["tags"]
    }
    context["ticket"] = ticket_info
    context["user"] = user
    guidance = " Ticket # %d" % ticket_num
    context["guidance"] = guidance

    url = "https://zccumink.zendesk.com/api/v2/users/%d/identities.json" \
        % response["requester_id"]
    print("Requesting:", url)
    req = requests.get(
        url,
        auth=HTTPBasicAuth(username=user, password=password)
    )
    if req.status_code != 200:
        abort(req.status_code)
    response = req.json()["identities"][0]
    context["requester"] = {
        "type": response["type"],
        "value": response["value"]
    }

    return flask.render_template("single_ticket.html", **context)


@zticketviewer.app.errorhandler(HTTPException)
def handle_exception(exception):
    """Handle exception."""
    context = {
        "error_code": exception.code,
        "error_message": exception.description,
    }
    if "user" in session:
        context["user"] = session["user"]
    return flask.render_template("bad_request.html", **context)
