from Website import create_app



app = create_app()

# --- TEMPORARY ROUTE: create all database tables on Render ---
@app.route("/init-db")
def init_db():
    from Website import db
    db.create_all()
    return "Database initialized successfully!"

#the debug = True means that any change i make in pythin right now automatically updates to the website as well
#when it goes live, i should turn it off

if __name__ == '__main__':

    app.run(debug =True )
