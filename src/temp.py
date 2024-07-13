from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import timedelta
import os
from werkzeug.utils import secure_filename
from dao.DAOUser import DAOUser
from dao.DAOAdmin import DAOAdmin
from dao.DAOCliente import DAOCliente
from dao.DAOEmpleado import DAOEmpleado
from dao.DAOVisitor import DAOVisitor

app = Flask(__name__)

app.secret_key = "mys3cr3tk3y"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Instancias de los DAOs
dbUsuario = DAOUser()
dbAdmin = DAOAdmin()
dbCliente = DAOCliente()
dbEmpleado = DAOEmpleado()
dbInvitado = DAOVisitor()

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('main'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    gmail = request.form['correo']
    password = request.form['password']
    user = dbUsuario.verify_user(gmail, password)
    if user:
        session.permanent = True  # Marca la sesión como permanente
        if user['isAdmin']:
            admin = dbAdmin.get_admin(user['dni'])
            if admin:
                session['user'] = admin
                return redirect(url_for('main'))
        elif user['isCliente']:
            cliente = dbCliente.get_cliente(user['dni'])
            if cliente:
                session['user'] = cliente
                return redirect(url_for('main'))
        else:
            session['user'] = user
            return redirect(url_for('main'))
    flash("Correo o contraseña incorrectos")
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    print(request.form)
    if request.method == 'POST' and request.form['save']:
        if dbUsuario.create_user(request.form):
            flash("Usuario registrado")
            return redirect(url_for('index'))
        else:
            flash("Error al registrar")
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/main')
def main():
    if 'user' in session:
        user = session.get('user')
        if user and user.get('dni'):
            visitors = dbInvitado.get_visitors(user['dni'])
            if visitors is None:
                visitors = []
            return render_template('main.html', user=user, visitors=visitors)
        else:
            flash("Sesión inválida. Por favor, inicia sesión de nuevo.")
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('index'))

@app.route('/instrucciones')
def instrucciones():
    return render_template('instrucciones.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/configuracion')
def configuracion():
    if 'user' in session:
        return render_template('configuracion.html')
    else:
        return redirect(url_for('index'))

@app.route('/usuario')
def usuario():
    if 'user' in session:
        return render_template('usuario.html', user=session['user'])
    else:
        return redirect(url_for('index'))

@app.route('/agregar_invitado', methods=['GET', 'POST'])
def agregar_invitado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        dni = request.form['dni']
        dni_cliente = session['user']['dni']
        
        # Save the photo
        if 'foto' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['foto']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            foto_path = os.path.join('uploads', filename)

        data = {
            'dni': dni,
            'nombre': nombre,
            'apellido': apellido,
            'edad': edad,
            'foto': foto_path,
            'dni_cliente': dni_cliente
        }

        if dbInvitado.create_visitor(data):
            flash("Invitado agregado")
            return redirect(url_for('main'))
        else:
            flash("Error al agregar invitado")
            return redirect(url_for('agregar_invitado'))
    return render_template('agregar_invitado.html')

@app.route('/info_invitado/<dni>')
def info_invitado(dni):
    visitor = dbInvitado.get_visitor(dni)
    if visitor:
        return render_template('info_invitado.html', visitor=visitor)
    else:
        flash("Invitado no encontrado")
        return redirect(url_for('main'))
    
@app.route('/editar_invitado/<dni>', methods=['GET', 'POST'])
def editar_invitado(dni):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        edad = request.form['edad']
        dni_cliente = session['user']['dni']

        # Save the photo if updated
        if 'foto' in request.files:
            file = request.files['foto']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                foto_path = os.path.join('uploads', filename)
            else:
                foto_path = request.form['existing_foto']
        else:
            foto_path = request.form['existing_foto']

        data = {
            'nombre': nombre,
            'apellido': apellido,
            'edad': edad,
            'foto': foto_path,
            'dni_cliente': dni_cliente
        }

        if dbInvitado.update_visitor(dni, data):
            flash("Datos del invitado actualizados")
            return redirect(url_for('info_invitado', dni=dni))
        else:
            flash("Error al actualizar los datos del invitado")
            return redirect(url_for('editar_invitado', dni=dni))

    visitor = dbInvitado.get_visitor(dni)
    if visitor:
        return render_template('editar_invitado.html', visitor=visitor)
    else:
        flash("Invitado no encontrado")
        return redirect(url_for('main'))

@app.route('/eliminar_invitado/<dni>', methods=['POST'])
def eliminar_invitado(dni):
    if dbInvitado.delete_visitor(dni):
        flash("Invitado eliminado")
    else:
        flash("Error al eliminar invitado")
    return redirect(url_for('main'))

# Rutas para empleados
@app.route('/empleados', methods=['POST'])
def create_empleado():
    data = request.json
    if dbEmpleado.create_empleado(data):
        return jsonify({'message': 'Empleado creado con éxito'}), 201
    return jsonify({'message': 'Error al crear el empleado'}), 500

@app.route('/empleados/<codigo_empleado>', methods=['PUT'])
def update_empleado(codigo_empleado):
    data = request.json
    if dbEmpleado.update_empleado(codigo_empleado, data):
        return jsonify({'message': 'Empleado actualizado con éxito'}), 200
    return jsonify({'message': 'Error al actualizar el empleado'}), 500

@app.route('/empleados/<codigo_empleado>', methods=['DELETE'])
def delete_empleado(codigo_empleado):
    if dbEmpleado.delete_empleado(codigo_empleado):
        return jsonify({'message': 'Empleado eliminado con éxito'}), 200
    return jsonify({'message': 'Error al eliminar el empleado'}), 500

@app.route('/empleados', methods=['GET'])
def list_empleados():
    empleados = dbEmpleado.list_empleados()
    if empleados:
        return jsonify(empleados), 200
    return jsonify({'message': 'Error al listar los empleados'}), 500

@app.route('/empleados/<codigo_empleado>', methods=['GET'])
def get_empleado(codigo_empleado):
    empleado = dbEmpleado.get_empleado(codigo_empleado)
    if empleado:
        return jsonify(empleado), 200
    return jsonify({'message': 'Empleado no encontrado'}), 404

# Rutas para visitantes
@app.route('/visitantes', methods=['POST'])
def create_visitor():
    data = request.json
    if dbInvitado.create_visitor(data):
        return jsonify({'message': 'Visitante creado con éxito'}), 201
    return jsonify({'message': 'Error al crear el visitante'}), 500

@app.route('/visitantes/<dni>', methods=['PUT'])
def update_visitor(dni):
    data = request.json
    if dbInvitado.update_visitor(dni, data):
        return jsonify({'message': 'Visitante actualizado con éxito'}), 200
    return jsonify({'message': 'Error al actualizar el visitante'}), 500

@app.route('/visitantes/<dni>', methods=['DELETE'])
def delete_visitor(dni):
    if dbInvitado.delete_visitor(dni):
        return jsonify({'message': 'Visitante eliminado con éxito'}), 200
    return jsonify({'message': 'Error al eliminar el visitante'}), 500

@app.route('/visitantes', methods=['GET'])
def list_visitors():
    visitors = dbInvitado.list_visitors()
    if visitors:
        return jsonify(visitors), 200
    return jsonify({'message': 'Error al listar los visitantes'}), 500

@app.route('/visitantes/<dni>', methods=['GET'])
def get_visitor(dni):
    visitor = dbInvitado.get_visitor(dni)
    if visitor:
        return jsonify(visitor), 200
    return jsonify({'message': 'Visitante no encontrado'}), 404

if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0", debug=True)
