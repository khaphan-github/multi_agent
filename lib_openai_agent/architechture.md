# Bao quat he thong
- Dich vu multi agent se setup rieng.
- Chu dong ket noi: database, redis.
- Cung cap cac API de tuong tac voi he thong khac.

# Flow nguoi dung tuong tac:
1. Flow chat giai quyet van de (Thong qua agent dieu phoi):
- Chat -> Agent dieu phoi -> [Ds cac agent] => Agent tong hop -> Out. (loai content final, defautl.)

2. Flow goi y: (Khong thong qua agent dieu phoi)
- Phan hoi thanh cong - goi chat goi y -> Agent goi y -> Out. Array goi y[]

# Xu ly ngu canh: (Thanh phan chung - nen viet de co the tai su dung.)
1. Nap ngu canh:
  - Input: chat_id, skill_id, user_id
  - Logic: Lay thong tin:{ user, history, skill }
        + User: Lay thong tin theo contact id (cache lai redis  co TTL ngan (5 phut / 20 phut))
        + Skill: Lay thong tin theo skill_id (cache lai redis - TTL ngan (5 phut / 20 phut))
        + History: 
            + Truong hop chat moi: (Khong co trong redis & db) => []
            + Truong hop chat da co lich su:
                - Neu chua co trong redis -> lay tu db (full) -> nap redis
                - Neu da co trong redis -> lay tu redis (full).
  - Output: { user, history, skill }

2. Luu ngu canh: (Luong nay khogn anh huong den stream - co the chay async)
  - Input: { chat_content, chat_id, metadata,...}
  - Logic: Luu thong tin vao redis (Luon luon luu vao redis)
  - Output: { success }

3. Giai phong/Luu tru:
  - Giai phong: (Lam trong redis - khi data khong con duoc su dung)
      - Sau khoan thoi gian x time - du lieu tren redis se bi xoa boi job.
        + Kiem tra da dong bo xuong db chua (Kiem tra ntn ??????)
          - truong hop chua - se khong xoa.
          - truong hop roi - se xoa.
  - Luu tru:
      - Bot dong bo lich su - phuc vu luu tru: 
        + Sau x time se chay job de dong bo voi db - [KHONG XOA REDIS]. (theo chat id - lastupdatedtime)

# Cau truc luu tru:
1. redis
   1.1: Skill (nghiep vu rieng) - prefix:skill:id -> luu info
   1.2. User (nghiep vu chung) - prefix:user:id -> luu info
   1.3. Chat (nghiep vu chung):
       + Quan ly trang thai dong bo: prefix:sync_status:chat_id -> { last_updated: 170923871823000 }
       + Quan ly noi dung chat: prefix:chat:chat_id -> [{ author, content, created_time, metadata, ...}]
2. database
   table: chat_history_sync
    column:
      - chat_id: unique_id (generate tu code)
      - timeupdated: number (get number).
      - status: LASTEST | ERROR | SYNCING
      - metadata: json (luu thong tin ve trang thai dong bo)

   table: chat_history_skill_up
   column:
    - id: unique_id (generate tu code)
    - user_type: string (AI|USER|AGENT|SYSSTEM bla bal - de mo trong)
    - content: text
    - previous_message_id: ()
    - metadata: json (muon luu gi cung duoc - chua thong tin chat)
    - timecreated: datetime
    - timeupdated: datetime
# Cung cap du lieu lich su.
  - API: get danh sach lich su chat theo truy van (metadata) -> muc dich mo rong - khong bi theo nghiep vu. (Khong cache - hoac cache voi key khac voi logic xu lu context)

# Tao mot cum multi agent khac:
- Tao mot module voi cacs thanh phan giong voi cai hien co - thay doi logic ben trong.
- Them route.

