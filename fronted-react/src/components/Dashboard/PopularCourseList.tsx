import React from "react";

const popularCourses = [
  {
    id: 1,
    title: "JavaScript Essentials",
    description: "Core JavaScript concepts.",
    popularity: 80,
  },
  {
    id: 2,
    title: "React Advanced",
    description: "Deep dive into React.",
    popularity: 60,
  },
  {
    id: 3,
    title: "Python Basics",
    description: "Introduction to Python.",
    popularity: 90,
  },
  {
    id: 4,
    title: "JavaScript Basics",
    description: "Introduction to JavaScript.",
    popularity: 60,
  },
  {
    id: 5,
    title: "Python Advanced",
    description: "Deep dive into Python.",
    popularity: 90,
  },
];

const PopularCourseList: React.FC = () => (
  <div className="flex-1 bg-white p-6 rounded-2xl shadow-lg">
    <h2 className="text-xl font-semibold mb-4 text-gray-900">
      Popular Courses
    </h2>
    <ul className="space-y-4">
      {popularCourses.map((course) => (
        <li
          key={course.id}
          className="flex items-center justify-between p-4 rounded-xl shadow-md bg-gradient-to-r from-gray-50 to-white hover:from-white hover:to-gray-50"
        >
          <div>
            <p className="font-semibold text-gray-800">{course.title}</p>
            <p className="text-sm text-gray-600 mt-1">{course.description}</p>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-sm font-medium text-gray-700">
              {course.popularity}%
            </span>
            <div className="bg-gray-300 h-2 w-24 rounded-full overflow-hidden">
              <div
                className="bg-green-500 h-2 rounded-full"
                style={{ width: `${course.popularity}%` }}
              ></div>
            </div>
          </div>
        </li>
      ))}
    </ul>
  </div>
);

export default PopularCourseList;
