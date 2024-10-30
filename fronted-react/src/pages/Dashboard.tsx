import React, { useRef } from "react";

type Course = {
  id: number;
  title: string;
  description: string;
  progress: number; // Progress percentage
};

const userCourses: Course[] = [
  {
    id: 1,
    title: "React Basics",
    description: "Learn the basics of React.",
    progress: 70,
  },
  {
    id: 2,
    title: "Advanced TypeScript",
    description: "Deep dive into TypeScript.",
    progress: 45,
  },
  {
    id: 3,
    title: "Tailwind CSS",
    description: "Design fast with Tailwind.",
    progress: 100,
  },
  {
    id: 4,
    title: "React Basics",
    description: "Learn the basics of React.",
    progress: 70,
  },
  {
    id: 5,
    title: "Advanced TypeScript",
    description: "Deep dive into TypeScript.",
    progress: 45,
  },
  {
    id: 6,
    title: "Tailwind CSS",
    description: "Design fast with Tailwind.",
    progress: 100,
  },
  {
    id: 7,
    title: "React Basics",
    description: "Learn the basics of React.",
    progress: 70,
  },
  {
    id: 8,
    title: "Advanced TypeScript",
    description: "Deep dive into TypeScript.",
    progress: 45,
  },
  {
    id: 9,
    title: "Tailwind CSS",
    description: "Design fast with Tailwind.",
    progress: 100,
  },
  // Add more courses here
];

const Dashboard: React.FC = () => {
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Обробник події для скролу колесиком миші
  const handleWheelScroll = (event: React.WheelEvent) => {
    if (scrollContainerRef.current) {
      event.preventDefault(); // Зупиняємо вертикальний скрол сторінки
      event.stopPropagation(); // Зупиняємо подію, щоб не прокручувалась сторінка
      scrollContainerRef.current.scrollLeft += event.deltaY; // Горизонтальний скрол
    }
  };
  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold">Welcome to Your Dashboard</h1>
        <p className="text-gray-600">Here are your current courses</p>
      </div>

      {/* User Courses with Horizontal Scroll on Mouse Wheel */}
      <div
        ref={scrollContainerRef}
        onWheel={handleWheelScroll} // Додаємо подію для горизонтального скролу
        className="overflow-x-auto scrollbar-hide" // Ховаємо панель прокрутки
      >
        <div className="flex space-x-4 p-4">
          {userCourses.map((course) => (
            <div
              key={course.id}
              className="flex-shrink-0 w-64 p-4 bg-white rounded-lg shadow-lg"
            >
              <h2 className="text-xl font-semibold">{course.title}</h2>
              <p className="text-gray-600">{course.description}</p>
              <div className="mt-2 bg-gray-200 rounded-full h-2.5">
                <div
                  className="bg-blue-500 h-2.5 rounded-full"
                  style={{ width: `${course.progress}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-500 mt-1">
                Progress: {course.progress}%
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};


export default Dashboard;
