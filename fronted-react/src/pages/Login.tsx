import { AuthInput } from "../components"
import { useAuthForm } from '../features';
import { API_URL } from '../config';

const LoginPage = () => {
    const { fields, errors, handleChange, handleSubmit } = useAuthForm({
        initialFields: { email: '', password: ''},
        onSubmit: async (fields) => {

            const response = await fetch(`${API_URL}login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(fields),
            });

            if (!response.ok) throw new Error('reg error');
        },
        validate: false,
    });

    return (
        <div className="register-page flex justify-center items-center h-screen bg-[#2d2d2d] m-0 p-0 font-[Raleway]">
            <div className="container flex w-[900px] h-[550px] shadow-lg rounded-lg overflow-hidden relative top-[30px]">
                <div className="image-section flex-1 bg-cover bg-center" style={{ backgroundImage: "url('https://static.overlay-tech.com/assets/77252b72-daed-406e-ab45-45eb73409a20.png')" }}></div>
                <div className="form-section flex-1 bg-black/20 flex justify-center items-center">
                    <div className="form-container w-[70%]">
                        <h2 className="text-white text-[40px] mb-[20px] mt-[20px] font-bold">Welcome Back!</h2>
                        <form onSubmit={handleSubmit}>
                            <label className="text-[#b3b3b3] text-sm mt-[20px]" htmlFor="email">Email Address</label>
                            <AuthInput
                                type="email"
                                id="email"
                                name="email"
                                placeholder="example@mail.com"
                                value={fields.email}
                                onChange={handleChange}
                            />
                            {errors.email && <p className="error text-red-500 text-sm font-semibold mt-[-15px]">{errors.email}</p>}

                            <label className="text-[#b3b3b3] text-sm mt-[20px]" htmlFor="password">Password</label>
                            <AuthInput
                                type="password"
                                id="password"
                                name="password"
                                placeholder="Your password"
                                value={fields.password}
                                onChange={handleChange}
                            />
                            {errors.password && <p className="error text-red-500 text-sm font-semibold mt-[-15px]">{errors.password}</p>}

                            <button className="box-content w-full h-[25px] p-[10px] mt-[19px] mb-[5px] bg-black text-white shadow-md border-none rounded-sm cursor-pointer text-base font-semibold" type="submit">Login</button>
                            {errors.form && <p className="error text-red-500 text-sm font-semibold">{errors.form}</p>}
                            <div className="signup-link mt-[5px] mb-[20px] text-[#b3b3b3] text-xs">
                                Dont have an account? <a className="text-[#0094FF] no-underline" href="/register">Register</a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
