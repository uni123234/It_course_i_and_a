import axios from 'axios';


import API_URL from "./index";

export const getGroups = async () => {
  const response = await fetch(`${API_URL}/groups/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch groups");
  }

  return await response.json();
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
