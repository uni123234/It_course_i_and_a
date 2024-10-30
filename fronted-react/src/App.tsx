import { FC } from "react";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { GoogleOAuthProvider } from "@react-oauth/google";
import { googleСlientId } from "./config";
import { Footer } from "./components";

import "./App.css";

type AppProps = { router: ReturnType<typeof createBrowserRouter> };

const App: FC<AppProps> = ({ router }) => {
  return (
    <GoogleOAuthProvider clientId={googleСlientId}>
      <RouterProvider router={router} />
      <Footer />
    </GoogleOAuthProvider>
  );
};

export default App;
