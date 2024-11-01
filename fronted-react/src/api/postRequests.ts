import axios from "axios";
import API_URL from "./index";
import { useAuth } from "../features";

interface CourseData {
  title: string;
  description: string;
}

export const useCreateCourse = () => {
    const { getAccessToken } = useAuth();
  
    const createCourse = async ({
      title,
      description,
    }: CourseData) => {
      const token = getAccessToken();
  
      try {
        const response = await axios.post(
          `${API_URL}/courses/create/`,
          {
            title,
            description,
            state: "not_started",
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
