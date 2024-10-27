import React, { ButtonHTMLAttributes, ReactNode } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
  label: string;
  icon: ReactNode;
  onClick?: () => void;
}

const SocialButton: React.FC<ButtonProps> = ({
  className,
  label,
  icon,
  onClick,
  ...props
}) => {
  const baseStyles =
    "w-full flex items-center justify-center space-x-2 py-2 font-semibold border border-gray-300 rounded-md hover:bg-gray-100 active:bg-gray-200";

  return (
    <button className={`${baseStyles} ${className}`} onClick={onClick} {...props}>
      {icon && <span>{icon}</span>}
      <span>{label}</span>
    </button>
  );
};

export default SocialButton;
