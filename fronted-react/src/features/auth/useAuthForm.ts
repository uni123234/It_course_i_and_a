import { useState } from "react";

type AuthFormFields = {
  email: string;
  password: string;
  username?: string;
  confirmPassword?: string;
  firstName?: string;
  lastName?: string;
  role?: string;
};

type UseAuthFormProps = {
  initialFields: AuthFormFields;
  onSubmit: (fields: AuthFormFields) => Promise<void>;
  validate?: boolean;
};

const API_URL = "http://127.0.0.1:8000/api";

const useAuthForm = ({
  initialFields,
  onSubmit,
  validate = true,
}: UseAuthFormProps) => {
  const [fields, setFields] = useState<AuthFormFields>(initialFields);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  const validateFields = () => {
    const newErrors: Record<string, string> = {};

    if (!fields.email) {
      newErrors.email = "Email is required.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(fields.email)) {
      newErrors.email = "Please enter a valid email address.";
    }

    if (
      validate &&
      fields.username !== undefined &&
      fields.username.length < 6
    ) {
      newErrors.username = "Username must be at least 6 characters long.";
    }

    if (!fields.password) {
      newErrors.password = "Password is required.";
    } else if (fields.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters long.";
    }

    if (validate && fields.password !== fields.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match.";
    }


    if (
      validate &&
      fields.lastName !== undefined &&
      fields.lastName.length < 2 &&
      fields.firstName !== undefined &&
      fields.firstName.length < 2
    ) {
      newErrors.fullname = "First name or last name fields are invalid.";
    }

    if (
      validate &&
      !fields.role
    ) {
      newErrors.role = "Please, choose your role."
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0; // returns true, if there is no errors
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFields({
      ...fields,
      [e.target.name]: e.target.value,
    });

    setErrors((prevErrors) => ({
      ...prevErrors,
      [e.target.name]: "",
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    console.log("submit")
    e.preventDefault();
    if (!validateFields()) return;

    setIsLoading(true);
    try {
      await onSubmit(fields);
      setErrors({});
    } catch (err) {
      setErrors({ form: "An unexpected error occurred. Please try again." });
    } finally {
      setIsLoading(false);
    }
  };

  return {
    fields,
    errors,
    isLoading,
    handleChange,
    handleSubmit,
    API_URL,
  };
};

export default useAuthForm;
