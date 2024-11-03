import React from "react";
import CreateModalBase from "./ModalCreateBase";
import { useCreateHomeworkForm, useAuth } from "../../features";
import { useCreateHomework } from "../../api";
import { Homework } from "../../types";

interface HomeworkModalProps {
  isOpen: boolean;
  onClose: () => void;
  courseId: number | undefined;
  lessonId: number | undefined;
  onHomeworkCreate: (newHomework: Homework) => void;
}

const CreateHomeworkModal: React.FC<HomeworkModalProps> = ({
  isOpen,
  onClose,
  courseId,
  onHomeworkCreate,
  lessonId
}) => {
  const { getUserId } = useAuth();

  const userId = getUserId();

  const { createHomework } = useCreateHomework()

  const { fields, errors, isLoading, handleChange, handleSubmit } =
    useCreateHomeworkForm(async (fields) => {
      try {
        const newHomework = await createHomework({
          title: fields.homeworkTitle,
          description: fields.description,
          dateTime: fields.dateTime,
          id: userId,
          courseId: courseId,
          lesson: lessonId,
        });

        onHomeworkCreate(newHomework);

        console.log("Homework created successfully:", newHomework);
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
          label: "Deadline",
          name: "dateTime",
          type: "datetime-local",
          required: true,
          min: new Date().toISOString().slice(0, 16),
        },
      ]}
      submitLabel="Create Homework"
    />
  );
};

export default CreateHomeworkModal;
