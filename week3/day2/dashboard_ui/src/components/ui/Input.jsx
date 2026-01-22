'use client';

export default function Input({
    type = 'text',
    placeholder,
    value,
    onChange,
}) {
    return (
        <input
            type={type}
            placeholder={placeholder}
            value={value}
            onChange={onChange}
            className="w-auto px-4 py-2 text-sm text-black border border-gray-300 outline-none focus:ring-2 focus:ring-blue-500"
        />
    );
}