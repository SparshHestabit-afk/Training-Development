import Link from "next/link";

export default function Sidebar({ isOpen }) {
    return (
        <aside 
            className="fixed top-16 left-0 h-[calc(100vh-4rem)] w-64 bg-sidebar text-gray-300"
            style={{ display: isOpen?"block" : "none",}}
        >
            <nav className="p-4 space-y-6">

                {/* Core */}
                <div>
                    <p className="text-xs uppercase tracking-wider tet-gray-400 mb-2">
                        Core
                    </p>
                    <Link href="/dashboard" className="flex items-center px-4 py-2 rounded-md bg-gray-700 text-white">
                        Dashboard
                    </Link>
                </div>

                {/* interface */}
                <div>
                    <p className="text-xs uppercase tracking-wider tet-gray-400 mb-2">
                        Interface
                    </p>
                    <ul className="space-y-1">
                        <li className="px-4 py-2 rounded-md hover:bg-gray-700 cursor-pointer">
                            <Link href="/about">About</Link>
                        </li>
                        <li className="px-4 py-2 rounded-md hover:bg-gray-700 cursor-pointer">
                            <Link href="/dashboard/profile">Profile</Link>
                        </li>
                        <li className="px-4 py-2 rounded-md hover:bg-gray-700 cursor-pointer">
                            <Link href="/dashboard/users">Users</Link>
                        </li>
                    </ul>
                </div>

                {/* Addons */}
                <div>
                    <p className="text-xs uppercase tracking-wider tet-gray-400 mb-2">
                        Addons
                    </p>
                    <ul className="sapce-y-1">
                        <li className="px-4 py-2 rounded-md hover:bg-gray-700 cursor-pointer">
                            <Link href="/dashboard#stats">Stats</Link>
                        </li>
                        <li className="px-4 py-2 rounded-md hover:bg-gray-700 cursor-pointer">
                            <Link href="/dashboard#charts">Charts</Link>
                        </li>
                        <li className="px-4 py-2 rounded-md hover:bg-gray-700 cursor-pointer">
                            <Link href="/dashboard#users">Tables</Link>
                        </li>
                    </ul>
                </div>

            </nav>
        </aside>
    );
}
