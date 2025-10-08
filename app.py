import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://book_store_sql_user:wfcjH1HyloTKgWBbLjsC1VwQ8l2dflAn@dpg-d3j0he6mcj7s739iub3g-a.oregon-postgres.render.com/book_store_sql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500), default='https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    book = db.relationship('Book', backref='cart_items')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.Column(db.Text)

# Decorators
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập!', 'error')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user.is_admin:
            flash('Bạn không có quyền truy cập!', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    search = request.args.get('search', '')
    if search:
        books = Book.query.filter(
            (Book.title.ilike(f'%{search}%')) | 
            (Book.author.ilike(f'%{search}%'))
        ).all()
    else:
        books = Book.query.all()
    
    return render_template('index.html', books=books, search=search)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Tên đăng nhập đã tồn tại!', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email đã được sử dụng!', 'error')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Đã đăng xuất!', 'success')
    return redirect(url_for('index'))

@app.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
    total = sum(item.book.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:book_id>')
@login_required
def add_to_cart(book_id):
    cart_item = Cart.query.filter_by(user_id=session['user_id'], book_id=book_id).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(user_id=session['user_id'], book_id=book_id)
        db.session.add(cart_item)
    
    db.session.commit()
    flash('Đã thêm vào giỏ hàng!', 'success')
    return redirect(url_for('index'))

@app.route('/remove_from_cart/<int:cart_id>')
@login_required
def remove_from_cart(cart_id):
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id == session['user_id']:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Đã xóa khỏi giỏ hàng!', 'success')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
    
    if not cart_items:
        flash('Giỏ hàng trống!', 'error')
        return redirect(url_for('cart'))
    
    total = sum(item.book.price * item.quantity for item in cart_items)
    items_text = ', '.join([f"{item.book.title} x{item.quantity}" for item in cart_items])
    
    order = Order(user_id=session['user_id'], total=total, items=items_text)
    db.session.add(order)
    
    for item in cart_items:
        db.session.delete(item)
    
    db.session.commit()
    
    # Lưu thông tin đơn hàng vào session để hiển thị trang thành công
    session['last_order'] = {
        'id': order.id,
        'total': total,
        'items': items_text,
        'date': order.created_at.strftime('%d/%m/%Y %H:%M')
    }
    
    return redirect(url_for('order_success'))

@app.route('/order-success')
@login_required
def order_success():
    if 'last_order' not in session:
        return redirect(url_for('index'))
    
    order_info = session.pop('last_order')
    return render_template('order_success.html', order=order_info)

# Admin routes
@app.route('/admin')
@admin_required
def admin():
    books = Book.query.all()
    return render_template('admin.html', books=books)

@app.route('/admin/add_book', methods=['GET', 'POST'])
@admin_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = float(request.form['price'])
        description = request.form['description']
        stock = int(request.form['stock'])
        image_url = request.form.get('image_url', 'https://images.unsplash.com/photo-1543002588-bfa74002ed7e?w=400')
        
        book = Book(title=title, author=author, price=price, 
                   description=description, stock=stock, image_url=image_url)
        db.session.add(book)
        db.session.commit()
        
        flash('Đã thêm sách mới!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('add_book.html')

@app.route('/admin/edit_book/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.price = float(request.form['price'])
        book.description = request.form['description']
        book.stock = int(request.form['stock'])
        book.image_url = request.form.get('image_url', book.image_url)
        
        db.session.commit()
        flash('Đã cập nhật sách!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('edit_book.html', book=book)

@app.route('/admin/delete_book/<int:book_id>')
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Đã xóa sách!', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)