# FIle get hong tin user info
class UserInfoContextProvider:
    def __init__(self, ):
        """
        Initializes the User Info Context Provider.
        This class is responsible for providing user information context.
        """
        pass

    def get_user_info(self, user_id: str) -> dict:
        """Retrieve user information from the database."""
        if user_id is None:
            user_id = ''
        return user_id + 'Ten cua toi la Phan Hoang Kha'
