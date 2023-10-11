from flask import render_template, redirect, request, url_for, flash, jsonify, make_response, session
from sqlalchemy import select
import forms
import models
import utils.search as search

from app import db
from routes.search import bp


#   =======================================
#                  Search
#   =======================================


# Advanced search page, accessed from deployable searchbar on timeline
@bp.route("/campaigns/<campaign_name>-<campaign_id>/search", methods=["GET", "POST"])
def search_campaign(campaign_name, campaign_id):

  campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id, title=campaign_name)).scalar()
    
  form = forms.AdvancedSearchForm()

  return render_template("advanced_search.html", form=form, campaign=campaign)