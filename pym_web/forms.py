import datetime
from typing import Union

from flask_wtf import FlaskForm
from wtforms import Form as BaseForm
# try:  # wtforms 2.x
#    from wtforms.fields.html5 import IntegerField, DateField, TimeField, DateTimeField, DateTimeLocalField
# except ImportError:  # wtforms 3.x
# unused: IntegerRangeField, RadioField
from wtforms import IntegerField, DateField, TimeField, DateTimeLocalField
from wtforms import BooleanField, StringField, URLField, TextAreaField, SelectField, FormField
from wtforms.validators import Optional, DataRequired, NumberRange, ValidationError
# 3. 3rd
import dateutil
import vobject
# 4. local
from pym_core.todo import enums as core_enums
# from models import todo_store_model
from pym_core.todo.data import TodoVObj

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


def _tz_local():
    # return dateutil.tz.tz.tzlocal()     # 'MSK'
    return dateutil.tz.gettz()


def _tz_utc():
    return vobject.icalendar.utc  # FIXME: don't use vobject


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

    def getData(self) -> Union[None, datetime.date, datetime.datetime]:
        if self.t.data is None:
            return self.d.data
        else:
            return datetime.datetime.combine(
                self.d.data,
                self.t.data,
                tzinfo=_tz_local() if self.msk.data else None
            ).replace(microsecond=0)


class TodoEntryForm(FlaskForm):
    store = SelectField("Store:", coerce=int)
    summary = StringField("Summary:", validators=[DataRequired()])
    category = StringField("Category:", validators=[Optional()])
    class_ = SelectField("Class:", choices=CLASS_LIST, coerce=int, validators=[Optional()])
    priority = IntegerField("Prio:", validators=[Optional(), NumberRange(min=0, max=9)])
    dtstart = FormField(DaTimeForm)
    due = FormField(DaTimeForm)
    status = SelectField("Status:", choices=STATUS_LIST, coerce=int, validators=[Optional()])
    progress = IntegerField("Progress", validators=[Optional(), NumberRange(min=0, max=100)])
    completed = DateTimeLocalField("Completed", validators=[Optional()])
    location = StringField("Location:", validators=[Optional()])
    url = URLField("URL:", validators=[Optional()])
    description = TextAreaField("Description:", validators=[Optional()])

    def to_obj(self, vobj: TodoVObj) -> bool:
        """Update VTodoObj from form.
        :param vobj: VTodoObj to update
        :return: True if vobj was changed
        """
        chgd = False
        if v_new := self.category.data.strip():
            v_new = [s.strip() for s in v_new.split(',')]
            v_new.sort()
        else:  # empty list
            v_new = None
        chgd |= vobj.set_Categories(v_new)
        if v_new := self.class_.data:  # 0 = None
            chgd |= vobj.set_Class(core_enums.EClass(v_new))
        if v_new := self.status.data:  # 0 = None
            chgd |= vobj.set_Status(core_enums.EStatus(v_new))
        if v_new := self.completed.data:
            chgd |= vobj.set_Completed(v_new.astimezone(_tz_utc()))
        chgd |= vobj.set_DTStart(self.dtstart.getData())
        chgd |= vobj.set_Due(self.due.getData())
        chgd |= vobj.set_Progress(self.progress.data)  # int or None
        chgd |= vobj.set_Priority(self.priority.data)  # int or None
        chgd |= vobj.set_Summary(self.summary.data.strip() or None)
        chgd |= vobj.set_Location(self.location.data.strip() or None)
        chgd |= vobj.set_URL(self.url.data.strip() or None)
        chgd |= vobj.set_Description(self.description.data.strip() or None)
        if chgd:
            vobj.updateStamps()
        return chgd
