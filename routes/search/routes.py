from flask import render_template, redirect, request, url_for, flash, jsonify, make_response, session
from sqlalchemy import select
import forms
import models
import utils.search as search

from app import db
from routes.search import bp


# =======================================
#                Search
# =======================================


# Advanced search page, accessed from deployable searchbar on timeline
@bp.route("/campaigns/<campaign_name>-<campaign_id>/search", methods=["GET", "POST"])
def advanced_search(campaign_name, campaign_id):

    campaign = db.session.execute(
                select(models.Campaign)
                .filter_by(id=campaign_id, title=campaign_name)).scalar()
        
    form = forms.AdvancedSearchForm()

    # Check if page has any results to render
    if "results" not in request.args:
        results = None
    else:
        results = request.args["results"]

    # Check if user came from the edit timeline page
    if "edit" in request.args:
        edit = bool(request.args["edit"])
    else:
        edit = False

    # If form submitted, search database
    if form.validate_on_submit():
        search_query = request.form["search"]

        search_engine = search.SearchEngine()
        search_engine.search_campaign(campaign=campaign,
                                    query=search_query)
        
        results = search_engine.return_results()

        if len(results) == 0:
            flash("No results found")
            if edit:
                return redirect(url_for("search.advanced_search",
                                        campaign_name=campaign.title,
                                        campaign_id=campaign.id,
                                        edit=edit))
            else:
                return redirect(url_for("search.advanced_search",
                                        campaign_name=campaign.title,
                                        campaign_id=campaign.id))
        else:
            if edit:
                return render_template("advanced_search.html",
                                        form=form,
                                        campaign=campaign,
                                        edit=edit,
                                        results=results)
            else:
                return render_template("advanced_search.html",
                                        form=form,
                                        campaign=campaign,
                                        results=results)

    return render_template("advanced_search.html",
                           form=form,
                           campaign=campaign,
                           edit=edit,
                           results=results)
