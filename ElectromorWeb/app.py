from flask import Flask, flash, render_template, request, redirect, url_for, flash
from database import Base, engine, SessionLocal
from models import Cliente, Motor, Orden, Diagnostico, Usuario, Reporte
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Crear tablas
Base.metadata.create_all(bind=engine)

# Ruta raíz
@app.route("/")
def inicio():
    # Redirige al login directamente
    return redirect(url_for("login"))

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("username")
        contraseña = request.form.get("password")

        # Buscar usuario en la base de datos
        db = SessionLocal()
        user = db.query(Usuario).filter_by(username=usuario).first()

        if user and user.verificar_contraseña(contraseña):  # método que compara hash
            return redirect(url_for("dashboard"))
        else:
            flash("⚠️ Contraseña incorrecta, intenta nuevamente.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/registro_usuario", methods=["POST"])
def registro_usuario():
    db = SessionLocal()
    username = request.form["username"]
    password = generate_password_hash(request.form["password"])
    nuevo = Usuario(username=username, password=password)
    db.add(nuevo)
    db.commit()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# Ejemplo: Gestión de clientes
@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    db = SessionLocal()
    if request.method == "POST":
        nombre = request.form["nombre"]
        empresa = request.form["empresa"]
        telefono = request.form["telefono"]
        correo = request.form["correo"]
        cliente = Cliente(nombre=nombre, empresa=empresa, telefono=telefono, correo=correo)
        db.add(cliente)
        db.commit()
    lista = db.query(Cliente).all()
    return render_template("clientes.html", clientes=lista)

# --- Motores ---
@app.route("/motores", methods=["GET", "POST"])
def motores():
    db = SessionLocal()
    if request.method == "POST":
        marca = request.form["marca"]
        modelo = request.form["modelo"]
        potencia = request.form["potencia"]
        tipo = request.form["tipo"]
        serie = request.form["serie"]
        cliente_id = request.form["cliente_id"]
        motor = Motor(marca=marca, modelo=modelo, potencia=potencia, tipo=tipo, serie=serie, cliente_id=cliente_id)
        db.add(motor)
        db.commit()
    motores = db.query(Motor).all()
    clientes = db.query(Cliente).all()
    return render_template("motores.html", motores=motores, clientes=clientes)

# --- Órdenes ---
@app.route("/ordenes", methods=["GET", "POST"])
def ordenes():
    db = SessionLocal()
    if request.method == "POST":
        problema = request.form["problema"]
        responsable = request.form["responsable"]
        motor_id = request.form["motor_id"]
        orden = Orden(problema=problema, responsable=responsable, motor_id=motor_id)
        db.add(orden)
        db.commit()
    ordenes = db.query(Orden).all()
    motores = db.query(Motor).all()
    return render_template("ordenes.html", ordenes=ordenes, motores=motores)

# --- Diagnóstico ---
@app.route("/diagnostico", methods=["GET", "POST"])
def diagnostico():
    db = SessionLocal()
    if request.method == "POST":
        descripcion = request.form["descripcion"]
        trabajos = request.form["trabajos"]
        repuestos = request.form["repuestos"]
        pruebas = request.form["pruebas"]
        observaciones = request.form["observaciones"]
        orden_id = request.form["orden_id"]
        diag = Diagnostico(descripcion=descripcion, trabajos=trabajos,
                           repuestos=repuestos, pruebas=pruebas,
                           observaciones=observaciones, orden_id=orden_id)
        db.add(diag)
        db.commit()
    diagnosticos = db.query(Diagnostico).all()
    ordenes = db.query(Orden).all()
    return render_template("diagnostico.html", diagnosticos=diagnosticos, ordenes=ordenes)

# --- Seguimiento ---
@app.route("/seguimiento")
def seguimiento():
    db = SessionLocal()
    ordenes = db.query(Orden).all()
    return render_template("seguimiento.html", ordenes=ordenes)

# --- Reportes ---
@app.route("/reportes", methods=["GET", "POST"])
def reportes():
    db = SessionLocal()
    if request.method == "POST":
        contenido = request.form["contenido"]
        reporte = Reporte(contenido=contenido)
        db.add(reporte)
        db.commit()
    reportes = db.query(Reporte).all()
    return render_template("reportes.html", reportes=reportes)

if __name__ == "__main__":
    app.run(debug=True)