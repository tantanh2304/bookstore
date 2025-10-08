"""
Script để import dữ liệu mẫu vào database
Chạy file này để tạo dữ liệu mẫu cho ứng dụng bookstore
"""

from app import app, db, User, Book, Cart, Order
from werkzeug.security import generate_password_hash
from datetime import datetime

def clear_database():
    """Xóa tất cả dữ liệu hiện tại"""
    print("🗑️  Đang xóa dữ liệu cũ...")
    try:
        Order.query.delete()
        Cart.query.delete()
        Book.query.delete()
        User.query.delete()
        db.session.commit()
        print("✅ Đã xóa dữ liệu cũ thành công!")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Lỗi khi xóa dữ liệu: {e}")
        raise

def create_users():
    """Tạo người dùng mẫu"""
    print("\n👥 Đang tạo người dùng...")
    
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@bookstore.com',
            'password': 'admin123',  # Mật khẩu gốc
            'is_admin': True
        },
        {
            'username': 'tt',
            'email': 'thanhtruc@gmail.com',
            'password': 'tt123456',
            'is_admin': False
        },
        {
            'username': 'dlinh',
            'email': 'dlinh@gmail.com',
            'password': 'dlinh123',
            'is_admin': False
        },
        {
            'username': 'hoangvy',
            'email': 'hoangvy@gmail.com',
            'password': 'vy123456',
            'is_admin': False
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password=generate_password_hash(user_data['password']),
            is_admin=user_data['is_admin'],
            created_at=datetime.utcnow()
        )
        db.session.add(user)
        users.append(user)
        print(f"  ✓ Tạo user: {user_data['username']} (pass: {user_data['password']})")
    
    db.session.commit()
    print(f"✅ Đã tạo {len(users)} người dùng!")
    return users

def create_books():
    """Tạo sách mẫu"""
    print("\n📚 Đang tạo sách...")
    
    books_data = [
        {
            'title': 'Đắc Nhân Tâm',
            'author': 'Dale Carnegie',
            'price': 95000,
            'description': 'Cuốn sách nổi tiếng về nghệ thuật giao tiếp và ứng xử',
            'stock': 50,
            'image_url': 'https://dilib.vn/img/news/2022/09/larger/403-dac-nhan-tam-1.jpg?v=5198'
        },
        {
            'title': 'Nhà Giả Kim',
            'author': 'Paulo Coelho',
            'price': 79000,
            'description': 'Hành trình tìm kiếm kho báu và ý nghĩa cuộc sống',
            'stock': 30,
            'image_url': 'https://toplist.vn/images/800px/nha-gia-kim-paulo-coelho-4777.jpg'
        },
        {
            'title': 'Sapiens',
            'author': 'Yuval Noah Harari',
            'price': 199000,
            'description': 'Lược sử loài người từ thời nguyên thủy đến hiện đại',
            'stock': 25,
            'image_url': 'https://miro.medium.com/v2/resize:fit:992/1*RIkc_6ybZDixrc6mKryWcg.jpeg'
        },
        {
            'title': 'Atomic Habits',
            'author': 'James Clear',
            'price': 149000,
            'description': 'Cách xây dựng thói quen tốt và phá bỏ thói quen xấu',
            'stock': 40,
            'image_url': 'https://cdn2.penguin.com.au/covers/original/9781473565425.jpg'
        },
        {
            'title': 'Tuổi Trẻ Đáng Giá Bao Nhiêu',
            'author': 'Rosie Nguyễn',
            'price': 89000,
            'description': 'Sách về phát triển bản thân cho giới trẻ',
            'stock': 60,
            'image_url': 'https://bookfun.vn/wp-content/uploads/2024/08/tuoi-tre-dang-gia-bao-nhieu-1.png'
        },
        {
            'title': 'Chiến Lược Đại Dương Xanh',
            'author': 'W. Chan Kim',
            'price': 135000,
            'description': 'Hướng dẫn doanh nghiệp tạo thị trường mới, tránh cạnh tranh khốc liệt',
            'stock': 15,
            'image_url': 'https://tse1.mm.bing.net/th/id/OIP.gcfxZbgACFRhcHvOdfn-cQHaKX?cb=12&rs=1&pid=ImgDetMain&o=7&rm=3'
        },
        {
            'title': 'Tư Duy Nhanh Và Chậm',
            'author': 'Daniel Kahneman',
            'price': 155000,
            'description': 'Khám phá cách con người ra quyết định qua hai hệ thống tư duy',
            'stock': 20,
            'image_url': 'https://th.bing.com/th/id/OIP.bq4y8rzTP0a5OqV-90iC2AHaHa?o=7&cb=12rm=3&rs=1&pid=ImgDetMain&o=7&rm=3'
        },
        {
            'title': 'Mắt Biếc',
            'author': 'Nguyễn Nhật Ánh',
            'price': 85000,
            'description': 'Câu chuyện tình buồn và trong sáng của Ngạn và Hà Lan',
            'stock': 40,
            'image_url': 'https://tse1.mm.bing.net/th/id/OIP.MQCPs6JTGo36srhT4IzBVwAAAA?cb=12&rs=1&pid=ImgDetMain&o=7&rm=3'
        },
        {
            'title': 'Chí Phèo',
            'author': 'Nam Cao',
            'price': 55000,
            'description': 'Truyện ngắn kinh điển về bi kịch của người nông dân bị tha hóa',
            'stock': 100,
            'image_url': 'https://salt.tikicdn.com/cache/w1200/ts/product/4d/db/88/f0c2ade75790bc8335120fd270edbdbd.jpg'
        },
        {
            'title': 'Mình Là Cá, Việc Của Mình Là Bơi',
            'author': 'Takeshi Furukawa',
            'price': 95000,
            'description': 'Sách truyền động lực, rất được giới trẻ Việt yêu thích',
            'stock': 27,
            'image_url': 'https://th.bing.com/th/id/OIP.tX0P_Jbf17mdya6KbsAk7wHaNK?o=7&cb=12rm=3&rs=1&pid=ImgDetMain&o=7&rm=3'
        },
        {
            'title': 'Dế Mèn Phiêu Lưu Ký',
            'author': 'Tô Hoài',
            'price': 75000,
            'description': 'Tác phẩm thiếu nhi kinh điển kể về hành trình trưởng thành của Dế Mèn',
            'stock': 40,
            'image_url': 'https://tse2.mm.bing.net/th/id/OIP.t1G1I0yNGQd_xK69i6zubwAAAA?cb=12&rs=1&pid=ImgDetMain&o=7&rm=3'
        }
    ]
    
    books = []
    for book_data in books_data:
        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            price=book_data['price'],
            description=book_data['description'],
            stock=book_data['stock'],
            image_url=book_data['image_url'],
            created_at=datetime.utcnow()
        )
        db.session.add(book)
        books.append(book)
        print(f"  ✓ Tạo sách: {book_data['title']} - {book_data['price']:,}đ")
    
    db.session.commit()
    print(f"✅ Đã tạo {len(books)} cuốn sách!")
    return books

def create_orders():
    """Tạo đơn hàng mẫu"""
    print("\n📦 Đang tạo đơn hàng...")
    
    orders_data = [
        {
            'user_id': 2,  # tt
            'total': 278000,
            'status': 'pending',
            'items': 'Nhà Giả Kim x1, Sapiens x1'
        },
        {
            'user_id': 3,  # dlinh
            'total': 284000,
            'status': 'pending',
            'items': 'Atomic Habits x1, Chiến Lược Đại Dương Xanh x1'
        },
        {
            'user_id': 4,  # hoangvy
            'total': 244000,
            'status': 'pending',
            'items': 'Tuổi Trẻ Đáng Giá Bao Nhiêu x1, Tư Duy Nhanh Và Chậm x1'
        },
        {
            'user_id': 4,  # hoangvy
            'total': 95000,
            'status': 'completed',
            'items': 'Đắc Nhân Tâm x1'
        }
    ]
    
    orders = []
    for order_data in orders_data:
        order = Order(
            user_id=order_data['user_id'],
            total=order_data['total'],
            status=order_data['status'],
            items=order_data['items'],
            created_at=datetime.utcnow()
        )
        db.session.add(order)
        orders.append(order)
        print(f"  ✓ Tạo đơn hàng: User {order_data['user_id']} - {order_data['total']:,}đ")
    
    db.session.commit()
    print(f"✅ Đã tạo {len(orders)} đơn hàng!")
    return orders

def create_cart_items():
    """Tạo giỏ hàng mẫu"""
    print("\n🛒 Đang tạo giỏ hàng...")
    
    # Admin có 1 sản phẩm trong giỏ (Atomic Habits)
    cart_item = Cart(
        user_id=1,
        book_id=4,
        quantity=1
    )
    db.session.add(cart_item)
    db.session.commit()
    
    print("  ✓ Tạo giỏ hàng cho admin")
    print("✅ Đã tạo giỏ hàng!")

def main():
    """Hàm chính để chạy import"""
    print("=" * 60)
    print("🚀 BẮT ĐẦU IMPORT DỮ LIỆU VÀO DATABASE")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Tạo tất cả các bảng nếu chưa có
            print("\n📋 Đang tạo các bảng trong database...")
            db.create_all()
            print("✅ Đã tạo các bảng!")
            
            # Xóa dữ liệu cũ
            clear_database()
            
            # Tạo dữ liệu mới
            users = create_users()
            books = create_books()
            orders = create_orders()
            create_cart_items()
            
            print("\n" + "=" * 60)
            print("✅ HOÀN TẤT IMPORT DỮ LIỆU!")
            print("=" * 60)
            print("\n📊 TỔNG KẾT:")
            print(f"  • Người dùng: {len(users)}")
            print(f"  • Sách: {len(books)}")
            print(f"  • Đơn hàng: {len(orders)}")
            print(f"  • Giỏ hàng: 1 mục")
            
            print("\n🔐 THÔNG TIN ĐĂNG NHẬP:")
            print("  Admin:")
            print("    - Username: admin")
            print("    - Password: admin123")
            print("\n  User thường:")
            print("    - Username: tt | Password: tt123456")
            print("    - Username: dlinh | Password: dlinh123")
            print("    - Username: hoangvy | Password: vy123456")
            
            print("\n💡 Bây giờ bạn có thể chạy: python app.py")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ LỖI: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    main()