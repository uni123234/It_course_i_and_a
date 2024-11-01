// CoursePage.tsx
import React from 'react';

const CoursePage: React.FC = () => {
  const homeworks = [
    { title: 'Homework 1: Introduction to Organic Chemistry', dueDate: 'Due Oct 24' },
    { title: 'Homework 2: Hydrocarbons', dueDate: 'Due Oct 28' },
    { title: 'Homework 3: Functional Groups', dueDate: 'Due Nov 1' },
  ];

  return (
    <div className="bg-gray-100 min-h-screen">
      {/* Header with Buttons */}
      <nav className="flex justify-end p-4 space-x-4 bg-white shadow">
        <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
          Course Calendar
        </button>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
          Users
        </button>
      </nav>

      {/* Course Info Card */}
      <div className="max-w-4xl mx-auto p-4">
        <div className="bg-indigo-600 text-white p-8 rounded-md shadow-md text-center">
          <h1 className="text-3xl font-bold">Organic Chemistry</h1>
          <p className="mt-2 text-lg">Class 10 - VG</p>
        </div>

        {/* Homework List */}
        <div className="mt-6">
          {homeworks.map((homework, index) => (
            <div key={index} className="p-4 bg-white rounded-md shadow mb-4 flex justify-between items-center">
              <div>
                <h3 className="font-semibold text-lg">{homework.title}</h3>
                <p className="text-gray-500">{homework.dueDate}</p>
              </div>
              <button className="text-blue-600 hover:text-blue-700">View Details</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CoursePage;
