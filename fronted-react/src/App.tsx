import { FC } from "react"; // Alias for FunctionComponent
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { googleСlientId } from "./config";

type AppProps = { router: ReturnType<typeof createBrowserRouter> };

const App: FC<AppProps> = ({ router }) => {
  
  return (
    <GoogleOAuthProvider clientId={googleСlientId}>
      <RouterProvider router={router} />
    </GoogleOAuthProvider>
  );
};

export default App;
