import React from 'react';
import BaseInput from '../BaseInput';

interface ModalInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
}

const ModalInput: React.FC<ModalInputProps> = ({ label, ...props }) => {
  return (
    <div className="mb-4">
      <label className="block text-gray-700 text-sm font-bold mb-2">{label}</label>
      <BaseInput { ...props }/>
    </div>
  );
};

export default ModalInput;
