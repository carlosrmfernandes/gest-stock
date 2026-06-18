from flask import jsonify, make_response
from flask_jwt_extended import get_jwt_identity
from src.Application.Service.dashboard_service import DashboardService

class DashboardController:
    @staticmethod
    def get_dashboard_data():
        try:
            seller_id = get_jwt_identity()
            dados = DashboardService.obter_indicadores(seller_id)
            return make_response(jsonify(dados), 200)
        except Exception as e:
            return make_response(jsonify({"erro": f"Erro ao carregar dashboard: {str(e)}"}), 500)