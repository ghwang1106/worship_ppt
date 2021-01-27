from flask import Flask, render_template, send_file
from livereload import Server

def create_app():
  app = Flask(__name__)

  @app.route("/", methods=["GET"])
  def index():
    return render_template("index.html")
  
  @app.route('/download')
  def downloadFile ():
    path = "sample.txt"
    return send_file(path, as_attachment=True)


  return app


if __name__ == "__main__":
  app = create_app()
  server = Server(app.wsgi_app)
  server.serve(debug=True)
