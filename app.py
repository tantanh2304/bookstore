import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import random
from datetime import datetime, timedelta
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

class BookReview(db.Model):
    __tablename__ = 'book_reviews'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    book = db.relationship('Book', backref='reviews')
    user = db.relationship('User', backref='reviews') 

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
    page = request.args.get('page', 1, type=int)
    per_page = 9  # Số sách mỗi trang
    
    if search:
        # Tìm kiếm với phân trang
        pagination = Book.query.filter(
            (Book.title.ilike(f'%{search}%')) | 
            (Book.author.ilike(f'%{search}%'))
        ).paginate(page=page, per_page=per_page, error_out=False)
    else:
        # Lấy tất cả sách với phân trang
        pagination = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    
    books = pagination.items
    total = pagination.total
    total_pages = pagination.pages
    
    return render_template('index.html', 
                         books=books, 
                         search=search,
                         page=page,
                         total_pages=total_pages,
                         total=total)

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

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Lấy đánh giá
    reviews = BookReview.query.filter_by(book_id=book_id).order_by(BookReview.created_at.desc()).all()
    
    # Tính điểm trung bình
    avg_rating = db.session.query(db.func.avg(BookReview.rating)).filter_by(book_id=book_id).scalar() or 0
    
    # Thống kê đánh giá
    rating_stats = db.session.query(
        BookReview.rating, 
        db.func.count(BookReview.id)
    ).filter_by(book_id=book_id).group_by(BookReview.rating).all()
    
    # Sách liên quan (cùng thể loại hoặc cùng tác giả)
    related_books = Book.query.filter(
        (Book.author == book.author) | (Book.id != book_id)
    ).limit(4).all()
    
    # Kiểm tra xem người dùng đã mua sách này chưa
    user_purchased = False
    if 'user_id' in session:
        # Thay đổi logic kiểm tra đã mua
        user_purchased = Order.query.filter(
            Order.user_id == session['user_id'], 
            Order.status == 'completed',
            Order.items.like(f'%{book.title}%')
        ).first() is not None
    
    return render_template('book_detail.html', 
                           book=book, 
                           reviews=reviews, 
                           avg_rating=avg_rating,
                           rating_stats=rating_stats,
                           related_books=related_books,
                           user_purchased=user_purchased)

@app.route('/book/<int:book_id>/review', methods=['POST'])
@login_required
def add_book_review(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Kiểm tra người dùng đã mua sách
    order = Order.query.join(Order.items).filter(
        Order.user_id == session['user_id'], 
        Order.status == 'completed',
        db.text(f"items LIKE '%{book.title}%'")
    ).first()
    
    if not order:
        flash('Bạn phải mua sách để có thể đánh giá!', 'error')
        return redirect(url_for('book_detail', book_id=book_id))
    
    rating = request.form.get('rating', type=int)
    comment = request.form.get('comment')
    
    if not rating or rating < 1 or rating > 5:
        flash('Vui lòng chọn đánh giá từ 1-5 sao!', 'error')
        return redirect(url_for('book_detail', book_id=book_id))
    
    # Kiểm tra xem người dùng đã đánh giá sách này chưa
    existing_review = BookReview.query.filter_by(
        book_id=book_id, 
        user_id=session['user_id']
    ).first()
    
    if existing_review:
        # Cập nhật đánh giá cũ
        existing_review.rating = rating
        existing_review.comment = comment
        flash('Đã cập nhật đánh giá!', 'success')
    else:
        # Tạo đánh giá mới
        review = BookReview(
            book_id=book_id, 
            user_id=session['user_id'], 
            rating=rating, 
            comment=comment
        )
        db.session.add(review)
        flash('Cảm ơn đánh giá của bạn!', 'success')
    
    db.session.commit()
    return redirect(url_for('book_detail', book_id=book_id))

@app.template_filter('average_rating')
def average_rating(reviews):
    if not reviews:
        return 0
    return sum(review.rating for review in reviews) / len(reviews)

@app.route('/my-orders')
@login_required
def my_orders():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Số đơn hàng mỗi trang
    
    # Lấy đơn hàng của user hiện tại với phân trang
    pagination = Order.query.filter_by(user_id=session['user_id'])\
        .order_by(Order.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    orders = pagination.items
    total_pages = pagination.pages
    
    # Tính tổng tiền đã chi tiêu
    total_spent = db.session.query(db.func.sum(Order.total))\
        .filter_by(user_id=session['user_id']).scalar() or 0
    
    return render_template('my_orders.html', 
                         orders=orders, 
                         page=page,
                         total_pages=total_pages,
                         total_spent=total_spent)

@app.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Kiểm tra quyền xem đơn hàng
    if order.user_id != session['user_id'] and not session.get('is_admin'):
        flash('Bạn không có quyền xem đơn hàng này!', 'error')
        return redirect(url_for('my_orders'))
    
    return render_template('order_detail.html', order=order)

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

# User Management Routes
@app.route('/admin/users')
@admin_required
def manage_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('manage_users.html', users=users)

@app.route('/admin/user/<int:user_id>')
@admin_required
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    total_spent = db.session.query(db.func.sum(Order.total)).filter_by(user_id=user_id).scalar() or 0
    
    return render_template('view_user.html', user=user, orders=orders, total_spent=total_spent)

@app.route('/admin/user/<int:user_id>/toggle_active')
@admin_required
def toggle_user_active(user_id):
    user = User.query.get_or_404(user_id)
    
    # Không cho phép khóa chính mình
    if user.id == session['user_id']:
        flash('Bạn không thể khóa tài khoản của chính mình!', 'error')
        return redirect(url_for('manage_users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'kích hoạt' if user.is_active else 'khóa'
    flash(f'Đã {status} tài khoản {user.username}!', 'success')
    return redirect(url_for('manage_users'))

@app.route('/admin/user/<int:user_id>/toggle_admin')
@admin_required
def toggle_user_admin(user_id):
    user = User.query.get_or_404(user_id)
    
    # Không cho phép tự bỏ quyền admin của mình
    if user.id == session['user_id']:
        flash('Bạn không thể thay đổi quyền admin của chính mình!', 'error')
        return redirect(url_for('manage_users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'cấp quyền' if user.is_admin else 'gỡ quyền'
    flash(f'Đã {status} admin cho {user.username}!', 'success')
    return redirect(url_for('manage_users'))

@app.route('/admin/user/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Không cho phép xóa chính mình
    if user.id == session['user_id']:
        flash('Bạn không thể xóa tài khoản của chính mình!', 'error')
        return redirect(url_for('manage_users'))
    
    # Xóa các đơn hàng và giỏ hàng liên quan
    Order.query.filter_by(user_id=user_id).delete()
    Cart.query.filter_by(user_id=user_id).delete()
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Đã xóa tài khoản {user.username}!', 'success')
    return redirect(url_for('manage_users'))

@app.route('/admin/user/<int:user_id>/reset_password', methods=['POST'])
@admin_required
def reset_user_password(user_id):
    user = User.query.get_or_404(user_id)
    new_password = request.form.get('new_password')
    
    if not new_password or len(new_password) < 6:
        flash('Mật khẩu phải có ít nhất 6 ký tự!', 'error')
        return redirect(url_for('view_user', user_id=user_id))
    
    user.password = generate_password_hash(new_password)
    db.session.commit()
    
    flash(f'Đã đặt lại mật khẩu cho {user.username}!', 'success')
    return redirect(url_for('view_user', user_id=user_id))

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

# Order Management Routes
@app.route('/admin/manage_orders')
@admin_required
def manage_orders():
    """Quản lý tất cả đơn hàng"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    search = request.args.get('search', '')
    per_page = 15
    
    # Tạo query cơ bản
    query = Order.query
    
    # Lọc theo trạng thái
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    # Tìm kiếm theo ID đơn hàng hoặc tên người dùng
    if search:
        query = query.join(User).filter(
            (Order.id == int(search) if search.isdigit() else False) |
            (User.username.ilike(f'%{search}%'))
        )
    
    # Phân trang và sắp xếp
    pagination = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    orders = pagination.items
    total_pages = pagination.pages
    
    # Thống kê
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    completed_orders = Order.query.filter_by(status='completed').count()
    cancelled_orders = Order.query.filter_by(status='cancelled').count()
    total_revenue = db.session.query(db.func.sum(Order.total)).filter_by(status='completed').scalar() or 0
    
    # Lấy thông tin user cho mỗi đơn hàng
    for order in orders:
        order.user = User.query.get(order.user_id)
    
    return render_template('manage_orders.html',
                         orders=orders,
                         page=page,
                         total_pages=total_pages,
                         status_filter=status_filter,
                         search=search,
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         completed_orders=completed_orders,
                         cancelled_orders=cancelled_orders,
                         total_revenue=total_revenue)

@app.route('/admin/manage_order/<int:order_id>')
@admin_required
def admin_order_detail(order_id):
    """Xem chi tiết đơn hàng (admin)"""
    order = Order.query.get_or_404(order_id)
    user = User.query.get(order.user_id)
    
    # Lấy tất cả đơn hàng của user này
    user_orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    
    return render_template('admin_order_detail.html', 
                         order=order, 
                         user=user,
                         user_orders=user_orders)

@app.route('/admin/manage_order/<int:order_id>/update_status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    """Cập nhật trạng thái đơn hàng"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status not in ['pending', 'processing', 'completed', 'cancelled']:
        flash('Trạng thái không hợp lệ!', 'error')
        return redirect(url_for('admin_order_detail', order_id=order_id))
    
    old_status = order.status
    order.status = new_status
    db.session.commit()
    
    status_names = {
        'pending': 'Chờ xử lý',
        'processing': 'Đang xử lý',
        'completed': 'Hoàn thành',
        'cancelled': 'Đã hủy'
    }
    
    flash(f'Đã cập nhật trạng thái từ "{status_names[old_status]}" sang "{status_names[new_status]}"!', 'success')
    return redirect(url_for('admin_order_detail', order_id=order_id))

@app.route('/admin/manage_order/<int:order_id>/delete', methods=['POST'])
@admin_required
def delete_order(order_id):
    """Xóa đơn hàng"""
    order = Order.query.get_or_404(order_id)
    
    # Chỉ cho phép xóa đơn hàng đã hủy
    if order.status != 'cancelled':
        flash('Chỉ có thể xóa đơn hàng đã hủy!', 'error')
        return redirect(url_for('admin_order_detail', order_id=order_id))
    
    db.session.delete(order)
    db.session.commit()
    
    flash(f'Đã xóa đơn hàng #{order_id}!', 'success')
    return redirect(url_for('manage_orders'))

@app.route('/admin/manage_orders/export')
@admin_required
def export_orders():
    """Xuất danh sách đơn hàng ra CSV"""
    import csv
    from io import StringIO
    from flask import make_response
    
    status_filter = request.args.get('status', 'all')
    
    # Lấy đơn hàng theo bộ lọc
    query = Order.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    orders = query.order_by(Order.created_at.desc()).all()
    
    # Tạo CSV
    si = StringIO()
    writer = csv.writer(si)
    
    # Header
    writer.writerow(['ID', 'Người dùng', 'Tổng tiền', 'Trạng thái', 'Ngày đặt', 'Sản phẩm'])
    
    # Dữ liệu
    for order in orders:
        user = User.query.get(order.user_id)
        writer.writerow([
            order.id,
            user.username,
            f'{order.total:,.0f}đ',
            order.status,
            order.created_at.strftime('%d/%m/%Y %H:%M'),
            order.items
        ])
    
    # Tạo response
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename=orders_{status_filter}_{datetime.now().strftime('%Y%m%d')}.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output

@app.route('/admin/statistics')
@admin_required
def admin_statistics():
    """Thống kê tổng quan"""
    # Thống kê đơn hàng
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    processing_orders = Order.query.filter_by(status='processing').count()
    completed_orders = Order.query.filter_by(status='completed').count()
    cancelled_orders = Order.query.filter_by(status='cancelled').count()
    
    # Thống kê doanh thu
    total_revenue = db.session.query(db.func.sum(Order.total)).filter_by(status='completed').scalar() or 0
    pending_revenue = db.session.query(db.func.sum(Order.total)).filter_by(status='pending').scalar() or 0
    
    # Top khách hàng
    top_customers = db.session.query(
        User.id,
        User.username,
        User.email,
        db.func.count(Order.id).label('order_count'),
        db.func.sum(Order.total).label('total_spent')
    ).join(Order).group_by(User.id).order_by(db.func.sum(Order.total).desc()).limit(10).all()
    
    # Sách bán chạy (phân tích từ items text)
    books_sold = {}
    orders = Order.query.filter_by(status='completed').all()
    for order in orders:
        items = order.items.split(', ')
        for item in items:
            # Format: "Tên sách xSố lượng"
            parts = item.rsplit(' x', 1)
            if len(parts) == 2:
                book_name = parts[0]
                quantity = int(parts[1])
                books_sold[book_name] = books_sold.get(book_name, 0) + quantity
    
    top_books = sorted(books_sold.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Thống kê người dùng
    total_users = User.query.count()
    admin_users = User.query.filter_by(is_admin=True).count()
    
    # Tổng số sách
    total_books = Book.query.count()
    total_stock = db.session.query(db.func.sum(Book.stock)).scalar() or 0
    
    # Tính giá trị trung bình mỗi đơn hàng (chỉ tính đơn đã hoàn thành)
    average_order_value = (total_revenue / completed_orders) if completed_orders > 0 else 0


    return render_template('admin_statistics.html',
                         total_orders=total_orders,
                         pending_orders=pending_orders,
                         processing_orders=processing_orders,
                         completed_orders=completed_orders,
                         cancelled_orders=cancelled_orders,
                         total_revenue=total_revenue,
                         pending_revenue=pending_revenue,
                         top_customers=top_customers,
                         top_books=top_books,
                         total_users=total_users,
                         admin_users=admin_users,
                         total_books=total_books,
                         total_stock=total_stock,
                         average_order_value=average_order_value)

@app.route('/admin/export_statistics')
@admin_required
def export_statistics():
    period = request.args.get('period', 'all')

    # Ở đây bạn có thể tạo file Excel hoặc CSV xuất dữ liệu thống kê
    # Ví dụ: chỉ tạo file CSV đơn giản để test

    import csv
    from io import StringIO
    from flask import make_response

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(["Tên sách", "Số lượng bán"])

    # Lấy dữ liệu bán chạy nhất (giống trong admin_statistics)
    books_sold = {}
    orders = Order.query.filter_by(status='completed').all()
    for order in orders:
        items = order.items.split(', ')
        for item in items:
            parts = item.rsplit(' x', 1)
            if len(parts) == 2:
                name = parts[0]
                qty = int(parts[1])
                books_sold[name] = books_sold.get(name, 0) + qty

    for name, qty in sorted(books_sold.items(), key=lambda x: x[1], reverse=True):
        cw.writerow([name, qty])

    response = make_response(si.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=statistics.csv"
    response.headers["Content-type"] = "text/csv"
    return response

@app.route('/seed-book-reviews')
@admin_required
def seed_book_reviews_route():
    try:
        seed_book_reviews()
        flash('Đã seed dữ liệu đánh giá sách thành công!', 'success')
    except Exception as e:
        flash(f'Lỗi khi seed dữ liệu đánh giá: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)