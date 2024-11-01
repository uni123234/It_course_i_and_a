// CoursePage.tsx
import React, { useEffect, useState } from 'react';
import { useAuth } from "../features";
import { getHomeworks } from "../api"

const CoursePage: React.FC = () => {
  const homeworks = [
    { title: 'Homework 1: Introduction to Organic Chemistry', dueDate: 'Due Oct 24' },
    { title: 'Homework 2: Hydrocarbons', dueDate: 'Due Oct 28' },
    { title: 'Homework 3: Functional Groups', dueDate: 'Due Nov 1' },
  ];

  const { getAccessToken } = useAuth();
  const token = getAccessToken();

    const courseId = 1

  const [homeworkss, setHomeworks] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHomeworks = async () => {
      setLoading(true);
      setError(null);

      try {
        const homeworksData = await getHomeworks(token, courseId);
        setHomeworks(homeworksData);
      } catch (err) {
        setError('Не вдалося отримати домашні завдання. Спробуйте ще раз.');
      } finally {
        setLoading(false);
      }
    };

    fetchHomeworks();
  }, [token, courseId]);

  return (
    <div className="bg-gradient-to-br from-blue-50 to-blue-100 min-h-screen">
    {/* Page Container */}
    <div className="max-w-4xl mx-auto p-4">
      {/* Buttons above Course Info Card */}
      <div className="flex justify-between space-x-4 mb-6">
        <button className="px-4 py-2 bg-gradient-to-r from-amber-400 to-lime-400 text-white rounded-full hover:shadow-lg transition-transform transform hover:scale-105">
          Course Calendar
        </button>
        <button className="px-4 py-2 bg-gradient-to-r from-amber-400 to-lime-400 text-white rounded-full hover:shadow-lg transition-transform transform hover:scale-105">
          Users
        </button>
      </div>

      {/* Course Info Card */}
      <div className="bg-gradient-to-br from-pink-400 to-orange-300 text-white p-8 rounded-lg shadow-lg text-center transition-transform transform hover:scale-105">
        <h1 className="text-4xl font-extrabold tracking-wide">Organic Chemistry</h1>
        <p className="mt-2 text-xl">Class 10 - VG</p>
      </div>

      {/* Homework List */}
      <div className="mt-10 space-y-6">
        {homeworks.map((homework, index) => (
          <div 
            key={index} 
            className="p-6 bg-white rounded-lg shadow-lg flex justify-between items-center transition-transform transform hover:scale-105 hover:shadow-xl">
            <div>
              <h3 className="font-semibold text-xl text-pink-500">{homework.title}</h3>
              <p className="text-gray-500">{homework.dueDate}</p>
            </div>
            <button className="text-yellow-500 font-semibold hover:text-yellow-600 hover:underline">
              View Details
            </button>
          </div>
        ))}
      </div>
    </div>
  </div>
  );
};

export default CoursePage;
