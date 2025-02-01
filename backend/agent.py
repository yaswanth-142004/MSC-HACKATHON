from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
import os
import json

def call(question, correct_answer, student_answer):
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            return json.dumps({"error": "API key missing"})

        system_prompt = """You are an academic evaluator. Return JSON strictly using this format:
        {
            "summary_report": {
                "total_marks": "X/Y",
                "overall_feedback": "concise summary"
            },
            "per_question_evaluations": [{
                "question": "question text",
                "marks_awarded": "X/Y",
                "justifications": {
                    "strengths": ["list", "of", "strengths"],
                    "weaknesses": ["list", "of", "weaknesses"],
                    "improvement_suggestions": ["list", "of", "suggestions"]
                }
            }]
        }
        Return ONLY valid JSON without any formatting or commentary."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"QUESTION: {question}"),
            HumanMessage(content=f"MODEL ANSWER: {correct_answer}"),
            HumanMessage(content=f"STUDENT ANSWER: {student_answer}")
        ]

        chat = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile")
        response = chat.invoke(messages).content
        
        # Validate JSON format before returning
        json.loads(response)
        return response

    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid response format from AI model"})
    except Exception as e:
        return json.dumps({"error": str(e)})