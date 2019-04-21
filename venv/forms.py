# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, \
    TextField, PasswordField, SubmitField, BooleanField, SelectField, TimeField
from wtforms.validators import DataRequired, Length, Required
import time

# 增加故障的表单

class AddFaultForm(FlaskForm):
    hospital    = SelectField(  label       = u'医院',
                                validators  = [DataRequired()],
                                render_kw   = {},
                                choices     = [(1,u'请选择医院')],
                                coerce = int,)

    components  = SelectField(  label       = u'组件',
                                validators  = [DataRequired()],
                                render_kw   = {},
                                choices     = [(1,u'请选择组件')],
                                coerce=int,
                              )
    staff       = SelectField(  label       = u'负责人',
                                validators=[Required()],
                                render_kw   = {},
                                choices     = [(1,u'请选择责任人')],
                                coerce=int,
                              )
    describe    = TextAreaField(u'故障描述',validators=[DataRequired()])
    solution    = TextAreaField(u'解决方案')
    reasion     = TextAreaField(u'故障原因')
    progress    = TextAreaField(u'进展', render_kw={'placeholder':'进展，解决计划，ECR等'})
    remark      = TextAreaField(u'备注')
    faultTime   = StringField(u'time',validators=[DataRequired()])
    submit      = SubmitField(u'提交')

class AddPartForm(FlaskForm):
    hospital = StringField(u'医院',
                           render_kw = {'placeholder':u'请输入医院'},
                           validators=[DataRequired()])
    submitHospital = SubmitField(u'提交')

    components = StringField(u'组件',
                             render_kw={'placeholder': u'请输入组件'},
                             validators=[DataRequired()])
    submitComponents = SubmitField(u'提交')

    staff = StringField(u'责任人',
                        render_kw={'placeholder': u'责任人'},
                        validators=[DataRequired()])
    submitStaff = SubmitField(u'提交')


