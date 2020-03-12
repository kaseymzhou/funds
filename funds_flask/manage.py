from app import app
from app import db
# from flask_script import Manager
# from flask_migrate import Migrate,MigrateCommand
# from app.models import Funddetails,Catalog,Sbi,Sbr,Sbm
# print(app.url_map)

# manager= Manager(app)
# migrate = Migrate(app,db)
# manager.add_command('db',MigrateCommand)

app.run(debug=True)