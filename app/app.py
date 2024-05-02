from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Conexion MySQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "prueba"

conexion = MySQL(app)

@app.before_request
def before_request():
    print("Antes de la petición...")
    
@app.after_request
def after_request(response):
    print("Después de la petición...")
    return response

@app.route("/")
def index():
    cursos = "PHP, Python, Java, Kotlin, Dart, Javascript"
    cursos = cursos.split(", ")
    print(cursos)
    data = {"titulo" : "Index", 
            "bienvenida" : "Saludos",
            "cursos": cursos,
            "numero_cursos": len(cursos)}
    return render_template("index.html", data=data, cursos=cursos);

@app.route("/contacto/<nombre>/<int:edad>")
def contacto(nombre, edad):
    data = {
        "titulo" : "Contacto",
        "nombre" : nombre,
        "edad" : edad
    }
    return render_template("contacto.html", data = data)

def query_string():
    print(request)
    print(request.args)
    print(request.args.get("Param1").capitalize())
    print(request.args.get("param2"))
    return "Ok"

@app.route("/cursos")
def listar_cursos():
    data = {}
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT Nombre, Apellido FROM personal"
        cursor.execute(sql)
        cursos = cursor.fetchall()
        # print(cursos)
        data["cursos"] = cursos
        data["mensaje"] = "Exito"
    except Exception as ex:
        data["mensaje"] = "Error..."
    return jsonify(data)

def page_not_found(error):
    #return render_template("404.html"), 404
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.add_url_rule("/query_string", view_func=query_string)
    app.register_error_handler(404, page_not_found)
    app.run(debug=True, port=5000)