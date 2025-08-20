from waitress import serve

from pratiche.wsgi_prod import application

if __name__ == "__main__":
    serve(application, host="0.0.0.0", port=8080)
