// src/components/Result.tsx
import React from 'react';
import { ClipboardDocumentIcon, CheckIcon } from '@heroicons/react/24/outline';

// Define prop types
interface ResultProps {
  result: string | null;
  isLoading: boolean;
  error: string | null;
}

const Result: React.FC<ResultProps> = ({ result, isLoading, error }) => {
  const [copied, setCopied] = React.useState<boolean>(false);

  const handleCopy = () => {
    if (result) {
      navigator.clipboard.writeText(result);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
        <h3 className="text-red-600 font-medium mb-2">Evaluation Error</h3>
        <p className="text-red-500 text-sm">{error}</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="p-6 text-center text-gray-500">
        <svg 
          className="animate-spin h-8 w-8 mx-auto text-blue-600" 
          viewBox="0 0 24 24"
        >
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
        </svg>
        <p className="mt-2">Analyzing answers...</p>
      </div>
    );
  }

  if (!result) return null;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold text-gray-800">Evaluation Result</h2>
          <button
            onClick={handleCopy}
            className="flex items-center text-sm text-gray-500 hover:text-gray-700 transition-colors"
          >
            {copied ? (
              <>
                <CheckIcon className="h-4 w-4 mr-1 text-green-600" />
                <span className="text-green-600">Copied!</span>
              </>
            ) : (
              <>
                <ClipboardDocumentIcon className="h-4 w-4 mr-1" />
                Copy
              </>
            )}
          </button>
        </div>
      </div>
      
      <div className="p-6 bg-gray-50">
        <div className="whitespace-pre-wrap bg-white p-4 rounded-md shadow-sm border border-gray-200">
          {result.split('\n').map((line, index) => (
            <p key={index} className="text-gray-700 mb-2 last:mb-0">
              {line}
            </p>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Result;