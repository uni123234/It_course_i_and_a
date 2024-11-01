import React, { InputHTMLAttributes } from "react";

interface InputFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  className?: string;
}

const BaseInput: React.FC<InputFieldProps> = ({ className, ...props }) => {
  const baseStyles =
    "w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-slate-600";

  return <input className={`${baseStyles} ${className}`} {...props} />;
};

export default BaseInput;
