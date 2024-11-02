import { useState } from "react";


type HomeworkFormFields = {
  homeworkTitle: string;
  description: string;
  dateTime: string; // New dateTime field for due date and time
};

type UseCreateHomeworkFormProps = {
  initialFields: HomeworkFormFields;
  onSubmit: (fields: HomeworkFormFields) => Promise<void>;
  validate?: boolean;
};

const useCreateHomeworkForm = ({
  initialFields,
  onSubmit,
}: UseCreateHomeworkFormProps) => {
  const [fields, setFields] = useState<HomeworkFormFields>(initialFields);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const validateFields = (fieldsToValidate: HomeworkFormFields) => {
    const newErrors: Record<string, string> = {};

    if (!fieldsToValidate.homeworkTitle) {
      newErrors.homeworkTitle = "Homework title is required.";
    } else if (fieldsToValidate.homeworkTitle.length < 3) {
      newErrors.homeworkTitle = "Homework title must be at least 3 characters long.";
    }

    if (!fieldsToValidate.description) {
      newErrors.description = "Description is required.";
    } else if (fieldsToValidate.description.length < 10) {
      newErrors.description = "Description must be at least 10 characters long.";
    }

    if (!fieldsToValidate.dateTime) {
      newErrors.dateTime = "Due date and time are required.";
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

    if (isSubmitted) {
      validateFields(newFields);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitted(true);
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
    errors: isSubmitted ? errors : {},
    isLoading,
    handleChange,
    handleSubmit,
  };
};

export default useCreateHomeworkForm;