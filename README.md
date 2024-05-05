
# Web Phân Tích Bóng Đá Sử Dụng Học Sâu Và Thị Giác Máy Tính

## Đồ án cuối kì - Nhập môn học máy - 21KHDL1
## VNU - HCMUS

## Thông tin nhóm
| Name              | ID       |
|-------------------|----------|
| Trần Nguyên Huân  | 21127050 |
| Doãn Anh Khoa   | 21127076 |
| Nguyễn Minh Quân   | 21127143 |
| Nguyễn Phát Đạt   | 21127240 |

## Mục tiêu của đồ án
Tạo ra một ứng dụng web phân tích bóng đá tự động, và cung cấp thông tin hữu ích giúp đưa ra quyết định trong phân tích chiến lược.

## Tiến độ của dự án:
Tận dụng streamlit để phát triển ứng dụng web cho phát hiện cầu thủ, thủ môn mỗi đội, trọng tài, theo dõi quả bóng, và trực quan bằng bản đồ chiến thuật.

## Các chức năng chính
1. Nhận diện cầu thủ, trọng tài và bóng.
2. Dự đoán đội cầu thủ.
3. Ước tính vị trí của cầu thủ và quả bóng trên bản đồ chiến thuật.
4. Theo dõi quả bóng.

## Cách sử dụng
Mô tả các bước:
1. Tải lên một video để phân tích, sử dụng nút `Browse Files` bên dưới.
2. Nhập tên đội tương ứng với video đã tải lên vào các trường văn bản.
3. Chọn một khung hình (thứ tự của frame) mà ở đó cầu thủ và thủ môn từ cả hai đội có thể được nhận diện.
4. Chọn màu của cầu thủ và thủ môn của mỗi đội tương ứng với khung nhận diện ở trên mà bạn cho là phù hợp nhất (bạn có thể tùy chình lại màu đội ở các ô bên dưới nếu chưa hài lòng).
5. Chuyển đến tab `Tùy chỉnh Tham Số và Nhận diện`, điều chỉnh các tham số và chọn các tùy chọn chú thích. (Tham số mặc định được đề xuất)
6. Chạy Phát hiện!
7. Nếu chọn tùy chọn `Lưu kết quả`, video đã lưu có thể được tìm thấy trong thư mục `outputs`

## Flow Chart của dự án
Hành trình từ lúc tải lên video đầu vào và các chức năng khác nhau được minh họa trong sơ đồ quy trình (`Flow Chart`) bên dưới.

![Flow Chart](https://raw.githubusercontent.com/knightstark7/FootBall-Analytics-with-Deep-Learning-and-Computer-Vision/main/Flow%20Chart.png?token=GHSAT0AAAAAACRBG4ZFVO7PT4YOFJF4KMOAZRXF4WA)