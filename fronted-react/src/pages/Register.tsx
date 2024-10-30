import React from "react";
import AuthPage from "../components/auth/AuthPage";
import useAuthForm from "../features/auth/useAuthForm";

const Register: React.FC = () => {
  const { fields, errors, handleChange, handleSubmit, isLoading, API_URL } =
    useAuthForm({
      initialFields: { email: "", password: "", username: "" },
      onSubmit: async (fields) => {
        const response = await fetch(`${API_URL}/register`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: fields.email,
            username: fields.username,
            password: fields.password,
          }),
        });

        if (!response.ok) {
          throw new Error("Failed to log in");
        }
      },
      validate: true,
    });

  return (
    <AuthPage
      title="Welcome!"
      buttonText={isLoading ? "Signing up..." : "Sign up"}
      inputs={[
        {
          name: "email",
          placeholder: "Email",
          value: fields.email,
          error: errors.email,
        },
        {
          name: "username",
          placeholder: "Username",
          value: fields.username || "",
          error: errors.username,
        },
        {
          name: "password",
          placeholder: "Password",
          value: fields.password,
          error: errors.password,
        },
        {
          name: "confirmPassword",
          placeholder: "Confirm password",
          value: fields.confirmPassword || "",
          error: errors.confirmPassword,
        },
      ]}
      onSubmit={handleSubmit}
      onInputChange={handleChange}
      linkText="Already have an account?"
      linkHref="/login"
      formClassName="md:h-auto"
    />
  );
};

export default Register;
