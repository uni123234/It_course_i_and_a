import React, { InputHTMLAttributes } from 'react';
 import "../../styles/customInputShadow.css" //custom shadow css class

interface InputFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  className?: string;
}

const AuthInput: React.FC<InputFieldProps> = ({ className, ...props }) => {
  const baseStyles =
    "custom-shadow box-content w-full h-[25px] p-[10px] mb-[20px] bg-black/20 text-white text-sm border-none rounded-sm placeholder:text-[#b3b3b3] placeholder:leading-[25px]";

  return <input className={`${baseStyles} ${className}`} {...props} />;
};

export default AuthInput;
