from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
import os

def call(q, c, s):
    # Ensure the GROQ_API_KEY is set
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    
    # Define the system message and user input messages
    system_message = SystemMessage(
        content=(
            "You are the evaluator of the university. You are given the question paper, "
            "the correct solution, and the student's answer. Your task is to evaluate the student's answer "
            "and provide marks accordingly with a brief justification."
        )
    )

    question_message = HumanMessage(content=f"Question: {q}")
    correct_answer_message = HumanMessage(content=f"Correct Answer: {c}")
    student_answer_message = HumanMessage(content=f"Student's Answer: {s}")
    
    # Create a list of messages
    messages = [
        system_message,
        question_message,
        correct_answer_message,
        student_answer_message
    ]
    
    # Initialize the ChatGroq model
    chat = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")
    
    # Generate evaluation by invoking the model with the messages
    response = chat.invoke(messages)
    
    # Return the content of the response
    return response.content

# if __name__ == "__main__":
#     question = "Explain the concept of polymorphism in Object-Oriented Programming."
#     correct_answer = (
#         "Polymorphism is a concept in object-oriented programming that allows methods or functions "
#         "to process objects differently based on their type or class. It enables one interface to be used for a general class of actions."
#     )
#     student_answer = (
#         "Polymorphism means having many forms. In OOP, it refers to the ability of a function or object to take on multiple forms."
#     )
    
#     # Call the function and print the result
#     try:
#         result = call(question, correct_answer, student_answer)
#         print("Evaluation Result:", result)
#     except ValueError as e:
#         print("Error:", e)