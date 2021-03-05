from .bible2pptx_web import make_verse_ppt
from flask import Flask, request, render_template, send_file
from livereload import Server


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route('/download', methods=["GET", "POST"])
    def downloadFile():
        if request.method == "POST":
            ppt_inputs = []
            ppt_inputs.append(request.form['date_type'])
            ppt_inputs.append(request.form['sermon_title'])
            ppt_inputs.append(request.form['preacher'])
            ppt_inputs.append(request.form['main_passage'])
            ppt_inputs.append(request.form['quotes'])
            try:
                if request.form['action'] == '본문 PPT':
                    path = make_verse_ppt(ppt_inputs)
                    return send_file(path + '.pptx', as_attachment=True)
                elif request.form['action'] == '자막 PPT':
                    path = make_verse_ppt(ppt_inputs, 1)
                    return send_file(path + '.pptx', as_attachment=True)
            except TypeError:
                pass

    return app


if __name__ == "__main__":
    app = create_app()
    server = Server(app.wsgi_app)
    server.serve(debug=True)
