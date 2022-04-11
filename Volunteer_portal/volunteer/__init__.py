from flask import Flask, render_template
import psycopg2

def create_app():
    app=Flask("volunteer")

    app.config.from_mapping(
        DATABASE="volunteer"
    )

    from . import main
    app.register_blueprint(main.bp)

    from . import db
    db.init_app(app)

    @app.route("/")
    def index():
        return render_template("index.html")
 
    

    return app  
