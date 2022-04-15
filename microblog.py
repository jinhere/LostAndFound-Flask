from app import app,db 
from app.models import User,Post
# If a file named __init__.py is present in a package directory, it's going to be invoked 
# when the package or a module inside that package is imported.
@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User,'Post':Post}
# in fact, form app import app is only required to run the application. 
# the rest(db,User,Post) are the features required for flask shell command..