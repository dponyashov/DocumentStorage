import os
from flask import Flask, render_template, request, url_for, redirect
from flask_wtf.csrf import CSRFProtect
from functools import wraps

# import DB
import DB_ORM as DB
from comparator import TextComparator, Differ
from exceptions import NotFoundDocumentError, SaveDocumentError


app = Flask(__name__)

app.config.update(
    DEBUG=os.environ.get('DEBUG', True),
    SECRET_KEY=os.environ.get('SECRET_KEY', 'very secret key')
)

csrf = CSRFProtect()
csrf.init_app(app)


def error_404(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFoundDocumentError as err:
            return render_template('error_404.html', error=str(err))
    return inner_func

def error_save(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFoundDocumentError as err:
            return render_template('error_save.html', error=str(err))
    return inner_func

@app.route('/')
@app.route('/docs')
def docs():
    docs=DB.get_doc_list()
    return render_template('doc_list.html', docs=docs)


@app.route('/docs/new', methods=['GET', 'POST'])
@error_save
@error_404
def new_doc():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        DB.save_new_doc(title, content)
        return redirect(url_for('docs'))

    return render_template('doc_edit.html')


@app.route('/docs/archiv/<int:doc_id>')
@error_404
def archiv_for_doc(doc_id):
    doc = DB.get_doc_by_id(doc_id)
    archiv_list = DB.get_arch_list_by_doc(doc_id)
    return render_template('history_list.html', doc=doc, archiv_list=archiv_list)


@app.route('/docs/archiv/<int:arch_id>/detail')
@error_404
def get_archiv(arch_id):
    arch = DB.get_arch_by_id(arch_id)
    return render_template('arch.html', arch=arch)


@app.route('/docs/<int:doc_id>/minor')
@error_404
def compare_doc_minor(doc_id):
    doc = DB.get_doc_by_id(doc_id)
    vers = DB.get_version(doc_id)
    titleComparator = TextComparator()
    contentComparator = TextComparator()
    if vers:
         titleComparator = TextComparator(doc.title, vers.title)
         contentComparator = TextComparator(doc.content, vers.content)
    diff = Differ(titleComparator.text_differences(), contentComparator.text_differences())
    return render_template('doc_compare.html', doc=doc, vers=vers, diff=diff)



@app.route('/docs/<int:doc_id>/major')
@error_404
def compare_doc_major(doc_id):
    doc = DB.get_doc_by_id(doc_id)
    vers = DB.get_version(doc_id, last=True)
    titleComparator = TextComparator()
    contentComparator = TextComparator()
    if vers:
        titleComparator = TextComparator(doc.title, vers.title)
        contentComparator = TextComparator(doc.content, vers.content)

    diff = Differ(titleComparator.text_differences(), contentComparator.text_differences())
    return render_template('doc_compare.html', doc=doc, vers=vers, diff=diff)



@app.route('/docs/<int:doc_id>', methods=['GET'])
@error_404
def get_doc(doc_id):
    doc = DB.get_doc_by_id(doc_id)
    return render_template('doc.html', doc=doc)



@app.route('/docs/<int:doc_id>/edit', methods=['GET', 'POST'])
@error_404
@error_save
def update_doc(doc_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        DB.save_doc(doc_id, title, content)
        doc = DB.get_doc_by_id(doc_id)
        return redirect(url_for('get_doc', doc_id=doc_id))

    doc = DB.get_doc_by_id(doc_id)
    return render_template('doc_edit.html', doc=doc)



@app.route('/docs/<int:doc_id>/delete', methods=['GET', 'POST'])
@error_404
def del_doc(doc_id):
    if request.method == 'POST':
        DB.delete_doc(doc_id)
        return redirect(url_for('docs'))

    doc = DB.get_doc_by_id(doc_id)
    return render_template('doc_delete.html', doc=doc)


if __name__ == '__main__':
    app.run()