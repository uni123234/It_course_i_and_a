import axios, { AxiosError } from "axios";
import API_URL from "./index";
import { useAuth } from "../features";

// Utility function for POST requests
const postRequest = async (url: string, data: object, token: string) => {
  try {
    const response = await axios.post(url, data, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    const err = error as AxiosError;
    console.error(`Error with POST request to ${url}:`, err.response?.data || err.message);
    throw err;
  }
};

// Hook for creating a course
export const useCreateCourse = () => {
  const { getAccessToken } = useAuth();

  const createCourse = async (courseData: CourseData) => {
    const token = getAccessToken();
    if (!token) {
      throw new Error("Authentication token is missing.");
    }
    
    return postRequest(`${API_URL}/courses/create/`, courseData, token);
  };

  return { createCourse };
};

// Hook for creating homework
export const useCreateHomework = () => {
  const { getAccessToken } = useAuth();

  const createHomework = async (homeworkData: HomeworkData) => {
    const token = getAccessToken();

    if (!token) {
      throw new Error("Authentication token is missing.");
    }

    const data = {
      title: homeworkData.title,
      description: homeworkData.description,
      submitted_by: homeworkData.id,
      due_date: homeworkData.dateTime,
      course_id: homeworkData.courseId,
    };
    return postRequest(`${API_URL}/homework/`, data, token);
  };

  return { createHomework };
};

export const useCreateLesson = () => {
  const { getAccessToken } = useAuth();

  const createLesson = async (lessonData: LessonData) => {
    const token = getAccessToken();
    
    if (!token) {
      throw new Error("Authentication token is missing.");
    }

    const data = {
      title: lessonData.title,
      description: lessonData.description,
      scheduled_time: lessonData.dateTime,
      course: lessonData.courseId,
    };
    
    return postRequest(`${API_URL}/lessons/create/`, data, token);
  };

  return { createLesson };
};

// Interfaces
interface CourseData {
  title: string;
  description: string;
}

interface HomeworkData {
  title: string;
  description: string;
  id: number | null;
  dateTime: string;
  courseId: number | undefined;
}

interface LessonData {
  title: string;
  description: string;
  dateTime: string;
  courseId: number | undefined;
}
