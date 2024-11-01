import React from "react";
import AuthPage from "../components/auth/AuthPage";
import useAuthForm from "../features/auth/useAuthForm";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../api";

const Register: React.FC = () => {
  const navigate = useNavigate(); // Ініціалізація навігатора

  const { fields, errors, handleChange, handleSubmit, isLoading } = useAuthForm({
    initialFields: {
      email: "",
      password: "",
      firstName: "",
      lastName: "",
      role: "",
    },
    onSubmit: async (fields) => {
      try {
        await registerUser({
          email: fields.email,
          password: fields.password,
          firstName: fields.firstName,
          lastName: fields.lastName,
          role: fields.role,
        });

        navigate("/login");
      } catch (error) {
        console.error("Error:", error);
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
