import React, { useEffect, useState } from "react";
import { useAuth } from "../../features";

import { getReminders } from "../../api";

interface ReminderModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const ReminderModal: React.FC<ReminderModalProps> = ({ isOpen, onClose }) => {
  const { getAccessToken } = useAuth();
  const [reminders, setReminders] = useState([]);

  const fetchReminders = async () => {
    const token = getAccessToken();
    try {
      const data = await getReminders(token);
      console.log(data);

      if (data) {
        setReminders(data);
      }
    } catch (error) {
      console.error("Failed to fetch reminders:", error);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchReminders();
    }
  }, [isOpen]);
  return (
    <>
      <div
        className={`absolute mt-2 right-0 w-64 bg-white shadow-lg rounded-lg p-4 z-50 transition-all duration-300 transform ${
          isOpen
            ? "opacity-100 translate-y-0"
            : "opacity-0 -translate-y-2 pointer-events-none"
        }`}
      >
        <h2 className="text-lg font-semibold mb-2">Нагадування</h2>
        <ul className="space-y-2">
          <li className="border-b pb-2">
            <strong>Домашнє завдання:</strong> Розв'язати задачі з математики
            <br />
            <span className="text-gray-500 text-sm">Здати до: 05.11.2024</span>
          </li>
          <li className="border-b pb-2">
            <strong>Проект:</strong> Написати реферат з історії
            <br />
            <span className="text-gray-500 text-sm">Здати до: 10.11.2024</span>
          </li>
        </ul>
        <button
          className="mt-4 w-full bg-blue-600 text-white py-1 rounded"
          onClick={onClose}
        >
          Закрити
        </button>
      </div>
    </>
  );
};

export default ReminderModal;
