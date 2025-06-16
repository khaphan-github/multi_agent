# Module Giới Hạn Tỷ Lệ Truy Cập (Rate Limiting)

## Tổng Quan

Module Giới Hạn Tỷ Lệ Truy Cập là một thành phần bảo mật được thiết kế để bảo vệ Chat Assistant API khỏi việc lạm dụng, các cuộc tấn công từ chối dịch vụ và sử dụng quá mức. Nó giám sát các yêu cầu đến, theo dõi mẫu sử dụng theo địa chỉ IP và tạm thời chặn các máy khách vượt quá ngưỡng yêu cầu đã cấu hình.

## Tính Năng

- Theo dõi và chặn dựa trên IP
- Giới hạn tỷ lệ truy cập và thời gian chặn có thể cấu hình
- Lưu trữ dựa trên Redis cho các triển khai phân tán
- Tích hợp middleware FastAPI
- Cấu hình dựa trên biến môi trường

## Kiến Trúc

Module sử dụng Redis làm nơi lưu trữ để theo dõi tỷ lệ yêu cầu và các IP bị chặn, cho phép duy trì và hoạt động trên nhiều phiên bản API phân tán.

```
┌─────────────┐     ┌────────────────────────┐     ┌──────────────┐
│  Yêu cầu    │     │RateLimitBlockMiddleware│     │  Trình xử lý │
│  đến        ├────►│ - Kiểm tra trạng thái IP├────►│   FastAPI    │
└─────────────┘     └────────────┬───────────┘     └──────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐     ┌──────────────┐
                    │    RateLimiter         │     │  Cơ sở dữ    │
                    │  - Theo dõi yêu cầu    ├────►│  liệu Redis  │
                    │  - Chặn các IP         │     │              │
                    └────────────────────────┘     └──────────────┘
```

## Các Thành Phần

### 1. RateLimitBlockMiddleware

Middleware FastAPI chặn các yêu cầu đến, kiểm tra xem IP của máy khách có bị chặn không và trả về phản hồi 403 nếu cần thiết.

### 2. RateLimiter

Thành phần logic nghiệp vụ cốt lõi:

- Ghi lại các lần thử yêu cầu từ địa chỉ IP
- Thực hiện logic chặn khi vượt quá ngưỡng
- Kiểm tra trạng thái IP đối chiếu với dữ liệu Redis

### 3. Cơ Sở Hạ Tầng Redis

Sử dụng mẫu Singleton để duy trì một kết nối Redis duy nhất cho việc theo dõi giới hạn tỷ lệ truy cập.

### 4. Cấu Hình Môi Trường

Quản lý tập trung các biến môi trường cho tất cả các tham số giới hạn tỷ lệ truy cập.

## Logic Nghiệp Vụ

Quá trình giới hạn tỷ lệ truy cập diễn ra như sau:

1. **Chặn Yêu Cầu**: Mỗi yêu cầu đến được chặn lại bởi middleware.
2. **Xác Thực IP**: IP của máy khách được kiểm tra đối chiếu với danh sách chặn.
3. **Xử Lý Yêu Cầu**:
   - Nếu IP bị chặn, phản hồi 403 Forbidden được trả về.
   - Nếu IP không bị chặn, yêu cầu được tiếp tục đến trình xử lý API.
4. **Theo Dõi Tỷ Lệ**: Bộ giới hạn tỷ lệ theo dõi tần suất yêu cầu theo IP.
5. **Logic Chặn**: Nếu một IP vượt quá ngưỡng đã cấu hình:
   - IP được thêm vào danh sách chặn trong Redis
   - Việc chặn tồn tại trong thời gian chặn đã cấu hình
   - Tất cả các yêu cầu tiếp theo từ IP đó bị từ chối cho đến khi hết thời gian chặn

## Cấu Hình

Module được cấu hình thông qua các biến môi trường:

| Biến                          | Mô Tả                                          | Mặc Định    |
| ----------------------------- | ---------------------------------------------- | ----------- |
| IOREDIS_RATE_LIMIT_HOST       | Máy chủ Redis                                  | localhost   |
| IOREDIS_RATE_LIMIT_PORT       | Cổng Redis                                     | 6379        |
| IOREDIS_RATE_LIMIT_DB_INDEX   | Chỉ mục DB Redis                               | 0           |
| IOREDIS_RATE_LIMIT_KEY_PREFIX | Tiền tố khóa Redis                             | rate_limit: |
| RATE_LIMIT_MAX_ATTEMPTS       | Số lần thử tối đa trước khi chặn               | 5           |
| RATE_LIMIT_BLOCK_TIME         | Thời gian chặn tính bằng giây                  | 60          |
| RATE_LIMIT_SPAM_EXP           | Thời gian hết hạn theo dõi spam tính bằng giây | 3600        |

## Ví Dụ Sử Dụng

Để áp dụng giới hạn tỷ lệ truy cập cho ứng dụng FastAPI của bạn:

```python
from fastapi import FastAPI
from libs.rate_limit.rate_limit_block_middleware import RateLimitBlockMiddleware

app = FastAPI()

# Thêm middleware giới hạn tỷ lệ truy cập
app.add_middleware(RateLimitBlockMiddleware)

# Các route API của bạn bên dưới
@app.get("/api/endpoint")
async def example_endpoint():
    return {"message": "Endpoint này được giới hạn tỷ lệ truy cập"}
```

## Chi Tiết Triển Khai

Bộ giới hạn tỷ lệ truy cập giám sát tỷ lệ yêu cầu theo địa chỉ IP. Khi một IP thực hiện quá nhiều yêu cầu trong một khoảng thời gian ngắn:

1. IP được đánh dấu là bị chặn trong Redis
2. Bộ hẹn giờ hết hạn chặn được thiết lập
3. Tất cả các yêu cầu từ IP đó bị từ chối với mã 403 Forbidden cho đến khi hết thời gian chặn
4. Đường dẫn yêu cầu được theo dõi trong phản hồi lỗi để giám sát

## Sử Dụng Decorator Limiter

Module cũng cung cấp decorator `limiter.limit()` để giới hạn tỷ lệ truy cập cho các endpoint cụ thể:

```python
"""
File này chịu trách nhiệm định tuyến các yêu cầu đến tới các endpoint tương ứng.

Giới Hạn Tỷ Lệ Truy Cập:
- Module bao gồm chức năng giới hạn tỷ lệ truy cập thông qua 'limiter' đã nhập.
- Các route có thể được bảo vệ với giới hạn tỷ lệ bằng decorator @limiter.limit.
- Giới hạn tỷ lệ được chỉ định theo định dạng "{số lượng}/{khoảng_thời_gian}" (ví dụ: "1/second").
- Khi khách hàng vượt quá giới hạn tỷ lệ, phản hồi 429 Too Many Requests được trả về.
"""

@api_router.get("/ping", response_class=JSONResponse)
# Giới hạn endpoint này đến 1 yêu cầu mỗi giây cho mỗi IP
@limiter.limit("1/second")
async def ping(
    request: Request,
):
    """
    Endpoint kiểm tra sức khỏe để xác minh API đang hoạt động.
    Giới hạn tỷ lệ truy cập là 1 yêu cầu mỗi giây cho mỗi địa chỉ IP.
    """
    return {
        "message": "Ứng dụng đang chạy!",
        "status": "thành công",
    }
```
