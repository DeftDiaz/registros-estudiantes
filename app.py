from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'clave123'

#lista de estudiantes
estudiantes = [
    {
        'id': 1,
        'nombre': 'Juan Perez',
        'carrera': 'Ingeniería de Sistemas',
        'promedio': 8.5,
        'fecha': '2022-05-10'
    },

    {
        'id': 2,
        'nombre': 'Luis Endara',
        'carrera': 'Ciberseguridad',
        'promedio': 9.5,
        'fecha': '2024-06-12'
    },

    {
        'id': 3,
        'nombre': 'Carlos Reina',
        'carrera': 'Desarrollo de Software',
        'promedio': 9.0,
        'fecha': '2023-05-15'
    },
]

siguiente_id = 4

@app.route('/')
def index():
    busqueda = request.args.get('busqueda', '').strip().lower()
    if busqueda:
        filtrados = [e for e in estudiantes
                    if busqueda in e['nombre'].lower() or busqueda in e['carrera'].lower()]
    else:
        filtrados = estudiantes
    detalle_id = request.args.get('detalle')
    detalle = None
    if detalle_id:
        detalle = next((e for e in estudiantes if str(e['id']) == detalle_id), None)

    return render_template('index.html', estudiantes=filtrados, busqueda=busqueda, detalle=detalle)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        carrera = request.form.get('carrera', '').strip()
        promedio_str = request.form.get('promedio', '').strip()

        # Validar que los campos no estén vacíos
        if not nombre or not carrera or not promedio_str:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('nuevo.html')

        if any(e['nombre'].lower() == nombre.lower() for e in estudiantes):
            flash('El estudiante ya existe.', 'error')
            return render_template('nuevo.html')
        
        try:
            promedio = float(promedio_str)
            if promedio < 0 or promedio > 10:
                flash('El promedio debe estar entre 0 y 10.', 'error')
                return render_template('nuevo.html')
        except:
            flash('Promedio inválido.', 'error')
            return render_template('nuevo.html')
        
        global siguiente_id
        estudiantes.append({
            'id': siguiente_id,
            'nombre': nombre,
            'carrera': carrera,
            'promedio': promedio,
            'fecha': '2024-10-25'
        })
        siguiente_id += 1
        flash(f'Estudiante {nombre} agregado exitosamente.', 'success')
        return redirect(url_for('index'))
    return render_template('nuevo.html')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    global estudiantes
    estudiante = next((e for e in estudiantes if e['id'] == id), None)
    if estudiante:
        estudiantes = [e for e in estudiantes if e['id'] != id]
        flash(f'Estudiante {estudiante["nombre"]} eliminado exitosamente.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)