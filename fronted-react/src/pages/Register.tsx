import React from "react";
import AuthPage from "../components/auth/AuthPage";
import useAuthForm from "../features/auth/useAuthForm";

const Register: React.FC = () => {
  const { fields, errors, handleChange, handleSubmit, isLoading, API_URL } =
    useAuthForm({
      initialFields: {
        email: "",
        password: "",
        firstName: "",
        lastName: "",
        role: "",
      },
      onSubmit: async (fields) => {
        const response = await fetch(`${API_URL}/register/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: fields.email,
            password: fields.password,
            first_name: fields.firstName,
            last_name: fields.lastName,
            user_type: fields.role,
          }),
        });

        if (!response.ok) {
          throw new Error("Failed to register");
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
          type: "text",
          name: "email",
          placeholder: "Email",
          value: fields.email,
          error: errors.email,
        },
        {
          type: "text-group",
          names: ["firstName", "lastName"],
          placeholders: ["First Name", "Last Name"],
          values: [fields.firstName || "", fields.lastName || ""],
          error: errors.fullname,
        },
        {
          type: "password",
          name: "password",
          placeholder: "Password",
          value: fields.password,
          error: errors.password,
        },
        {
          type: "password",
          name: "confirmPassword",
          placeholder: "Confirm password",
          value: fields.confirmPassword || "",
          error: errors.confirmPassword,
        },
        {
          type: "radio-group",
          name: "role",
          options: [
            { value: "teacher", label: "Teacher" },
            { value: "student", label: "Student" },
          ],
          selected: fields.role,
          error: errors.role,
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
