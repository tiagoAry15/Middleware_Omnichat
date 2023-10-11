import threading
import uuid

from dialogflowFolder.session_manager import SessionManager


def user_simulation(user_id: str):
    manager = SessionManager()
    ds = manager.get_session(user_id)
    ds.initialize_session(user_id)

    response_dict = {}
    message_pool = ["Oi", "Vou querer duas pizzas de frango", "Sim", "Vou querer um guaraná", "Pix"]
    for message in message_pool:
        response = ds.getDialogFlowResponse(message=message)
        bot_answer = response.query_result.fulfillment_text
        response_dict[message] = bot_answer
    return response_dict


def main():
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())

    user1_results = {}
    user2_results = {}

    def user1_thread():
        nonlocal user1_results
        user1_results = user_simulation(user1_id)

    def user2_thread():
        nonlocal user2_results
        user2_results = user_simulation(user2_id)

    thread1 = threading.Thread(target=user1_thread)
    thread2 = threading.Thread(target=user2_thread)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print("User 1 Results:", user1_results)
    print("User 2 Results:", user2_results)

    assert user1_results == user2_results, "Results are different!"
    print("Both users received the same responses!")


if __name__ == "__main__":
    main()
