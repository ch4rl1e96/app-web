from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.ModelUser import ModelUser
from models.entities.User import User

app = Flask(__name__)

app.config['SECRET_KEY'] = '$$$$slñfcsmfpcasñ$$$'


# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Julius'
app.config['MYSQL_PASSWORD'] = 'Pandas0702'
app.config['MYSQL_DB'] = 'flask_login'

mysql = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql, id)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    cur = mysql.connection.cursor()
    cur.execute("SELECT titulo, descripcion FROM proyectos")
    projects_data = cur.fetchall()
    cur.close()
    return render_template('projects.html', projects=projects_data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/Experience')
def Experience():
    return render_template('Experience.html')

@app.route('/Education')
def Education():
    return render_template('Education.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(mysql, user)
        if logged_user is not None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('logueado'))
            else:
                flash("Invalid password...")
                return render_template('login.html')
        else:
            flash("User not found ...")
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logueado')
@login_required 
def logueado():
    return render_template('logueado.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada exitosamente.", "success")
    return redirect(url_for('home'))

@app.route('/publicar_proyecto', methods=['GET', 'POST'])
@login_required
def publicar_proyecto():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO proyectos (titulo, descripcion) VALUES (%s, %s)", (titulo, descripcion))
        mysql.connection.commit()
        cur.close()

        flash("Proyecto publicado con éxito.", "success")
        return redirect(url_for('publicar_proyecto'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, titulo, descripcion FROM proyectos")
        projects_data = cur.fetchall()
        cur.close()
        return render_template('publicar_proyecto.html', projects=projects_data)

@app.route('/editar_proyecto/<int:proyecto_id>', methods=['GET', 'POST'])
@login_required
def editar_proyecto(proyecto_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM proyectos WHERE id = %s", (proyecto_id,))
    proyecto = cur.fetchone()
    cur.close()
    
    if proyecto is None:
        flash("Proyecto no encontrado.", "danger")
        return redirect(url_for('publicar_proyecto'))

    if request.method == 'POST':
        nuevo_titulo = request.form['nuevo_titulo']
        nueva_descripcion = request.form['nueva_descripcion']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE proyectos SET titulo = %s, descripcion = %s WHERE id = %s", (nuevo_titulo, nueva_descripcion, proyecto_id))
        mysql.connection.commit()
        cur.close()

        flash("Proyecto editado con éxito.", "success")
        return redirect(url_for('publicar_proyecto'))
    else:
        return render_template('editar_proyecto.html', proyecto=proyecto)


@app.route('/eliminar_proyecto/<int:proyecto_id>', methods=['GET'])
@login_required
def eliminar_proyecto(proyecto_id):
    # Conectarse a la base de datos y eliminar el proyecto con el ID proporcionado
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM proyectos WHERE id = %s", (proyecto_id,))
    mysql.connection.commit()
    cur.close()

    flash("Proyecto eliminado con éxito.", "success")
    
    # Redirigir de nuevo a la página 'publicar_proyecto'
    return redirect(url_for('publicar_proyecto'))


if __name__ == '__main__':
    app.run(debug=True)

