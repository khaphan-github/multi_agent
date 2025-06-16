# Bao quát hệ thống
- Dịch vụ multi agent sẽ setup riêng.
- Chủ động kết nối: database, redis.
- Cung cấp các API để tương tác với hệ thống khác.

# Flow người dùng tương tác:
1. Flow chat giải quyết vấn đề (Thông qua agent điều phối):
- Chat -> Agent điều phối -> [Ds các agent] => Agent tổng hợp -> Out. (loại content final, defautl.)

2. Flow gợi ý: (Không thông qua agent điều phối)
- Phản hồi thành công - gọi chat gợi ý -> Agent gợi ý -> Out. Array gợi ý[]

# Xử lý ngữ cảnh: (Thành phần chung - nên viết để có thể tái sử dụng.)
1. Nạp ngữ cảnh:
  - Input: chat_id, skill_id, user_id
  - Logic: Lấy thông tin:{ user, history, skill }
        + User: Lấy thông tin theo contact id (cache lại redis có TTL ngắn (5 phút / 20 phút))
        + Skill: Lấy thông tin theo skill_id (cache lại redis - TTL ngắn (5 phút / 20 phút))
        + History: 
            + Trường hợp chat mới: (Không có trong redis & db) => []
            + Trường hợp chat đã có lịch sử:
                - Nếu chưa có trong redis -> lấy từ db (full) -> nạp redis
                - Nếu đã có trong redis -> lấy từ redis (full).
  - Output: { user, history, skill }

2. Lưu ngữ cảnh: (Luồng này không ảnh hưởng đến stream - có thể chạy async)
  - Input: { chat_content, chat_id, metadata,...}
  - Logic: Lưu thông tin vào redis (Luôn luôn lưu vào redis)
  - Output: { success }

3. Giải phóng/Lưu trữ:
  - Giải phóng: (Làm trong redis - khi data không còn được sử dụng)
      - Sau khoản thời gian x time - dữ liệu trên redis sẽ bị xóa bởi job.
        + Kiểm tra đã đồng bộ xuống db chưa (Kiểm tra như thế nào ??????)
          - trường hợp chưa - sẽ không xóa.
          - trường hợp rồi - sẽ xóa.
  - Lưu trữ:
      - Bot đồng bộ lịch sử - phục vụ lưu trữ: 
        + Sau x time sẽ chạy job để đồng bộ với db - [KHÔNG XÓA REDIS]. (theo chat id - lastupdatedtime)

# Cấu trúc lưu trữ:
1. redis
   1.1: Skill (nghiệp vụ riêng) - prefix:skill:id -> lưu info
   1.2. User (nghiệp vụ chung) - prefix:user:id -> lưu info
   1.3. Chat (nghiệp vụ chung):
       + Quản lý nội dung chat: prefix:chat:chat_id -> [{ author, content, created_time, metadata, ...}]
2. database
   table: chat_history_sync (Lưu trạng thái sync và thời gian cuối cùng sync.)
    column:
      - chat_id: unique_id (generate từ code)
      - timeupdated: number (get number).
      - status: LASTEST | ERROR | SYNCING
      - metadata: json (lưu thông tin về trạng thái đồng bộ)

   table: chat_history_skill_up
   column:
    - chat_id: unique_id (generate từ code)
    - message_id: unique_id (generate từ code)
    - user_type: string (AI|USER|AGENT|SYSSTEM bla bla - để mở rộng)
    - content: text
    - previous_message_id: ()
    - metadata: json (muốn lưu gì cũng được - chứa thông tin chat)
    - timecreated: datetime
    - timeupdated: datetime

# Cung cấp dữ liệu lịch sử.
  - API: get danh sách lịch sử chat theo truy vấn (metadata) -> mục đích mở rộng - không bị theo nghiệp vụ. Luồng get lịch sử trong redis.

# Tạo một cụm multi agent khác:
- Tạo một module với các thành phần giống với cái hiện có - thay đổi logic bên trong.
- Thêm route.

