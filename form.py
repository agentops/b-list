from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FloatField, SelectField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    product_name = StringField(label='Name', validators=[DataRequired()])
    product_price = FloatField(label='Price', validators=[DataRequired()])
    product_date = StringField(label='Date. Format "YYYY/MM/DD"', validators=[DataRequired()])
    product_category = SelectField(label='Category', validators=[DataRequired()], coerce=str, choices=[])
    product_supplier = SelectField(label="Supplier", validators=[DataRequired()], coerce=str, choices=[])
    submit = SubmitField(label="Add Product")


class SupplierForm(FlaskForm):
    supplier_name = StringField(label="Name", validators=[DataRequired()])
    supplier_addr = StringField(label="Address", validators=[DataRequired()])
    supplier_contact = StringField(label="Contact", validators=[DataRequired()])
    submit = SubmitField(label="Add Supplier")


class CategoryForm(FlaskForm):
    category_name = StringField(label="Name", validators=[DataRequired()])
    category_desc = StringField(label="Description", validators=[DataRequired()])
    submit = SubmitField(label="Add category")