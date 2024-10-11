import os
from flask import Flask, render_template, request, url_for, redirect
from flask_wtf.csrf import CSRFProtect

# import DB
import DB_ORM as DB
from comparator import TextComparator, Differ
from exceptions import NotFoundDocumentError, SaveDocumentError


app = Flask(__name__)

app.config.update(
    DEBUG=os.environ.get('DEBUG', False),
    SECRET_KEY=os.environ.get('SECRET_KEY', 'very secret key')
)

csrf = CSRFProtect()
csrf.init_app(app)

@app.route('/')
@app.route('/docs')
def docs():
    docs=DB.get_doc_list()
    return render_template('doc_list.html', docs=docs)


@app.route('/docs/new', methods=['GET', 'POST'])
def new_doc():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        try:
            DB.save_new_doc(title, content)

        except SaveDocumentError as err:
            return render_template('error.html', error=str(err))
        return redirect(url_for('docs'))

    return render_template('doc_edit.html')


@app.route('/docs/archiv/<int:doc_id>')
def archiv_for_doc(doc_id):
    try:
        doc = DB.get_doc_by_id(doc_id)
        archiv_list = DB.get_arch_list_by_doc(doc_id)
        return render_template('history_list.html', doc=doc, archiv_list=archiv_list)
    except NotFoundDocumentError as err:
        return render_template('error.html', error=str(err))


@app.route('/docs/archiv/<int:arch_id>/detail')
def get_archiv(arch_id):
    try:
        arch = DB.get_arch_by_id(arch_id)
        return render_template('arch.html', arch=arch)
    except NotFoundDocumentError as err:
        return render_template('error.html', error=str(err))


@app.route('/docs/<int:doc_id>/minor')
def compare_doc_minor(doc_id):
    try:
        doc = DB.get_doc_by_id(doc_id)
        vers = DB.get_version(doc_id)
        titleComparator = TextComparator()
        contentComparator = TextComparator()
        if vers:
            titleComparator = TextComparator(doc.title, vers.title)
            contentComparator = TextComparator(doc.content, vers.content)
        diff = Differ(titleComparator.text_differences(), contentComparator.text_differences())
        return render_template('doc_compare.html', doc=doc, vers=vers, diff=diff)
    except NotFoundDocumentError as err:
        return render_template('error.html', error=str(err))



@app.route('/docs/<int:doc_id>/major')
def compare_doc_major(doc_id):
    try:
        doc = DB.get_doc_by_id(doc_id)
        vers = DB.get_version(doc_id, last=True)
        titleComparator = TextComparator()
        contentComparator = TextComparator()
        if vers:
            titleComparator = TextComparator(doc.title, vers.title)
            contentComparator = TextComparator(doc.content, vers.content)

        diff = Differ(titleComparator.text_differences(), contentComparator.text_differences())
        return render_template('doc_compare.html', doc=doc, vers=vers, diff=diff)
    except NotFoundDocumentError as err:
        return render_template('error.html', error=str(err))



@app.route('/docs/<int:doc_id>', methods=['GET'])
def get_doc(doc_id):
    try:
        doc = DB.get_doc_by_id(doc_id)
        return render_template('doc.html', doc=doc)
    except NotFoundDocumentError as err:
        return render_template('error.html', error=str(err))



@app.route('/docs/<int:doc_id>/edit', methods=['GET', 'POST'])
def update_doc(doc_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        try:
            DB.save_doc(doc_id, title, content)
            doc = DB.get_doc_by_id(doc_id)
            return redirect(url_for('get_doc', doc_id=doc_id))
        except NotFoundDocumentError as err:
            return render_template('error.html', error=str(err))
        except SaveDocumentError as err:
            return render_template('error.html', error=str(err))

    try:
        doc = DB.get_doc_by_id(doc_id)
        return render_template('doc_edit.html', doc=doc)
    except NotFoundDocumentError as err:
        return render_template('error.html', error=str(err))



@app.route('/docs/<int:doc_id>/delete', methods=['GET', 'POST'])
def del_doc(doc_id):
    if request.method == 'POST':
        try:
            DB.delete_doc(doc_id)
        except NotFoundDocumentError as err:
            return render_template('error.html', error=str(err))
        return redirect(url_for('docs'))

    try:
        doc = DB.get_doc_by_id(doc_id)
        return render_template('doc_delete.html', doc=doc)
    except NotFoundDocumentError as err:
        return render_template('error.html', error=str(err))


if __name__ == '__main__':
    app.run()