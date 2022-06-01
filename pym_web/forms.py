from flask_wtf import FlaskForm
from wtforms import Form as BaseForm
# try:  # wtforms 2.x
#    from wtforms.fields.html5 import IntegerField, DateField, TimeField, DateTimeField, DateTimeLocalField
# except ImportError:  # wtforms 3.x
# unused: IntegerRangeField, RadioField
from wtforms import IntegerField, DateField, TimeField, DateTimeLocalField
from wtforms import BooleanField, StringField, URLField, TextAreaField, SelectField, FormField
from wtforms.validators import Optional, DataRequired, NumberRange, ValidationError
# 3. local
from pym_core.todo import enums as core_enums
# from models import todo_store_model

CLASS_LIST = (
    (0, '---'),
    (core_enums.EClass.Public.value, "Public"),
    (core_enums.EClass.Private.value, "Private"),
    (core_enums.EClass.Confidential.value, "Confidential")
)
STATUS_LIST = (
    (0, '---'),
    (core_enums.EStatus.NeedsAction.value, "Need action"),
    (core_enums.EStatus.InProcess.value, "In progress"),
    (core_enums.EStatus.Completed.value, "Completed"),
    (core_enums.EStatus.Cancelled.value, "Cancelled")
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


class DaTimeForm(BaseForm):  # w/o csrf chk
    d = DateField('', validators=[Optional()])
    t = TimeField('', validators=[Optional()])
    msk = BooleanField("MSK:", validators=[Optional()])

    def validate_t(self, field):
        if not self.d.data and field.data:
            raise ValidationError("Time cannot be without date")


class TodoEntryForm(FlaskForm):
    store = SelectField("Store:", coerce=int)
    summary = StringField("Summary:", validators=[DataRequired()])
    category = StringField("Category:", validators=[Optional()])
    class_ = SelectField("Class:", choices=CLASS_LIST, coerce=int, validators=[Optional()])
    prio = IntegerField("Prio:", validators=[Optional(), NumberRange(min=0, max=9)])
    dtstart = FormField(DaTimeForm)
    due = FormField(DaTimeForm)
    status = SelectField("Status:", choices=STATUS_LIST, coerce=int, validators=[Optional()])
    progress = IntegerField("Progress", validators=[Optional(), NumberRange(min=0, max=100)])
    completed = DateTimeLocalField("Completed", validators=[Optional()])
    location = StringField("Location:", validators=[Optional()])
    url = URLField("URL:", validators=[Optional()])
    desc = TextAreaField("Description:", validators=[Optional()])
