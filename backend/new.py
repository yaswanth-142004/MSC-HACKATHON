import streamlit as st
from ocr import initialize_client, perform_ocr
from agent import call  # Importing the call function from agent
import json

def main():
    st.title("Automated Answer Evaluation with OCR and Agents")
    st.write("Upload images of the question paper, correct answers, and the student's answer for evaluation.")

    # File uploaders
    st.subheader("Upload Question Paper")
    question_paper_file = st.file_uploader("Question paper image:", type=["jpg", "jpeg", "png"], key="qp")

    st.subheader("Upload Correct Answer Paper")
    correct_answer_file = st.file_uploader("Correct answer image:", type=["jpg", "jpeg", "png"], key="ca")

    st.subheader("Upload Student's Answer")
    student_answer_file = st.file_uploader("Student answer image:", type=["jpg", "jpeg", "png"], key="sa")

    if all([question_paper_file, correct_answer_file, student_answer_file]):
        try:
            # Display uploaded images
            cols = st.columns(3)
            with cols[0]:
                st.image(question_paper_file, caption="Question Paper")
            with cols[1]:
                st.image(correct_answer_file, caption="Correct Answer")
            with cols[2]:
                st.image(student_answer_file, caption="Student Answer")

            # Initialize OCR client
            client = initialize_client()

            # Perform OCR with progress
            with st.status("Processing documents...", expanded=True) as status:
                st.write("Extracting text from question paper...")
                question_text = perform_ocr(client, question_paper_file.read())

                st.write("Extracting text from correct answer...")
                correct_answer_text = perform_ocr(client, correct_answer_file.read())

                st.write("Extracting text from student answer...")
                student_answer_text = perform_ocr(client, student_answer_file.read())
                status.update(label="OCR Complete!", state="complete")

            # Show extracted text in expanders
            with st.expander("View Extracted Text"):
                tabs = st.tabs(["Question", "Correct Answer", "Student Answer"])
                with tabs[0]:
                    st.code(question_text)
                with tabs[1]:
                    st.code(correct_answer_text)
                with tabs[2]:
                    st.code(student_answer_text)

            if st.button("Evaluate Answer", type="primary"):
                # Call the agent's evaluation function
                with st.spinner("Evaluating answer..."):
                    response = call(question_text, correct_answer_text, student_answer_text)
                
                try:
                    # Parse the JSON response into a Python dictionary
                    response_content = json.loads(response)

                    # Display results
                    st.title("Student Answer Evaluation Report")

                    # Display summary report
                    st.subheader("Summary Report")
                    st.markdown(f"**Total Marks:** {response_content['summary_report']['total_marks']}")
                    st.markdown(f"**Overall Feedback:** {response_content['summary_report']['overall_feedback']}")

                    # Display evaluations for each question
                    st.subheader("Per-Question Evaluations")
                    for evaluation in response_content["per_question_evaluations"]:
                        st.markdown(f"### Question {evaluation['question']}")
                        st.markdown(f"**Marks Awarded:** {evaluation['marks_awarded']}")
                        with st.expander("Justifications"):
                            st.markdown("**Strengths:**")
                            for strength in evaluation["justifications"]["strengths"]:
                                st.markdown(f"- {strength}")
                            st.markdown("**Weaknesses:**")
                            for weakness in evaluation["justifications"]["weaknesses"]:
                                st.markdown(f"- {weakness}")
                            st.markdown("**Improvement Suggestions:**")
                            for suggestion in evaluation["justifications"]["improvement_suggestions"]:
                                st.markdown(f"- {suggestion}")
                except json.JSONDecodeError:
                    st.error("Failed to parse the response. Please check if the response is a valid JSON.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

        except Exception as e:
            st.error(f"Processing error: {str(e)}")
    else:
        st.warning("Please upload all required documents to continue")

if __name__ == "__main__":
    main()