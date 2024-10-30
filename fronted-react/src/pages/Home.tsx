import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-blue-100 text-gray-800 flex flex-col items-center py-12 px-4">
      {/* Контейнер */}
      <div
        className="max-w-5xl w-full space-y-8"
      >
        {/* Заголовок */}
        <section className="text-center bg-white rounded-lg shadow-md p-8">
          <h1 className="text-4xl font-bold 6">
            Unlock Your Learning Potential
          </h1>
          <p className="text-lg mt-4 text-gray-600">
            Master new skills with expert-led courses in various fields
          </p>
          <button
            className="mt-6 px-6 py-3 text-white rounded-lg bg-slate-800 hover:bg-slate-700 active:bg-gray-600"
            onClick={() => navigate("/register")}
          >
            Get Started
          </button>
        </section>

        {/* Переваги платформи */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <h3 className="text-xl font-semibold 6">Expert-Led Content</h3>
            <p className="mt-4 text-gray-600">
              Learn from industry leaders who share their expertise and
              real-world experience.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <h3 className="text-xl font-semibold 6">Flexible Learning</h3>
            <p className="mt-4 text-gray-600">
              Access courses at your own pace and on any device, whenever it
              suits you.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <h3 className="text-xl font-semibold 6">
              Certificates & Achievements
            </h3>
            <p className="mt-4 text-gray-600">
              Earn certificates to showcase your skills and progress to
              employers.
            </p>
          </div>
        </section>

        {/* Заклик до дії */}
        <section className="text-center bg-white rounded-lg shadow-md p-8">
          <h2 className="text-2xl font-semibold text-gray-700">
            Ready to Start Learning?
          </h2>
          <p className="text-gray-600 mt-4">
            Join thousands of learners today and take the first step towards
            mastering new skills!
          </p>
          <button
            className="mt-6 px-6 py-3 text-white rounded-lg bg-slate-800 hover:bg-slate-700 active:bg-gray-600"
            onClick={() => navigate("/login")}
          >
            Join Now
          </button>
        </section>

        {/* Відгуки користувачів */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <p className="text-gray-600">
              "This platform helped me land my dream job. Highly recommend!"
            </p>
            <h4 className="mt-4 font-semibold text-slate-700">– Alex P.</h4>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <p className="text-gray-600">
              "I love the flexibility and the range of courses available."
            </p>
            <h4 className="mt-4 font-semibold text-slate-700">
              – Kirpich Anton
            </h4>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md text-center">
            <p className="text-gray-600">
              "The certificate really helped boost my resume!"
            </p>
            <h4 className="mt-4 font-semibold text-slate-700">– John S.</h4>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Home;
