from utils import constants


class CustomJsonResponse:

    @staticmethod
    def return_server_error():
        server_err_resp = {constants.ERROR_KEY: f"Server Error"}

        return server_err_resp

    @staticmethod
    def return_endpoint_not_found():
        not_found_resp = {constants.ERROR_KEY: f"Not Found"}

        return not_found_resp

    @staticmethod
    def return_user_not_found():
        not_found_resp = {constants.ERROR_KEY: f"User does not exist."}

        return not_found_resp

    @staticmethod
    def return_user_unauth():
        unauth_resp = {constants.ERROR_KEY: f"Unauthorized access."}

        return unauth_resp

    @staticmethod
    def return_portfolio_unauth(username, user_id, portfolio_id):
        unauth_resp = {constants.ERROR_KEY: f"User (username: '{username}', ID: '{user_id}') not authorized to view "
                                            f"portfolio '{portfolio_id}' stocks."}
        return unauth_resp

    @staticmethod
    def return_portfolio_not_found(id):
        not_found_resp = {constants.ERROR_KEY: f"Portfolio id: '{id}' does not exist."}

        return not_found_resp

    @staticmethod
    def return_portfolio_stock_not_found():
        not_found_resp = {constants.ERROR_KEY: f"Stock does not exist."}

        return not_found_resp

    @staticmethod
    def return_portfolio_stock_found(stock_name):
        not_found_resp = {constants.ERROR_KEY: f"Stock '{stock_name}' exist."}

        return not_found_resp

    @staticmethod
    def return_portfolio_noti_not_found():
        not_found_resp = {constants.ERROR_KEY: f"Notification does not exist."}

        return not_found_resp

    @staticmethod
    def return_portfolio_trans_not_found(transaction_id):
        not_found_resp = {constants.ERROR_KEY: f"Transaction '{transaction_id}' does not exist."}

        return not_found_resp

    @staticmethod
    def return_successful_inserted(id):
        resp = {constants.INFO_KEY: f"Successfully inserted '{id}'"}

        return resp

    @staticmethod
    def return_successful_delete():
        resp = {constants.INFO_KEY: f"Successfully deleted."}

        return resp

    @staticmethod
    def return_successful_updated(id):
        resp = {constants.INFO_KEY: f"Successfully updated '{id}'"}

        return resp
