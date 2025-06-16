# Hien trang openai:
## loai
- Chat
- Chat Assistant

## Method data cHAT VOI ASISTATN:
- Complete
- Stream 

## TODO List for Functions
1. **Chat**
   - [x] Implement chat functionality.
   - [x] Save chat history.

2. **Assistant Threads**
   - [x] Allow maintaining context with threads.
   - [x] CRUD operations for threads:
   - [ ] Auto-delete threads via Redis (default: 1 day). (chua lam)

3. **Permissions**
   - [x] Restrict to read-only access.
   - [x] Require admin to create assistants on OpenAI and provide `assistant_id`.

4. **Usage Limits**
   - [x] Track usage based on tokens.
   - [ ] Implement daily max token limit.  (chua lam)

5. **File Utilities**
   - [x] CRUD operations for files:

6. **Vector Operations**
   - [x] CRUD operations for vectors:
   - [x] Add/Remove/Update/List files in vectors:

7. **Function Calls**
   - [x] Add configurable function calls.
   - [x] Define implementation guidelines for function calls.

8. **Fine-tuning**
   - [ ] Add fine-tuning support.  (chua lam)
---

# Han che:
- [ ] Chua co co che remove thread => rac thread tren tai khoan openai.
   
# Module structure
- constants.py
- openai_assistant_proxy.py:
  + Chua cac fucntion module co the dung:
    - Chua cac function goi openai.
- utils: Cac tien ich: stream, event pooling.
- thread.py: xu ly create update thread
- shared_tool: Chua cac function cua asstant de no goi, co the dung chung - khong chua cac nghiep vu rieng, cac func co the gom: Lay thoi gian, Thoi tiet, Tin tuc, Web search,...

# New feature:
- https://cookbook.openai.com/