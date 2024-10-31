import { googleIcon } from "../../assets";
import SocialButton from "./SocialButton";
import { GOOGLE_AUTH_URL } from "../../config";

import { useGoogleLogin } from "@react-oauth/google";

const SocialLoginButtons = () => {
  const loginWithGoogle = useGoogleLogin({
    onSuccess: async (tokenResponse) => {
      console.log("Google Token:", tokenResponse);
      const accessToken = tokenResponse.access_token;

      try {
        const response = await fetch(`${GOOGLE_AUTH_URL}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
          body: JSON.stringify({ accessToken }),
        });

        if (!response.ok) {
          throw new Error("Не вдалося авторизуватись");
        }

        const data = await response.json();
        console.log("Дані з бекенду:", data);
      } catch (error) {
        console.error("Помилка при авторизації з Google:", error);
      }
    },
    onError: () => {
      console.log("Google Login failed");
    },
  });

  return (
    <div className="space-y-3">
      <SocialButton
        label="Continue with Googleф"
        icon={<img src={googleIcon} className="w-5 h-5" />}
        onClick={loginWithGoogle}
      />
    </div>
  );
};

export default SocialLoginButtons;
