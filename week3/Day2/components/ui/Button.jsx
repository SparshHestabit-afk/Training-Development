'use client';

export default function Button({
    children,
    variant = 'primary',
    size = 'md',
    onClick,
    type = 'button'
}) {
    const variants = {
        primary: "bg-blue-600 hover:bg-blue-700 text-white",
        warning: "bg-yellow-500 hover:bg-yellow-600 text-white",
        success: "bg-green-600 hover:bg-green-700 text-white",
        danger: "bg-red-600 hover:bg-red-700 text-white",
        search: "bg-gray-300 text-black",
        hamburger: "text-xl p-6",
    };

    const sizes = {
        sm: "px-3 py-1 text-sm",
        md: "px-4 py-2 text-md",
        lg: "px-6 py-4 text-lg",
    };

    return (
        <div className="px-4 py-3">
            <button
                type={type}
                onClick={onClick}
                className={`rounded-md font-medium transition ${variants[variant]} ${sizes[size]}`}
            >
                {children}
            </button>
        </div>
    );
}