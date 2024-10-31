import { FC } from "react";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { googleСlientId } from "./config";
import { Footer } from "./components";
import { AuthProvider } from "./features";

import "./App.css";

type AppProps = { router: ReturnType<typeof createBrowserRouter> };

const App: FC<AppProps> = ({ router }) => {
  return (
    <AuthProvider>
    <GoogleOAuthProvider clientId={googleСlientId}>
      <RouterProvider router={router} />
      <Footer />
    </GoogleOAuthProvider>
    </AuthProvider>
  );
};

export default App;
