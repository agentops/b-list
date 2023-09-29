from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from form import ProductForm, SupplierForm, CategoryForm
from dotenv import load_dotenv 
from models import db, Product, Supplier, Category
import os

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
db.init_app(app=app)
Bootstrap(app=app)
# with app.app_context():
#     db.create_all()

@app.route("/")
def index():
    products = db.session.query(Product).all()
    suppliers = db.session.query(Supplier).count()
    category = db.session.query(Category).count()
    return render_template('index.html', products=products, num_suppliers=suppliers, num_categories=category)

@app.route('/add-supplier', methods=['GET', 'POST'])
def new_supplier():
    form = SupplierForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form['supplier_name']
        address = request.form['supplier_addr']
        contact = request.form['supplier_contact']
        supplier = Supplier(name=name, address=address, contact=contact)
        db.session.add(supplier)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add-supply.html', form=form)

@app.route('/add-category', methods=['GET', 'POST'])
def new_category():
    form = CategoryForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form['category_name']
        description = request.form['category_desc']

        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add-category.html', form=form)


@app.route('/add-product', methods=['GET', 'POST'])
def new_product():
    form = ProductForm()
    form.product_category.choices=[category.name for category in db.session.query(Category).all()]
    form.product_supplier.choices=[supplier.name for supplier in db.session.query(Supplier).all()]
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form['product_name']
        price = request.form['product_price']
        date = request.form['product_date']
        category = request.form['product_category']
        supplier = request.form['product_supplier']


        product = Product(name=name, 
                          price=float(price), 
                          date=date, 
                          category=Category.query.filter_by(name=category).first(), 
                          supplier=Supplier.query.filter_by(name=supplier).first())
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add-product.html', form=form)


@app.route('/edit-product/<int:id>', methods=["GET","POST"])
def edit_product(id):
    product = Product.query.get(id)
    form = ProductForm(product_name=product.name, 
                    product_date=product.date,
                    product_price=product.price,
                    )
    
    form.product_category.choices=[category.name for category in db.session.query(Category).all()]
    form.product_supplier.choices=[supplier.name for supplier in db.session.query(Supplier).all()]  

    if form.validate_on_submit():
        category = form.product_category.data
        supplier = form.product_supplier.data

        product.price = form.product_price.data
        product.name = form.product_name.data
        product.date = form.product_date.data
        product.category = Category.query.filter_by(name=category).first()
        product.supplier = Supplier.query.filter_by(name=supplier).first()
        db.session.commit()
        return redirect(url_for('all_products')) 

    return render_template('edit-product.html', form=form)


@app.route('/delete/<id>')
def del_product(id):
    product = db.session.get(Product, id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('all_products'))

@app.route("/all-products")
def all_products():
    products = db.session.query(Product).all()
    return render_template('all-products.html', products=products)

@app.route('/all-categories')
def all_categories():
    categories = db.session.query(Category).all()
    return render_template('all-categories.html', categories=categories)

@app.route('/all-suppliers')
def all_suppliers():
    suppliers = db.session.query(Supplier).all()
    return render_template('all-suppliers.html', suppliers=suppliers)

if __name__ == '__main__':
    app.run(debug=True)