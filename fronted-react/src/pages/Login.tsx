import React from "react";
import AuthPage from "../components/auth/AuthPage";
import useAuthForm from "../features/auth/useAuthForm";

const Login: React.FC = () => {
  const { fields, errors, handleChange, handleSubmit, isLoading, API_URL } =
    useAuthForm({
      initialFields: { email: "", password: "" },
      onSubmit: async (fields) => {
        const response = await fetch(`${API_URL}/login/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: fields.email,
            password: fields.password,
          }),
        });

        if (!response.ok) {
          throw new Error("Failed to log in");
        }
        console.log(response);
      },
      validate: false,
    });

  return (
    <AuthPage
      title="Welcome back!"
      buttonText={isLoading ? "Signing in..." : "Sign in"}
      inputs={[
        {
          type: "text",
          name: "email",
          placeholder: "Email",
          value: fields.email,
          error: errors.email,
        },
        {
          type: "password",
          name: "password",
          placeholder: "Password",
          value: fields.password,
          error: errors.password,
        },
      ]}
      onSubmit={handleSubmit}
      onInputChange={handleChange}
      linkText="Don't have an account?"
      linkHref="/register"
    />
  );
};

export default Login;
