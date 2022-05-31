from flask_wtf import FlaskForm
try:  # wtforms 2.x
    from wtforms.fields.html5 import IntegerField, DateField, TimeField, DateTimeField, DateTimeLocalField
except ImportError:  # wtforms 3.x
    from wtforms import IntegerField, DateField, TimeField, DateTimeField, DateTimeLocalField
from wtforms import BooleanField, StringField, URLField, SelectField, TextAreaField
from wtforms.validators import DataRequired
# 3. local
from pym_core.todo import enums as core_enums

CLASS_LIST = (
    (core_enums.EClass.Public.value, "Public"),
    (core_enums.EClass.Confidential.value, "Confidential"),
    (core_enums.EClass.Private.value, "Private")
)
STATUS_LIST = (
    (core_enums.EStatus.NeedsAction.value, "Need action"),
    (core_enums.EStatus.InProcess.value, "In progress"),
    (core_enums.EStatus.Cancelled.value, "Cancelled"),
    (core_enums.EStatus.Completed.value, "Completed")
)


class StoreForm(FlaskForm):
    """Form to add new store
    :todo: check name/path uniqueness; path validity"""
    name = StringField("Name:", validators=[DataRequired()])
    path = StringField("Path:", validators=[DataRequired()])
    active = BooleanField("Active:")


class TodoEntryForm(FlaskForm):
    # store: select
    summary = StringField("Summary:", validators=[DataRequired()])
    category = StringField("Category:")
    class_ = SelectField("Class:", choices=CLASS_LIST, coerce=int)  # FIXME: optional
    # prio: checkbox + ~slider~ radio
    dtstart_d = DateField("DTStart.date:")  # FIXME: optional
    dtstart_t = TimeField("DTStart.time:")  # FIXME: optional, validate on date
    due_d = DateField("Due.date:")  # FIXME: optional
    due_t = TimeField("Due.time:")  # FIXME: optional, validate on date
    status = SelectField("Class:", choices=STATUS_LIST, coerce=int)  # FIXME: optional
    progress = IntegerField("Progress")  # FIXME: optional
    completed = DateTimeField("Completed")  # FIXME: optional
    location = StringField("Location:")
    url = URLField("URL:")
    desc = TextAreaField("Description:")
