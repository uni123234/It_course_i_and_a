import { Outlet, useNavigate } from "react-router-dom";

const NavBar: React.FC = () => {
  const navigate = useNavigate();

  return (
    <>
      <nav className="bg-gray-100 shadow-md p-4 flex justify-between items-center fixed w-full">
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
            <a href="#" className="text-gray-800 hover:text-gray-900 font-bold">
              Contact
            </a>
          </li>
        </ul>
      </nav>
      <Outlet />
    </>
  );
};

export default NavBar;
