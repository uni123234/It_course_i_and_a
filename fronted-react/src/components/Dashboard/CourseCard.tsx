import React from "react";

type CourseCardProps = {
  course: Course;
  onClick: () => void;
};

type Course = {
  id: number;
  title: string;
  description: string;
  progress: number;
};

const CourseCard: React.FC<CourseCardProps> = ({ course, onClick }) => (
  <div
    className="flex-shrink-0 w-44 md:w-64 p-6 rounded-xl shadow-lg cursor-pointer"
    style={{
      background: `linear-gradient(135deg, hsl(${
        course.id * 45
      }, 100%, 85%), hsl(${course.id * 45}, 100%, 90%))`,
    }}
    onClick={onClick}
  >
    <h2 className="text-2xl font-semibold text-gray-900">{course.title}</h2>
    <p className="text-gray-700 mt-2">{course.description}</p>
    <div className="mt-4 bg-gray-300 rounded-full h-2.5 overflow-hidden">
      <div
        className="bg-green-500 h-2.5 rounded-full"
        style={{ width: `${course.progress || 0}%` }}
      ></div>
    </div>
    <p className="text-sm text-gray-600 mt-2">
      Progress: {course.progress || 0}%
    </p>
  </div>
);

export default CourseCard;
