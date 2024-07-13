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
        user = session['user']
        if user['isAdmin']:
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('main'))
    return render_template('index.html')

@app.route('/live')
def live():
    return render_template('live.html')

@app.route('/login', methods=['POST'])
def login():
    gmail = request.form['correo']
    password = request.form['password']
    user = dbUsuario.verify_user(gmail, password)
    print("Usuario verificado:", user)
    
    if user:
        session.permanent = True  # Marca la sesión como permanente
        session['temp_user'] = user
        print("Usuario temporal guardado en sesión:", session['temp_user'])
        
        if user['isAdmin']:
            print("Usuario es administrador, redirigiendo a verificación de administrador.")
            return redirect(url_for('verify_admin'))
        
        elif user['isCliente']:
            print('DNI del usuario cliente:', user['dni'])
            cliente = dbCliente.get_cliente(user['dni'])
            print("Cliente obtenido:", cliente)
            
            if cliente:
                # Combinar los datos del usuario y del cliente
                session['user'] = {**user, **cliente}
                print("Cliente guardado en sesión:", session['user'])
                return redirect(url_for('main'))
        
        else:
            print("Usuario no es administrador ni cliente.")
            session['user'] = user
            print("Usuario guardado en sesión:", session['user'])
            return redirect(url_for('main'))
    
    flash("Correo o contraseña incorrectos")
    return redirect(url_for('index'))

@app.route('/verify_admin', methods=['GET', 'POST'])
def verify_admin():
    if request.method == 'POST':
        admin_code = request.form['admin_code']
        print(admin_code)
        user = session.get('temp_user')
        print(user)
        if user and dbAdmin.verify_admin_code(user['dni'], admin_code):
            session['user'] = user
            session.pop('temp_user', None)
            return redirect(url_for('admin'))
        else:
            flash("Código de administrador incorrecto")
            return redirect(url_for('verify_admin'))
    return render_template('verify_admin.html')

import requests

import requests
from werkzeug.utils import secure_filename

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'save' in request.form:
        data = request.form.to_dict()

        # Manejar la carga de la foto
        if 'foto' in request.files:
            file = request.files['foto']
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                data['foto'] = filename  # Guardar solo el nombre del archivo, no la ruta completa
            else:
                data['foto'] = None
        
        data['politicas'] = 'on' in request.form and request.form['politicas'] == 'on'
        data['isAdmin'] = False  # o True si es necesario
        data['isCliente'] = False  # o True si es necesario
        
        # Enviar solicitud POST al endpoint de Heroku
        response = requests.post(
            'https://secure-kery-db-92806f36d1d8.herokuapp.com/users',
            json=data
        )
        
        if response.status_code == 201:
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
        print("Usuario en sesión:", user)
        if user and 'dni' in user:
            visitors = dbInvitado.get_visitors(user['dni'])
            if visitors is None:
                visitors = []
            print("Visitantes obtenidos:", visitors)
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
    
@app.route('/editar_perfil', methods=['GET', 'POST'])
def editar_perfil():
    if 'user' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        gmail = request.form['gmail']
        dni = session['user']['dni']

        # Save the photo if updated
        if 'foto' in request.files:
            file = request.files['foto']
            if file.filename != '':
                filename = secure_filename(f"{dni}_avatar{os.path.splitext(file.filename)[1]}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                foto_path = os.path.join('uploads', filename)
            else:
                foto_path = session['user']['foto']
        else:
            foto_path = session['user']['foto']

        data = {
            'nombre': nombre,
            'apellido': apellido,
            'gmail': gmail,
            'foto': foto_path,
            'password': session['user']['password'],  # Keep existing password
            'politicas': session['user']['politicas']  # Keep existing politicas
        }

        if dbUsuario.update_user(dni, data):
            session['user'].update(data)
            flash("Perfil actualizado")
            return redirect(url_for('usuario'))
        else:
            flash("Error al actualizar el perfil")
            return redirect(url_for('editar_perfil'))

    return render_template('editar_perfil.html', user=session['user'])

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

@app.route('/admin')
def admin():
    if 'user' in session and session['user']['isAdmin']:
        user = session.get('user')
        if user:
            empleados = dbEmpleado.list_empleados()
            print(empleados)
            print(user)
            if empleados is None:
                empleados = []
            return render_template('admin.html', user=user, empleados=empleados)
        else:
            flash("Sesión inválida. Por favor, inicia sesión de nuevo.")
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('index'))

@app.route('/admin_info')
def admin_info():
    if 'user' in session and session['user']['isAdmin']:
        print(session['user'])
        return render_template('admin_info.html', user=session['user'])
    else:
        return redirect(url_for('index'))

@app.route('/editar_admin/<dni>', methods=['GET', 'POST'])
def editar_admin(dni):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        gmail = request.form['gmail']
        password = request.form['password']
        codAdmin = request.form['codAdmin']
        
        print("si entra aqui 1")

        # Verificar el código del administrador
        if not dbAdmin.verify_admin_code(dni, codAdmin):
            flash("Código de administrador incorrecto")
            return redirect(url_for('editar_admin', dni=dni))

        print("si entra aqui 2")

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
        
        print("si entra aqui ")

        data = {
            'nombre': nombre,
            'apellido': apellido,
            'gmail': gmail,
            'password': password if password else session['user']['password'],
            'foto': foto_path,
            'codAdmin': codAdmin
        }
        

        if dbAdmin.update_admin(dni, data):
            # Obtener la información actualizada del administrador
            updated_user = dbAdmin.get_admin(dni)
            print("Datos del administrador actualizados:", updated_user)
            if updated_user:
                session['user'] = updated_user
                print("Datos de sesión actualizados:", session['user'])
                flash("Datos del administrador actualizados")
                return redirect(url_for('admin_info'))
            else:
                flash("Error al obtener los datos actualizados del administrador")
                return redirect(url_for('editar_admin', dni=dni))
        else:
            flash("Error al actualizar los datos del administrador")
            return redirect(url_for('editar_admin', dni=dni))

    if 'user' in session and session['user']['dni'] == dni and session['user']['isAdmin']:
        print("Rendering editar_admin with user data:", session['user'])
        return render_template('editar_admin.html', user=session['user'])
    else:
        flash("Sesión inválida. Por favor, inicia sesión de nuevo.")
        return redirect(url_for('logout'))




@app.route('/info_empleado/<codigo_empleado>')
def info_empleado(codigo_empleado):
    empleado = dbEmpleado.get_empleado(codigo_empleado)
    print(empleado)
    if empleado:
        return render_template('info_empleado.html', empleado=empleado)
    else:
        flash("Empleado no encontrado")
        return redirect(url_for('admin'))
    
@app.route('/agregar_empleado', methods=['GET', 'POST'])
def agregar_empleado():
    if request.method == 'POST':
        codigo_empleado = request.form['codigo_empleado']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        email = request.form['email']
        cargo = request.form['cargo']
        dni_admin = session['user']['dni']
        
        # Save the photo
        if 'foto' in request.files:
            file = request.files['foto']
            if file.filename != '':
                extension = file.filename.rsplit('.', 1)[1].lower()  # get the file extension
                filename = secure_filename(f"{nombre}_{dni_admin}_{dni}.{extension}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                foto_path = os.path.join('uploads', filename)
            else:
                foto_path = ''
        else:
            foto_path = ''

        data = {
            'codigo_empleado': codigo_empleado,
            'nombre': nombre,
            'apellido': apellido,
            'dni': dni,
            'email': email,
            'cargo': cargo,
            'foto': foto_path
        }

        if dbEmpleado.create_empleado(data):
            flash("Empleado agregado")
            return redirect(url_for('admin'))
        else:
            flash("Error al agregar empleado")
            return redirect(url_for('agregar_empleado'))
    return render_template('agregar_empleado.html')


@app.route('/editar_empleado/<codigo_empleado>', methods=['GET', 'POST'])
def editar_empleado(codigo_empleado):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        dni = request.form['dni']
        email = request.form['email']
        cargo = request.form['cargo']
        dni_admin = session['user']['dni']  # Assuming the admin's dni is stored in the session

        # Save the photo if updated
        if 'foto' in request.files:
            file = request.files['foto']
            if file.filename != '':
                filename = secure_filename(f"{nombre}_{dni_admin}_{dni}.jpeg")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                foto_path = os.path.join('uploads', filename)
            else:
                foto_path = request.form['existing_foto']
        else:
            foto_path = request.form['existing_foto']

        data = {
            'nombre': nombre,
            'apellido': apellido,
            'dni': dni,
            'email': email,
            'cargo': cargo,
            'foto': foto_path
        }

        if dbEmpleado.update_empleado(codigo_empleado, data):
            flash("Datos del empleado actualizados")
            return redirect(url_for('info_empleado', codigo_empleado=codigo_empleado))
        else:
            flash("Error al actualizar los datos del empleado")
            return redirect(url_for('editar_empleado', codigo_empleado=codigo_empleado))

    empleado = dbEmpleado.get_empleado(codigo_empleado)
    if empleado:
        return render_template('editar_empleado.html', empleado=empleado)
    else:
        flash("Empleado no encontrado")
        return redirect(url_for('admin'))


@app.route('/eliminar_empleado/<codigo_empleado>', methods=['POST'])
def eliminar_empleado(codigo_empleado):
    if dbEmpleado.delete_empleado(codigo_empleado):
        flash("Empleado eliminado")
    else:
        flash("Error al eliminar empleado")
    return redirect(url_for('admin'))
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

@app.route('/contacts')
def contacts():
    if 'user' in session:
        return render_template('contacts.html')
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=3000, host="0.0.0.0", debug=True)
