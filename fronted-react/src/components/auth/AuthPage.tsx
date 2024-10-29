import React, { useEffect, useState } from "react";
import AuthInput from "./AuthInput";
import SocialLoginButtons from "./SocialLoginButtons";
import { loginImage } from "../../assets";

import { useNavigate } from "react-router-dom";

interface AuthPageProps {
  title: string;
  buttonText: string;
  inputs: {
    name: string;
    placeholder: string;
    value: string;
    error?: string;
  }[];
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
  const [isSmallScreen, setIsSmallScreen] = useState(window.innerWidth < 768);

  const navigate = useNavigate();

  const [navbarHeight, setNavbarHeight] = useState<number>(0);

  useEffect(() => {
    const navbar = document.querySelector("nav") as HTMLElement;
    if (navbar) {
      setNavbarHeight(navbar.offsetHeight);
      console.log("a ", navbar.offsetHeight);
    }
  }, []);

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
      className="flex min-h-screen items-center justify-center bg-gray-200 sm:bg-cover sm:bg-center"
      style={{
        backgroundImage: isSmallScreen ? `url(${loginImage})` : "none",
        backgroundSize: isSmallScreen ? "cover" : "auto",
        backgroundPosition: isSmallScreen ? "center" : "initial",
      }}
    >
      <div
        className={`flex flex-col md:flex-row max-w-md md:max-w-2xl h-auto md:h-[600px] shadow-lg rounded-lg overflow-hidden bg-white mx-4 ${formClassName}
        ${isSmallScreen ? "w-[350px]" : "w-full"}`}
        style={{ marginTop: `${navbarHeight}px` }}
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
                  <AuthInput
                    name={input.name}
                    placeholder={input.placeholder}
                    value={input.value}
                    onChange={onInputChange}
                  />
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
