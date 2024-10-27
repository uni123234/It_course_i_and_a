import { AuthInput } from "../components"
import { useAuthForm } from '../features';

const RegisterPage = () => {
    const { fields, errors, handleChange, handleSubmit, API_URL } = useAuthForm({
        initialFields: { email: '', password: '', username: '', firstname: '', lastname: '', confirmPassword: ''},
        onSubmit: async (fields) => {
            const { confirmPassword, firstname, lastname, ...restFields } = fields;
            const fieldsToSubmit = {
                ...restFields,
                first_name: firstname,
                last_name: lastname
            };

            const response = await fetch(`${API_URL}register/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(fieldsToSubmit),
            });
            console.log(fieldsToSubmit);

            if (!response.ok) throw new Error('reg error');
        },
        validate: true,
    });

    return (
        <div className="register-page flex justify-center items-center h-screen bg-[#2d2d2d] m-0 p-0 font-[Raleway]">
            <div className="container flex max-h-[800px] max-w-[1050px] ml-[30px] mr-[30px] shadow-lg rounded-lg overflow-hidden relative top-[30px]">
                <div className="image-section flex-1 bg-cover bg-center" style={{ backgroundImage: "url('https://static.overlay-tech.com/assets/77252b72-daed-406e-ab45-45eb73409a20.png')" }}></div>
                <div className="form-section flex-1 bg-black/20 flex justify-center items-center">
                    <div className="form-container w-[70%]">
                        <h2 className="text-white text-[40px] mb-[20px] mt-[20px] font-bold">Welcome Back!</h2>
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

                            <label className="text-[#b3b3b3] text-sm mt-[20px]" htmlFor="firstname">First name</label>
                            <AuthInput
                                type="text"
                                id="firstname"
                                name="firstname"
                                placeholder="Your first name"
                                value={fields.firstname}
                                onChange={handleChange}
                            />
                            {errors.firstname && <p className="error text-red-500 text-sm font-semibold mt-[-15px]">{errors.firstname}</p>}

                            <label className="text-[#b3b3b3] text-sm mt-[20px]" htmlFor="lastname">Last name</label>
                            <AuthInput
                                type="text"
                                id="lastname"
                                name="lastname"
                                placeholder="Your last name"
                                value={fields.lastname}
                                onChange={handleChange}
                            />
                            {errors.lastname && <p className="error text-red-500 text-sm font-semibold mt-[-15px]">{errors.lastname}</p>}

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

                            <button className="box-content w-full h-[25px] p-[10px] mt-[19px] mb-[5px] bg-black text-white shadow-md border-none rounded-sm cursor-pointer text-base font-semibold" type="submit">Register</button>
                            {errors.form && <p className="error text-red-500 text-sm font-semibold">{errors.form}</p>}
                            <div className="signup-link mt-[5px] mb-[20px] text-[#b3b3b3] text-xs">
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
