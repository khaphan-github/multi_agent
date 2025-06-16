# Tài liệu thư viện llm_proxy

Thư viện `llm_proxy` hoạt động như một trung gian để kết nối với các dịch vụ LLM bên ngoài như OpenAI, Gemini và DeepSeek. Thư viện cung cấp logic nghiệp vụ để quản lý ngân sách, giới hạn yêu cầu và hỗ trợ cả tương tác trò chuyện thông thường và trò chuyện với trợ lý.

---

## Cấu trúc thư mục

### 1. `shared`
Chứa các tiện ích và triển khai dùng chung trong thư viện:
- **`history`**: Quản lý lịch sử tin nhắn bằng Redis.
  - `message_history_redis_impl.py`: Triển khai lưu trữ và truy xuất tin nhắn trong Redis.
  - `env.py`: Đọc cấu hình liên quan đến Redis từ các biến môi trường.

### 2. `openai`
Xử lý tích hợp cụ thể cho OpenAI:
- `openai_service.py`: Triển khai các chức năng trò chuyện và streaming của OpenAI.
- `openai_config.py`: Định nghĩa cấu hình cho các dịch vụ OpenAI.
- `env.py`: Đọc cấu hình cụ thể của OpenAI từ các biến môi trường.

### 3. `model`
Định nghĩa các mô hình cốt lõi và lớp cơ sở:
- `llm_config.py`: Lớp cấu hình cơ bản cho các dịch vụ LLM.
- `llm_budget.py`: Quản lý các ràng buộc ngân sách cho việc sử dụng LLM.
- `llm_service_base.py`: Lớp cơ sở cho các dịch vụ LLM, cung cấp các chức năng chung như kiểm tra ngân sách.

### 4. `deepseek`
Xử lý tích hợp cụ thể cho DeepSeek:
- `deepseek_config.py`: Định nghĩa cấu hình cho các dịch vụ DeepSeek.
- `env.py`: Đọc cấu hình cụ thể của DeepSeek từ các biến môi trường.

---

## Các tính năng chính

### 1. Quản lý ngân sách
- Đảm bảo việc sử dụng LLM nằm trong giới hạn ngân sách được định trước.
- Triển khai theo dõi ngân sách dựa trên token.

### 2. Lịch sử tin nhắn
- Lưu trữ và truy xuất lịch sử trò chuyện bằng Redis.
- Hỗ trợ các trình xử lý tin nhắn tùy chỉnh để linh hoạt.

### 3. Hỗ trợ đa LLM
- Cung cấp giao diện thống nhất để tương tác với nhiều dịch vụ LLM (ví dụ: OpenAI, DeepSeek).

### 4. Trò chuyện và Streaming
- Hỗ trợ cả tương tác trò chuyện đồng bộ và bất đồng bộ.
- Cho phép phản hồi streaming cho các ứng dụng thời gian thực.

---

## Hướng dẫn sử dụng

### 1. Cấu hình
Thiết lập các biến môi trường trong tệp `.env`:
```env
# Cấu hình Redis
LLM_PROXY_OPEN_AI_IOREDIS_HOST=localhost
LLM_PROXY_OPEN_AI_IOREDIS_PORT=6379
LLM_PROXY_OPEN_AI_IOREDIS_DB_INDEX=0
LLM_PROXY_OPEN_AI_IOREDIS_KEY_PREFIX=llm_proxy

# Cấu hình OpenAI
LLM_PROXY_OPEN_AI_DEFAULT_OPEN_API_KEY=your_openai_api_key
```

### 2. Khởi tạo dịch vụ
```python
from libs.llm_proxy.openai.openai_service import OpenAIService
from libs.llm_proxy.openai.openai_config import OpenAILLMConfig

config = OpenAILLMConfig(api_key="your_openai_api_key", enable=True, use_message=True)
service = OpenAIService(config=config)

response = await service.chat("Xin chào, tôi có thể giúp gì cho bạn?")
print(response)
```

### 3. Sử dụng lịch sử tin nhắn
Mặc định, dữ liệu lịch sử tin nhắn sẽ được lưu trữ trong Redis thông qua lớp `LLMMessageHandlerImpl`. Nếu bạn muốn tùy chỉnh để lưu trữ ở nơi khác (ví dụ: cơ sở dữ liệu khác hoặc tệp), bạn cần triển khai lại lớp `LLMMessageHandler` và truyền nó vào khi OpenAIService khi khởi tạo dịch vụ.

#### Lưu trữ mặc định với Redis
```python
from libs.llm_proxy.shared.history.message_history_redis_impl import LLMMessageHandlerImpl

handler = LLMMessageHandlerImpl()
handler.push_message(message)  # Lưu tin nhắn vào Redis
```

#### Tùy chỉnh lưu trữ
Để tùy chỉnh lưu trữ, hãy triển khai lại lớp `LLMMessageHandler`:
```python
from libs.llm_proxy.model.llm_message import LLMMessageHandler

class CustomMessageHandler(LLMMessageHandler):
    def push_message(self, message):
        # Triển khai logic lưu trữ tùy chỉnh
        print(f"Lưu tin nhắn: {message}")

# Sử dụng handler tùy chỉnh
custom_handler = CustomMessageHandler()
service = OpenAIService(config=config, message_handler=custom_handler)
```

Khi sử dụng handler tùy chỉnh, các tin nhắn sẽ được lưu trữ theo logic bạn định nghĩa thay vì Redis.

#### Đọc dữ liệu từ Redis
Ngoài việc sử dụng module này để lưu trữ tin nhắn, bạn cũng có thể đọc dữ liệu từ Redis theo logic lưu trữ. Dữ liệu được lưu trữ dưới dạng danh sách (`lrange`) và các mục chi tiết trong hash (`hget`).

Ví dụ:
```python
from redis import Redis

redis_client = Redis(host="localhost", port=6379, db=0)
key_prefix = "llm_proxy"
chat_session_key = f"{key_prefix}:llm_proxy_history_key_list"

# Lấy danh sách các khóa tin nhắn
message_keys = redis_client.lrange(chat_session_key, 0, -1)

# Lấy chi tiết từng tin nhắn
for message_key in message_keys:
    message_data = redis_client.hgetall(message_key)
    print(f"Tin nhắn: {message_data}")
```

Logic này cho phép bạn truy xuất lịch sử tin nhắn đã lưu trữ trong Redis để sử dụng hoặc phân tích thêm.

---

## Hướng dẫn bảo trì

1. **Đồng nhất mã nguồn**:
   - Tuân theo cấu trúc thư mục và quy tắc đặt tên hiện có.
   - Sử dụng gợi ý kiểu dữ liệu và docstring cho tất cả các phương thức.

3. **Tài liệu**:
   - Cập nhật tài liệu này mỗi khi thêm tính năng hoặc module mới.
   - Cung cấp ví dụ cho các chức năng mới.

4. **Biến môi trường**:
   - Tài liệu hóa bất kỳ biến môi trường mới nào trong các tệp `env.py` tương ứng.
---

## Các trường hợp sử dụng ví dụ
### 1. Trò chuyện với ngân sách giới hạn
```python
from libs.llm_proxy.openai.openai_service import OpenAIService
from libs.llm_proxy.openai.openai_config import OpenAILLMConfig
from libs.llm_proxy.model.llm_budget import LLMBudget

budget = LLMBudget(max_tokens=1000) 
config = OpenAILLMConfig()
service = OpenAIService(config=config)

response = await service.chat("Thời tiết hôm nay thế nào?")

```

### 2. Trò chuyện streaming
```python
async for chunk in service.chat_stream("Kể tôi nghe một câu chuyện."):
    print(chunk, end="")
```

---

## Các cải tiến trong tương lai
- Thêm hỗ trợ cho nhiều nhà cung cấp LLM hơn (ví dụ: Gemini).
- Triển khai các cơ chế caching nâng cao cho lịch sử tin nhắn.
- Cung cấp bảng điều khiển web để giám sát việc sử dụng và ngân sách.

## Cach dung tool assistant
```python
# https://platform.openai.com/docs/assistants/tools
def get_weather_today_assistant_func(location):
    # Call api thoi tiet
    return f'Thoi tiet hom nay bla bla'

LLM_OPEN_AI_BUDDY_WEB_CONFIG = OpenAILLMConfig(
    ...
    tools=[
        OpenAIFileSearch(enable=True),
        OpenAICodeInterpreter(enable=False),
        OpenAIFunctionCall(
            enable=False,
            name="get_weather_today",
            description="Lay thong tin thoi tiet hom nay",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Dia diem can lay thong tin thoi tiet"
                    }
                },
                "required": ["location"]
            },
            instance_function=get_weather_today_assistant_func
        )
    ]
)
```