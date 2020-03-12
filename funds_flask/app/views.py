from app import app
from .comments import comments
from .funds import funds


# app.register_blueprint(admin,url_prefix='/admin')
# app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(funds,url_prefix='/funds')
app.register_blueprint(comments, url_prefix='/comments')