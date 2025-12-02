# Instalar dependencias con: pip install flask flask-bootstrap
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Base de datos en memoria
usuarios = {"admin": "1234"}
clientes = []
destinos = []
reservas = []

# ================== Rutas del sistema ==================
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/logueo")
def logueo():
    return render_template("login.html")

# Página de inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        if usuario in usuarios and usuarios[usuario] == password:
            session["usuario"] = usuario
            return redirect(url_for("dashboard"))
        else:
            flash("Credenciales incorrectas", "danger")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

# ================== Gestión de Clientes ==================
@app.route("/clientes", methods=["GET", "POST"])
def gestion_clientes():
    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        telefono = request.form["telefono"]
        
        global clientes
        clientes.append({"id": len(clientes) + 1, "nombre": nombre, "email": email, "telefono": telefono})
        flash("Cliente agregado con éxito", "success")

    return render_template("clientes.html", clientes=clientes)

@app.route("/clientes/eliminar/<int:id>", methods=["POST"])
def eliminar_cliente(id):
    global clientes
    clientes = [c for c in clientes if c["id"] != id]
    flash("Cliente eliminado con éxito", "success")
    return redirect(url_for("gestion_clientes"))

@app.route("/clientes/editar", methods=["POST"])
def editar_cliente():
    id_cliente = int(request.form["id"])
    for cliente in clientes:
        if cliente["id"] == id_cliente:
            cliente["nombre"] = request.form["nombre"]
            cliente["email"] = request.form["email"]
            cliente["telefono"] = request.form["telefono"]
            flash("Cliente actualizado con éxito", "success")
            break
    return redirect(url_for("gestion_clientes"))

# ================== Gestión de Destinos ==================
@app.route("/destinos", methods=["GET", "POST"])
def gestion_destinos():
    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        
        global destinos
        destinos.append({"id": len(destinos) + 1, "nombre": nombre, "descripcion": descripcion})
        flash("Destino agregado con éxito", "success")

    return render_template("destinos.html", destinos=destinos)

@app.route("/destinos/eliminar/<int:id>", methods=["POST"])
def eliminar_destino(id):
    global destinos
    destinos = [d for d in destinos if d["id"] != id]
    flash("Destino eliminado con éxito", "success")
    return redirect(url_for("gestion_destinos"))

@app.route("/destinos/editar", methods=["POST"])
def editar_destino():
    id_destino = int(request.form["id"])
    for destino in destinos:
        if destino["id"] == id_destino:
            destino["nombre"] = request.form["nombre"]
            destino["descripcion"] = request.form["descripcion"]
            flash("Destino actualizado con éxito", "success")
            break
    return redirect(url_for("gestion_destinos"))

# ================== Gestión de Reservas ==================
@app.route("/reservas", methods=["GET", "POST"])
def gestion_reservas():
    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        cliente = request.form["cliente"]
        destino = request.form["destino"]
        
        global reservas
        reservas.append({"id": len(reservas) + 1, "cliente": cliente, "destino": destino})
        flash("Reserva agregada con éxito", "success")

    return render_template("reservas.html", clientes=clientes, destinos=destinos, reservas=reservas)

@app.route("/reservas/eliminar/<int:id>", methods=["POST"])
def eliminar_reserva(id):
    global reservas
    reservas = [r for r in reservas if r["id"] != id]
    flash("Reserva eliminada con éxito", "success")
    return redirect(url_for("gestion_reservas"))

@app.route("/reservas/editar", methods=["POST"])
def editar_reserva():
    id_reserva = int(request.form["id"])
    for reserva in reservas:
        if reserva["id"] == id_reserva:
            reserva["cliente"] = request.form["cliente"]
            reserva["destino"] = request.form["destino"]
            flash("Reserva actualizada con éxito", "success")
            break
    return redirect(url_for("gestion_reservas"))


# ================== Iniciar servidor ==================
if __name__ == "__main__":
    app.run(debug=True)