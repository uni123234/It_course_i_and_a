import API_URL from "./index"

export const loginUser = async (email: string, password: string) => {
  const response = await fetch(`${API_URL}/login/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to log in");
  }

  const data = await response.json();
  return data;
};


export const registerUser = async (userData: {
    email: string;
    password: string;
    firstName: string | undefined;
    lastName: string | undefined;
    role: string | undefined;
  }) => {
    const response = await fetch(`${API_URL}/register/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: userData.email,
        password: userData.password,
        first_name: userData.firstName,
        last_name: userData.lastName,
        user_type: userData.role,
      }),
    });
  
    if (!response.ok) {
      throw new Error("Failed to register");
    }
  
    return await response.json();
  };
