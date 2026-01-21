export default function Sidebar() {
    return (
        <aside className="fixed top-16 left-0 h-[calc(100vh-4rem)] w-64 bg-sidebar text-gray-300">
            <nav className="p-4 space-y-6">

                {/* Core */}
                <div>
                    <p className="text-xs uppercase tracking-wider tet-gray-400 mb-2">
                        Core
                    </p>
                    <a href="#" className="flex items-center px-4 py-2 rounded-md bg-gray-700 text-white">
                        Dashboard
                    </a>
                </div>

                {/* interface */}
                <div>
                    <p className="text-xs uppercase tracking-wider tet-gray-400 mb-2">
                        Interface
                    </p>
                    <ul className="space-y-1">
                        <li className="px-4 py-2 rounded-md hover:bg-gray-700 cursor-pointer">
                            Layouts
                        </li>
                        <li className="px-4 py-2 rounded-md hover:bg-gray-700 cursor-pointer">
                            Pages
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
                            Charts
                        </li>
                        <li className="px-4 py-2 rounded-md hover:bg-gray-700 cursor-pointer">
                            Tables
                        </li>
                    </ul>
                </div>

            </nav>
        </aside>
    );
}