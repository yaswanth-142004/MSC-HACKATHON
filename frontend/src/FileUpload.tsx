import React, { useState } from 'react';

const FileUpload = ({ label, onUpload }) => {
  const [preview, setPreview] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadCount, setUploadCount] = useState(0);
  const [isUploaded, setIsUploaded] = useState(false);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsLoading(true);
    const reader = new FileReader();

    reader.onload = () => {
      setPreview(reader.result);

      setTimeout(() => {
        try {
          const mockResponse = {
            success: true,
            message: `Uploaded ${file.name}`,
            text: 'Uploaded text content'
          };

          onUpload({
            text: mockResponse.text,
            preview: reader.result
          });

          setUploadCount(prevCount => prevCount + 1);
          setIsUploaded(true);
          setIsLoading(false);
        } catch (error) {
          console.error('Error uploading file:', error);
          setIsLoading(false);
        }
      }, 1500);
    };

    reader.readAsDataURL(file);
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
      <h3 className="text-lg font-semibold mb-4 text-gray-700">{label || 'File Upload'}</h3>
      <label className="flex flex-col items-center px-4 py-6 bg-blue-50 rounded-md border-2 border-dashed border-blue-200 cursor-pointer hover:border-blue-300 transition-colors">
        <svg
          className="w-12 h-12 text-blue-400 mb-2"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
          />
        </svg>
        <span className="text-gray-600">Click to upload image</span>
        <input
          type="file"
          accept="image/*"
          onChange={handleFileUpload}
          className="hidden"
        />
      </label>

      {isLoading && (
        <div className="mt-4 text-center text-gray-500">
          <svg className="animate-spin h-5 w-5 mr-3 inline-block" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
          </svg>
          Processing...
        </div>
      )}

      {preview && (
        <div className="mt-4 w-full h-48 flex items-center justify-center overflow-hidden">
          <img
            src={preview}
            alt="Preview"
            className="max-w-full max-h-full object-contain rounded-md shadow-sm border border-gray-200"
          />
        </div>
      )}
    </div>
  );
};

export default FileUpload;