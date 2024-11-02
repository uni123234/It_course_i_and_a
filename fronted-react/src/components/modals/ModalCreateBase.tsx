import React from "react";
import Modal from "./ModalBase";
import ModalInput from "./ModalInput";

interface GenericModalFormProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  fields: Record<string, string>;
  errors: Record<string, string>;
  isLoading: boolean;
  handleChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  handleSubmit: (e: React.FormEvent) => Promise<void>;
  inputs: {
    label: string;
    name: string;
    type: string;
    required?: boolean;
    min?: string;
  }[];
  submitLabel: string;
}

const CreateModalBase: React.FC<GenericModalFormProps> = ({
  isOpen,
  onClose,
  title,
  fields,
  errors,
  isLoading,
  handleChange,
  handleSubmit,
  inputs,
  submitLabel,
}) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose} width="30%" height="auto">
      <h2 className="text-2xl font-bold text-gray-800 text-center mb-4">
        {title}
      </h2>

      <form onSubmit={handleSubmit} className="p-4">
        {inputs.map((input) => (
          <div key={input.name}>
            <ModalInput
              label={input.label}
              name={input.name}
              type={input.type}
              value={fields[input.name]}
              onChange={handleChange}
              required={input.required}
              min={input.min}
            />
            {errors[input.name] && (
              <p className="text-red-500">{errors[input.name]}</p>
            )}
          </div>
        ))}

        <button
          type="submit"
          className="mt-4 w-full bg-purple-500 text-white py-2 rounded-lg hover:bg-purple-600 transition duration-200"
          disabled={isLoading}
        >
          {isLoading ? "Завантаження..." : submitLabel}
        </button>
      </form>
    </Modal>
  );
};

export default CreateModalBase;
