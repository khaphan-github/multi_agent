# TODO: Get thong tin nguoi dung , get thong tin info, lay tong tin kill
from ..models.models import CustomContexModel

# Skill mapping dictionary
SKILL_MAP = {
    "skill_001": {
        "mo_ta": '''
        Ứng phó với nhiệm vụ mới
        Giả sử giờ bạn sẽ là một nhân viên văn phòng vừa được giao phụ trách một dự án mới – dù bạn chưa có nhiều kinh nghiệm ở mảng này.
        Trong đó, bạn gặp phải tình huống như thế này:
        Sếp của bạn bất ngờ hỏi: "Bạn nghĩ mất bao lâu để hoàn thành dự án này?"
        Trong khi bạn mới chỉ đọc sơ qua tài liệu và chưa nắm rõ nguồn lực, khối lượng công việc, hay thời hạn cụ thể.
        🧠 Vậy, trong trường hợp này bạn sẽ làm thế nào?
        '''
    },
    "skill_002": {
        "mo_ta": '''
        Kỹ năng giao tiếp hiệu quả
        Bạn đang tham gia một cuộc họp quan trọng với khách hàng. Đột nhiên khách hàng đặt câu hỏi về một vấn đề kỹ thuật mà bạn chưa nắm rõ.
        Bạn cần phải trả lời một cách thuyết phục và chuyên nghiệp mà không làm mất lòng tin của khách hàng.
        🧠 Bạn sẽ xử lý tình huống này như thế nào?
        '''
    },
    "skill_003": {
        "mo_ta": '''
        Quản lý thời gian và ưu tiên công việc
        Bạn có 5 nhiệm vụ cần hoàn thành trong tuần này, nhưng tất cả đều có deadline gấp.
        Đồng thời, sếp vừa giao thêm một công việc khẩn cấp cần hoàn thành ngay hôm nay.
        🧠 Bạn sẽ sắp xếp và ưu tiên các công việc như thế nào?
        '''
    }
}


def get_context(user_id: str = None, chat_id: str = None, skill_id: str = None) -> CustomContexModel:
    # lấy thông tin ngữ cảnh
    # Default to skill_001 if skill_id not found
    skill_info = SKILL_MAP.get(skill_id, SKILL_MAP["skill_001"])

    return CustomContexModel(
        mo_ta=skill_info["mo_ta"],
        history=[
            {"role": "user", "content": "Tôi tên gì?"},
            {"role": "assistant", "content": "Bạn tên là Nguyễn Văn A."},
        ]
    )
