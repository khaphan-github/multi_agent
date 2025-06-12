import asyncio
from modules.eduzaa_skill_up_agent_cluster.service_manager import ServiceManager
import json
import nest_asyncio
nest_asyncio.apply()


async def extract_chat_id_from_stream(response_stream):
    """Extract chat_id from streaming response"""
    chat_id = None
    response_content = ""

    async for event in response_stream:
        try:
            # Parse the JSON text
            event_data = json.loads(event)

            # Print only the content field if it exists
            if 'content' in event_data and event_data['content']:
                print(event_data['content'], end='', flush=True)

            # Extract and concatenate only the content field
            if 'content' in event_data and event_data['content']:
                response_content += event_data['content']

            # Extract chat_id from the parsed JSON if available
            if 'chat_id' in event_data:
                chat_id = event_data['chat_id']
        except json.JSONDecodeError:
            print(f"\n❌ Failed to parse JSON: {event}")
            response_content += event

    return chat_id, response_content


async def run_agent_transition_tests(service_manager: ServiceManager, user_id, skill_id):
    """Run 4 automated messages to test agent transitions"""
    test_cases = [
        {
            "message": "Ten cua toi la Nguyen Van A, toi muon tim hieu ve ky nang giao tiep",
            "description": "=> Agent phân loại"
        },
        {
            "message": "Chịu, tôi không nghỉ ra được bất cứ điều gì",
            "description": "=> Agent phân loại"
        },
        {
            "message": "Cho 1 gợi ý nhỏ",
            "description": "=> Chuyển sang Agent Gợi ý"
        },
        {
            "message": "Tôi chưa hiểu rõ nội dung tình huống",
            "description": "=> Chuyển sang Agent Làm rõ tình huống"
        },
        {
            "message": """Xem xét kỹ hơn các tài liệu dự án;
        Làm việc với các bên liên quan để nắm rõ yêu cầu và nguồn lực;
        Xác định các yếu tố rủi ro có thể ảnh hưởng đến tiến độ.
        Tôi dự kiến sẽ hoàn tất việc đánh giá sơ bộ trong vòng [1–2 ngày làm việc]""",
            "description": "=> Agent solution"
        }
    ]

    chat_id = None

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n=== Test {i}: Agent Transition ===")
        print(f"Description: {test_case['description']}")
        print(f"Message: {test_case['message']}")
        print("Response: ", end='')

        try:
            response_stream = await service_manager.run(
                user_id=user_id,
                chat_id=chat_id,  # First request will be None, subsequent will use same chat_id
                skill_id=skill_id,
                messsage=test_case['message']
            )

            extracted_chat_id, response_content = await extract_chat_id_from_stream(response_stream)

            # Use the chat_id from first response for subsequent requests
            if chat_id is None and extracted_chat_id:
                chat_id = extracted_chat_id
                print(f"\n🔗 Using chat_id: {chat_id}")
            elif chat_id is None:
                chat_id = service_manager.create_chat_id(None)
                print(f"\n🔗 Generated chat_id: {chat_id}")

        except Exception as e:
            print(f"\n❌ Error in test {i}: {e}")

        print("\n" + "-"*80)

        # Add delay between tests for sequential processing
        if i < len(test_cases):
            print("⏳ Waiting 3 seconds before next test...")
            await asyncio.sleep(3)

    return chat_id


async def continuous_chat(service_manager, user_id, skill_id, chat_id):
    """Allow continuous user chat"""
    print("\n" + "="*50)
    print("🗣️  CONTINUOUS CHAT MODE")
    print("Type 'quit' or 'exit' to end the conversation")
    print("="*50 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye! Chat session ended.")
                break

            if not user_input:
                print("Please enter a message or 'quit' to exit.")
                continue

            print("Assistant: ", end='')

            response_stream = await service_manager.run(
                user_id=user_id,
                chat_id=chat_id,
                skill_id=skill_id,
                messsage=user_input
            )

            _, response_content = await extract_chat_id_from_stream(response_stream)
            print()  # New line after response

            # Add small delay for better UX in continuous chat
            await asyncio.sleep(0.5)

        except KeyboardInterrupt:
            print("\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")


async def main():

    # Initialize ServiceManager
    service_manager = ServiceManager()
    user_id = "user_123"

    # Skill selection menu
    print("🎯 SKILL SELECTION")
    print("="*30)
    print("1. Ứng phó với nhiệm vụ mới")
    print("2. Kỹ năng giao tiếp hiệu quả")
    print("3. Quản lý thời gian và ưu tiên công việc")
    print("="*30)

    while True:
        try:
            choice = input("Choose a skill (1, 2, or 3): ").strip()
            if choice in ['1', '2', '3']:
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return

    # Use choice directly as skill_id
    skill_id = choice

    skill_names = {
        '1': 'Ứng phó với nhiệm vụ mới',
        '2': 'Kỹ năng giao tiếp hiệu quả',
        '3': 'Quản lý thời gian và ưu tiên công việc'
    }

    print(f"\n✅ Selected: {skill_names[skill_id]} (ID: {skill_id})")

    # Send one chat message
    print("\n💬 SENDING CHAT MESSAGE")
    print("="*50)
    user_message = "Chao ban!"
    response_stream = await service_manager.run(
        user_id=user_id,
        chat_id=None,  # New chat session
        skill_id=skill_id,
        messsage=user_message
    )

    chat_id, response_content = await extract_chat_id_from_stream(response_stream)

    # Run agent transition tests
    print("\n🤖 RUNNING AGENT TRANSITION TESTS")
    print("="*80)
    chat_id = await run_agent_transition_tests(service_manager, user_id, skill_id)

    print(f"\n✅ All automated tests completed! Final chat_id: {chat_id}")

    # Ask user if they want to continue chatting
    print("\n" + "="*50)
    while True:
        try:
            continue_choice = input(
                "Would you like to continue chatting? (y/n): ").strip().lower()
            if continue_choice in ['y', 'yes']:
                await continuous_chat(service_manager, user_id, skill_id, chat_id)
                break
            elif continue_choice in ['n', 'no']:
                print("👋 Goodbye!")
                break
            else:
                print("❌ Please enter 'y' for yes or 'n' for no.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

    print("👋 Done!")


if __name__ == "__main__":
    asyncio.run(main())
