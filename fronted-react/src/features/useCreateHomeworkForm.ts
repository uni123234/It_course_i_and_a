import useForm from "./useForm";

type HomeworkFormFields = {
  homeworkTitle: string;
  description: string;
  dateTime: string;
};

const validateHomeworkFields = (fields: HomeworkFormFields): Record<string, string> => {
  const errors: Record<string, string> = {};

  if (!fields.homeworkTitle) {
    errors.homeworkTitle = "Homework title is required.";
  } else if (fields.homeworkTitle.length < 3) {
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

const useCreateHomeworkForm = (onSubmit: (fields: HomeworkFormFields) => Promise<void>) => {
  return useForm({
    initialFields: { homeworkTitle: "", description: "", dateTime: "" },
    onSubmit,
    validateFields: validateHomeworkFields,
  });
};

export default useCreateHomeworkForm;
