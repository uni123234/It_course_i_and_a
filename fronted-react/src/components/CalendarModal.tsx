import React, { useState, useEffect } from "react";
import dayjs from 'dayjs';

const daysOfWeek = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П’ятниця', 'Субота', 'Неділя'];

interface CalendarModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const CalendarModal: React.FC<CalendarModalProps> = ({ isOpen, onClose }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setIsVisible(true);
    } else {
      const timeout = setTimeout(() => setIsVisible(false), 300); // Matches transition duration
      return () => clearTimeout(timeout);
    }
  }, [isOpen]);

  const closeModal = () => {

    setIsVisible(false);
      setTimeout(() => onClose(), 300);
  };

  const [currentMonth, setCurrentMonth] = useState(dayjs());

  const startDay = currentMonth.startOf('month').startOf('week');
  const endDay = currentMonth.endOf('month').endOf('week');
  const days = [];

  let day = startDay;
  while (day.isBefore(endDay, 'day')) {
    days.push(day);
    day = day.add(1, 'day');
  }

  const handlePreviousMonth = () => setCurrentMonth(currentMonth.subtract(1, 'month'));
  const handleNextMonth = () => setCurrentMonth(currentMonth.add(1, 'month'));
  const handleToday = () => setCurrentMonth(dayjs());

  if (!isOpen && !isVisible) return null;

  return (
    <div>
      {/* Background Blur */}
      <div
        className={`fixed inset-0 bg-black bg-opacity-50 transition-opacity duration-300 backdrop-blur-sm z-10 ${
            isVisible ? "opacity-100" : "opacity-0"
        }`}
      ></div>

      {/* Modal Window */}
      <div className="fixed inset-0 flex items-center justify-center z-50">
        <div
          className={`bg-white p-4 rounded-2xl shadow-lg w-full max-w-5xl h-[90vh] overflow-y-auto transition-transform transform duration-500 ${
            isVisible ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0"
          }`}
        >
          <button
            onClick={closeModal}
            className="absolute top-4 right-4 grayscale hover:grayscale-0 transition-transform duration-300 transform hover:scale-110 text-2xl"
          >
            &times;
          </button>
          <h2 className="text-2xl font-bold text-gray-800 text-center mb-4">Календар</h2>

          {/* Calendar Layout */}
          <div className="p-4">
            <div className="flex justify-center items-center mb-4">
              <button onClick={handleToday} className="bg-purple-500 text-white px-4 py-1 rounded">
                Сьогодні
              </button>
            </div>

            <div className="flex justify-center items-center mb-2 text-2xl">
              <button onClick={handlePreviousMonth} className="text-gray-600">
                &lt;
              </button>
              <h3 className="text-lg font-semibold mx-2">
                {currentMonth.format('MMMM YYYY')}
              </h3>
              <button onClick={handleNextMonth} className="text-gray-600 text-2xl">
                &gt;
              </button>
            </div>

            <div className="grid grid-cols-7 gap-1 text-center">
              {daysOfWeek.map((day, index) => (
                <div key={index} className="font-semibold">
                  {day}
                </div>
              ))}
            </div>

            <div className="grid grid-cols-7 gap-1">
              {days.map((dayItem, index) => (
                <div
                  key={index}
                  className={`border p-2 min-h-28 min-w-[100px] flex flex-col ${
                    dayItem.month() !== currentMonth.month() ? 'text-gray-400' : ''
                  }`}
                >
                  <span className="text-xs">{dayItem.date()}</span>
                  {/* Event example */}
                  {dayItem.date() === 1 && dayItem.month() === currentMonth.month() ? (
                    <div className="bg-purple-200 text-purple-700 rounded p-1 mt-2 text-xs">
                      Презентація проєкта
                    </div>
                  ) : null}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CalendarModal;
