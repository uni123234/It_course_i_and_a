import axios from "axios";
import API_URL from "./index";

const fetchData = async (endpoint: string, params: Record<string, any> = {}, token: string | null) => {
  try {
    const response = await axios.get(`${API_URL}${endpoint}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params,
    });

    console.log(response.data)
    return response.data;
  } catch (error) {
    console.error(`Error fetching data from ${endpoint}:`, error);
    throw error;
  }
};

export const getCourses = (token: string | null) => fetchData("/course/", {}, token);
export const getReminders = (token: string | null) => fetchData("/reminders/", {}, token);
export const fetchCourse = (courseId: number, token: string | null) => fetchData(`/course/${courseId}/`, {}, token);
export const getLessons = (token: string | null) => fetchData("/lessons/", {}, token);
export const getCalendar = (token: string | null) => fetchData("/calendar/", {}, token);
export const getHomeworks = (courseId: number, token: string | null) =>
  fetchData("/homework/", { course_id: courseId }, token);
