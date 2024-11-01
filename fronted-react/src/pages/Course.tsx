// CoursePage.tsx
import React from 'react';

const CoursePage: React.FC = () => {
  const homeworks = [
    { title: 'Homework 1: Introduction to Organic Chemistry', dueDate: 'Due Oct 24' },
    { title: 'Homework 2: Hydrocarbons', dueDate: 'Due Oct 28' },
    { title: 'Homework 3: Functional Groups', dueDate: 'Due Nov 1' },
  ];

  return (
    <div className="bg-gradient-to-br from-gray-100 to-indigo-100 min-h-screen">
      {/* Header with Buttons */}
      <nav className="flex justify-between items-center p-4 bg-white shadow-md">
        <h1 className="text-xl font-bold text-indigo-600 ml-4">IT Course</h1>
        <div className="flex space-x-4">
          <button className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-blue-500 text-white rounded-full hover:shadow-lg transition-transform transform hover:scale-105">
            Course Calendar
          </button>
          <button className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-blue-500 text-white rounded-full hover:shadow-lg transition-transform transform hover:scale-105">
            Users
          </button>
        </div>
      </nav>

      {/* Course Info Card */}
      <div className="max-w-4xl mx-auto mt-8 p-4">
        <div className="bg-gradient-to-br from-purple-600 to-indigo-600 text-white p-8 rounded-lg shadow-lg text-center transition-transform transform hover:scale-105">
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
                <h3 className="font-semibold text-xl text-indigo-800">{homework.title}</h3>
                <p className="text-gray-500">{homework.dueDate}</p>
              </div>
              <button className="text-indigo-600 font-semibold hover:text-indigo-700 hover:underline">
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
