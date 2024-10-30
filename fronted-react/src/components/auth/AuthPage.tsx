import React, { useEffect, useState } from "react";
import AuthInput from "./AuthInput";
import SocialLoginButtons from "./SocialLoginButtons";
import { loginImage } from "../../assets";
import { useNavbarHeight } from "../../hooks";
import { useNavigate } from "react-router-dom";

interface AuthPageProps {
  title: string;
  buttonText: string;
  inputs: Array<{
    type: string;
    name?: string;
    names?: string[];
    placeholder?: string;
    placeholders?: string[];
    value?: string;
    values?: string[];
    error?: string;
    errors?: string[];
    label?: string;
    checked?: boolean;
    options?: Array<{ value: string; label: string }>;
    selected?: string;
  }>;
  onSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  linkText: string;
  linkHref: string;
  formClassName?: string;
}

const AuthPage: React.FC<AuthPageProps> = ({
  title,
  buttonText,
  inputs,
  onSubmit,
  onInputChange,
  linkText,
  linkHref,
  formClassName,
}) => {
  const navbarHeight = useNavbarHeight();
  const [isSmallScreen, setIsSmallScreen] = useState(window.innerWidth < 768);
  const navigate = useNavigate();

  useEffect(() => {
    const handleResize = () => {
      setIsSmallScreen(window.innerWidth < 768 || window.innerHeight < 400);
    };

    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <div
      className={`flex items-center justify-center sm:bg-cover sm:bg-center`}
      style={{
        backgroundImage: `${isSmallScreen ? `url(${loginImage}), ` : ""}linear-gradient(to bottom, rgb(239 246 255), rgb(219 234 254))`,
        backgroundSize: isSmallScreen ? "cover" : "auto",
        backgroundPosition: isSmallScreen ? "center" : "initial",
        minHeight: `calc(100vh - ${navbarHeight}px)`
      }}
    >
      <div
        className={`flex flex-col md:flex-row max-w-md md:max-w-2xl h-auto md:h-[600px] shadow-lg rounded-lg overflow-hidden bg-white mx-4 ${formClassName}
        ${isSmallScreen ? "w-[350px]" : "w-full"}`}
      >
        {!isSmallScreen && (
          <section
            className="hidden md:block md:w-1/2"
            style={{
              backgroundImage: `url(${loginImage})`,
              backgroundSize: "cover",
              backgroundPosition: "center",
            }}
          ></section>
        )}
        <section
          className={`flex w-full items-center justify-center p-8 ${
            isSmallScreen ? "" : "md:w-1/2"
          }`}
        >
          <div className="w-full space-y-6">
            <div className="flex flex-col items-center space-y-2">
              <h2 className="text-2xl font-bold text-gray-800">{title}</h2>
            </div>
            <form className="space-y-6" onSubmit={onSubmit}>
              {inputs.map((input, index) => (
                <div key={index}>
                  {input.type === "text-group" ? (
                    <div className="flex gap-4">
                      {input.names?.map((name, i) => (
                        <AuthInput
                          key={name}
                          type="text"
                          name={name}
                          placeholder={input.placeholders?.[i] || ""}
                          value={input.values?.[i] || ""}
                          onChange={onInputChange}
                        />
                      ))}
                    </div>
                  ) : input.type === "radio-group" ? (
                    <div className="flex items-center space-x-4">
                      {input.options?.map((option) => (
                        <label key={option.value} className="flex items-center">
                          <input
                            type="radio"
                            name={input.name}
                            value={option.value}
                            checked={input.selected === option.value}
                            onChange={onInputChange}
                            className="mr-2"
                          />
                          {option.label}
                        </label>
                      ))}
                    </div>
                  ) : (
                    <AuthInput
                      type={input.type}
                      name={input.name || ""}
                      placeholder={input.placeholder || ""}
                      value={input.value || ""}
                      onChange={onInputChange}
                    />
                  )}
                  {input.error && (
                    <p className="text-red-500 text-sm font-semibold mt-1">
                      {input.error}
                    </p>
                  )}
                </div>
              ))}
              <button
                type="submit"
                className="w-full py-2 font-semibold bg-slate-900 text-white rounded-md hover:bg-gray-800 active:bg-gray-700"
              >
                {buttonText}
              </button>
            </form>
            <div className="text-center text-sm text-gray-500">
              {linkText}
              <button
                className="font-bold text-black ml-1"
                onClick={() => navigate(linkHref)}
              >
                {linkHref === "/register" ? "Sign up" : "Sign in"}
              </button>
            </div>
            <div className="relative my-4">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">or</span>
              </div>
            </div>
            <div className="space-y-3">
              <SocialLoginButtons />
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default AuthPage;
