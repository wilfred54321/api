import json
def json_formatter(user):
        result = {"id": user.user_id,
                  "firstname": user.firstname,
                  "lastname": user.lastname,
                  "email": user.email,
                  "password": user.password,
                  "date_created": f'{user.date_created}',
                  "role":user.role_id}
        return result



