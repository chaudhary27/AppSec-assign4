from app import app
#from app.models import User

if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host="0.0.0.0", debug=True)

#@app.shell_context_processor
#def make_shell_context():
#    return {'db': db, 'User': User}
