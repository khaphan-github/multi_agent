
# Agent Architecture

![Agent Architecture](image.png)

## User Input Examples

```python
# Example 1: Agent classification
user_input = "Chịu, tôi không nghỉ ra được bất cứ điều gì"

# Example 2: Switch to Suggestion Agent
# user_input = "Cho 1 gợi ý nhỏ"

# Example 3: Switch to Clarification Agent
# user_input = "Tôi chưa hiểu rõ nội dung tình huống"

# Example 4: Agent solution
# user_input = """
# Xem xét kỹ hơn các tài liệu dự án;
# Làm việc với các bên liên quan để nắm rõ yêu cầu và nguồn lực;
# Xác định các yếu tố rủi ro có thể ảnh hưởng đến tiến độ.
# Tôi dự kiến sẽ hoàn tất việc đánh giá sơ bộ trong vòng [1–2 ngày làm việc]
# """
```

## Supervisor

- **Supervisor**: Quản lý các agent, phân công nhiệm vụ, quản lý luồng thực thi, giúp việc giao tiếp giữa các agent.
- **Swarm**: Một agent có thể tương tác với các agent khác và ngược lại.

## Tasks

- [ ] Lấy thông tin nội bộ - API demo function call.
- [x] Lấy thông tin lịch sử chat của riêng người dùng.
- [x] Agent điều phối.
- [x] Agent tổng hợp.
- [x] Thêm lịch sử.
- [x] Agent hook - Lấy thông tin trace để lưu local.
- [x] Opensource tracing: [Langfuse](https://github.com/langfuse/langfuse)
  - [ ] Chưa lấy được content của agent cuối cùng trả về.
- [ ] Build vector database (ChromaDB persistent).
- [ ] Đánh giá mô hình.

- [ ] service rieng
- [ ] Lich xu thi tu xu (): nhu cau luu va dung, nhu cau xem thi get ra duoc:
      -> Gia phap :
         + Luu redis truoc (chuaw co thi goi db nap len).
         + [] Can co co che truy xuat.
         + [] Can co co che giai phong.
      -> Luong 9 se tuong tac tren redis thoi.
      -> job1: Sau x time se co job chay sync voi redis va luu vao db.
      -> job2: ..... sau bao lau khong thay hoat dong thi giao phong khoi redis.
      -> Data: To chuc data trong redis: 
         1. ds cac tinh huong: theu user (skill_id: co last update, info,....)

         2. (unique_id) key tro chuyen, time update cuoi cung, chi tiet noi dung. [{ id, ai, conten, time, ...}]

- [ ] Cung cap api truy van lich su chat.
- [ ] Hint de lam sau uu tien caii solution.


## Resources

- [OpenAI Agents SDK with Local LLM](https://medium.com/@shamim_ru/openai-agents-sdk-with-local-llm-461c77a5e7fb)

### Core Components

- **Agent Loop**: Lặp lại quá trình gọi tools và xử lý kết quả (15–22 lần như Copilot).
- **Handoff System**: Phân công nhiệm vụ tự động giữa các agent.
- **Guardrails**: Thực hiện các pipeline xác thực song song để làm sạch dữ liệu nhập và kiểm tra an toàn dữ liệu xuất.
- **Tracing**: Quan sát trực tuyến luồng thực thi và giám sát hiệu suất.

## OpenAI Swarm

- [Multi-Agent Orchestration with OpenAI Swarm](https://www.akira.ai/blog/multi-agent-orchestration-with-openai-swarm?utm_source=chatgpt.com)
- [OpenAI Swarm GitHub](https://github.com/openai/swarm)

## Summary

### OpenAI

- **Đánh giá tính năng**:
  1. Một agent có thể làm được gì:
     - Tools: Tool có sẵn, tools tự chế.
     - Subagent (HandOffs).
     - MCP connect.
     - Guardrail: Quy định input/output.
  2. Nhiều agent có thể làm được gì.

- **Triển khai**:
  1. Một service handle mọi thứ trong workflow.
  2. Nhiều agent phối hợp.

- **Use Case**: Đang cập nhật.

### LangGraph

- **Đánh giá tính năng**:
  1. Một agent có thể làm được gì.
  2. Nhiều agent có thể làm được gì.

- **Triển khai**: Đang cập nhật.
- **Use Case**: Đang cập nhật.

### CrawAI

- **Đánh giá tính năng**:
  1. Một agent có thể làm được gì.
  2. Nhiều agent có thể làm được gì.

- **Triển khai**: Đang cập nhật.
- **Use Case**: Đang cập nhật.

## Questions

1. How to scale out for multiple services?

## Notes

- **OpenAI Documentation**: [OpenAI Agents Python Models](https://openai.github.io/openai-agents-python/models/)

## Demo Content

- **Tổng quan về multi-agent OpenAI**:
  - **Assistant là gì?**: Same same.
  - **Agent là gì?**: Same same.

- **Các thành phần Agents OpenAI - Multi**:
  - **Agent**: Một con AI.
  - **HandOffs**: Một agent có thể bàn giao cho agent khác để xử lý.
  - **Context**: Thông tin liên quan đến người dùng và cuộc hội thoại.
  - **Tools**: Công cụ để agent tương tác với ngữ cảnh và dữ liệu thực tế (thời tiết, data từ service...).

- **Các khái niệm phụ**:
  - **Guardrails**.
  - **MCP**.
  - **Tracing**: Opensource, Admin OpenAI.

- **Mức độ ứng dụng - khai thác**:
  - Cơ bản.
  - Chưa dùng: Voice.

- **Demo Chat**: Đang cập nhật.
- **Ước tính chi phí**: Đang cập nhật.