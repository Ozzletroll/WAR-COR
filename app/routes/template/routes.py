from flask import make_response, request, render_template

from app import db, models
import app.utils.authenticators as authenticators

from app.routes.template import bp



@bp.route("/campaigns/<campaign_name>-<campaign_id>/get-templates", methods=["GET"])
@authenticators.login_required_api
def get_templates(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign)

    return render_template("components/template_list.html", campaign=campaign)


@bp.route("/campaigns/<campaign_name>-<campaign_id>/create-template", methods=["POST"])
@authenticators.login_required_api
def create_template(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign)

    json_data = request.get_json()

    new_template = models.Template(name=json_data["template_name"],
                                   format=json_data["format"],
                                   parent_campaign=campaign)
    new_template.update()

    response = make_response({"Message": "New template created"}, 200)

    return response
