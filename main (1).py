#importacion de librerias
import psycopg2
from flask import Flask,render_template, request, url_for, redirect
#from flaskext.mysql import MySQL#
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="/static")
db = SQLAlchemy(app)
conn = psycopg2.connect(

    host="ec2-34-197-105-186.compute-1.amazonaws.com",
    database="d4rpk4sfoiglj7",
    user="nlfszitavdcnzj",
    password="24472049d38dcbb2177d99a65cebf4b7bc2ddcd9e2c6b3552e438fca0cbf7d69"
)
#creacion de objeto tipo flask

app = Flask(__name__, static_url_path='/static')
#creacion de ruta a pagina principal
@app.route("/")
#cracion de funcion para llamar a index (pagina principal)
def index():
    return render_template("index.html")

@app.route("/rejilla")
def rejilla_html():
    return render_template("html_rejilla.html")

@app.route("/boostrap")
def boostrap():
    return render_template("/boostrap.html")

@app.route("/acerca")
def acerca_html():
    return render_template("acerca.html")

@app.route("/formulario")
def formulario():
    connectar = conn.cursor()

    connectar.execute("SELECT*FROM datos_formulario ")

    datos = connectar.fetchall()

    print(datos)
    connectar.close()

    return render_template("formulario.html", lista=datos)

@app.route("/consultar_producto/<id>")
def obtener_producto(id):

    connectar = conn.cursor()

    connectar.execute("SELECT * FROM datos_formulario where id=%s", id)
    dato = connectar.fetchone()
    print(dato)
    connectar.close()
    return render_template("form_editar_producto.html", producto=dato)

@app.route("/editar_producto/<id>", methods=["POST"])
def editar_producto(id):
    nproducto = request.form["nproducto"]
    preciop = request.form["preciop"]
    descripcion = request.form["descripcion"]

    connectar = conn.cursor()
    connectar.execute("UPDATE datos_formulario SET producto=%s, precio=%s, descripcion=%s WHERE id=%s",
                   (nproducto, preciop, descripcion, id))
    conn.commit()
    connectar.close()


    return redirect("/formulario")


@app.route("/guardar_datos", methods=["POST"])
def guardar_datos():
    nproducto = request.form["nproducto"]
    preciop = request.form["preciop"]
    descripcion = request.form["descripcion"]

    connectar = conn.cursor()
    connectar.execute("INSERT INTO datos_formulario(producto, precio, descripcion) VALUES (%s,%s,%s)",
                   (nproducto, preciop, descripcion))

    conn.commit()
    connectar.close()

   # return "dato insertado" + nproducto + " " + preciop + " " + descripcion

    return redirect("/formulario")

@app.route("/eliminar_producto/<string:id>")
def eliminar_producto(id):


    connectar = conn.cursor()

    connectar.execute("DELETE FROM datos_formulario where id={0}".format(id))
    conn.commit()
    connectar.close()

    return redirect("/formulario")

#definir el servidor web
if __name__ == '__main__':
    # configuracion del puerto de escucha del servidor web
      app.run(port = 3000,debug = True)



