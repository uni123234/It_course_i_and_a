import React from "react";
import CreateModalBase from "./ModalCreateBase";
import { useCreateLessonForm } from "../../features";

import { useCreateLesson } from "../../api";

interface LessonModalProps {
  isOpen: boolean;
  onClose: () => void;
  courseId: number | undefined;
}

const CreateLessonModal: React.FC<LessonModalProps> = ({
  isOpen,
  onClose,
  courseId,
}) => {
  const { createLesson } = useCreateLesson();
  const { fields, errors, isLoading, handleChange, handleSubmit } =
    useCreateLessonForm(async (fields) => {
      try {
        const response = await createLesson({
          title: fields.lessonTitle,
          description: fields.description,
          dateTime: fields.dateTime,
          courseId: courseId,
        });

        console.log("Lesson created successfully:", response);
        // За потреби можна очистити поля форми або виконати інші дії
      } catch (error) {
        console.error("Error creating homework:", error);
        // Обробка помилки (наприклад, показ повідомлення або оновлення інтерфейсу)
      }
    });

  return (
    <CreateModalBase
      isOpen={isOpen}
      onClose={onClose}
      title="Create Lesson"
      fields={fields}
      errors={errors}
      isLoading={isLoading}
      handleChange={handleChange}
      handleSubmit={handleSubmit}
      inputs={[
        {
          label: "Lesson Title",
          name: "lessonTitle",
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
      submitLabel="Create Lesson"
    />
  );
};

export default CreateLessonModal;
