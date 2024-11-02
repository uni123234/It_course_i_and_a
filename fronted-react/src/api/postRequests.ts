import axios, { AxiosError } from "axios";
import API_URL from "./index";
import { useAuth } from "../features";

// Utility function for POST requests with token retrieval
const postRequest = async (url: string, data: object) => {
  const { getAccessToken } = useAuth();
  const token = getAccessToken();

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

// Function for creating a course
export const createCourse = async (courseData: CourseData) => {
  return postRequest(`${API_URL}/courses/create/`, courseData);
};

// Function for creating homework
export const createHomework = async (homeworkData: HomeworkData) => {
  const data = {
    title: homeworkData.title,
    description: homeworkData.description,
    submitted_by: homeworkData.id,
    due_date: homeworkData.dateTime,
    course_id: homeworkData.courseId,
  };
  return postRequest(`${API_URL}/homework/`, data);
};

// Function for creating a lesson
export const createLesson = async (lessonData: LessonData) => {
  const data = {
    title: lessonData.title,
    description: lessonData.description,
    scheduled_time: lessonData.dateTime,
    course: lessonData.courseId,
  };
  return postRequest(`${API_URL}/lessons/create/`, data);
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
