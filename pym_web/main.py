from flask import Flask, render_template, redirect, url_for, request
# 3. local
from pym_core.base.data import Store
from settings import Cfg
from models import todo_store_model, todo_entry_model
import forms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'


@app.before_first_request
def autostart():
    Cfg.setup("pym-web.json")
    todo_store_model.load_self()
    todo_store_model.load_entries()


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
    # TODO: stores, filter, sort, entry_list, entry_detail
    #
    return render_template('todo_board.html', stores=todo_store_model, entries=todo_entry_model)


@app.route('/todo/add/', methods=['GET', 'POST'])
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


@app.route('/todo/del/<int:store>/', methods=['GET'])
def todo_store_del(store: int):
    todo_store_model.item_del(store)
    return redirect(url_for('todo_board'))


@app.route('/todo/sel/', methods=['POST'])
def todo_store_sel():
    """Switch store on/off"""
    if request.method == 'POST':
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


if __name__ == '__main__':
    app.run()
