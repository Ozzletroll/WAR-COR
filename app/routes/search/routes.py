from flask import render_template, redirect, request, url_for, flash, session
from flask_login import current_user
from sqlalchemy import select

from app.forms import forms
from app import db, models, limiter
import app.utils.search as search
from app.routes.search import bp


# =======================================
#                Search
# =======================================

# Advanced search page, accessed from deployable searchbar on timeline
@bp.route("/campaigns/<campaign_name>-<campaign_id>/search", methods=["GET", "POST"])
@limiter.limit("60/minute")
def advanced_search(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    form = forms.SearchForm()

    # Set back button route, excluding this route
    if request.referrer:
        if "/search" not in request.referrer:
            session["previous_url"] = request.referrer
        
    # Check if page has any results to render
    if "results" not in request.args:
        results = None
    else:
        results = request.args["results"]

    # If form submitted, search database
    if form.validate_on_submit():
        search_query = request.form["search"]

        search_engine = search.SearchEngine()
        search_engine.search_campaign(campaign=campaign,
                                      query=search_query)
        results = search_engine.return_results()

        if len(results) == 0:
            flash("No results found")
            return redirect(url_for("search.advanced_search",
                                    campaign_name=campaign.title,
                                    campaign_id=campaign.id))
        else:
            edit = False
            if current_user.is_authenticated:
                if campaign in current_user.permissions:
                    edit = True

            return render_template("advanced_search.html",
                                   form=form,
                                   campaign=campaign,
                                   results=results,
                                   edit=edit)

    return render_template("advanced_search.html",
                           form=form,
                           campaign=campaign,
                           results=results)
