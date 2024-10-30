import { googleIcon, facebookIcon } from "../../assets";
import SocialButton from "./SocialButton";

import { useGoogleLogin } from "@react-oauth/google";

const SocialLoginButtons = () => {
  const loginWithGoogle = useGoogleLogin({
    onSuccess: (tokenResponse) => {
      console.log("Google Token:", tokenResponse);
    },
    onError: () => {
      console.log("Google Login failed");
    },
  });

  const handleFacebookLoginSuccess = (response: any) => {
    console.log("Успішний вхід через Facebook:", response);
  };

  const handleFacebookLoginFailure = (error: any) => {
    console.error("Помилка при вході через Facebook:", error);
  };

  return (
    <div className="space-y-3">
      <SocialButton
        label="Continue with Google"
        icon={<img src={googleIcon} className="w-5 h-5" />}
        onClick={loginWithGoogle}
      />
    </div>
  );
};

export default SocialLoginButtons;
