from langchain_core.messages import SystemMessage, HumanMessage
from langchain_grok import ChatGrok
import os

# Define the evaluation criteria and their weights
SCORING_CRITERIA = {
    "Accuracy": 40,       # Percentage weight
    "Completeness": 30,
    "Clarity": 20,
    "Understanding": 10
}

def calculate_total_score(scores):
    """
    Calculate the weighted total score from the individual criteria scores.
    """
    total_weight = sum(SCORING_CRITERIA.values())
    weighted_score = sum((scores[criterion] * weight) / 100 for criterion, weight in SCORING_CRITERIA.items())
    total_percentage = (weighted_score / total_weight) * 100
    return total_percentage

def call(q, c, s):
    # Ensure the GROQ_API_KEY is set
    grok_api_key = os.getenv("GROK_API_KEY")
    if not grok_api_key:
        raise ValueError("GROK_API_KEY environment variable is not set.")
    
    # Define the system message and input messages
    system_message = SystemMessage(
        content=(
            "You are a precise university evaluator. Evaluate the student's answer based on the following criteria:\n"
            "1. **Accuracy** (40% weight): How closely the student's answer matches the correct answer.\n"
            "2. **Completeness** (30% weight): Does the student's answer cover all key aspects?\n"
            "3. **Clarity** (20% weight): Is the student's answer clear and well-articulated?\n"
            "4. **Understanding** (10% weight): Does the student demonstrate an understanding of the core concept?\n\n"
            "Provide a percentage score (0-100%) for each criterion. Output the evaluation in this format:\n"
            "- Accuracy: [Score]%\n"
            "- Completeness: [Score]%\n"
            "- Clarity: [Score]%\n"
            "- Understanding: [Score]%"
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
    
    # Initialize the ChatGrok model
    chat = ChatGrok(temperature=0.2, grok_api_key=grok_api_key, model_name="mixtral-8x7b-32768")
    
    # Generate evaluation by invoking the model with the messages
    response = chat.invoke(messages)
    
    # Parse the response to extract scores
    evaluation = response.content
    scores = {}
    for criterion in SCORING_CRITERIA.keys():
        match = re.search(rf"{criterion}: (\d+)%", evaluation)
        if match:
            scores[criterion] = int(match.group(1))
        else:
            scores[criterion] = 0  # Assign 0% if the score is not found
    
    # Calculate the total score
    total_score = calculate_total_score(scores)
    
    # Compile and return the evaluation results
    evaluation_result = {
        "Total Score": f"{total_score:.2f}%",
        "Scores Breakdown": scores,
        "Raw Evaluation Response": evaluation
    }
    return evaluation_result

# Example Usage
if __name__ == "__main__":
    question = "Explain the concept of polymorphism in Object-Oriented Programming."
    correct_answer = (
        "Polymorphism is a concept in object-oriented programming that allows methods or functions "
        "to process objects differently based on their type or class. It enables one interface to be used for a general class of actions."
    )
    student_answer = (
        "Polymorphism means having many forms. In OOP, it refers to the ability of a function or object to take on multiple forms."
    )
    
    # Call the function and print the result
    try:
        result = call(question, correct_answer, student_answer)
        print("Evaluation Result:")
        print(result)
    except ValueError as e:
        print("Error:", e)
