import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getHomeworks, fetchCourse } from "../api";
import { CreateHomeworkModal, CreateLessonModal } from "../components";
import { useAuth } from "../features";

interface CourseData {
  id: number;
  title: string;
  description: string;
}

interface Homework {
  title: string;
  dueDate: string;
}

const CoursePage: React.FC = () => {
  const { getAccessToken } = useAuth();
  const { courseId } = useParams<{ courseId: string }>();
  const courseIdNumber = courseId ? parseInt(courseId, 10) : undefined;

  const [course, setCourse] = useState<CourseData | null>(null);
  const [homeworks, setHomeworks] = useState<Homework[]>([]);
  // const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);


  
  const [isHomeworkModalOpen, setHomeworkModalOpen] = useState(false);
  const [isLessonModalOpen, setLessonModalOpen] = useState(false);

  useEffect(() => {
    const token = getAccessToken();
    const fetchData = async () => {
      if (!courseIdNumber) return;
      setError(null);
  
      try {
        const [courseData, homeworksData] = await Promise.all([
          fetchCourse(courseIdNumber, token),
          getHomeworks(courseIdNumber, token),
        ]);
        setCourse(courseData.course);
        setHomeworks(homeworksData);
      } catch {
        setError("Не вдалося отримати дані. Спробуйте ще раз.");
      }
    };
  
    if (error) {
      console.log(error);
    }


  
    fetchData();
  }, [courseIdNumber, error, getAccessToken]);
  

  // if (loading) return <p>Loading...</p>;
  // if (error) return <p>{error}</p>;

  return (
    <div className="bg-gradient-to-br from-blue-50 to-blue-100 min-h-screen">
      <div className="max-w-4xl mx-auto p-4">
        {/* Action Buttons */}
        <div className="flex justify-around space-x-4 mb-6">
          <button className="px-4 py-2 bg-gradient-to-r from-amber-400 to-lime-400 text-white rounded-full hover:shadow-lg transform hover:scale-105">
            Course Calendar
          </button>
          <button
            onClick={() => setHomeworkModalOpen(true)}
            className="px-4 py-2 bg-gradient-to-r from-amber-400 to-lime-400 text-white rounded-full hover:shadow-lg transform hover:scale-105"
          >
            Create Homework
          </button>
          <button
            onClick={() => setLessonModalOpen(true)}
            className="px-4 py-2 bg-gradient-to-r from-amber-400 to-lime-400 text-white rounded-full hover:shadow-lg transform hover:scale-105"
          >
            Create Lesson
          </button>
          <button className="px-4 py-2 bg-gradient-to-r from-amber-400 to-lime-400 text-white rounded-full hover:shadow-lg transform hover:scale-105">
            Users
          </button>
        </div>

        {/* Course Info */}
        <div className="bg-gradient-to-br from-pink-400 to-orange-300 text-white p-8 rounded-lg shadow-lg text-center transform hover:scale-105">
          <h1 className="text-4xl font-extrabold tracking-wide">
            {course?.title}
          </h1>
          <p className="mt-2 text-xl">{course?.description}</p>
        </div>

        {/* Homework List */}
        <div className="mt-10 space-y-6">
          {homeworks.map((homework, index) => (
            <div
              key={index}
              className="p-6 bg-white rounded-lg shadow-lg flex justify-between items-center transform hover:scale-105 hover:shadow-xl"
            >
              <div>
                <h3 className="font-semibold text-xl text-pink-500">
                  {homework.title}
                </h3>
                <p className="text-gray-500">{homework.dueDate}</p>
              </div>
              <button className="text-yellow-500 font-semibold hover:text-yellow-600 hover:underline">
                View Details
              </button>
            </div>
          ))}
        </div>
      </div>

      <CreateHomeworkModal
        isOpen={isHomeworkModalOpen}
        onClose={() => setHomeworkModalOpen(false)}
        courseId={courseIdNumber}
      />
      <CreateLessonModal
        isOpen={isLessonModalOpen}
        onClose={() => setLessonModalOpen(false)}
        courseId={courseIdNumber}
      />
    </div>
  );
};

export default CoursePage;
