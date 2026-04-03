'use client';

export default function Modal({
    open,
    title,
    children,
    onClose,
}) {
    if (!open) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
            <div className="bg-white w-full max-w-md rounded-md shadow-lg">
                <div className="flex justify-between items-center px-4 py-3 border-b">
                    <h3 className="font-semibold">{title}</h3>
                    <button onClick={onClose} className="text-xl">&tiimes;</button>
                </div>

                <div className="p-4">
                    {children}
                </div>
            </div>
        </div>
    );
}
