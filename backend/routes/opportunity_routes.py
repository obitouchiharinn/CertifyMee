from flask import Blueprint
from controllers.opportunity_controller import (
    create_opportunity, 
    get_opportunities, 
    get_opportunity, 
    update_opportunity, 
    delete_opportunity
)

opp_bp = Blueprint('opportunity', __name__)

opp_bp.route('/opportunities', methods=['POST'])(create_opportunity)
opp_bp.route('/opportunities', methods=['GET'])(get_opportunities)
opp_bp.route('/opportunities/<int:id>', methods=['GET'])(get_opportunity)
opp_bp.route('/opportunities/<int:id>', methods=['PUT'])(update_opportunity)
opp_bp.route('/opportunities/<int:id>', methods=['DELETE'])(delete_opportunity)
