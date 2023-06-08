from flask import redirect, url_for, session
from routes.data import bp


#   =======================================
#            User Data Management
#   =======================================


# Backup campaign data
@bp.route("/campaigns/<campaign_name>/backup")
def campaign_backup(campaign_name):
    target_campaign_id = session.get("campaign_id", None)
    # Export campaign data as json file.
    return redirect(url_for("campaign.show_timeline", id=target_campaign_id))


# Import campaign backup
@bp.route("/campaigns/<campaign_name>/import")
def import_campaign(campaign_name):
    target_campaign_id = session.get("campaign_id", None)
    # Export campaign data as json file.
    return redirect(url_for("campaign.show_timeline", id=target_campaign_id))


# Export campaign timeline as pdf
@bp.route("/campaigns/<campaign_name>/export")
def export_campaign(campaign_name):
    target_campaign_id = session.get("campaign_id", None)
    # Export campaign data as json file.
    return redirect(url_for("campaign.show_timeline", id=target_campaign_id))
