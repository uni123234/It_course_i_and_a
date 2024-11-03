import React from "react";
import CreateModalBase from "./ModalCreateBase";
import { useCreateCourseForm } from "../../features";
import { useCreateCourse } from "../../api";
import { Course } from "../../types"

interface CourseModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCourseCreate: (newCourse: Course) => void;
}

const CreateCourseModal: React.FC<CourseModalProps> = ({ isOpen, onClose, onCourseCreate }) => {
  const { createCourse } = useCreateCourse();

  const { fields, errors, isLoading, handleChange, handleSubmit } =
    useCreateCourseForm(async (fields) => {
      try {
        const newCourse = await createCourse({
          title: fields.courseTitle,
          description: fields.description,
        });

        console.log("Course created successfully:", newCourse);
        onCourseCreate(newCourse);
        onClose();
      } catch (error) {
        console.error("Error creating course:", error);
      }
    });

  return (
    <CreateModalBase
      isOpen={isOpen}
      onClose={onClose}
      title="Create your own course"
      fields={fields}
      errors={errors}
      isLoading={isLoading}
      handleChange={handleChange}
      handleSubmit={handleSubmit}
      inputs={[
        {
          label: "Course Title",
          name: "courseTitle",
          type: "text",
          required: true,
        },
        {
          label: "Description",
          name: "description",
          type: "text",
          required: true,
        },
      ]}
      submitLabel="Додати курс"
    />
  );
};
export default CreateCourseModal;
