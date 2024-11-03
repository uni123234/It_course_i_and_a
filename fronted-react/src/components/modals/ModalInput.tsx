import React from 'react';

interface ModalInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
}

const ModalInput: React.FC<ModalInputProps> = ({ label, ...props }) => {
  return (
    <div className="mb-5">
      <label className="block text-gray-700 text-sm font-medium mb-1">{label}</label>
      <input
        {...props}
        className="w-full p-2.5 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
      />
    </div>
  );
};

export default ModalInput;
