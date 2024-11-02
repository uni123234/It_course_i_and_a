import axios from "axios";
import API_URL from "./index";
import { useAuth } from "../features";

interface CourseData {
  title: string;
  description: string;
}

export const useCreateCourse = () => {
  const { getAccessToken } = useAuth();

  const createCourse = async ({ title, description }: CourseData) => {
    const token = getAccessToken();

    try {
      const response = await axios.post(
        `${API_URL}/courses/create/`,
        {
          title,
          description,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`, // Використання заголовка refresh
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error("Error creating course:", error);
      throw error;
    }
  };

  return { createCourse };
};


interface HomeworkData {
  title: string;
  description: string;
  id: number | null;
  dateTime: string;
  courseId: number | undefined;
}

export const useCreateHomework = () => {
  const { getAccessToken } = useAuth();

  const createHomework = async ({ title, description, id, dateTime, courseId }: HomeworkData) => {
    const token = getAccessToken();

    try {
      const response = await axios.post(
        `${API_URL}/homework/`,
        {
          title,
          description,
          submitted_by: id,
          due_date: dateTime,
          course_id: courseId
        },
        {
          headers: {
            Authorization: `Bearer ${token}`, // Використання заголовка refresh
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error("Error creating course:", error);
      throw error;
    }
  };

  return { createHomework };
};


interface LessonData {
  title: string;
  description: string;
  // id: number | null;
  dateTime: string;
  courseId: number | undefined;
}

export const useCreateLesson = () => {
  const { getAccessToken } = useAuth();

  const createLesson = async ({ title, description, dateTime, courseId }: LessonData) => {
    const token = getAccessToken();

    try {
      const response = await axios.post(
        `${API_URL}/lessons/create/`,
        {
          title,
          description,
          // submitted_by: id,
          scheduled_time: dateTime,
          course_id: courseId
        },
        {
          headers: {
            Authorization: `Bearer ${token}`, // Використання заголовка refresh
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error("Error creating course:", error);
      throw error;
    }
  };

  return { createLesson };
};

// export const useCreateLesson = () => {
//     const { getAccessToken } = useAuth();

//     const createLesson = async ({
//     }: CourseData) => {
//       const token = getAccessToken();

//       try {
//         const response = await axios.post(
//           `${API_URL}/lessons/create/`,
//           { id: 1
//             course,
//             description,
//             state: "not_started",
//           },
//           {
//             headers: {
//                 Authorization: `Bearer ${token}`, // Використання заголовка refresh
//               },
//           }
//         );
//         return response.data;
//       } catch (error) {
//         console.error("Error creating course:", error);
//         throw error;
//       }
//     };

//     return { createLesson };
//   };
