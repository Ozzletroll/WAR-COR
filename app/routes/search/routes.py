from flask import render_template, redirect, request, url_for, flash, session
from flask_login import current_user

from app.forms import forms
from app import db, models
import app.utils.search as search_tools
from app.utils.paginators import Paginator

from app.routes.search import bp


# =======================================
#                Search
# =======================================

# Advanced search page, accessed from deployable searchbar on timeline
@bp.route("/campaigns/<campaign_name>-<campaign_id>/search", methods=["GET", "POST"])
def advanced_search(campaign_name, campaign_id):
    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    form = forms.SearchForm()

    page = request.args.get("page", 1, type=int)
    per_page = 10
    search_engine = search_tools.SearchEngine()

    # Set back button route, excluding this route
    if not session["previous_url"]:
        session["previous_url"] = url_for("campaign.show_timeline",
                                          campaign_name=campaign.url_title,
                                          campaign_id=campaign.id)

    if request.method == "GET":

        if "search" not in request.args:
            paginator = None
            search = None
        else:
            search = request.args["search"]
            form.search.data = search

            search_engine.search_campaign(campaign=campaign,
                                          query=search)
            results = search_engine.return_results()

            edit = False
            if current_user.is_authenticated:
                if campaign in current_user.permissions:
                    edit = True

            paginator = Paginator(data=results, page=page, per_page=per_page)

        return render_template("pages/advanced_search.html",
                               form=form,
                               campaign=campaign,
                               search=search,
                               paginator=paginator)

    elif request.method == "POST":

        if form.validate_on_submit():

            page = 1
            search = request.form["search"].lower()
            search_engine.search_campaign(campaign=campaign,
                                          query=search)
            results = search_engine.return_results()
            paginator = Paginator(data=results, page=page, per_page=per_page)

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

                return render_template("pages/advanced_search.html",
                                       form=form,
                                       campaign=campaign,
                                       paginator=paginator,
                                       search=search,
                                       edit=edit)

        return redirect(url_for("search.advanced_search",
                                campaign_name=campaign.title,
                                campaign_id=campaign.id))
