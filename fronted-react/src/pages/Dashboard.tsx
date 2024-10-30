import { useNavbarHeight } from "../hooks";

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
    title: "Tailwind CSSaa",
    description: "Design fast with Tailwind.",
    progress: 100,
  },
  // Add more courses here
];

const Dashboard: React.FC = () => {
  const navbarHeight = useNavbarHeight();

  const handleMouseEnter = () => {
    document.body.style.overflowY = "hidden"; // вимкнення вертикального скролу сторінки
  };

  const handleMouseLeave = () => {
    document.body.style.overflowY = "auto"; // ввімкнення вертикального скролу сторінки
  };

  const handleWheel = (event: React.WheelEvent<HTMLDivElement>) => {
    if (event.deltaY !== 0) {
      event.currentTarget.scrollBy({
        left: event.deltaY * 3,
        behavior: 'smooth' // плавна анімація скролу
      });
      event.preventDefault(); // запобігання вертикальному скролу сторінки
    }
  };

  return (
    <div
      className="bg-gradient-to-b from-blue-50 to-blue-100 text-gray-900 flex flex-col items-center"
      style={{ 
        minHeight: `calc(100vh - ${navbarHeight}px)`
      }}
    >
      <h1 className="mt-6 text-6xl font-semibold"> Your Courses:</h1>
      <div
        className="flex w-[60vw] h-full mt-8 p-6 overflow-x-hidden overflow-y-hidden bg-white rounded-2xl shadow-2xl transform transition-transform hover:scale-105"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onWheel={handleWheel}
      >
        <div className="flex space-x-6 items-center justify-start">
          {userCourses.map((course, index) => (
            <div
              key={course.id}
              className="flex-shrink-0 w-64 p-6 rounded-xl shadow-lg transform transition-transform hover:scale-105"
              style={{
                background: `linear-gradient(135deg, hsl(${index * 45}, 100%, 85%), hsl(${index * 45}, 100%, 90%))`,
              }}
            >
              <h2 className="text-2xl font-semibold text-gray-900">{course.title}</h2>
              <p className="text-gray-700 mt-2">{course.description}</p>
              <div className="mt-4 bg-gray-300 rounded-full h-2.5 overflow-hidden">
                <div
                  className="bg-green-500 h-2.5 rounded-full"
                  style={{ width: `${course.progress}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-600 mt-2">Progress: {course.progress}%</p>
            </div>
          ))}
        </div>
      </div>
      
    </div>
  );
};

export default Dashboard;
