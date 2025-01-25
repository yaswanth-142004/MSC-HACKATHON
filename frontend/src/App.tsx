import React, { useState } from 'react';
import FileUpload from './FileUpload';

type UploadType = {
  text: string;
  preview: string;
};

type UploadsState = {
  question: UploadType;
  correctAnswer: UploadType;
  studentAnswer: UploadType;
};

function App() {
  const [uploads, setUploads] = useState<UploadsState>({
    question: { text: '', preview: '' },
    correctAnswer: { text: '', preview: '' },
    studentAnswer: { text: '', preview: '' }
  });
  const [result, setResult] = useState<string | null>(null);
  const [isEvaluating, setIsEvaluating] = useState<boolean>(false);
  const [isSubmitted, setIsSubmitted] = useState<boolean>(false);

  const handleUpload = (data: { text?: string, preview?: string }, type: keyof UploadsState) => {
    setUploads(prev => ({
      ...prev,
      [type]: {
        ...prev[type],
        ...(data.text && { text: data.text }),
        ...(data.preview && { preview: data.preview })
      }
    }));
  };

  const handleSubmit = () => {
    setIsSubmitted(true);
  };

  const handleEvaluate = async () => {
    setIsEvaluating(true);
    try {
      const mockResponse = await new Promise<{ result: string }>(resolve => {
        setTimeout(() => {
          resolve({
            result: 'Evaluation complete. Student answer shows good understanding of the topic.'
          });
        }, 2000);
      });
      
      setResult(mockResponse.result);
    } catch (error) {
      console.error('Evaluation Error:', error);
      setResult('Error evaluating answer. Please try again.');
    } finally {
      setIsEvaluating(false);
    }
  };

  const allUploadsComplete = Object.values(uploads).every(u => u.text.trim() !== '');

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Automated Answer Evaluation System
          </h1>
          <p className="text-lg text-gray-600">
            Upload images of question paper, correct answer, and student's answer for evaluation
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <FileUpload 
            label="Question Paper" 
            onUpload={(data) => handleUpload(data, 'question')} 
          />
          <FileUpload 
            label="Correct Answer" 
            onUpload={(data) => handleUpload(data, 'correctAnswer')} 
          />
          <FileUpload 
            label="Student Answer" 
            onUpload={(data) => handleUpload(data, 'studentAnswer')} 
          />
        </div>

        {allUploadsComplete && !isSubmitted && (
          <div className="text-center mb-8">
            <button 
              onClick={handleSubmit}
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-green-600 hover:bg-green-700 transition-colors duration-200"
            >
              Submit Uploads
            </button>
          </div>
        )}

        {isSubmitted && (
          <div className="text-center mb-8">
            <button 
              onClick={handleEvaluate}
              disabled={isEvaluating}
              className={`inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white ${
                isEvaluating ? 'bg-blue-400' : 'bg-blue-600 hover:bg-blue-700'
              } transition-colors duration-200`}
            >
              {isEvaluating && (
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                </svg>
              )}
              {isEvaluating ? 'Evaluating...' : 'Evaluate Answer'}
            </button>
          </div>
        )}

        {result && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Evaluation Result</h2>
            <div className="p-4 bg-blue-50 rounded-md border border-blue-200 text-gray-700 whitespace-pre-wrap">
              {result}
            </div>
          </div>
        )}

        <div className="text-center mt-8">
          <a 
            href="https://u66wzghpxc89jeji.vercel.app/" 
            target="_blank" 
            rel="noopener noreferrer" 
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 transition-colors duration-200"
          >
            Analytics
          </a>
        </div>
      </div>
    </div>
  );
}

export default App;
