import React from "react";
import AuthPage from "../components/auth/AuthPage";
import useAuthForm from "../features/auth/useAuthForm";
import { useAuth } from "../features"
import { loginUser } from "../api";

const Login: React.FC = () => {
  const { login } = useAuth();

  const { fields, errors, handleChange, handleSubmit, isLoading } = useAuthForm({
    initialFields: { email: "", password: "" },
    onSubmit: async (fields) => {
      try {
        const data = await loginUser(fields.email, fields.password);
        console.log("Response from backend:", data);

        const { access, refresh, user } = data;
        login(access, refresh, user);
      } catch (error) {
        console.error("Error:", error);
      }
    },
    validate: false,
  });

  return (
    <AuthPage
      title="Welcome back!"
      buttonText={isLoading ? "Signing in..." : "Sign in"}
      inputs={[
        {
          type: "email",
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
