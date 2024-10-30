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
  const [isSubmitted, setIsSubmitted] = useState(false);

  const validateFields = (fieldsToValidate: AuthFormFields) => {
    const newErrors: Record<string, string> = {};

    if (!fieldsToValidate.email) {
      newErrors.email = "Email is required.";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(fieldsToValidate.email)) {
      newErrors.email = "Please enter a valid email address.";
    }

    if (
      validate &&
      fieldsToValidate.username !== undefined &&
      fieldsToValidate.username.length < 6
    ) {
      newErrors.username = "Username must be at least 6 characters long.";
    }

    if (!fieldsToValidate.password) {
      newErrors.password = "Password is required.";
    } else if (fieldsToValidate.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters long.";
    }

    if (
      validate &&
      fieldsToValidate.password !== fieldsToValidate.confirmPassword
    ) {
      newErrors.confirmPassword = "Passwords do not match.";
    }

    if (
      validate && (
        (!fieldsToValidate.lastName || fieldsToValidate.lastName.length < 2) ||
      !fieldsToValidate.firstName ||
      fieldsToValidate.firstName.length < 2)
    ) {
      newErrors.fullname = "First name or last name fields are invalid.";
    }

    if (validate && !fieldsToValidate.role) {
      newErrors.role = "Please, choose your role.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newFields = {
      ...fields,
      [e.target.name]: e.target.value,
    };
    setFields(newFields);

    // Очищення помилок після відправки форми
    if (isSubmitted) {
      validateFields(newFields);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitted(true); // Встановлюємо в true після натискання submit
    const isValid = validateFields(fields);

    if (!isValid) return;

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
    errors: isSubmitted ? errors : {}, // Відображаємо помилки тільки після submit
    isLoading,
    handleChange,
    handleSubmit,
    API_URL,
  };
};

export default useAuthForm;
