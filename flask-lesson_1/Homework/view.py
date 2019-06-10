from app import app
from flask import render_template, abort, request
from db_access import fetch_from_fruits, fetch_from_vegatables, insert_into_fruit, insert_into_vegetable, delete


@app.route('/<index>')
def v_or_f(index):
    if index == "vegetables":
        vegetables = fetch_from_vegatables()
        return render_template('f_or_v.html', index=index, content=vegetables)
    elif index == 'fruits':
        fruits = fetch_from_fruits()
        return render_template('f_or_v.html', index=index, content=fruits)
    else:
        return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.route('/')
def index():
    return render_template('main_page.html')


@app.route('/<index>/add')
def add(index):
    return render_template('add.html', index=index)


@app.route('/<index>/added', methods=['GET', 'POST'])
def added(index):
    if request.method == 'POST':
        if (request.form['name'] and request.form['desc'] and request.form['pic']):
            new_product = (request.form['name'], request.form['desc'], request.form['pic'])
        else:
            return render_template('not_null.html')

        if index == 'fruits':
            insert_into_fruit(new_product)
            return render_template('added.html', index='index')
        if index == 'vegetables':
            insert_into_vegetable(new_product)
            return render_template('added.html', index='index')


@app.route('/<index>/delete')
def del_item(index):
    return render_template('delete.html', index=index)


@app.route('/<index>/deleted', methods=['POST'])
def deleted(index):
    deleted_item = request.form['del_item']
    try:
        delete(index, deleted_item)
        return render_template('deleted.html', deleted_item=deleted_item)
    except ValueError:
        return render_template('no_item.html', deleted_item=deleted_item)




