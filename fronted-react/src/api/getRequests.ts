import axios from 'axios';
import API_URL from "./index";


import { useAuth } from "../features";

export const getCourses = async () => {
  const { getAccessToken } = useAuth();
  const token = getAccessToken();
  console.log("get")

  try {
    const response = await axios.get(`${API_URL}/courses/`, {
      headers: {
        Authorization: `Bearer ${token}`, // Переконайтеся, що токен отримується правильно
      },
    });
    return response.data; // Переконайтеся, що тут повертаються правильні дані
  } catch (error) {
    console.error("Error fetching courses:", error);
    throw error; // Переконайтеся, що ви обробляєте помилки
  }
};

export const getReminders = async (refreshToken: string) => {
  try {
    const response = await axios.get(API_URL, {
      headers: {
        refresh: refreshToken,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching reminders:", error);
    throw error;
  }
};
