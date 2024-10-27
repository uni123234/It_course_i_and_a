import { AuthInput } from "../components";
import { useAuthForm } from "../features";
import { API_URL } from "../config";

import { googleIcon, loginImage } from "../assets";
import { useEffect, useState } from "react";

const LoginPage = () => {
  const [isSmallScreen, setIsSmallScreen] = useState(window.innerWidth < 640);

  useEffect(() => {
    const handleResize = () => {
      setIsSmallScreen(window.innerWidth < 768);
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  // const { fields, errors, handleChange, handleSubmit } = useAuthForm({
  //   initialFields: { email: "", password: "" },
  //   onSubmit: async (fields) => {
  //     const response = await fetch(`${API_URL}login/`, {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify(fields),
  //     });

  //     if (!response.ok) throw new Error("reg error");
  //   },
  //   validate: false,
  // });

  return (
    <div
      className="flex items-center justify-center min-h-screen bg-gray-200 sm:bg-cover sm:bg-center "
      style={{
        backgroundImage: isSmallScreen ? `url(${loginImage})` : "none",
        backgroundSize: isSmallScreen ? "cover" : "auto",
        backgroundPosition: isSmallScreen ? "center" : "initial",
      }}
    >
      <div className="flex flex-col md:flex-row w-full max-w-md md:max-w-2xl h-auto md:h-[500px] shadow-lg rounded-lg overflow-hidden bg-white mx-4">
        <div
          className="hidden md:block md:w-1/2"
          style={{
            backgroundImage: `url(${loginImage})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        ></div>

        <div className="flex w-full md:w-1/2 items-center justify-center p-8">
          <div className="w-full space-y-6">
            <div className="flex flex-col items-center space-y-2">
              <h2 className="text-2xl font-bold text-gray-800">
                Welcome back!
              </h2>
            </div>

            <form className="space-y-6">
              <div>
                <input
                  type="email"
                  placeholder="name@email.com"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-slate-600"
                />
              </div>
              <div>
                <input
                  type="password"
                  placeholder="Password"
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-slate-600"
                />
              </div>

              <button
                type="submit"
                className="w-full py-2 bg-slate-900 text-white rounded-md hover:bg-gray-800 active:bg-gray-700"
              >
                Sign in
              </button>
            </form>

            <div className="text-center text-sm text-gray-500">
              Don't have an account?
              <a href="#" className="font-bold text-black ml-1">
                Sign up
              </a>
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
              <button className="w-full flex items-center justify-center space-x-2 py-2 border border-gray-300 rounded-md hover:bg-gray-100 active:bg-gray-200">
                <img src={googleIcon} className="w-5 h-5" />{" "}
                <span>Continue with Google</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
