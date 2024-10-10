from flask import Flask, render_template, request, url_for, redirect
import copy

import DB
from comparator import TextComparator, Differ

app = Flask(__name__)

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
        DB.save_new_doc(title, content)
        return redirect(url_for('docs'))

    return render_template('new_doc.html')


@app.route('/docs/archiv/<int:doc_id>')
def archiv_for_doc(doc_id):
    doc = DB.get_doc_by_id(doc_id)
    archiv_list = DB.get_arch_list_by_doc(doc_id)
    return render_template('history_list.html', doc=doc, archiv_list=archiv_list)


@app.route('/docs/archiv/<int:arch_id>/detail')
def get_archiv(arch_id):
    arch = DB.get_arch_by_id(arch_id)
    return render_template('arch.html', arch=arch)


@app.route('/docs/<int:doc_id>/minor')
def compare_doc_minor(doc_id):
    doc = DB.get_doc_by_id(doc_id)
    vers = DB.get_version(doc_id)
    titleComparator = TextComparator()
    contentComparator = TextComparator()
    if vers:
        titleComparator = TextComparator(doc['title'], vers['title'])
        contentComparator = TextComparator(doc['content'], vers['content'])
    diff = Differ(titleComparator.text_differences(), contentComparator.text_differences())
    return render_template('doc_compare.html', doc=doc, vers=vers, diff=diff)


@app.route('/docs/<int:doc_id>/major')
def compare_doc_major(doc_id):
    doc = DB.get_doc_by_id(doc_id)
    vers = DB.get_version(doc_id, desc=True)
    titleComparator = TextComparator()
    contentComparator = TextComparator()
    if vers:
        titleComparator = TextComparator(doc['title'], vers['title'])
        contentComparator = TextComparator(doc['content'], vers['content'])

    diff = Differ(titleComparator.text_differences(), contentComparator.text_differences())
    return render_template('doc_compare.html', doc=doc, vers=vers, diff=diff)


@app.route('/docs/<int:doc_id>', methods=['GET'])
def get_doc(doc_id):
    doc = DB.get_doc_by_id(doc_id)
    return render_template('doc.html', doc=doc)


@app.route('/docs/<int:doc_id>', methods=['POST'])
def update_doc(doc_id):
    title = request.form['title']
    content = request.form['content']
    DB.save_doc(doc_id, title, content)
    doc = DB.get_doc_by_id(doc_id)
    return render_template('doc.html', doc=doc)


@app.route('/docs/<int:doc_id>/delete', methods=['GET', 'POST'])
def del_doc(doc_id):
    if request.method == 'POST':
        DB.delete_doc(doc_id)
        return redirect(url_for('docs'))
    doc = DB.get_doc_by_id(doc_id)
    return render_template('doc_delete.html', doc=doc)

if __name__ == '__main__':
    DB.create_db()
    app.run(debug=True)