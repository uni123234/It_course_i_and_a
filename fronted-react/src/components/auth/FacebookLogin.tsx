// import React from "react";
// import FacebookLogin from "react-facebook-login";
// import { facebookIcon } from "../../assets";

// type FacebookLoginButtonProps = {
//   onLoginSuccess: (response: any) => void;
//   onLoginFailure?: (error: any) => void;
// };

// const FacebookLoginButton: React.FC<FacebookLoginButtonProps> = ({
//   onLoginSuccess,
//   onLoginFailure,
// }) => {
//   const handleResponse = (response: any) => {
//     if (response.status !== "unknown") {
//       onLoginSuccess(response);
//     } else if (onLoginFailure) {
//       onLoginFailure(response);
//     }
//   };

//   return (
//     <FacebookLogin
//       appId="1108802073929707"
//       autoLoad={false}
//       fields="name,email,picture"
//       callback={handleResponse}
//       cssClass="w-full flex items-center justify-center space-x-2 py-2 mt-3 font-semibold border border-gray-300 rounded-md hover:bg-gray-100 active:bg-gray-200"
//       textButton="Sign in with Facebook"
//       icon={<img src={facebookIcon} className="w-5 h-5 mr-2" />}
//     />
//   );
// };

// export default FacebookLoginButton;
