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
    print("\n📦 Đang tạo đơn hàng...")

    # Lấy lại danh sách người dùng vừa được tạo
    # *QUAN TRỌNG: Cần đảm bảo hàm create_users() trả về danh sách các đối tượng User
    # Nếu không, bạn cần truy vấn lại từ database.
    # Tuy nhiên, cách tốt nhất là truyền danh sách users từ hàm main() vào đây.

    # Giả sử hàm main() đã được sửa để truyền users vào, ta sẽ dùng user.query
    # để lấy chính xác ID.

    # Lấy các đối tượng người dùng dựa trên username đã biết
    try:
        user_tt = User.query.filter_by(username='tt').first()
        user_dlinh = User.query.filter_by(username='dlinh').first()
        user_hoangvy = User.query.filter_by(username='hoangvy').first()
    except:
        # Xử lý trường hợp không tìm thấy user (rất hiếm nếu create_users() thành công)
        print("❌ Lỗi: Không tìm thấy người dùng mẫu (tt, dlinh, hoangvy) trong database.")
        return []

    # Lấy các đối tượng sách để tính tổng tiền (total)
    book_nkg = Book.query.filter_by(title='Nhà Giả Kim').first()
    book_sp = Book.query.filter_by(title='Sapiens').first()
    book_ah = Book.query.filter_by(title='Atomic Habits').first()
    book_cl = Book.query.filter_by(title='Chiến Lược Đại Dương Xanh').first()
    book_ttdgbn = Book.query.filter_by(title='Tuổi Trẻ Đáng Giá Bao Nhiêu').first()
    book_tdnhc = Book.query.filter_by(title='Tư Duy Nhanh Và Chậm').first()
    book_dnt = Book.query.filter_by(title='Đắc Nhân Tâm').first()


    orders_data = [
        {
            'user_id': user_tt.id if user_tt else 0, # Dùng user_tt.id thay cho ID cố định
            'total': book_nkg.price + book_sp.price,
            'status': 'pending',
            'items': 'Nhà Giả Kim x1, Sapiens x1'
        },
        {
            'user_id': user_dlinh.id if user_dlinh else 0, # Dùng user_dlinh.id
            'total': book_ah.price + book_cl.price,
            'status': 'pending',
            'items': 'Atomic Habits x1, Chiến Lược Đại Dương Xanh x1'
        },
        {
            'user_id': user_hoangvy.id if user_hoangvy else 0, # Dùng user_hoangvy.id
            'total': book_ttdgbn.price + book_tdnhc.price,
            'status': 'pending',
            'items': 'Tuổi Trẻ Đáng Giá Bao Nhiêu x1, Tư Duy Nhanh Và Chậm x1'
        },
        {
            'user_id': user_hoangvy.id if user_hoangvy else 0, # Dùng user_hoangvy.id
            'total': book_dnt.price,
            'status': 'completed',
            'items': 'Đắc Nhân Tâm x1'
        }
    ]

    orders = []
    for data in orders_data:
        if data['user_id'] != 0: # Chỉ tạo đơn hàng nếu tìm thấy user
            order = Order(
                user_id=data['user_id'],
                total=data['total'],
                status=data['status'],
                created_at=datetime.utcnow(),
                items=data['items']
            )
            db.session.add(order)
            orders.append(order)
            print(f"  ✓ Tạo đơn hàng: User {data['user_id']} - {data['total']:,}đ")


    try:
        db.session.commit()
        print(f"✅ Đã tạo {len(orders)} đơn hàng!")
        return orders
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ LỖI KHI TẠO ĐƠN HÀNG: {e.orig}") # Sửa lại để in lỗi gốc
        return []
    
def create_cart_items():
    print("\n🛒 Đang tạo giỏ hàng mẫu...")

    # 1. Lấy đối tượng User (Admin) dựa trên username
    # Admin là user đầu tiên được tạo, ta sử dụng username='admin' để đảm bảo lấy đúng ID
    admin_user = User.query.filter_by(username='admin').first()

    # 2. Lấy đối tượng Book (ví dụ: Atomic Habits) dựa trên tên sách
    book = Book.query.filter_by(title='Atomic Habits').first()

    if not admin_user:
        print("❌ Lỗi: Không tìm thấy người dùng 'admin'.")
        return []

    if not book:
        print("❌ Lỗi: Không tìm thấy sách 'Atomic Habits'.")
        return []

    # 3. Tạo một mục giỏ hàng cho Admin
    try:
        cart_item = Cart(
            user_id=admin_user.id, # Sử dụng ID thực tế của Admin
            book_id=book.id,       # Sử dụng ID thực tế của sách
            quantity=1
        )
        db.session.add(cart_item)
        db.session.commit()
        print(f"  ✓ Tạo giỏ hàng: Admin (ID: {admin_user.id}) - {book.title} x1")
        print("✅ Đã tạo 1 mục giỏ hàng!")
        return [cart_item]
    except Exception as e:
        db.session.rollback()
        # Bắt lỗi IntegrityError để báo lỗi chi tiết hơn
        print(f"\n❌ LỖI KHI TẠO GIỎ HÀNG: {e.orig}")
        return []
    
def seed_book_reviews():
    """
    Hàm thêm dữ liệu mẫu chi tiết cho đánh giá sách
    """
    # Danh sách nhận xét chi tiết theo từng thể loại sách
    review_comments = {
        # Sách văn học
        'literary': [
            "Một tác phẩm nghệ thuật, từng câu từ đều được chăm chút.",
            "Cốt truyện sâu sắc, khơi gợi nhiều cảm xúc.",
            "Tác giả đã thành công trong việc khắc họa tâm lý nhân vật.",
            "Một góc nhìn mới mẻ và sáng tạo về cuộc sống.",
            "Văn phong tinh tế, đọc như một bản nhạc.",
        ],
        
        # Sách phát triển bản thân
        'self_help': [
            "Những lời khuyên thực tế và áp dụng được ngay.",
            "Đã thay đổi cách nhìn của tôi về bản thân.",
            "Rất hữu ích cho việc phát triển kỹ năng sống.",
            "Những insights sâu sắc và đầy động lực.",
            "Cuốn sách như một người bạn đồng hành.",
        ],
        
        # Sách kinh doanh
        'business': [
            "Những chiến lược kinh doanh thực tế và hiệu quả.",
            "Đã học được nhiều bài học quan trọng từ kinh nghiệm của các chuyên gia.",
            "Rất hữu ích cho những ai muốn khởi nghiệp.",
            "Cung cấp cái nhìn toàn diện về thế giới kinh doanh.",
            "Những ví dụ minh họa rõ ràng và thuyết phục.",
        ],
        
        # Sách khoa học
        'science': [
            "Giải thích các khái niệm phức tạp một cách dễ hiểu.",
            "Mở rộng tầm nhìn về thế giới khoa học.",
            "Những phát hiện mới và thú vị.",
            "Viết rất chuyên nghiệp nhưng vẫn hấp dẫn.",
            "Nguồn thông tin đáng tin cậy và chi tiết.",
        ],
        
        # Sách du ký
        'travel': [
            "Như được trải nghiệm một cuộc phiêu lưu thực sự.",
            "Những mô tả sống động và chân thực.",
            "Khơi gợi niềm đam mê du lịch và khám phá.",
            "Cung cấp cái nhìn sâu sắc về các nền văn hóa.",
            "Những câu chuyện không thể rời mắt.",
        ]
    }

    # Chi tiết nhận xét cho từng mức đánh giá
    rating_comments = {
        5: [
            "Tuyệt vời! Một trong những cuốn sách hay nhất tôi từng đọc.",
            "Hoàn hảo từng chi tiết, không thể chê được.",
            "Một kiệt tác! Tôi sẽ đọc đi đọc lại nhiều lần.",
            "Vượt xa mọi kỳ vọng của tôi.",
            "Một trải nghiệm đọc sách tuyệt vời!"
        ],
        4: [
            "Rất hay, chỉ thiếu một chút để hoàn hảo.",
            "Đáng để đọc, có nhiều insights thú vị.",
            "Ấn tượng với phần lớn nội dung.",
            "Khuyến khích mọi người nên đọc.",
            "Một cuốn sách đáng giá thời gian."
        ],
        3: [
            "Ở mức trung bình, có cả ưu và nhược điểm.",
            "Một số phần rất hay, một số phần hơi nhạt.",
            "Đọc được nhưng chưa thực sự ấn tượng.",
            "Có thể cải thiện ở một số khía cạnh.",
            "Không tệ nhưng cũng chưa thực sự xuất sắc."
        ],
        2: [
            "Còn nhiều điểm chưa thuyết phục.",
            "Khá thất vọng so với mong đợi.",
            "Thiếu chiều sâu và sự thuyết phục.",
            "Cần nhiều cải thiện.",
            "Chưa đáp ứng được kỳ vọng."
        ],
        1: [
            "Hoàn toàn không đáp ứng được mong đợi.",
            "Sách này thực sự không đáng để đọc.",
            "Rất thất vọng với nội dung.",
            "Không thể hiểu tại sao sách lại được xuất bản.",
            "Lãng phí thời gian và tiền bạc."
        ]
    }

    # Lấy danh sách users và books
    users = User.query.all()
    books = Book.query.all()

    # Số lượng đánh giá muốn tạo
    review_count = 200

    # Seed dữ liệu
    for _ in range(review_count):
        user = random.choice(users)
        book = random.choice(books)
        
        # Xác định thể loại sách (giả định dựa trên tiêu đề)
        book_category = 'literary'
        if 'Kinh doanh' in book.title or 'Startup' in book.title:
            book_category = 'business'
        elif 'Khoa học' in book.title or 'Công nghệ' in book.title:
            book_category = 'science'
        elif 'Du ký' in book.title or 'Phiêu lưu' in book.title:
            book_category = 'travel'
        elif 'Phát triển' in book.title or 'Kỹ năng' in book.title:
            book_category = 'self_help'

        # Chọn ngẫu nhiên rating
        rating = random.randint(1, 5)
        
        # Chọn comment phù hợp với thể loại và rating
        comment = random.choice(review_comments.get(book_category, review_comments['literary']))
        
        # Thêm một số comment cụ thể theo rating
        if random.random() < 0.3:  # 30% sẽ dùng comment theo rating
            comment = random.choice(rating_comments[rating])

        # Kiểm tra đánh giá đã tồn tại chưa
        existing_review = BookReview.query.filter_by(
            user_id=user.id, 
            book_id=book.id
        ).first()

        if not existing_review:
            review = BookReview(
                user_id=user.id,
                book_id=book.id,
                rating=rating,
                comment=comment,
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 365))
            )
            db.session.add(review)

    # Commit changes
    db.session.commit()
    print(f"Đã thêm {review_count} đánh giá mẫu.")




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