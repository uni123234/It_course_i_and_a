import { useState } from "react";

type FormFields = Record<string, any>;

type UseFormProps<T extends FormFields> = {
  initialFields: T;
  onSubmit: (fields: T) => Promise<void>;
  validateFields: (fields: T) => Record<string, string>;
};

const useForm = <T extends FormFields>({
  initialFields,
  onSubmit,
  validateFields,
}: UseFormProps<T>) => {
  const [fields, setFields] = useState<T>(initialFields);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newFields = {
      ...fields,
      [e.target.name]: e.target.value,
    };
    setFields(newFields);

    if (isSubmitted) {
      setErrors(validateFields(newFields));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitted(true);
    const newErrors = validateFields(fields);

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

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
    errors: isSubmitted ? errors : {},
    isLoading,
    handleChange,
    handleSubmit,
  };
};

export default useForm;
