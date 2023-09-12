from flask import redirect, url_for, flash
from flask_login import logout_user

def logout():
    # Realiza la acción de cierre de sesión aquí (por ejemplo, utilizando Flask-Login)
    logout_user()
    flash("Sesión cerrada exitosamente.", "success")
    return redirect(url_for('base'))  # Redirige al usuario a la página de inicio u otra página después del cierre de sesión
