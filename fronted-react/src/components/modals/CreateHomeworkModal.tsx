import React from "react";
import CreateModalBase from "./ModalCreateBase";
import { useCreateHomeworkForm, useAuth } from "../../features";
import { createHomework } from "../../api";

interface HomeworkModalProps {
  isOpen: boolean;
  onClose: () => void;
  courseId: number | undefined;
}

const CreateHomeworkModal: React.FC<HomeworkModalProps> = ({
  isOpen,
  onClose,
  courseId,
}) => {
  const { getUserId } = useAuth();

  const userId = getUserId();

  const { fields, errors, isLoading, handleChange, handleSubmit } =
    useCreateHomeworkForm(async (fields) => {
      try {
        const response = await createHomework({
          title: fields.homeworkTitle,
          description: fields.description,
          dateTime: fields.dateTime,
          id: userId,
          courseId: courseId,
        });

        console.log("Homework created successfully:", response);
      } catch (error) {
        console.error("Error creating homework:", error);
      }
    });

  return (
    <CreateModalBase
      isOpen={isOpen}
      onClose={onClose}
      title="Create Homework"
      fields={fields}
      errors={errors}
      isLoading={isLoading}
      handleChange={handleChange}
      handleSubmit={handleSubmit}
      inputs={[
        {
          label: "Homework Title",
          name: "homeworkTitle",
          type: "text",
          required: true,
        },
        {
          label: "Description",
          name: "description",
          type: "text",
          required: true,
        },
        {
          label: "Start Date & Time",
          name: "dateTime",
          type: "datetime-local",
          required: true,
          min: new Date().toISOString().slice(0, 16),
        },
      ]}
      submitLabel="Додати завдання"
    />
  );
};

export default CreateHomeworkModal;
