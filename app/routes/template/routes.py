from flask import make_response, request
from flask_login import login_required

from app import db, models
import app.utils.authenticators as authenticators

from app.routes.template import bp


@bp.route("/campaigns/<campaign_name>-<campaign_id>/create-template", methods=["POST"])
@login_required
def create_template(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign)

    json_data = request.get_json()

    models.Template(name=json_data["template_name"],
                    format=json_data["format"],
                    parent_campaign=campaign)

    response = make_response({"Message": "New template created"}, 200)

    return response
