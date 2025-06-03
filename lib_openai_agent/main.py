import asyncio
from modules.eduzaa_skill_up_agent_cluster.tools import *
from modules.eduzaa_skill_up_agent_cluster.models import *
from modules.eduzaa_skill_up_agent_cluster.agents import *
from modules.eduzaa_skill_up_agent_cluster.runner import run_skillup_conversation
from modules.eduzaa_skill_up_agent_cluster.contexts.context import get_context

# region get thong tin bo xugn cho model
# https://openai.github.io/openai-agents-python/tools/


async def main():
    # draw_graph(triage_agent, filename="agent_graph")
    # draw_graph(triage_agent).view()
    context = get_context()
    # user_input = 'Toi ten gi'
    # user_input = 'Toi danng o dau'
    # user_input = "Chịu, tôi không nghỉ ra được bất cứ điều gì"  # => Agetn phan loai

    user_input = "Cho 1 gợi ý nhỏ"  # => Chuyen sang Agent Gợi ý

    # => Chuyen sang Agent Làm rõ tình huống
    # user_input = "Tôi chưa hiểu rõ nội dung tình huống"

    # Agent solution
    # user_input = """
    # Xem xét kỹ hơn các tài liệu dự án;
    # Làm việc với các bên liên quan để nắm rõ yêu cầu và nguồn lực;
    # Xác định các yếu tố rủi ro có thể ảnh hưởng đến tiến độ.
    # Tôi dự kiến sẽ hoàn tất việc đánh giá sơ bộ trong vòng [1–2 ngày làm việc]s
    # """
    async for response in run_skillup_conversation(user_input, context):
        print(response, end='', flush=True)
if __name__ == "__main__":
    asyncio.run(main())
