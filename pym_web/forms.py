from flask_wtf import FlaskForm
# try:  # wtforms 2.x
#    from wtforms.fields.html5 import IntegerField, DateField, TimeField, DateTimeField, DateTimeLocalField
# except ImportError:  # wtforms 3.x
from wtforms import IntegerField, IntegerRangeField, DateField, TimeField, DateTimeLocalField
from wtforms import BooleanField, StringField, URLField, TextAreaField, SelectField, RadioField
from wtforms.validators import Optional, DataRequired, NumberRange
# 3. local
from pym_core.todo import enums as core_enums
from models import todo_store_model

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
PRIO_LIST = (
    ((9, "min"), (7, "low"), (5, "normal"), (3, "high"), (1, "max"))
)


class StoreForm(FlaskForm):
    """Form to add new store
    :todo: check name/path uniqueness; path validity"""
    name = StringField("Name:", validators=[DataRequired()])
    path = StringField("Path:", validators=[DataRequired()])
    active = BooleanField("Active:")


class TodoEntryForm(FlaskForm):
    store = SelectField("Store:", coerce=int)
    summary = StringField("Summary:", validators=[DataRequired()])
    category = StringField("Category:", validators=[Optional()])
    class_ = SelectField("Class:", choices=CLASS_LIST, coerce=int, validators=[Optional()])  # FIXME: optional
    prio_s = RadioField("Prio:", choices=PRIO_LIST, validators=[Optional()])  # FIXME: optional
    prio_n = IntegerField("#", validators=[Optional(), NumberRange(min=0, max=9)])  # FIXME: optional, limit 0..9
    dtstart_d = DateField("DTStart.date:", validators=[Optional()])  # FIXME: optional
    dtstart_t = TimeField("time:", validators=[Optional()])  # FIXME: optional, validate on date
    dtstart_l = BooleanField("MSK:")
    due_d = DateField("Due.date:", validators=[Optional()])  # FIXME: optional
    due_t = TimeField("Due.time:", validators=[Optional()])  # FIXME: optional, validate on date
    due_l = BooleanField("MSK:")
    status = SelectField("Status:", choices=STATUS_LIST, coerce=int, validators=[Optional()])  # FIXME: optional
    progress = IntegerRangeField("Progress", validators=[Optional(), NumberRange(min=0, max=100)])  # FIXME: optional, limit 0..100
    completed = DateTimeLocalField("Completed", validators=[Optional()])  # FIXME: optional
    location = StringField("Location:", validators=[Optional()])
    url = URLField("URL:", validators=[Optional()])
    desc = TextAreaField("Description:", validators=[Optional()])
