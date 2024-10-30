import React from "react";

import { gitHubIcon } from "../assets";

const Footer: React.FC = () => {
  const authors = {
    "Andrii(backend)": "https://github.com/uni123234",
    "Ivan(frontend)": "https://github.com/Vano0928",
  };
  return (
    <footer className="bg-gray-800 text-gray-400 py-10">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-start space-y-8 md:space-y-0 md:space-x-8">
          {/* Лого і слоган */}
          <div className="flex flex-col items-start">
            <img
              src="/path/to/logo.png"
              alt="Platform Logo"
              className="h-10 w-10 mb-3"
            />
            <p className="text-white font-bold">
              Achieve mastery through challenge.
            </p>
            <div className="mt-4">
              <p className="text-gray-500">Was made with</p>
              <div className="flex flex-wrap mt-2">
                {[
                  "Python",
                  "Django",
                  "DRF",
                  "PosrgreSQL",
                  "TypeScript",
                  "Vite",
                  "React",
                  "Tailwind CSS",
                ].map((language) => (
                  <span
                    key={language}
                    className="bg-gray-700 text-gray-300 rounded-full px-2 py-1 mr-1 mt-1 text-xs"
                  >
                    {language}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Колонки з посиланнями */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-8 text-sm">
            <div>
              <h3 className="text-white font-semibold mb-2">DEVELOPERS</h3>
              <ul>
                {Object.entries(authors).map(([key, link]) => (
                  <li className="flex items-center space-x-2" key={key}>
                    <img src={gitHubIcon} className="w-5 h-5" />
                    <a href={link} className="text-gray-50 hover:text-white hover:font-bold">
                      {key}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div className="ml-6">
              <h3 className="text-white font-semibold mb-2">DOJO</h3>
              <ul>
                <li>
                  <a href="#kata-library" className="hover:text-white">
                    Kata Library
                  </a>
                </li>
                <li>
                  <a href="#leaderboard" className="hover:text-white">
                    Leaderboard
                  </a>
                </li>
                <li>
                  <a href="#docs" className="hover:text-white">
                    Docs
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-2">EDUCATORS</h3>
              <ul>
                <li>
                  <a href="#educator-partnerships" className="hover:text-white">
                    Educator Partnerships
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-2">COMPANIES</h3>
              <ul>
                <li>
                  <a href="#skill-assessments" className="hover:text-white">
                    Skill Assessments
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>

        {/* Авторське право і соціальні іконки */}
        <div className="mt-10 border-t border-gray-700 pt-6 flex flex-col md:flex-row items-center justify-between">
          <p className="text-gray-500 text-sm">
            © {new Date().getFullYear()} Learning Platform. All rights reserved.
          </p>
          <div className="flex space-x-4 mt-4 md:mt-0">
            <a
              href="https://twitter.com/platform"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-white"
            >
              <i className="fab fa-twitter"></i>
            </a>
            <a
              href="https://linkedin.com/company/platform"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-white"
            >
              <i className="fab fa-linkedin"></i>
            </a>
            <a
              href="https://github.com/platform"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-white"
            >
              <i className="fab fa-github"></i>
            </a>
            <a
              href="https://discord.com/invite/platform"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-white"
            >
              <i className="fab fa-discord"></i>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
