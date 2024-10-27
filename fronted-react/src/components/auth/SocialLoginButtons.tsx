import { googleIcon, facebookIcon } from "../../assets";
import SocialButton from "./SocialButton";

import { useGoogleLogin } from "@react-oauth/google";
import FacebookLogin from "react-facebook-login";

import { facebookAppId } from "../../config";

const SocialLoginButtons = () => {
  const loginWithGoogle = useGoogleLogin({
    onSuccess: (tokenResponse) => {
      console.log("Google Token:", tokenResponse);
    },
    onError: () => {
      console.log("Google Login failed");
    },
  });

  const handleResponse = (response: any) => {
    if (response.status !== "unknown") {
      handleFacebookLoginSuccess(response);
    } else if (handleFacebookLoginFailure) {
      handleFacebookLoginFailure(response);
    }
  };

  const handleFacebookLoginSuccess = (response: any) => {
    console.log("Успішний вхід через Facebook:", response);
  };

  const handleFacebookLoginFailure = (error: any) => {
    console.error("Помилка при вході через Facebook:", error);
  };

  return (
    <div className="space-y-3">
      <SocialButton
        label="Sign in with Google"
        icon={<img src={googleIcon} className="w-5 h-5" />}
        onClick={loginWithGoogle}
      />
      <FacebookLogin
        appId={facebookAppId}
        autoLoad={false}
        fields="name,email,picture"
        callback={handleResponse}
        cssClass="w-full flex items-center justify-center space-x-2 py-2 mt-3 font-semibold border border-gray-300 rounded-md hover:bg-gray-100 active:bg-gray-200"
        textButton="Sign in with Facebook"
        icon={<img src={facebookIcon} className="w-5 h-5 mr-2" />}
      />
    </div>
  );
};

export default SocialLoginButtons;
