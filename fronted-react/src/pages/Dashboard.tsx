import React, { useEffect, useState } from "react";
import { useNavbarHeight } from "../hooks";
import { useMediaQuery } from "react-responsive";
import { CreateCourseModal } from "../components";
import { getCourses } from "../api";
import { useNavigate } from "react-router-dom";
import { PopularCourseList, ProgressChart } from "../components";
import { useAuth } from "../features";
import { Course } from "../types"

const Dashboard: React.FC = () => {
  const { getAccessToken } = useAuth();
  const navigate = useNavigate();
  const navbarHeight = useNavbarHeight();
  const isLargeScreen = useMediaQuery({ minWidth: 1024 });

  const [userCourses, setUserCourses] = useState<Course[]>([]);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  useEffect(() => {
    const token = getAccessToken();
    const fetchCourses = async () => {
      try {
        const data = await getCourses(token);
        setUserCourses(data);
      } catch (err) {
      } finally {
      }
    };

    fetchCourses();
  }, []);

  const openCreateModal = () => setIsCreateModalOpen(true);
  const closeCreateModal = () => setIsCreateModalOpen(false);

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

  const addCourse = (newCourse: Course) => {
    setUserCourses((prevCourses) => [...prevCourses, newCourse]);
  };

  const courseNavigate = (courseId: number) => {
    handleMouseLeave()
    navigate(`/course/${courseId}`)
  }

  return (
    <div
      className="bg-gradient-to-b from-blue-50 via-blue-100 to-blue-200 text-gray-900 flex flex-col items-center"
      style={{ minHeight: `calc(100vh - ${navbarHeight}px)` }}
    >
      <h1 className="mt-6 text-center text-6xl font-semibold text-transparent bg-clip-text bg-gradient-to-r from-indigo-500 to-purple-600">
        Your Courses:
      </h1>

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
                }, 100%, 75%), hsl(${index * 45}, 100%, 85%))`,
              }}
              onClick={() => courseNavigate(course.id)}
            >
              <h2 className="text-2xl font-semibold text-gray-900">
                {course.title}
              </h2>
              <p className="text-gray-700 mt-2">{course.description}</p>
              <div className="mt-4 bg-gray-300 rounded-full h-2.5 overflow-hidden">
                <div
                  className="bg-green-500 h-2.5 rounded-full transition-all duration-500 ease-in-out"
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
              background: `linear-gradient(135deg, hsl(0, 100%, 75%), hsl(0, 100%, 85%))`,
            }}
          >
            <span className="text-4xl font-semibold text-gray-900">+</span>
            <p className="text-lg text-gray-700 ml-2">Create your own course</p>
          </div>
        </div>
      </section>

      <section className="flex flex-col md:flex-row w-[90vw] md:w-[60vw] mt-8 mb-10 space-y-6 md:space-y-0 md:space-x-6 border border-gray-200 rounded-lg p-4 bg-white shadow-xl">
        <ProgressChart />
        <PopularCourseList />
      </section>

      <CreateCourseModal
        isOpen={isCreateModalOpen}
        onClose={closeCreateModal}
        onCourseCreate={addCourse}
      />
    </div>
  );
};

export default Dashboard;
