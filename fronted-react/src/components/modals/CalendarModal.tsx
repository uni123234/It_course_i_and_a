import React, { useEffect, useState } from "react";
import dayjs from "dayjs";
import ModalBase from "./ModalBase";
import { getLessons } from "../../api";
import { useAuth } from "../../features";

const daysOfWeek = [
  "Понеділок",
  "Вівторок",
  "Середа",
  "Четвер",
  "П’ятниця",
  "Субота",
  "Неділя",
];

interface CalendarModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const CalendarModal: React.FC<CalendarModalProps> = ({ isOpen, onClose }) => {
  const [lessons, setLessons] = useState<any[]>([]); // Замість 'any' використовуйте ваш тип даних
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const { getAccessToken } = useAuth();
  const token = getAccessToken();

  useEffect(() => {
    const fetchLessons = async () => {
      setLoading(true);
      setError(null); // Скинути помилку

      try {
        const lessonsData = await getLessons(token);
        setLessons(lessonsData); // Зберегти дані уроків
      } catch (err) {
        setError("Не вдалося отримати уроки. Спробуйте ще раз."); // Обробка помилок
      } finally {
        setLoading(false); // Завершити завантаження
      }
    };

    fetchLessons();
  }, [token]);
  const [currentMonth, setCurrentMonth] = useState(dayjs());

  const startDay = currentMonth.startOf("month").startOf("week");
  const endDay = currentMonth.endOf("month").endOf("week");
  const days: dayjs.Dayjs[] = [];

  let day = startDay;
  while (day.isBefore(endDay, "day")) {
    days.push(day);
    day = day.add(1, "day");
  }

  const handlePreviousMonth = () =>
    setCurrentMonth(currentMonth.subtract(1, "month"));
  const handleNextMonth = () => setCurrentMonth(currentMonth.add(1, "month"));
  const handleToday = () => setCurrentMonth(dayjs());

  return (
    <ModalBase isOpen={isOpen} onClose={onClose} width="80%" height="85vh">
      <h2 className="text-2xl font-bold text-gray-800 text-center mb-4">
        Календар
      </h2>

      {/* Calendar Layout */}
      <div className="p-4">
        <div className="flex justify-center items-center mb-4">
          <button
            onClick={handleToday}
            className="bg-purple-500 text-white px-4 py-1 rounded"
          >
            Сьогодні
          </button>
        </div>

        <div className="flex justify-center items-center mb-2 text-2xl">
          <button onClick={handlePreviousMonth} className="text-gray-600">
            &lt;
          </button>
          <h3 className="text-lg font-semibold mx-2">
            {currentMonth.format("MMMM YYYY")}
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
                dayItem.month() !== currentMonth.month() ? "text-gray-400" : ""
              }`}
            >
              <span className="text-xs">{dayItem.date()}</span>
              {/* Event example */}
              {dayItem.date() === 1 &&
              dayItem.month() === currentMonth.month() ? (
                <div className="bg-purple-200 text-purple-700 rounded p-1 mt-2 text-xs">
                  Презентація проєкта
                </div>
              ) : null}
            </div>
          ))}
        </div>
      </div>
    </ModalBase>
  );
};

export default CalendarModal;
