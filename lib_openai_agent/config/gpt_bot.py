from config.main import config

# TODO: Move all this config to specific module
GPT_MODEL_CONFIG = [
    'gpt-3.5-turbo-0125',
    'gpt-4-1106-preview',
    'gpt-4-0125-preview',
    'gpt-4-turbo-preview',
    'gpt-4-turbo',
    'gpt-4o-mini',
    'gpt-4o',
]

GPT_BOTS_CONFIG = {
    # TODO: Need refactor code to config same same buddy web, mobile
    'learning_course': {
        'name': config.BUDDY_LEARNING_ASSISTANT_EDUZAA_FULLCOURSE_PREFIX,
        'temperature': 0.3,
        'metadata': {
            'version': '1',
            'tags': 'assistance_service',
        },
        'default_model': config.BUDDY_LEARNING_COURSE_MODEL_NAME,
        'desc': 'Model training khoa hoc theo kich ban',
        'sys_prompt': """
Bạn là Buddy AI, trợ lý học tập của Eduzaa, giúp sinh viên hiểu bài nhanh và áp dụng ngay. 
1. Nhiệm vụ của bạn bao gồm:
- Cung cấp thông tin chi tiết:
Hiểu và trả lời chính xác về nội dung khóa học, bao gồm: mục tiêu, lịch học, thời lượng, giảng viên, học phí, tài liệu, và yêu cầu đầu vào.
Nếu người dùng cung cấp thông tin không rõ ràng, bạn cần đặt câu hỏi để làm rõ yêu cầu trước khi trả lời.
2. Một khóa học có nhiều bài học chi tiết hơn, nhiệm vụ của bạn chỉ trả lời thông tin liên quan đến bài học chi tiết,
3. Đây là danh sách từng tài học nằm trong khóa: 
{phu_luc}

📌 **Nguyên tắc phản hồi:**  
1️⃣ **Ưu tiên trả lời sát nội dung bài học trước tiên** 📚  
Trả lời ngắn gọn, không dài dòng, không lan man, tối đa 50-80 từ (trong trường hợp thật cần thiết mới trả lời dài hơn, nếu có thể hãy ngắn gọn dí dỏm trong 1 vài câu ngắn), giọng điệu thân thiện, dí dỏm như bạn cùng lớp.   

2️⃣ **Nếu câu hỏi không liên quan đến bài học** → **Trả lời ngắn gọn, dí dỏm nhưng lưu ý người học là họ đang hỏi ngoài bài học**  
Bạn là Buddy, trợ lý AI giúp sinh viên học kỹ năng nhanh hơn vui hơn, dễ hơn. Bạn không phải trợ lý toàn năng. Do đó những câu hỏi ngoài các bài học và các chủ đề: [kỹ năng học tập, nghề nghiệp, kỹ năng mềm, công cụ số, đời sống sinh viên], hãy dí dỏm và khéo léo chuyển đề tài về các chủ đề trên.
        """
    },
}


'''
LEARNING_COURSE
Cau hinh cac prompt cho cac action cua bot learning course
kem voi learning_course o tren
'''


def generate_assistant_prompt(course_name, course_content_plain_text, custom_prompt=''):
    '''
        Noi dung build thong tin bo xung cua asisstance cua chi tiet bai hoc
    '''
    if not course_name or not course_content_plain_text:
        return "Nội dung bài học chưa được cập nhật"

    if len(custom_prompt) > 0:
        return custom_prompt.replace('{course_name}', course_name).replace('{course_content_plain_text}', course_content_plain_text)

    return f'''
Dưới đây là thông tin chi tiết của bài học:
1. Tiêu đề của bài học: {course_name}.
2. Nội dung: {course_content_plain_text}.
Bạn cần tôi hỗ trợ gì thêm không? 
Tôi có thể tạo bài tập, tóm tắt nội dung bài học này và giải thích thêm những ý bạn chưa nắm rõ.
Nếu cần hãy cho tôi biết nhé.
    '''


def generate_assistant_action_tom_tat_prompt(course_item_name, custom_prompt=''):
    if len(custom_prompt) > 0:
        return custom_prompt.replace('{course_item_name}', course_item_name)

    return f'''
Bạn hãy tóm tắt cho tôi bài học: {course_item_name}.
    '''


def generate_assistant_action_tom_tat_again_prompt(course_item_name, custom_prompt=''):
    if len(custom_prompt) > 0:
        return custom_prompt.replace('{course_item_name}', course_item_name)

    return f'''
Bạn hãy tóm tắt cho tôi bài học: {course_item_name}.
    '''


def generate_assistant_action_giai_thich_them_prompt(course_item_name, custom_prompt=''):
    if len(custom_prompt) > 0:
        return custom_prompt.replace('{course_item_name}', course_item_name)

    return f'''
Sinh viên muốn hiểu nhanh về nội dung bài học sau. Hãy cung cấp một lời giải thích, tóm tắt cực kỳ ngắn gọn, dạng danh sách, khoảng 50-80 từ. Lưu ý quan trọng: không dài dòng lan man, chỉ 50-80 từ.
Yêu cầu:
- Giải thích, tóm tắt ngắn gọn, đọc được nhanh.
- Tô đậm những chỗ quan trọng
Nội dung bài học: {course_item_name}
    '''


def generate_assistant_action_giai_thich_them_again_prompt(course_item_name, custom_prompt=''):
    if len(custom_prompt) > 0:
        return custom_prompt.replace('{course_item_name}', course_item_name)

    return f'''
Bạn hãy giải thích thêm cho tôi về bài học: {course_item_name}. Hãy cung cấp một lời giải thích thêm cực kỳ ngắn gọn, dạng danh sách, khoảng 50-80 từ, kèm theo ví dụ minh họa hoặc ứng dụng thực tế nếu có. Lưu ý quan trọng: không dài dòng lan man, chỉ 50-80 từ.
    '''


def generate_assistant_action_bai_tap_prompt(course_item_name, custom_prompt=''):
    if len(custom_prompt) > 0:
        return custom_prompt.replace('{course_item_name}', course_item_name)
    return f'''
        Bạn hãy tạo bài tập cho bài học: {course_item_name}
        1. Cho tôi danh sách bài tập cho khóa học này gồm 10 bài tập trắc nghiệp kèm đáp án và giải thích
        2. Luôn luôn trả về dữ liệu dưới dạng JSON với cấu trúc sau: 
            [  
                {
                "id": 1,
                "noi_dung": "\"Do yoga\" có nghĩa là gì?",
                "selection": [
                    {
                        "key": "a",
                        "noi_dung": "Chơi thể thao"
                    },
                    {
                        "key": "b",
                        "noi_dung": "Tập gym"
                    },
                    {
                        "key": "c",
                        "noi_dung": "Tập yoga"
                    },
                    {
                        "key": "d",
                        "noi_dung": "Chạy bộ 1"
                    }
                ],
                "dap_an": "c"
                },
            ]
        Các key trong json này được mô tả như sau:
            - id: Số thứ tự của câu hỏi
            - noi_dung: Nội dung câu hỏi
            - selection: Các lựa chọn cho câu hỏi: 
                + key: Mã lựa chọn
                + noi_dung: Nội dung lựa chọn
            - dap_an: Đáp án đúng của câu hỏi
'''


def user_query_builder(user_query, custom_prompt=''):
    if len(custom_prompt) > 0:
        return custom_prompt.replace('{user_query}', user_query)
    return f'''
       {user_query}
    '''


# TODO: Update config for learning course TRA VE SJON
# user_query: dtruong hop user quest prompt
LEARNING_COURSE_ACTION_KEY_CONFIG = {
    'bai_tap': {
        'response_type': 'json',
        'new_action_prompt': generate_assistant_action_bai_tap_prompt,
        'action_prompt': generate_assistant_action_bai_tap_prompt,
        'display_prompt': '''Tạo trắc nghiệm''',
        'assistant_prompt': generate_assistant_prompt,
    },
    'tom_tat': {
        'response_type': 'text',
        'action_prompt': generate_assistant_action_tom_tat_again_prompt,
        'new_action_prompt': generate_assistant_action_tom_tat_prompt,
        'display_prompt': '''Giúp tôi tóm tắt nội dung của bài học này''',
        'assistant_prompt': generate_assistant_prompt,
    },
    'giai_thich_them': {
        'response_type': 'text',
        'action_prompt': generate_assistant_action_giai_thich_them_again_prompt,
        'new_action_prompt': generate_assistant_action_giai_thich_them_prompt,
        'display_prompt': '''Hãy giúp tôi giải thích thêm nội dung của bài học này''',
        'assistant_prompt': generate_assistant_prompt,
    },
    'user_query': {
        'response_type': 'text',
        'action_prompt': user_query_builder,
        'new_action_prompt': user_query_builder,
        'display_prompt': '''''',
        'assistant_prompt': generate_assistant_prompt,
    },
}
