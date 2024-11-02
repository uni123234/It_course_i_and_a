import React, { useEffect, useState } from "react";
import { useNavbarHeight } from "../hooks";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { useMediaQuery } from "react-responsive";
import { CreateCourseModal } from "../components"
import { getCourses, getLessons } from "../api"
import { useAuth } from "../features";
import { useNavigate } from "react-router-dom";

ChartJS.register(ArcElement, Tooltip, Legend);

type Course = {
  id: number;
  title: string;
  description: string;
  progress: number;
};


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

const pieData = {
  labels: ["Completed", "Uncompleted", "Missed Deadline"],
  datasets: [
    {
      data: [60, 30, 10], // Приклад даних
      backgroundColor: ["#34D399", "#FBBF24", "#EF4444"],
    },
  ],
};

const options = {
  plugins: {
    legend: {
      display: true,
      position: "bottom" as const,
      labels: {
        usePointStyle: true,
        padding: 20,
        font: {
          size: 14,
        },
        color: "#ffffff",
      },
    },
  },
};

const Dashboard: React.FC = () => {
  const { getAccessToken } = useAuth();

  const navigate = useNavigate();

  const [userCourses, setUserCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null)

  const [lessons, setLessons] = useState([])

  useEffect(() => {
    const fetchCourses = async () => {
      console.log("Fetching courses..."); // Додайте лог тут

      const token = getAccessToken();
      
      try {
        const data = await getCourses(token); // Передайте токен
        console.log("Data received:", data); // Лог даних
        setUserCourses(data);
      } catch (err) {
        setError('Failed to fetch courses.');
        console.error(err); // Лог для помилок
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();

    const fetchLessons = async () => {
      console.log("Fetching courses..."); // Додайте лог тут

      const token = getAccessToken();
      
      try {
        const data = await getLessons(token); // Передайте токен
        console.log("Data received calendar:", data); // Лог даних
        setLessons(data);
      } catch (err) {
        console.error(err);
      } finally {
      }
    };

    fetchLessons();
  }, [getAccessToken]);

  const navbarHeight = useNavbarHeight();
  const isLargeScreen = useMediaQuery({ minWidth: 1024 });

  const [isCreateModalOpen, setisCreateModalOpen] = useState(false);

  const openCreateModal = () => setisCreateModalOpen(true);
  const closeCreateModal = () => setisCreateModalOpen(false);

  const handleMouseEnter = () => {
    if (isLargeScreen) {
      document.body.style.overflowY = "hidden";
    }
  };

  const handleMouseLeave = () => {
    if (isLargeScreen) {
      document.body.style.overflowY = "auto";
    }
  };

  const handleWheel = (event: React.WheelEvent<HTMLDivElement>) => {
    if (event.deltaY !== 0) {
      event.currentTarget.scrollBy({
        left: event.deltaY * 3,
        behavior: "smooth",
      });
      event.preventDefault();
    }
  };
  

  return (
    <>
    <div
      className="bg-gradient-to-b from-blue-50 to-blue-100 text-gray-900 flex flex-col items-center"
      style={{ minHeight: `calc(100vh - ${navbarHeight}px)` }}
    >
      <h1 className="mt-6 text-center text-6xl font-semibold">Your Courses:</h1>

      <section
  className="flex w-[90vw] md:w-[60vw] z-0 h-full mt-8 p-6 overflow-x-auto md:overflow-x-hidden overflow-y-hidden bg-white rounded-2xl shadow-2xl transform transition-transform hover:scale-105"
  onMouseEnter={isLargeScreen ? handleMouseEnter : undefined}
  onMouseLeave={isLargeScreen ? handleMouseLeave : undefined}
  onWheel={handleWheel}
>
  <div className="flex space-x-6 items-center justify-start">
    {userCourses.map((course, index) => (
      <div
        key={course.id}
        className="flex-shrink-0 w-44 md:w-64 p-6 rounded-xl shadow-lg transform transition-transform hover:scale-105 cursor-pointer"
        style={{
          background: `linear-gradient(135deg, hsl(${
            index * 45
          }, 100%, 85%), hsl(${index * 45}, 100%, 90%))`,
        }}
        onClick={() => navigate(`/course/${course.id}`)}
      >
        <h2 className="text-2xl font-semibold text-gray-900">
          {course.title}
        </h2>
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
    ))}

    {/* Add "Create your own course" button */}
    <div
    onClick={openCreateModal}
      className="flex-shrink-0 w-44 md:w-64 p-6 rounded-xl shadow-lg transform transition-transform hover:scale-105 flex items-center justify-center cursor-pointer"
      style={{
        background: `linear-gradient(135deg, hsl(0, 100%, 85%), hsl(0, 100%, 90%))`,
      }}
    >
      <span className="text-4xl font-semibold text-gray-900">+</span>
      <p className="text-lg text-gray-700 ml-2">Create your own course</p>
    </div>
  </div>
</section>

      {/* Graph and Popular Cousres block */}
      <section className="flex flex-col md:flex-row w-[90vw] md:w-[60vw] mt-8 mb-10 space-y-6 md:space-y-0 md:space-x-6">
        {/* Pie graph block */}
        <div className="flex-1 bg-gray-900 p-6 rounded-2xl shadow-lg flex items-center justify-center">
          <Pie data={pieData} options={options} />
        </div>
        {/* Pipular courses bloack */}
        <div className="flex-1 bg-white p-6 rounded-2xl shadow-lg">
          <h2 className="text-xl font-semibold mb-4 text-gray-900">
            Popular Courses
          </h2>
          <ul className="space-y-4">
            {popularCourses.map((course) => (
              <li
                key={course.id}
                role="button"
      tabIndex={0}
                className="flex items-center justify-between p-4 rounded-xl shadow-md bg-gradient-to-r from-gray-50 to-white hover:from-white hover:to-gray-50 transition-transform hover:-translate-y-1"
              >
                <div>
                  <p className="font-semibold text-gray-800">{course.title}</p>
                  <p className="text-sm text-gray-600 mt-1">
                    {course.description}
                  </p>
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
      </section>
    </div>
    <CreateCourseModal isOpen={isCreateModalOpen} onClose={closeCreateModal} />
    </>
  );
};

export default Dashboard;
