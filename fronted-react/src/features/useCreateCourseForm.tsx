import { useState } from "react";

type CourseFormFields = {
  courseTitle: string;
  description: string;
};

type UseCreateCourseFormProps = {
  initialFields: CourseFormFields;
  onSubmit: (fields: CourseFormFields) => Promise<void>;
  validate?: boolean;
};

const useCreateCourseForm = ({
  initialFields,
  onSubmit,
}: UseCreateCourseFormProps) => {
  const [fields, setFields] = useState<CourseFormFields>(initialFields);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const validateFields = (fieldsToValidate: CourseFormFields) => {
    const newErrors: Record<string, string> = {};

    if (!fieldsToValidate.courseTitle) {
      newErrors.courseTitle = "Course title is required.";
    } else if (fieldsToValidate.courseTitle.length < 3) {
      newErrors.courseTitle =
        "Course title must be at least 3 characters long.";
    }

    if (!fieldsToValidate.description) {
      newErrors.description = "Description is required.";
    } else if (fieldsToValidate.description.length < 10) {
      newErrors.description =
        "Description must be at least 10 characters long.";
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

export default useCreateCourseForm;
