from views import *
from models import *
#from myblog.blue import simple_page
#----------------------------------------
# facebook authentication
#----------------------------------------

if __name__ == '__main__':
    #register blueprints
    #app.register_blueprint(simple_page)
    # or app.register_blueprint(simple_page, url_prefix='/pages')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
	
	
