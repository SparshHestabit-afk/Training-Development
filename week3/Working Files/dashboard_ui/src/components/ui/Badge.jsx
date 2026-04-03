export default function Badge({
    children,
    variant = 'primary',
}) {
    const variants = {
        primary: "bg-blue-600 text-white",
        success: "bg-yellow-500 text-white",
        warning: "bg-green-600 text-white",
        danger: "bg-red-600 text-white",
    }
    return (
        <span className={`px-3 py-1 text-sm rounded-full font-medium ${variants[variant]} `}>
            {children}
        </span>
    );
}