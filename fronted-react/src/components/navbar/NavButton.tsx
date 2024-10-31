import React, { ButtonHTMLAttributes } from "react";

interface NavButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    className?: string;
    label: string;
  }

const NavButton: React.FC<NavButtonProps> = ({ className, label, ...props }) => {
  const baseStyles =
    "text-gray-800 hover:text-gray-900 font-bold";

  return <button className={`${baseStyles} ${className}`} {...props}>{label}</button>;
};
  

export default NavButton;
