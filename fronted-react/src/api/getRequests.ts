import axios from 'axios';
import API_URL from "./index";


import { useAuth } from "../features";

export const getCourses = async (token: string | null) => {
  console.log("get");

  try {
    console.log("get1221");
    const response = await axios.get(`${API_URL}/course/`, {
      headers: {
        Authorization: `Bearer ${token}`, // Використовуйте переданий токен
      },
    });
    return response.data; // Переконайтеся, що тут повертаються правильні дані
  } catch (error) {
    console.error("Error fetching courses:", error);
    throw error; // Переконайтеся, що ви обробляєте помилки
  }
};


export const getLessons = async (token: string | null) => {
  console.log("get");

  try {
    console.log("get1221");
    const response = await axios.get(`${API_URL}/lessons/`, {
      headers: {
        Authorization: `Bearer ${token}`, // Використовуйте переданий токен
      },
    });
    return response.data; // Переконайтеся, що тут повертаються правильні дані
  } catch (error) {
    console.error("Error fetching courses:", error);
    throw error; // Переконайтеся, що ви обробляєте помилки
  }
};


export const getHomeworks = async (token: string | null, courseId: number) => {
  console.log("get");

  try {
    console.log("get1221");
    const response = await axios.post(`${API_URL}/homework/`, // Використовуємо POST запит
      {
        courseId: courseId, // Передача courseId у тілі запиту
      },
      {
        headers: {
          Authorization: `Bearer ${token}`, // Використовуйте переданий токен
        },
      }
    );
    return response.data; // Переконайтеся, що тут повертаються правильні дані
  } catch (error) {
    console.error("Error fetching homeworks:", error);
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
