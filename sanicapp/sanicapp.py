import sanic
from sanic_jwt import initialize, exceptions, protected, Configuration


class User:
    def __init__(self, id, username, password):
        self.user_id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "User(id='{}')".format(self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}


USERS = [
    User(1, "user1", "123456"),
    User(2, "user2", "123456")]

username_table = {u.username: u for u in USERS}
userid_table = {u.user_id: u for u in USERS}


class MyConfiguration(Configuration):
    secret = 'This is a not so big secret.'


def normalize_value(data_dict):
    return [value for key, value in data_dict.items() if "val" in key.lower()][0]


def normalize_list_of_dicts(list_of_dicts):
    return {value_dict["name"]: normalize_value(value_dict) for value_dict in list_of_dicts}


async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")
    user = username_table.get(username, None)
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")
    if password != user.password:
        raise exceptions.AuthenticationFailed("Password is incorrect.")
    return user


app = sanic.Sanic(name="API test")
initialize(app, authenticate=authenticate, configuration_class=MyConfiguration)


@app.post('/normalize')
@protected()
async def post_handler(request):
    return sanic.response.json(normalize_list_of_dicts(request.json))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=16001)

