import useForm from "./useForm";

type CourseFormFields = {
  courseTitle: string;
  description: string;
};

const validateCourseFields = (fields: CourseFormFields): Record<string, string> => {
  const errors: Record<string, string> = {};

  if (!fields.courseTitle) {
    errors.courseTitle = "Course title is required.";
  } else if (fields.courseTitle.length < 3) {
    errors.courseTitle = "Course title must be at least 3 characters long.";
  }

  if (!fields.description) {
    errors.description = "Description is required.";
  } else if (fields.description.length < 10) {
    errors.description = "Description must be at least 10 characters long.";
  }

  return errors;
};

const useCreateCourseForm = (onSubmit: (fields: CourseFormFields) => Promise<void>) => {
  return useForm({
    initialFields: { courseTitle: "", description: "" },
    onSubmit,
    validateFields: validateCourseFields,
  });
};

export default useCreateCourseForm;
