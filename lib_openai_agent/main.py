import asyncio
from modules.eduzaa_skill_up_agent_cluster.service_manager import ServiceManager
from modules.eduzaa_skill_up_agent_cluster.tools import *
from modules.eduzaa_skill_up_agent_cluster.models.models import *
from modules.eduzaa_skill_up_agent_cluster.agents import *
from modules.eduzaa_skill_up_agent_cluster.runner.main_agent_runner import run_skillup_conversation
from modules.eduzaa_skill_up_agent_cluster.contexts.context import get_context

# region get thong tin bo xugn cho model
# https://openai.github.io/openai-agents-python/tools/


async def main():
    # draw_graph(triage_agent, filename="agent_graph")
    # draw_graph(triage_agent).view()
    print("=== EduZaa Skill Up Agent ===")
    print("Type 'exit', 'quit', or 'bye' to end the conversation\n")

    # Predefined test inputs for automatic testing
    test_inputs = [
        "Chịu, tôi không nghỉ ra được bất cứ điều gì",  # => Agent phan loai
        "Cho 1 gợi ý nhỏ",  # => Chuyen sang Agent Gợi ý
        # => Chuyen sang Agent Làm rõ tình huống
        "Tôi chưa hiểu rõ nội dung tình huống",
        """Xem xét kỹ hơn các tài liệu dự án;
Làm việc với các bên liên quan để nắm rõ yêu cầu và nguồn lực;
Xác định các yếu tố rủi ro có thể ảnh hưởng đến tiến độ.
Tôi dự kiến sẽ hoàn tất việc đánh giá sơ bộ trong vòng [1–2 ngày làm việc]"""  # Agent solution
    ]

    test_index = 0
    auto_test_mode = True

    while True:
        try:
            # Get user input - either automatic or manual
            if auto_test_mode and test_index < len(test_inputs):
                user_input = test_inputs[test_index]
                print(
                    f"\nAuto Input [{test_index + 1}/{len(test_inputs)}]: {user_input}")
                test_index += 1

                # Switch to manual mode after all test inputs
                if test_index >= len(test_inputs):
                    auto_test_mode = False
            else:
                user_input = input("\nYou: ").strip()

            # Check for exit conditions
            if user_input.lower() in ['exit', 'quit', 'bye', '']:
                print("Goodbye!")
                break

            print("Agent: ", end='', flush=True)
            stream = await ServiceManager().run(
                user_id="user123",
                chat_id="chat456",
                skill_id="skill789",
                messsage=user_input
            )
            async for response in stream:
                print(response, end='', flush=True)
            print()  # Add newline after response
            print()  # Add newline after response

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")
if __name__ == "__main__":
    asyncio.run(main())
