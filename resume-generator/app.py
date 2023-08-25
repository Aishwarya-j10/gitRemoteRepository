from flask import Flask, request, Response, render_template
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    resume = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        resume = {'name': name, 'email': email}
    return render_template('generate.html', resume=resume)

# ... (existing routes) ...

@app.route('/download')
def download():
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    name = request.args.get('name', '')
    email = request.args.get('email', '')
    phone = request.args.get('phone', '')
    address = request.args.get('address', '')
    summary = request.args.get('summary', '')

    experience = request.args.get('experience', '')
    education = request.args.get('education', '')
    projects = request.args.get('projects', '')
    skills = request.args.get('skills', '')
    awards = request.args.get('awards', '')
    languages = request.args.get('languages', '')

    data = [
        ['Your Name', name],
        ['', ''],
        [summary, ''],
        ['', ''],
        ['Contact Information:', ''],
        ['Address:', address],
        ['Phone:', phone],
        ['Email:', email],
        ['', ''],
        ['EXPERIENCE', ''],
        [experience, ''],
        ['', ''],
        ['EDUCATION', ''],
        [education, ''],
        ['', ''],
        ['PROJECTS', ''],
        [projects, ''],
        ['', ''],
        ['SKILLS', ''],
        [skills, ''],
        ['', ''],
        ['AWARDS', ''],
        [awards, ''],
        ['', ''],
        ['LANGUAGES', ''],
        [languages, '']
    ]

    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.alignment = 0  # Left-align content

    table = Table(data)
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))

    elements = [table]
    pdf.build(elements)
    buffer.seek(0)
    return Response(buffer, mimetype='application/pdf', headers={'Content-Disposition': 'attachment; filename=resume.pdf'})
if __name__ == '__main__':
    app.run(debug=True)
