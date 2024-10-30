import { Outlet, useNavigate } from "react-router-dom";

const NavBar: React.FC = () => {
  const navigate = useNavigate();

  return (
    <>
      <nav className="bg-gray-100 shadow-md border-b-2 border-b-purple-950 p-4 flex justify-between items-center w-full">
        <h1 className="text-2xl font-semibold text-gray-900">Brand</h1>
        <ul className="flex space-x-6">
          <li>
            <button
              className="text-gray-800 hover:text-gray-900 font-bold"
              onClick={() => navigate("/")}
            >
              Home
            </button>
          </li>
          <li>
            <button
              className="text-gray-800 hover:text-gray-900 font-bold"
              onClick={() => navigate("/login")}
            >
              Login
            </button>
          </li>
          <li>
            <button
              className="text-gray-800 hover:text-gray-900 font-bold"
              onClick={() => navigate("/register")}
            >
              Register
            </button>
          </li>
          <li>
            <button className="text-gray-800 hover:text-gray-900 font-bold" onClick={() => navigate("/dashboard")}>
              Navbar
            </button>
          </li>
        </ul>
      </nav>
      <Outlet />
    </>
  );
};

export default NavBar;
