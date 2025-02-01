import streamlit as st
from ocr import initialize_client, perform_ocr
from agent import call  # Importing the call function from agent

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
            with cols[0]: st.image(question_paper_file, caption="Question Paper")
            with cols[1]: st.image(correct_answer_file, caption="Correct Answer")
            with cols[2]: st.image(student_answer_file, caption="Student Answer")

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
                with tabs[0]: st.code(question_text)
                with tabs[1]: st.code(correct_answer_text)
                with tabs[2]: st.code(student_answer_text)

            if st.button("Evaluate Answer", type="primary"):
                # Call the agent's evaluation function
                with st.spinner("Evaluating answer..."):
                    response = call(question_text, correct_answer_text, student_answer_text)

                # Display results
                st.subheader("Evaluation Results")
                st.markdown(f"**Marks and Feedback:**")
                st.success(response)

        except Exception as e:
            st.error(f"Processing failed: {str(e)}")
            st.exception(e)
    else:
        st.warning("Please upload all required documents to continue")

if __name__ == "__main__":
    main()
