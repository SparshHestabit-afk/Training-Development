export default function Badge({
    children,
    varient = 'info',
}) {
    const variants = {
        info: "bg-blue-100 text-blue-700",
        success: "bg-yellow-100 text-yellow-700",
        warning: "bg-green-100 text-green-700",
        danger: "bg-red-100 text-red-700",
    }
    return (
        <span className={`px-3 py-1 text-xs rounded-full font-medium ${variants[varient]} `}>
            {children}
        </span>
    );
}