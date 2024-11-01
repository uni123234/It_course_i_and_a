import React from 'react';
import Modal from './ModalBase';
import ModalInput from './ModalInput';
import { useCreateCourseForm } from '../../features';

import { useCreateCourse } from "../../api"

interface CourseModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const CreateCourseModal: React.FC<CourseModalProps> = ({ isOpen, onClose }) => {
    const { createCourse } = useCreateCourse();

  const { fields, errors, isLoading, handleChange, handleSubmit } = useCreateCourseForm({
    initialFields: { courseTitle: '', description: '' },
    onSubmit: async (fields) => {
      try {
        // Call the createCourse function and pass the required fields
        const response = await createCourse({
          title: fields.courseTitle,
          description: fields.description,
        });

        console.log('Course created successfully:', response);
        // Optionally, you can reset the form fields or perform other actions here

      } catch (error) {
        console.error('Error creating course:', error);
        // Handle error (e.g., display a notification or update UI)
      }
    },
  });


  return (
    <Modal isOpen={isOpen} onClose={onClose} width="30%" height="auto">
      <h2 className="text-2xl font-bold text-gray-800 text-center mb-4">Create your own course</h2>

      <form onSubmit={handleSubmit} className="p-4">
        <ModalInput
          label="Course Title"
          name="courseTitle"
          type="text"
          value={fields.courseTitle}
          onChange={handleChange}
          required
        />
        {errors.courseTitle && <p className="text-red-500">{errors.courseTitle}</p>}

        <ModalInput
          label="Description"
          name="description"
          type="text"
          value={fields.description}
          onChange={handleChange}
          required
        />
        {errors.description && <p className="text-red-500">{errors.description}</p>}

        <button
          type="submit"
          className="mt-4 w-full bg-purple-500 text-white py-2 rounded-lg hover:bg-purple-600 transition duration-200"
          disabled={isLoading}
        >
          {isLoading ? 'Завантаження...' : 'Додати курс'}
        </button>
      </form>
    </Modal>
  );
};

export default CreateCourseModal;
