import Button from "@/components/ui/Button";
import Image from "next/image";
import Link from "next/link";

export default function AboutPage() {
    return (
        <div className=" space-y-6 p-6 bg-gray-100">

            {/* Page Heading*/}
            <section>
                <h1 className="text-4xl font-bold text-center mb-3">
                    About this Dashboard Application
                </h1>
                <p className="py-5 px-6 text-gray-900 max-w-7xl mx-auto text-center text-lg mb-3">
                    This page outlines the purpose, structure, and technical direction of the
                    Admin Dashboard application. The content focuses on how the interface is
                    composed, how navigation is handled across routes, and how reusable
                    components contribute to consistency and maintainability.
                </p>
            </section>

            {/* Overview */}
            <section className="relative h-[50vh] py-20 px-6 rounded-md italic overflow-hidden">
                <Image
                    src="/Images/about-page.jpg"
                    alt="The image for About Page"
                    fill
                    priority
                    className="object-cover object-center opacity-100"
                />
                <div className="absolute inset-0 bg-black/30 py-20">
                    <h2 className="text-4xl font-semibold text-center mb-10 text-white hover:underline decoration-red-500 hover:italic hover:text-5xl">
                        Project Overview
                    </h2>
                    <p className="text-gray-100 leading-relaxed text-xl mb-4 max-w-6xl mx-auto">
                        The Admin Dashboard is designed as a structured frontend application
                        that simulates a real-world administrative interface. While the current
                        implementation focuses on static content, the layout and component
                        hierarchy are intentionally built to support future integration with
                        dynamic data sources and backend services.
                    </p>
                    <p className="text-gray-100 leading-relaxed text-xl mb-4 max-w-6xl mx-auto">
                        The project prioritizes clarity in layout design, predictable navigation,
                        and separation of concerns between UI structure and page-specific content.
                        Each section of the interface is deliberately isolated to ensure that
                        changes in one area do not introduce unintended side effects elsewhere.
                    </p>
                </div>
            </section>

            {/* Architecture */}
            <section className="space-y-4 py-10 px-6 bg-gray-200 rounded-lg">
                <h2 className="text-3xl font-bold text-center mb-10 hover:underline decoration-red-500 hover:italic hover:text-4xl">
                    Application Architecture
                </h2>
                <p className="text-gray-900 leading-relaxed text-lg  max-w-6xl mx-auto">
                    The application is structured around the Next.js App Router, allowing
                    layouts and pages to be composed hierarchically. Shared UI elements such
                    as the navbar and sidebar are implemented at the layout level, ensuring
                    consistency across all dashboard-related routes.
                </p>
                <p className="text-gray-900 leading-relaxed text-lg max-w-6xl mx-auto">
                    Page components are responsible only for rendering their respective
                    content, while reusable UI components handle presentation logic. This
                    separation simplifies debugging, improves readability, and supports
                    incremental enhancements.
                </p>

                <ul className="list-disc list-inside text-gray-900 space-y-2 text-lg  max-w-6xl mx-auto">
                    <li>Global and nested layouts manage shared navigation</li>
                    <li>Reusable UI components reduce repetition</li>
                    <li>Pages remain lightweight and focused on content</li>
                    <li>Layout logic is isolated from visual components</li>
                </ul>
            </section>

            {/* Technology Stack */}
            <section className="space-y-4 py-5 px-6 max-w-6xl mx-auto mb-10">
                <h2 className="text-3xl font-bold text-center mb-10 hover:underline decoration-red-500 hover:italic hover:text-4xl">
                    Technology Stack
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div className="bg-white p-6 rounded-lg shadow-md">
                        <h3 className="text-xl font-semibold mb-2 hover:underline">
                            Next.js
                        </h3>
                        <p className="text-md text-gray-600 italic">
                            Used for routing, layout composition, and managing server and client
                            component boundaries through the App Router.
                        </p>
                    </div>

                    <div className="bg-white p-6 rounded-lg shadow-md">
                        <h3 className="text-xl font-semibold mb-2 hover:underline">
                            Tailwind CSS
                        </h3>
                        <p className="text-md text-gray-600 italic">
                            Utility-first styling approach used to implement layouts, spacing,
                            and component-level styles in a predictable manner.
                        </p>
                    </div>

                    <div className="bg-white p-6 rounded-md shadow-lg">
                        <h3 className="text-xl font-semibold mb-2 hover:underline">
                            Reusable Components
                        </h3>
                        <p className="text-md text-gray-600 italic">
                            Common UI elements such as cards, buttons, badges, and modals are
                            abstracted into shared components.
                        </p>
                    </div>

                    <div className="bg-white p-6 rounded-lg shadow-md">
                        <h3 className="text-xl font-semibold mb-2 hover:underline">
                            Layout System
                        </h3>
                        <p className="text-md text-gray-600 italic">
                            Global and nested layouts are used to maintain consistent navigation
                            while allowing flexibility at the page level.
                        </p>
                    </div>
                </div>
            </section>

            {/* Learning Objectives */}
            <section className="space-y-3 py-16 px-6 bg-gray-300 rounded-lg shadow-md">
                <h2 className="text-3xl font-semibold text-center hover:underline decoration-gray-700 hover:italic hover:text-4xl">
                    Learning Objectives
                </h2>
                <p className="text-gray-800 py-2 px-6 text-center leading-relaxed font-medium text-xl">
                    This project is intended to reinforce practical understanding of frontend
                    application structure. Key learning outcomes include:
                </p>

                <ul className="list-disc list-inside text-gray-800 space-y-2 font-medium text-xl max-w-4xl mx-auto">
                    <li>Implementing routing using the Next.js App Router</li>
                    <li>Designing and managing nested layouts</li>
                    <li>Structuring reusable UI components</li>
                    <li>Applying consistent styling across complex layouts</li>
                </ul>
            </section>

            {/* Navigation */}
            <section className="py-20 px-6 text-center bg-black rounded-md">
                <h2 className="text-3xl font-semibold mb-4 text-white">
                    Start Exploring......
                </h2>
                <p className="text-lg text-gray-100 mb-4">
                    Navigate through pages, components, and layouts built for real-world use cases.
                </p>
                <div className="flex gap-4 justify-center">
                    <Button variant="primary" size="md">
                        <Link href="/dashboard">Open Dashboard</Link>
                    </Button>
                    <Button variant="success" size="md">
                        <Link href="/">Return to Home</Link>
                    </Button>
                </div>
            </section>

        </div>
    );
}