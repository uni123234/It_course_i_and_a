import useForm from "./useForm";

type LessonFormFields = {
  lessonTitle: string;
  description: string;
  dateTime: string;
};

const validateLessonFields = (fields: LessonFormFields): Record<string, string> => {
  const errors: Record<string, string> = {};

  if (!fields.lessonTitle) {
    errors.homeworkTitle = "Homework title is required.";
  } else if (fields.lessonTitle.length < 3) {
    errors.homeworkTitle = "Homework title must be at least 3 characters long.";
  }

  if (!fields.description) {
    errors.description = "Description is required.";
  } else if (fields.description.length < 10) {
    errors.description = "Description must be at least 10 characters long.";
  }

  if (!fields.dateTime) {
    errors.dateTime = "Due date and time are required.";
  }

  return errors;
};

const useCreateLessonForm = (onSubmit: (fields: LessonFormFields) => Promise<void>) => {
  return useForm({
    initialFields: { lessonTitle: "", description: "", dateTime: "" },
    onSubmit,
    validateFields: validateLessonFields,
  });
};

export default useCreateLessonForm;
