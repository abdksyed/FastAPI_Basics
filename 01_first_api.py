from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return "Hello New World!"


# prop_id is a path parameter
@app.get("/property/{prop_id}")
def property(prop_id):
    return f"This is a Property Pitch for property {prop_id}"


# mov_id is a path parameter with type
@app.get("/movie/{mov_id}")
def movie(mov_id: int):
    return f"This is a Movie Pitch for movie {mov_id}"


@app.get("/user/{username}")
def user(username):
    return f"This is the profile page of {username}"


# Doesn't work since the above dynamic API route
# accepts the admin as username and execute the user API.
# To avoid this we have to place this function above the dynamic
# routing function.
@app.get("/user/admin")
def user_admin():
    return "Administration Page"


# prod_id is Query Parameters
# <url>/products?prod_id=<value>
@app.get("/products")
def products(prod_id: int, price: int = None):
    return f"Product with an id {prod_id} and with Price: {price}"


# Combination of Path paratamer and Query parameter
@app.get("/profile/{userid}/comments")
def profile(userid: int, commentid: int = None):
    return f"Profile with id {userid} and comment with id {commentid}"
