import Button from "@/components/ui/Button";
import Image from "next/image";
import Link from "next/link";

export default function Home() {
  return (
    <div className="p-6 space-y-6 bg-gray-100">

      <section className="relative h-[60vh] bg-black text-white py-24 px-6 bg-cover bg-center text-center overflow-hidden">
        <Image
          src="/Images/hero-bg-2.jpg"
          alt="Hero Image of the Landing Page"
          fill
          priority
          className="object-cover object-center opacity-90"
        />

        <div className="absolute inset-0 bg-black-60 mt-10 py-24">
          <h1 className="text-5xl font-bold mb-6">
            Admin Dashboard Application
          </h1>

          <p className="max-w-2xl mx-auto text-lg text-gray-300 mb-8">
            A modern, scalable, and component-driven dashboard built using
            Next.js App Router and Tailwind CSS.
          </p>

          <div className="flex justify-center gap-4">
            <Button variant="primary">
              <Link href="/dashboard">Go to Dashboard</Link>
            </Button>
            <Button variant="success">
              <Link href="/about">Learn More</Link>
            </Button>
          </div>
        </div>
      </section>

      <section className="py-20 px-6 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-10">
          Core Capabilities
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">
              Component-Based UI
            </h3>
            <p className="text-gray-600 text-sm">
              Reusable and consistent UI components designed for scalability.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">
              App Router Architecture
            </h3>
            <p className="text-gray-600 text-sm">
              Built using Next.js layouts, nested routing, and shared navigation.
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">
              Responsive Layouts
            </h3>
            <p className="text-gray-600 text-sm">
              Optimized for desktop and adaptable across screen sizes.
            </p>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-gray-200 py-10 px-3 rounded-md">
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
          <div>
            <p className="text-4xl font-bold">Reusable</p>
            <p className="text-md text-gray-600">UI Components</p>
          </div>

          <div>
            <p className="text-4xl font-bold">Nested</p>
            <p className="text-md text-gray-600">Layouts</p>
          </div>

          <div>
            <p className="text-4xl font-bold">Modern</p>
            <p className="text-md text-gray-600">Tech Stack</p>
          </div>

          <div>
            <p className="text-4xl font-bold">Scalable</p>
            <p className="text-md text-gray-600">Architecture</p>
          </div>
        </div>
      </section>

      <section className="py-20 px-6 text-center bg-black rounded-md">
        <h2 className="text-3xl font-semibold mb-4 text-white">
          Start Exploring the Dashboard
        </h2>

        <p className="text-gray-100 mb-8">
          Navigate through pages, components, and layouts built for real-world use cases.
        </p>

        <div className="flex gap-1 justify-center">
          <Button variant="primary">
            <Link href="/dashboard">Open Dashboard</Link>
          </Button>
          <Button variant="success">
            <Link href="/login">Sign In</Link>
          </Button>
        </div>
      </section>


      {/* Footer */}
      <section className="p-2 text-center bg-gray-800 rounded-md">
        <p className="text-gray-100">
          &copy; 2026: All rights reseved | Design : HESTABIT
        </p>
      </section>
    </div>
  );
}
