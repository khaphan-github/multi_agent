import asyncio
import os
from datetime import datetime
from modules.eduzaa_skill_up_agent_cluster.service_manager import ServiceManager
from modules.eduzaa_skill_up_agent_cluster.tools import *
from modules.eduzaa_skill_up_agent_cluster.models.models import *
from modules.eduzaa_skill_up_agent_cluster.agents import *
from modules.eduzaa_skill_up_agent_cluster.runner.main_agent_runner import run_skillup_conversation
from modules.eduzaa_skill_up_agent_cluster.contexts.context import get_context, SKILL_MAP

# region get thong tin bo xugn cho model
# https://openai.github.io/openai-agents-python/tools/

# When error:
# export OPENAI_API_KEY=<your_api_key>

# Predefined test inputs for automatic testing
KICH_BAN_CHAY = [
    "Cho 1 gợi ý nhỏ",  # => Chuyen sang Agent Gợi ý
    "Tôi chưa hiểu rõ nội dung tình huống",  # => Agent lam ro tinh huong
    "Chịu, tôi không nghỉ ra được bất cứ điều gì",  # => Agent Emotion
    """
    Xem xét kỹ hơn các tài liệu dự án;
    Làm việc với các bên liên quan để nắm rõ yêu cầu và nguồn lực;
    Xác định các yếu tố rủi ro có thể ảnh hưởng đến tiến độ.
    Tôi dự kiến sẽ hoàn tất việc đánh giá sơ bộ trong vòng [1–2 ngày làm việc]
    """  # Agent solution
]


def display_skills():
    """Display available skills for user selection."""
    print("\n=== Available Skills ===")
    for i, (skill_id, skill_info) in enumerate(SKILL_MAP.items(), 1):
        title = skill_info["mo_ta"].split('\n')[1].strip(
        ) if '\n' in skill_info["mo_ta"] else f"Skill {skill_id}"
        print(f"{i}. {skill_id}: {title}")
    print()


def get_skill_choice():
    """Get user's skill selection."""
    skill_ids = list(SKILL_MAP.keys())

    while True:
        try:
            choice = input(f"Choose a skill (1-{len(skill_ids)}): ").strip()
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(skill_ids):
                    return skill_ids[index]
            print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            return None


def create_answer_file(skill_id):
    """Create a unique answer file for the conversation."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"answer_{skill_id}_{timestamp}.md"
    filepath = os.path.join("/workspaces/multi-agent", filename)

    # Create initial content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# EduZaa Skill Up Session - {skill_id}\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Skill ID:** {skill_id}\n\n")
        f.write("---\n\n")

    return filepath


def save_conversation_turn(filepath, user_input, agent_response, turn_number):
    """Save a single conversation turn to the answer file."""
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(f"## Turn {turn_number}\n\n")
        f.write(f"**User:** {user_input}\n\n")
        f.write(f"**Agent:** {agent_response}\n\n")
        f.write("---\n\n")


async def main():
    # draw_graph(triage_agent, filename="agent_graph")
    # draw_graph(triage_agent).view()
    print("=== EduZaa Skill Up Agent ===")

    # Skill selection
    display_skills()
    selected_skill_id = get_skill_choice()

    if not selected_skill_id:
        print("No skill selected. Goodbye!")
        return

    print(f"\nSelected skill: {selected_skill_id}")
    print("Type 'exit', 'quit', or 'bye' to end the conversation\n")

    # Create answer file
    answer_file = create_answer_file(selected_skill_id)
    print(f"Conversation will be saved to: {answer_file}\n")

    test_index = 0
    auto_test_mode = True
    turn_number = 1

    while True:
        try:
            # Get user input - either automatic or manual
            if auto_test_mode and test_index < len(KICH_BAN_CHAY):
                user_input = KICH_BAN_CHAY[test_index]
                print(
                    f"\nAuto Input [{test_index + 1}/{len(KICH_BAN_CHAY)}]: {user_input}")
                test_index += 1

                # Switch to manual mode after all test inputs
                if test_index >= len(KICH_BAN_CHAY):
                    auto_test_mode = False
            else:
                user_input = input("\nYou: ").strip()

            # Check for exit conditions
            if user_input.lower() in ['exit', 'quit', 'bye', '']:
                print("Goodbye!")
                break

            print("Agent: ", end='', flush=True)
            agent_response = ""
            stream = await ServiceManager().run(
                user_id="user123",
                chat_id="chat456",
                skill_id=selected_skill_id,
                messsage=user_input
            )
            async for response in stream:
                print(response, end='', flush=True)
                agent_response += response
            print()  # Add newline after response

            # Save conversation turn to file
            save_conversation_turn(
                answer_file, user_input, agent_response, turn_number)
            turn_number += 1

            print()  # Add newline after response

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")

    print(f"\nConversation saved to: {answer_file}")


if __name__ == "__main__":
    asyncio.run(main())
