from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from forms import AddFaultForm, AddPartForm
import click
import os

# set database path
dPath = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = True
    SECRET_KEY = b'\x9c\x12E\xa2\x85\x15\xd1\xf3u?\xc6\x83:\xf6V\xcf\x13N+G\xebo\xb4`\x98\xc0z\xad\xba\x01\x99['
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/data.db' % dPath
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATA_PATH = os.path.join(dPath, 'data')

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# db class
# 外键关联表
"""医院与组件"""
hospital_component_table    = db.Table( 'hospital_component',
                                        db.Column('hospital_id', db.Integer,db.ForeignKey('hospital.id')),
                                        db.Column('component_id',db.Integer,db.ForeignKey('component.id')))
"""医院与故障"""
hospital_fault_table        = db.Table( 'hospital_fault',
                                        db.Column('hospital_id', db.Integer,db.ForeignKey('hospital.id')),
                                        db.Column('fault_id',db.Integer,db.ForeignKey('fault.id')))

"""组件与故障"""
component_fault_table       = db.Table('component_fault',
                                       db.Column('component_id',db.Integer,db.ForeignKey('component.id')),
                                       db.Column('fault_id',db.Integer,db.ForeignKey('fault.id')))
# 医院表
class Hospital(db.Model):
    """基本属性"""
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,unique=True)

    """外键关联表"""
    """医院与组件"""
    component = db.relationship('Component',
                                secondary = hospital_component_table,
                                back_populates = 'hospital')
    """医院与故障"""
    fault = db.relationship('Fault',
                            secondary = hospital_fault_table,
                            back_populates = 'hospital')
    """特殊属性"""
    """省：医院在哪个省，故障汇报时使用"""
    province = db.Column(db.String)
# 组件表
class Component(db.Model):
    """基本属性"""
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32),unique=True)

    """外键关联表"""
    """医院与组件"""
    hospital = db.relationship('Hospital',
                                secondary=hospital_component_table,
                                back_populates='component')
    """组件与故障"""
    fault = db.relationship('Fault',
                            secondary = component_fault_table,
                            back_populates = 'component')
# 责任人表
class Staff(db.Model):
    """基本属性"""
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),unique=True)

    """与故障建立双向关系(一对多)"""
    fault = db.relationship('Fault',back_populates='staff')

# 故障表
class Fault(db.Model):
    """基本属性"""
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(48),unique=True)

    """外键&关联表"""
    """医院与故障"""
    hospital = db.relationship('Hospital',
                            secondary = hospital_fault_table,
                            back_populates = 'fault')
    """组件与故障"""
    component = db.relationship('Component',
                            secondary = component_fault_table,
                            back_populates = 'fault')
    """故障与责任人"""
    '''外键'''
    staff_id = db.Column(db.Integer,db.ForeignKey('staff.id'))
    '''关系属性'''
    staff = db.relationship('Staff',back_populates = 'fault')

    """特殊属性"""
    """故障描述"""
    describe = db.Column(db.String(512))
    """故障原因"""
    reasion = db.Column(db.String(512))
    """解决方案"""
    solution = db.Column(db.String(512))
    """发生时间"""
    faultTime = db.Column(db.String(32))
    """进展，解决计划，ECR等"""
    progress = db.Column(db.String(256))

# view functions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addFault',methods=['GET','POST'])
def AddFault():
    form = AddFaultForm()
    if (request.method == 'POST'):
        return redirect(url_for('index'))
    return render_template('forms/addFaultForm.html',form=form)

def AddPart2db():
    pass
@app.route('/addPart',methods=['GET','POST'])
def AddPart():
    form = AddPartForm()
    if(request.method == 'POST'):

        if(form.submitComponents.data):
            # 检查器件是否已经被添加
            for component in Component.query.all():
                if form.hospital.data == component.name:
                    flash('%s is exist'%hospital.name)
                    return redirect(url_for('index'))
            component = Component()
            component.name = form.components.data
            db.session.add(component)
            db.session.commit()
            flash('%s is added' % component.name)
        if(form.submitHospital.data):
            # 检查医院是否已经被添加
            for hospital in Hospital.query.all():
                if form.hospital.data == hospital.name:
                    flash('%s is exist'%hospital.name)
                    return redirect(url_for('index'))
            hospital = Hospital()
            hospital.name = form.hospital.data
            db.session.add(hospital)
            db.session.commit()
            flash('%s is added'%hospital.name)
        if(form.submitStaff.data):
            # 检查器件是否已经被添加
            for staff in Staff.query.all():
                if form.staff.data == staff.name:
                    flash('%s is exist' % staff.name)
                    return redirect(url_for('index'))
            staff = Staff()
            staff.name = form.staff.data
            db.session.add(staff)
            db.session.commit()
            flash('%s is added' % staff.name)
        return redirect(url_for('index'))
    return render_template('forms/addPartForm.html',form=form)
@app.route('/FaultCheck')
def FaultCheck():
    hospitals = Hospital.query.all()
    return render_template('forms/table.html',hospitals=hospitals)
@app.route('/ManagePart')
def ManagePart():
    hospitals = Hospital.query.all()
    return render_template('partManage.html',hospitals=hospitals)
@app.cli.command()
def creatTestDB():
    ha = Hospital()
    ha.name = 'Hospital a'
    hb = Hospital()
    hb.name = 'Hospital b'
    hc = Hospital()
    hc.name = 'Hospital c'

    ca = Component()
    ca.name = 'Comment a'
    cb = Component()
    cb.name = 'Comment b'
    cc = Component()
    cb.name = 'Comment b'

    f1 = Fault()
    f1.name = 'f1'
    f2 = Fault()
    f1.name = 'f2'
    f3 = Fault()
    f1.name = 'f3'
    f4 = Fault()
    f1.name = 'f4'

    sa = Staff()
    sa.name = 'sa'
    sc = Staff()
    sc.name = 'sc'

    """hospitalA componentA Fault1"""
    ha.component.append(ca)
    ha.fault.append(f1)
    ca.fault.append(f1)

    """hospitalA componentA Fault2"""
    ha.component.append(ca)
    ha.fault.append(f2)
    ca.fault.append(f2)

    """hospitalB componentA Fault1"""
    hb.component.append(ca)
    hb.fault.append(f1)
    ca.fault.append(f1)

    """hospitalB componentB Fault3"""
    hb.component.append(cb)
    hb.fault.append(f3)
    cb.fault.append(f3)

    """hospitalC componentC Fault4"""
    hc.component.append(cc)
    hc.fault.append(f4)
    cc.fault.append(f4)

    sa.fault.append(f1)
    sa.fault.append(f2)

    sc.fault.append(f3)
    sc.fault.append(f4)

    db.session.add(ha)
    db.session.add(hb)
    db.session.add(hc)
    db.session.add(ca)
    db.session.add(cb)
    db.session.add(cc)
    db.session.add(f1)
    db.session.add(f2)
    db.session.add(f3)
    db.session.add(f4)
    db.session.add(sa)
    db.session.add(sc)

    db.session.commit()

@app.cli.command()
def dbtest():
    print('list all fault')
    for hos in Hospital.query.all():
        for fault in hos.fault:
            print(hos.name,fault.name)

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    creatTestDB()
    click.echo('Initialized database.')