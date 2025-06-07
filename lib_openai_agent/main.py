import asyncio
import os
from modules.eduzaa_skill_up_agent_cluster.service_manager import ServiceManager


async def main():
    # Initialize ServiceManager
    service_manager = ServiceManager()

    # Hardcoded user ID and skill ID
    user_id = "user_123"
    skill_id = "skill_456"

    # First request - no chat_id provided (will be auto-generated)
    print("=== First Request ===")
    user_input_1 = "Tôi cần học kỹ năng giao tiếp"

    response_stream_1 = await service_manager.run(
        user_id=user_id,
        chat_id=None,  # Will be auto-generated
        skill_id=skill_id,
        messsage=user_input_1
    )

    # Process the streaming response and extract chat_id
    chat_id = None
    async for event in response_stream_1:
        print(f"Response chunk: {event}")
        # Extract chat_id from the response if available
        if hasattr(event, 'chat_id'):
            chat_id = event.chat_id
        elif isinstance(event, dict) and 'chat_id' in event:
            chat_id = event['chat_id']

    # If chat_id wasn't in the response, generate one for demonstration
    if not chat_id:
        chat_id = service_manager.create_chat_id(None)
        print(f"Generated chat_id: {chat_id}")

    print("\n" + "="*50 + "\n")

    # Second request - using the same chat_id to continue conversation
    print("=== Second Request (Same Chat) ===")
    user_input_2 = "Cho tôi một số gợi ý cụ thể"

    try:
        response_stream_2 = await service_manager.run(
            user_id=user_id,
            chat_id=chat_id,  # Use the same chat_id
            skill_id=skill_id,
            messsage=user_input_2
        )

        # Process the second streaming response
        async for event in response_stream_2:
            print(f"Response chunk: {event}")

    except Exception as e:
        print(f"Error in second request: {e}")

    print("\n" + "="*50 + "\n")

    # Third request - different scenario with new chat
    print("=== Third Request (New Chat) ===")
    user_input_3 = "Tôi muốn học một kỹ năng khác"

    try:
        response_stream_3 = await service_manager.run(
            user_id=user_id,
            chat_id=None,  # New chat session
            skill_id="skill_789",  # Different skill
            messsage=user_input_3
        )

        # Process the third streaming response
        async for event in response_stream_3:
            print(f"Response chunk: {event}")

    except Exception as e:
        print(f"Error in third request: {e}")


if __name__ == "__main__":
    asyncio.run(main())
