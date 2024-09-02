import { AuthInput } from "../components"
import useAuthForm from '../features/auth/useAuthForm';

const RegisterPage = () => {
    const { fields, errors, handleChange, handleSubmit } = useAuthForm({
        initialFields: { email: '', password: '', username: '', confirmPassword: '' },
        onSubmit: async (fields) => {
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(fields),
            });

            if (!response.ok) throw new Error('reg error');
        },
    });

    return (
        <div className="register-page flex justify-center items-center h-screen bg-[#2d2d2d] m-0 p-0 font-[Raleway]">
            <div className="container flex w-[950px] h-[650px] shadow-lg rounded-lg overflow-hidden relative top-[30px]">
                <div className="image-section flex-1 bg-cover bg-center" style={{ backgroundImage: "url('https://static.overlay-tech.com/assets/77252b72-daed-406e-ab45-45eb73409a20.png')" }}></div>
                <div className="form-section flex-1 bg-black/20 flex justify-center items-center">
                    <div className="form-container w-[70%]">
                        <h2 className="text-white text-[40px] mb-[20px] font-bold">Welcome Back!</h2>
                        <form onSubmit={handleSubmit}>
                            <label className="text-[#b3b3b3] text-sm mt-[20px]" htmlFor="username">Username</label>
                            <AuthInput
                                type="text"
                                id="username"
                                name="username"
                                placeholder="Your username"
                                value={fields.username}
                                onChange={handleChange}
                            />
                            {errors.username && <p className="error text-red-500 text-sm font-semibold mt-[-15px]">{errors.username}</p>}

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
                            />
                            {errors.password && <p className="error text-red-500 text-sm font-semibold mt-[-15px]">{errors.password}</p>}

                            <label className="text-[#b3b3b3] text-sm mt-[20px]" htmlFor="confirmPassword">Confirm Password</label>
                            <AuthInput
                                type="password"
                                id="confirmPassword"
                                name="confirmPassword"
                                placeholder="Confirm your password"
                                value={fields.confirmPassword}
                                onChange={handleChange}
                                
                            />
                            {errors.confirmPassword && <p className="error text-red-500 text-sm font-semibold mt-[-15px]">{errors.confirmPassword}</p>}

                            <button className="box-content w-full h-[25px] p-[10px] mt-[19px] mb-[20px] bg-black text-white shadow-md border-none rounded-sm cursor-pointer text-base font-semibold" type="submit">Register</button>
                            {errors.form && <p className="error text-red-500 text-sm font-semibold mt-[-15px]">{errors.form}</p>}
                            <div className="signup-link mt-[20px] text-[#b3b3b3] text-xs">
                                Already have an account? <a className="text-[#0094FF] no-underline" href="/login">Login</a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RegisterPage;
