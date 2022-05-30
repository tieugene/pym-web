# 1. std
import ctypes
# 2. 3rd
from flask import Flask, render_template, redirect, url_for, request
# 3. local
from pym_core.base.data import Store
from pym_core.todo.data import TodoEntry
from settings import Cfg
from models import todo_store_model, todo_proxy_model
import enums
import forms

app = Flask(__name__)  # type=flask.app.Flask
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'


# template filters
@app.template_filter()
def prio(n):
    ...


@app.template_filter()
def status(n):
    ...


# go
@app.before_first_request
def autostart():
    Cfg.setup("pym-web.json")
    todo_store_model.load_self()
    todo_store_model.load_entries()
    todo_proxy_model.switchFilter(Cfg.get(enums.SetGroup.ToDo, 'filt') or 0)


@app.route('/', methods=['GET'])
def index():  # put application's code here
    # return 'Hello World!'
    return render_template('index.html')


@app.route('/info/', methods=['GET'])
def info():
    return redirect(url_for('index'))


@app.route('/contacts/', methods=['GET'])
def contacts():
    return redirect(url_for('index'))


@app.route('/todo/', methods=['GET'])
def todo_board():
    # TODO: filter, sort, entry_detail
    filt = Cfg.get(enums.SetGroup.ToDo, 'filt') or 0
    return render_template('todo_board.html',
                           stores=todo_store_model,
                           filt=filt,
                           entries=todo_proxy_model
                           )


@app.route('/todo/store/add/', methods=['GET', 'POST'])
def todo_store_add():
    # Sample: ti.Cloud - /Users/eugene/VCS/my/GIT/pyqtpim/_data/eap/ti.Cloud
    form = forms.StoreForm()
    if form.validate_on_submit():
        todo_store_model.item_add(Store(
            name=form.name.data,
            dpath=form.path.data,
            active=form.active.data))
        return redirect(url_for('todo_board'))
    return render_template('store_form.html', form=form)


@app.route('/todo/store/del/<int:store>/', methods=['GET'])
def todo_store_del(store: int):
    todo_store_model.item_del(store)
    return redirect(url_for('todo_board'))


@app.route('/todo/store/sel/', methods=['POST'])
def todo_store_sel():
    """Switch store on/off"""
    # getlist(): list of checked checkboxes value:str
    checked_set = set([int(i) for i in request.form.getlist('store')])
    print("Checked:", checked_set)
    for i, store in enumerate(todo_store_model.items()):
        checked = i in checked_set
        if store.active != checked:
            store.active = checked
            todo_store_model.save_self()
            break  # just 1 click per request
    return redirect(url_for('todo_board'))


@app.route('/todo/sort/', methods=['POST'])
def todo_set_sort():
    """Set entries sort order"""
    print("Sort:", request.form.get('sort'))
    # set proxy sort
    # save cfg
    return redirect(url_for('todo_board'))


@app.route('/todo/filt/', methods=['POST'])
def todo_set_filt():
    """Set entries filter"""
    # print("Filt:", request.form.get('filt'))
    # set proxy filter
    filt = int(request.form.get('filt'))
    todo_proxy_model.switchFilter(filt)
    Cfg.set(enums.SetGroup.ToDo, 'filt', filt)
    return redirect(url_for('todo_board'))


@app.route('/todo/entry/view/', methods=['POST'])
def todo_entry_view():
    return redirect(url_for('todo_board'))


@app.route('/todo/entry/detail/', methods=['GET'])
def todo_entry_detail():
    """Powered by https://thewebdev.info/2022/04/10/how-to-get-object-by-id-with-python/"""
    oid = int(request.args.get('id'))
    entry: TodoEntry = ctypes.cast(oid, ctypes.py_object).value
    return render_template("todo_entry_details.html", entry=entry)


if __name__ == '__main__':
    app.run()
