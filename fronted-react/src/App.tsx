import { FC } from 'react'; // Alias for FunctionComponent
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

type AppProps = { router: ReturnType<typeof createBrowserRouter> };

const App: FC<AppProps> = ({ router }) => {
  return <RouterProvider router={router} />;
};

export default App;
