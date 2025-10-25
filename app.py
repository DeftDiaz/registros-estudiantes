from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave123'

estudiantes = [
    {
        'id': 1,
        'nombre': 'Juan Pérez',
        'carrera': 'Ingeniería de Sistemas',
        'promedio': 8.5,
        'fecha_registro': '2024-01-15'
    },
    {
        'id': 2,
        'nombre': 'Carlos Martínez',
        'carrera': 'Medicina',
        'promedio': 9.1,
        'fecha_registro': '2024-02-20'
    },
    {
        'id': 3,
        'nombre': 'Luis Endara',
        'carrera': 'Ciberseguridad',
        'promedio': 9.5,
        'fecha_registro': '2024-03-12'
    },
    {
        'id': 4,
        'nombre': 'Adrian Jimenez',
        'carrera': 'Desarrollo de Software',
        'promedio': 6.1,
        'fecha_registro': '2024-04-05'
    },
]

# Variable para asignar IDs únicos
siguiente_id = 5

#Ruta principal para listado y búsqueda de estudiantes
@app.route('/')
def index():
    busqueda = request.args.get('busqueda', '').strip().lower()
    if busqueda:
        estudiantes_filtrados = [
            est for est in estudiantes 
            if busqueda in est['nombre'].lower() or busqueda in est['carrera'].lower()
        ]
    else:
        estudiantes_filtrados = estudiantes
    return render_template('index.html', estudiantes=estudiantes_filtrados, busqueda=busqueda)

#Ruta para agregar un nuevo estudiante
@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        nombre = request.form.get['nombre', ''].strip()
        carrera = request.form.get['carrera', ''].strip()
        promedio_str = request.form.get['promedio', ''].strip()

        errores = []

        if not nombre:
            errores.append('El nombre es obligatorio.')
        if not carrera:
            errores.append('La carrera es obligatoria.')
        #validar que no exista el nombre previamente
        if nombre and any(est['nombre'].lower() for est in estudiantes):
            errores.append(f'Ya existe un estudiante con ese nombre "{nombre}"')
        #validar promedio
        try:
            promedio = float(promedio_str)
            if promedio < 0 or promedio > 10:
                errores.append('El promedio debe estar entre 0 y 10.')
        except (ValueError, TypeError):
            errores.append('El promedio debe ser un número válido.')
            promedio = None
        if errores:
            for error in errores:
                flash(error, 'error')
            return render_template('nuevo.html', nombre=nombre, carrera=carrera, promedio=promedio_str)
        
        global siguiente_id
        nuevo_estudiante = {
            'id': siguiente_id,
            'nombre': nombre,
            'carrera': carrera,
            'promedio': promedio,
            'fecha_registro': datetime.now().strftime('%Y-%m-%d')
        }
        estudiantes.append(nuevo_estudiante)
        siguiente_id += 1
        flash(f'Estudiante {nombre} registrado exitosamente.', 'success')
        return redirect(url_for('index'))
    return render_template('nuevo.html')

#Ruta para ver detalle de un estudiante
@app.route('/detalle/<int:id>')
def detalle(id):
    estudiante = next((est for est in estudiantes if est['id'] == id), None)
    if estudiante is None:
        flash('Estudiante no encontrado.', 'error')
        return redirect(url_for('index'))
    return render_template('detalle.html', estudiante=estudiante)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    global estudiantes
    estudiante = next((est for est in estudiantes if est['id'] == id), None)
    if estudiante:
        estudiantes = [est for est in estudiantes if est['id'] != id]
        flash(f'Estudiante {estudiante["nombre"]} eliminado exitosamente.', 'success')
    else:
        flash('Estudiante no encontrado.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)