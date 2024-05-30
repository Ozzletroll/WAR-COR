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

    authenticators.permission_required(campaign, api=True)

    return render_template("components/template_list.html", campaign=campaign)


@bp.route("/campaigns/<campaign_name>-<campaign_id>/create-template", methods=["POST"])
@authenticators.login_required_api
def create_template(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign, api=True)

    json_data = request.get_json()
    if len(json_data["template_name"]) == 0:
        return make_response({"Message": "Title Required"}, 400)

    new_template = models.Template(name=json_data["template_name"],
                                   format=json_data["format"],
                                   parent_campaign=campaign)
    new_template.update()
    
    return make_response({"Message": "New template created"}, 200)


@bp.route("/campaigns/<campaign_name>-<campaign_id>/import-template", methods=["POST"])
@authenticators.login_required_api
def import_template(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign, api=True)

    json_data = request.get_json()
    share_code = json_data["share_code"]

    template = (db.session.query(models.Template)
                .filter(models.Template.share_code == share_code)
                .first())
    
    if template is None:
        return make_response({"Message": "Share code invalid"}, 404)
    elif campaign == template.parent_campaign:
        return make_response({"Message": "Template already imported"}, 400)
    else:
        new_template = template.duplicate(campaign)
        new_template.update()
        return make_response({"Message": "Template imported"}, 200)


@bp.route("/campaigns/<campaign_name>-<campaign_id>/delete-template", methods=["POST"])
@authenticators.login_required_api
def delete_template(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign, api=True)

    json_data = request.get_json()
    template_id = json_data.get("template_id", None)

    template = (db.session.query(models.Template)
                .filter(models.Template.id == template_id)
                .first())
    
    if template:
        # Check if user can edit selected template
        authenticators.permission_required(template.parent_campaign, api=True)
        db.session.delete(template)
        db.session.commit()
        return make_response({"Message": "Template Deleted"}, 200)
    
    else:
        return make_response({"Message": "No matching template found"}, 404)
