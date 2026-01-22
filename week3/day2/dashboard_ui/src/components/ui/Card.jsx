export default function Card({title, children, varient, className="",content}) {
    const variants = {
        primary: "border-l-4 bg-blue-600 border-blue-600",
        warning: "border-l-4 bg-yellow-500 border-yellow-500",
        success: "border-l-4 bg-green-600 border-green-600",
        danger: "border-l-4 bg-red-600 border-red-600",
        area: "border-l-4 bg-gray-600 border-gray-700",
        bar: "border-l-4 bg-gray-600 border-gray-700",
        table: "border-l-4 bg-gray-600 border-gray-700",
    };
    const contents = {
        area: "text-black text-md px-4 py-3",
        bar: "text-black text-md px-4 py-3",
        table: "text-black text-md px-2 py-1 flex justify-between",
    };

    return (
        <div className={`bg-white rounded-md shadow-sm border border-gray-200 ${variants[varient]}  ${className}`}>

            {/* Header or Card Title*/}
            {title && (
                <div className="px-4 py-2 border-b border-gray-400">
                    <h3 className="text-sm font-semibold text-white">
                        {title}
                    </h3>
                </div>
            )}

            {/* Children or Card Content*/}
            {children && (
                <div className={`border-t bg-gray-100 text-m ${contents[content]}`}>
                    {children}
                </div>
            )}
        </div>
    );
}