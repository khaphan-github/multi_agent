# TODO: Get thong tin nguoi dung , get thong tin info, lay tong tin kill
from ..models.models import CustomContexModel


def get_context(user_id: str = None, chat_id: str = None, skill_id: str = None) -> CustomContexModel:
    # lấy thông tin ngữ cảnh
    return CustomContexModel(
        mo_ta='''
        Ứng phó với nhiệm vụ mới
        Giả sử giờ bạn sẽ là một nhân viên văn phòng vừa được giao phụ trách một dự án mới – dù bạn chưa có nhiều kinh nghiệm ở mảng này.
        Trong đó, bạn gặp phải tình huống như thế này:
        Sếp của bạn bất ngờ hỏi: "Bạn nghĩ mất bao lâu để hoàn thành dự án này?"
        Trong khi bạn mới chỉ đọc sơ qua tài liệu và chưa nắm rõ nguồn lực, khối lượng công việc, hay thời hạn cụ thể.
        🧠 Vậy, trong trường hợp này bạn sẽ làm thế nào?
      ''',
        history=[
            {"role": "user", "content": "Tôi tên gì?"},
            {"role": "assistant", "content": "Bạn tên là Nguyễn Văn A."},
            {"role": "user", "content": "Tôi đang ở đâu?"},
            {"role": "assistant", "content": "Bạn đang ở Thành phố Hồ Chí Minh."},
        ]
    )
